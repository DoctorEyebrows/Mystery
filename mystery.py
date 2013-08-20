import threading, Queue, urllib2

class Model():
    def __init__(self):
        crawler = Crawler(name="Crawler")
        parser = Parser(self)
        self.books = []

        crawler.start()
        parser.start()
    
class Book():
    def __init__(self,title,genre):
        self.title = title
        self.genre = genre


class Crawler(threading.Thread):
    """
    Thread that downloads book summary pages from www.iblist.com
    """

    def run(self):
        i = 1
        consecutiveHoles = 0
        while True:
            page = urllib2.urlopen("http://www.iblist.com/book%i.htm" % i)
            html = page.read()
            if html != "Error: No book found.":
                pageQueue.put(html)
                consecutiveHoles = 0
            else:
                print "Error: No book found", i
                consecutiveHoles += 1
                if consecutiveHoles >= 100:
                    break
            i += 1
            
        print "I think we're finished now. No more books."
            
class Parser(threading.Thread):
    """
    Extracts information from a book's html page
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Parser")
        self.model = model

    def run(self):
        while True:
            html = pageQueue.get(block=True)

            #extract title:
            start = html.find("<a class=")
            start = html.find(">",start) + 1
            end = html.find("<",start)
            title = html[start:end]
            
            #extract genres:
            start = html.find("<i>Genre:</i> ") + 14
            end = html.find("<br />",start)
            genreString = html[start:end]

            #remove tags from the html snippet we've excised:
            while True:
                start = genreString.find("<")
                if start == -1:
                    break
                end = genreString.find(">",start) + 1
                genreString = genreString[:start] + genreString[end:] #snip

            genre = genreString.split("&rarr;")
            genre = map(str.strip,genre)
            
            print title, genre

if __name__ == "__main__":
    pageQueue = Queue.Queue()
    
    model = Model()
