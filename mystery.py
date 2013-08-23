#!/usr/bin/env python

import wx
import logging

class MyFrame(wx.Frame):
    def __init__(self,parent,ID,title):
        wx.Frame.__init__(self,parent,ID,title,size=(500,300))
        self.SetBackgroundColour((190,190,190))

        #CREATE WIDGETS
        self.textbox = wx.TextCtrl(parent=self,id=wx.ID_ANY,
                                   style=wx.TE_MULTILINE|wx.TE_READONLY,
                                   size=(300,300))
        self.bRandom = wx.Button(parent=self, id=wx.ID_ANY,
                                 label="Random")
        self.bReveal = wx.Button(parent=self, id=wx.ID_ANY,
                                 label="Reveal")

        #SPECIFY LAYOUT
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        
        sizer1.Add(self.textbox,0,wx.GROW)
        sizer1.Add(sizer2,1,wx.GROW)

        spacer1 = wx.StaticText(parent=self)
        spacer2 = wx.StaticText(parent=self)
        spacer3 = wx.StaticText(parent=self)

        sizer2.Add(spacer1,2)
        sizer2.Add(self.bRandom,0,wx.ALIGN_CENTER)
        sizer2.Add(spacer2,1)
        sizer2.Add(self.bReveal,0,wx.ALIGN_CENTER)
        sizer2.Add(spacer3,2)

        self.SetSizer(sizer1)
        self.SetAutoLayout(True)
        sizer1.Fit(self)

        #EVEND BINDING
        self.Bind(wx.EVT_BUTTON, self.OnRandom, self.bRandom)
        self.Bind(wx.EVT_BUTTON, self.OnReveal, self.bReveal)

        self.Show(True)

    def OnRandom(self,event):
        print event

    def OnReveal(self,event):
        print event
    
def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Began logging.")
    app = wx.App(False)  #do not redirect output
    frame = MyFrame(None,wx.ID_ANY,"Mystery")
    app.MainLoop()
    logging.info("Finished logging.")
    
        
if __name__ == "__main__":
    main()
