import pickle
from modelThreads import Crawler, Parser, PeriodicAutosave

class Model():
    def __init__(self):
        try:
            self.load()
        except:
            self.books = []

        
        crawler = Crawler(self)     #downloads book webpages
        parser = Parser(self)       #extracts info, populates self.books
        saver = PeriodicAutosave(self)  #calls self.save() every 10 seconds
        
        #making the threads daemonic ensures everything terminates when i
        #close the IDLE shell
        #may become unnecessary when there's a GUI to terminate them properly
        crawler.daemon = True
        parser.daemon = True
        saver.daemon = True
        
        crawler.start()
        parser.start()
        saver.start()

    def save(self):
        fout = open("library.db",'wb')
        pickle.dump(self.books,fout)
        fout.close()

    def load(self):
        fin = open("library.db",'rb')
        self.books = pickle.load(fin)
        fin.close()

        print "Loaded", len(self.books), "books"
        

if __name__ == "__main__":
    model = Model()
