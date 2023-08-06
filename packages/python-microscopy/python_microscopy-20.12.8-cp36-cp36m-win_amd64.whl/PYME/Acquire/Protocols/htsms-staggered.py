from PYME.Acquire.protocol import *

# T(when, what, *args) creates a new task. "when" is the frame number, "what" is a function to
# be called, and *args are any additional arguments.
taskList = [
    T(-1, scope.l642.TurnOn),
    T(0, scope.focus_lock.DisableLock),
    T(8000, scope.l560.TurnOn),
    T(maxint, scope.turnAllLasersOff),
    T(maxint, scope.focus_lock.EnableLock),
    # T(maxint, scope.spoolController.LaunchAnalysis)
]

metaData = [
    ('Protocol.DataStartsAt', 0),
]

preflight = []  # no preflight checks

# must be defined for protocol to be discovered
PROTOCOL = TaskListProtocol(taskList, metaData, preflight, filename=__file__)
PROTOCOL_STACK = ZStackTaskListProtocol(taskList, 1, 1000, metaData, preflight, slice_order='triangle',
                                        require_camera_restart=False, filename=__file__)
