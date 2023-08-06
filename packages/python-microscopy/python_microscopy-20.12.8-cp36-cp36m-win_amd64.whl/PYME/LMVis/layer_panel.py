import wx
import wx.lib.newevent

#import PYME.ui.autoFoldPanel as afp
import PYME.ui.manualFoldPanel as afp
import PYME.ui.layerFoldPanel as lfp
import numpy as np

from PYME.ui import histLimits

import PYME.config

#DisplayInvalidEvent, EVT_DISPLAY_CHANGE = wx.lib.newevent.NewCommandEvent()

def CreateLayerPane(panel, visFr):
    pane = LayerPane(panel, visFr)
    panel.AddPane(pane)
    return pane

def CreateLayerPanel(visFr):
    import wx.lib.agw.aui as aui
    pane = LayerPane(visFr, visFr)
    pane.SetSize(pane.GetBestSize())
    pinfo = aui.AuiPaneInfo().Name("optionsPanel").Right().Caption('Layers').CloseButton(False).MinimizeButton(True).MinimizeMode(aui.AUI_MINIMIZE_CAPT_SMART|aui.AUI_MINIMIZE_POS_RIGHT)#.CaptionVisible(False)
    visFr._mgr.AddPane(pane, pinfo)

class LayerPane(afp.foldingPane):
    def __init__(self, panel, visFr, caption="Layers", add_button=True):
        afp.foldingPane.__init__(self, panel, -1, caption=caption, pinned=True)
        self.visFr = visFr
        
        self.il = wx.ImageList(16,16)
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, (16,16)))
        
        print('Image list size: %d' % self.il.GetImageCount())

        self.fp = afp.foldPanel(self, single_active_pane=True)

        self.AddNewElement(self.fp)
        
        self.pan = wx.Panel(self, -1)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        
        #self.nb = wx.Notebook(self.pan, size=(200, -1))
        #self.nb.AssignImageList(self.il)
        
        self.pages = []
        
        self.update()

        #self.vsizer.Add(self.nb, 1, wx.ALL|wx.EXPAND, 0)
        if add_button:
            bAddLayer = wx.Button(self.pan, -1, 'New', style=wx.BU_EXACTFIT)
            bAddLayer.Bind(wx.EVT_BUTTON, lambda e : self.visFr.add_pointcloud_layer())
    
            self.vsizer.Add(bAddLayer, 0, wx.ALIGN_CENTRE, 0)

        self.pan.SetSizerAndFit(self.vsizer)
        self.AddNewElement(self.pan)
        
        #print('Creating layer panel')
        
        self.visFr.layer_added.connect(self.update)
        
        #self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)

    def update(self, *args, **kwargs):
    
        #self.nb.DeleteAllPages()
        #for p in self.pages:
        #p.control.Destroy()
        #    p.dispose()
        #    pass
    
        #while (self.nb.GetPageCount() > 0):
        #    pg = self.nb.RemovePage(0)
    
        for p in self.pages:
            p.control.Close()
            p.dispose()
            pass
        
        self.fp.Clear()
        
        h = 0
    
        self.pages = []
        print('Creating layers GUI')
        for i, layer in enumerate(self.visFr.layers):
            #print(i, layer)
            item = lfp.LayerFoldingPane(self.fp, layer=layer, caption='Layer %d' % i, pinned=False, folded=False)
            page = layer.edit_traits(parent=item, kind='subpanel')
            item.AddNewElement(page.control)
            
            h = max(h, item.GetBestSize().height)
            self.fp.AddPane(item)
            self.pages.append(page)
            #self.fp.fold1(item)
            #print('Added layer: ', i)
            
        
        n_layers = len(self.pages)
        if  n_layers > 1:
            h += (n_layers -1)*(item.stCaption.GetBestSize().height+5)
        
        print('height: ', h)
        self.fp.SetMinSize((200, h))
        
        #self.vsizer.Fit(self.pan)
        #self.pan.SetMinSize(self.pan.GetSize())
        
    
        self.sizer.Fit(self)
    
        #print self.pan.GetBestSize(), self.pan.GetSize(), self.GetBestSize(), self.GetSize()
        print('NB best size: ' + repr(self.fp.GetBestSize()))
    
        try:
            self.GetParent().GetParent().Layout()
        except AttributeError:
            pass

        if n_layers > 1:
            item.Unfold()
        
    def _update(self, *args, **kwargs):
        
        #self.nb.DeleteAllPages()
        #for p in self.pages:
            #p.control.Destroy()
        #    p.dispose()
        #    pass
        
        while (self.nb.GetPageCount() > 0):
            pg = self.nb.RemovePage(0)

        for p in self.pages:
          p.control.Close()
          #p.dispose()
          pass
        
        self.pages = []
        for i, layer in enumerate(self.visFr.layers):
            page = layer.edit_traits(parent=self.nb, kind='subpanel')
            self.pages.append(page)
            self.nb.AddPage(page.control, 'Layer %d' % i)

        self.nb.InvalidateBestSize()

        h = self.nb.GetBestSize().height
        self.nb.SetMinSize((200, h))
        
        self.vsizer.Fit(self.pan)
        self.pan.SetMinSize(self.pan.GetSize())
        
        self.sizer.Fit(self)

        #print self.pan.GetBestSize(), self.pan.GetSize(), self.GetBestSize(), self.GetSize()
        print('NB best size: ' +  repr(self.nb.GetBestSize()))
        
        try:
            self.GetParent().GetParent().Layout()
        except AttributeError:
            pass
         
         
            
        #self.nb.AddPage(wx.Panel(self.nb), 'New', imageId=0)
        
    # def on_page_changed(self, event):
    #     if event.GetSelection() == (self.nb.GetPageCount() -1):
    #         #We have selected the 'new' page
    #
    #         wx.CallAfter(self.visFr.add_layer)
    #     else:
    #         event.Skip()
        
        