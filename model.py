import pickle, random
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

from modelThreads import Crawler, Parser, PeriodicAutosave
from wx.lib.pubsub import Publisher as pub

class Model():
    def __init__(self):
        try:
            self.load()
        except:
            self.books = []

        
        self.crawler = Crawler(self)         #downloads book webpages
        self.parser = Parser(self)           #extracts info, populates self.books
        self.saver = PeriodicAutosave(self)  #calls self.save() every 10 seconds
        
        #making the threads daemonic ensures everything terminates when i
        #close the IDLE shell
        #may become unnecessary when there's a GUI to terminate them properly
        self.crawler.daemon = True
        self.parser.daemon = True
        self.saver.daemon = True
        
        self.crawler.start()
        self.parser.start()
        self.saver.start()

    def getRandomBook(self):
        return random.choice(self.books)

    def getBookCount(self):
        return len(self.books)

    def getRandomBookWithGenre(self,*genres):
        order = range(len(self.books))
        random.shuffle(order)
        for i in order:
            fail = False
            for genre in genres:
                if not genre in self.books[i].genre:
                    fail = True
                    break
            if fail:
                continue
            else:
                return self.books[i]

        return None

    def save(self):
        fout = open("library.db",'wb')
        pickle.dump(self.books,fout)
        fout.close()

        print "Saved", len(self.books), "books"
        pub.sendMessage("SAVED",len(self.books))

    def load(self):
        fin = open("library.db",'rb')
        self.books = pickle.load(fin)
        fin.close()

        print "Loaded", len(self.books), "books"

    def terminateThreads(self):
        print "Terminating threads"
        self.crawler.terminate()
        self.parser.terminate()
        self.saver.terminate()
        

if __name__ == "__main__":
    model = Model()
