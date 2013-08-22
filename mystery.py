#!/usr/bin/env python

import wx
import logging

class MyFrame(wx.Frame):
    def __init__(self,parent,ID,title):
        wx.Frame.__init__(self,parent,ID,title)
        self.Show(True)
    
def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Began logging.")
    app = wx.App(False)  #do not redirect output
    frame = MyFrame(None,wx.ID_ANY,"Mystery")
    app.MainLoop()
    logging.info("Finished logging.")
    
        
if __name__ == "__main__":
    main()
