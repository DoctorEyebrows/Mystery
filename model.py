import pickle, random
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
