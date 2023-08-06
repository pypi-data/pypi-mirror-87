# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:12:24 2016

@author: david
"""
try:
    #python 2.x
    # noinspection PyCompatibility
    import Queue
except ImportError:
    #python 3.x
    import queue as Queue
    
import time
from PYME.contrib import dispatch
import weakref
import threading
from PYME.util import webframework
import numpy as np
import logging
logger = logging.getLogger(__name__)

class ActionManager(object):
    """This implements a queue for actions which should be called sequentially.
    
    The main purpose of the ActionManager is to facilitate automated imaging by 
    allowing multiple operations to be queued. Rather than being strictly FIFO,
    different tasks can be asigned different priorities, with higher priority 
    tasks bubbling up and and being executed before lower priority tasks. This 
    allows high priority "imaging" tasks to be inserted into a stream of lower
    priority "monitoring" tasks if something interesting is detected during 
    monitoring.
    
    An individual action is a function which can be found within the scope of
    our microscope object (for more details see the QueueAction method).
    
    To function correctly the Tick() method should be called regularly - e.g.
    from a GUI timer.
    """
    def __init__(self, scope):
        """Initialise our action manager
        
        Parameters
        ----------
        
        scope : PYME.Acquire.microscope.microscope object
            The microscope. The function object to call for an action should be 
            accessible within the scope namespace, and will be resolved by
            calling eval('scope.functionName')
        
        """
        self.actionQueue = Queue.PriorityQueue()
        self.scope = weakref.ref(scope)
        
        #this will be assigned to a callback to indicate if the last task has completed        
        self.isLastTaskDone = None
        self.paused = False
        
        self.currentTask = None
        
        self.onQueueChange = dispatch.Signal()
        
        self._timestamp = 0

        self._monitoring = True
        self._monitor = threading.Thread(target=self._monitor_defunct)
        self._monitor.start()
        
    def QueueAction(self, functionName, args, nice=10, timeout=1e6, 
                    max_duration=np.finfo(float).max):
        """Add an action to the queue
        
        Parameters
        ----------
        
        functionName : string
            The name of a function relative to the microscope object.
            e.g. to `call scope.spoolController.StartSpooling()`, you would use
            a functionName of 'spoolController.StartSpooling'.
            
            The function should either return `None` if the operation has already
            completed, or function which evaluates to True once the operation
            has completed. See `scope.spoolController.StartSpooling()` for an
            example.
            
        args : dict
            a dictionary of arguments to pass the function    
        nice : int (or float)
            The priority with which to execute the function. Functions with a
            lower nice value execute first.
        timeout : float
            A timeout in seconds from the current time at which the action
            becomes irrelevant and should be ignored.
        max_duration : float
            A generous estimate, in seconds, of how long the task might take, 
            after which the lasers will be automatically turned off and the 
            action queue paused. This will not interrupt the current task, 
            though it has presumably already failed at that point. Intended as a
            safety feature for automated acquisitions, the check is every 3 s 
            rather than fine-grained.
            
        """
        curTime = time.time()    
        expiry = curTime + timeout
        
        #make sure our timestamps strictly increment
        self._timestamp = max(curTime, self._timestamp + 1e-3)
        
        #ensure FIFO behaviour for events with the same priority
        nice_ = nice + self._timestamp*1e-10
        
        self.actionQueue.put_nowait((nice_, functionName, args, expiry, 
                                     max_duration))
        self.onQueueChange.send(self)
        
        
    def Tick(self, **kwargs):
        """Polling function to check if the current action is finished and, if so, start the next
        action if available.
        
        Should be called regularly for a timer or event loop.
        """
        if self.paused:
            return
            
        if (self.isLastTaskDone is None) or self.isLastTaskDone():
            try:
                self.currentTask = self.actionQueue.get_nowait()
                nice, functionName, args, expiry, max_duration = self.currentTask
                self._cur_task_kill_time = time.time() + max_duration
                self.onQueueChange.send(self)
            except Queue.Empty:
                self.currentTask = None
                return
            
            if expiry > time.time():
                print('%s, %s' % (self.currentTask, functionName))
                fcn = eval('.'.join(['self.scope()', functionName]))
                self.isLastTaskDone = fcn(**args)
            else:
                past_expire = time.time() - expiry
                logger.debug('task expired %f s ago, ignoring %s' % (past_expire,
                                                                     self.currentTask))
    
    def _monitor_defunct(self):
        """
        polling thread method to check that if a task is being executed through
        the action manager it isn't taking longer than its `max_duration`.
        """
        while self._monitoring:
            if self.currentTask is not None:
                #logger.debug('here, %f s until kill' % (self._cur_task_kill_time - time.time()))
                if time.time() > self._cur_task_kill_time:
                    self.scope().turnAllLasersOff()
                    # pause and reset so we can start up again later
                    self.paused = True
                    self.isLastTaskDone = None
                    self.currentTask = None
                    self.onQueueChange.send(self)
                    logger.error('task exceeded specified max duration')
        
            time.sleep(3)
    
    def __del__(self):
        self._monitoring = False


class ActionManagerWebWrapper(object):
    def __init__(self, action_manager):
        """ Wraps an action manager instance with server endpoints

        Parameters
        ----------
        action_manager : ActionManager
            action manager instance to wrap
        """
        self.action_manager = action_manager
    
    @webframework.register_endpoint('/queue_action', output_is_json=False)
    def queue_action(self, body):
        """
        adds an action to the queue

        Parameters
        ----------
        body: str
            json.dumps(dict) with the following keys:
                function_name : str
                    The name of a function relative to the microscope object.
                    e.g. to `call scope.spoolController.StartSpooling()`, you 
                    would use a functionName of 'spoolController.StartSpooling'.
                    
                    The function should either return `None` if the operation 
                    has already completed, or function which evaluates to True 
                    once the operation has completed. See 
                    `scope.spoolController.StartSpooling()` for an example.
                args : dict, optional
                    a dictionary of arguments to pass to `function_name`
                nice : int, optional
                    priority with which to execute the function, by default 10. 
                    Functions with a lower nice value execute first.
                timeout : float, optional
                    A timeout in seconds from the current time at which the 
                    action becomes irrelevant and should be ignored. By default
                    1e6.
                max_duration : float
                    A generous estimate, in seconds, of how long the task might
                    take, after which the lasers will be automatically turned 
                    off and the action queue paused.
        """
        import json
        params = json.loads(body)
        function_name = params['function_name']
        args = params.get('args', {})
        nice = params.get('nice', 10.)
        timeout = params.get('timeout', 1e6)
        max_duration = params.get('max_duration', np.finfo(float).max)

        self.action_manager.QueueAction(function_name, args, nice, timeout,
                                        max_duration)


class ActionManagerServer(webframework.APIHTTPServer, ActionManagerWebWrapper):
    def __init__(self, action_manager, port, bind_address=''):
        """
        Server process to expose queue_action functionality to everything on the
        cluster network.

        NOTE - this will likely not be around long, as it would be preferable to
        add the ActionManagerWebWrapper to
        `PYME.acquire_server.AcquireHTTPServer` and run a single server process
        on the microscope computer.

        Parameters
        ----------
        action_manager : ActionManager
            already initialized
        port : int
            port to listen on
        bind_address : str, optional
            specifies ip address to listen on, by default '' will bind to local 
            host.
        """
        webframework.APIHTTPServer.__init__(self, (bind_address, port))
        ActionManagerWebWrapper.__init__(self, action_manager)
        
        self.daemon_threads = True
        self._server_thread = threading.Thread(target=self._serve)
        self._server_thread.daemon_threads = True
        self._server_thread.start()

    def _serve(self):
        try:
            logger.info('Starting ActionManager server on %s:%s' % (self.server_address[0], self.server_address[1]))
            self.serve_forever()
        finally:
            logger.info('Shutting down ActionManager server ...')
            self.shutdown()
            self.server_close()

