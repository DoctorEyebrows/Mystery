#!/usr/bin/env python

"""
The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import wx
import logging
from model import Model
from wx.lib.pubsub import Publisher as pub

class MyFrame(wx.Frame):
    def __init__(self,parent,ID,title):
        wx.Frame.__init__(self,parent,ID,title,size=(500,300))
        self.SetBackgroundColour((190,190,190))

        self.model = Model()
        self.currentBook = None
        pub.subscribe(self.onPub,"SAVED")
        
        #CREATE WIDGETS
        self.textbox = wx.TextCtrl(parent=self,id=wx.ID_ANY,
                                   style=wx.TE_MULTILINE|wx.TE_READONLY,
                                   size=(300,300))
        self.bRandom = wx.Button(parent=self, id=wx.ID_ANY,
                                 label="Random")
        self.bReveal = wx.Button(parent=self, id=wx.ID_ANY,
                                 label="Reveal")
        self.bReveal.Disable()
        self.statusBar = self.CreateStatusBar()

        #SPECIFY LAYOUT
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        
        sizer1.Add(self.textbox,0,wx.GROW)
        sizer1.Add(sizer2,1,wx.GROW)

        spacer1 = wx.StaticText(parent=self)
        spacer2 = wx.StaticText(parent=self)
        spacer3 = wx.StaticText(parent=self)

        sizer2.Add(spacer1,2)
        sizer2.Add(self.bRandom,0,wx.GROW)
        sizer2.Add(spacer2,1)
        sizer2.Add(self.bReveal,0,wx.GROW)
        sizer2.Add(spacer3,2)

        self.SetSizer(sizer1)
        self.SetAutoLayout(True)
        sizer1.Fit(self)

        #EVEND BINDING
        self.Bind(wx.EVT_BUTTON, self.OnRandom, self.bRandom)
        self.Bind(wx.EVT_BUTTON, self.OnReveal, self.bReveal)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show(True)

    def OnRandom(self,event):
        self.currentBook = self.model.getRandomBook()
        genreString = "\n".join(self.currentBook.genre)
        self.textbox.SetValue(genreString)
        self.bReveal.Enable()

    def OnReveal(self,event):
        try:
            self.textbox.SetValue(self.textbox.GetValue() +
                                  "\n\n" + self.currentBook.title +
                                  "\nby " + self.currentBook.author)
        except UnicodeDecodeError:
            print self.currentBook.title
        self.bReveal.Disable()

    def onPub(self,message):
        self.statusBar.SetStatusText("Saved %i books" % message.data)

    def OnClose(self,event):
        self.model.terminateThreads()
        self.Destroy()
    
def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Began logging.")
    app = wx.App(False)  #do not redirect output
    frame = MyFrame(None,wx.ID_ANY,"Mystery")
    app.MainLoop()
    logging.info("Finished logging.")
    
        
if __name__ == "__main__":
    main()
