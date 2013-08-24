import threading, Queue, urllib2, time

class Crawler(threading.Thread):
    """
    Thread that downloads book summary pages from www.iblist.com
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Crawler")
        self.model = model
        self.die = False

    def run(self):
        i = len(self.model.books) + 1
        consecutiveHoles = 0
        while True:
            if self.die:
                break
            
            page = urllib2.urlopen("http://www.iblist.com/book%i.htm" % i)
            html = page.read()
            if html != "Error: No book found.":
                pageQueue.put(html)
                consecutiveHoles = 0
            else:
                print "Error: No book found", i
                consecutiveHoles += 1
                if consecutiveHoles >= 100:
                    print "I think we're finished now. No more books."
                    break
            i += 1

        print self.name, "terminated"

    def terminate(self):
        self.die = True
            
        
            
class Parser(threading.Thread):
    """
    Extracts information from a book's html page
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Parser")
        self.model = model
        self.die = False

    def run(self):
        while True:
            if self.die:
                break
            
            html = pageQueue.get(block=True)

            #extract title:
            start = html.find("<a class=")
            start = html.find(">",start) + 1
            end = html.find("<",start)
            title = html[start:end]

            #extract author:
            start = html.find("iblist.com/author")
            start = html.find(">",start) + 1
            end = html.find("<",start)
            author = html[start:end]
            author = author.replace("  "," ")   #get rid of double spaces
                                                #(no idea why but they're always there)
            
            #extract genres:
            genre = []
            start = 0
            while html.find("genre=",start) != -1:
                start = html.find("genre=",start)
                start = html.find(">",start) + 1
                end = html.find("<",start)
                genre.append(html[start:end])
            
            
            if genre == [] or genre[0] != "Fiction":
                continue    #filtering any genre-less or non-fiction books
            
            while "Fiction" in genre:
                genre.remove("Fiction") #they're all meant to be fiction
                genre = set(genre)      #removing multiple occurances
                genre = list(genre)
                book = Book(title,author,genre)
                self.model.books.append(book)

        print self.name, "terminated"

    def terminate(self):
        self.die = True
                
class PeriodicAutosave(threading.Thread):
    """
    Triggers model.save() every 10 seconds
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Autosave")
        self.model = model
        self.die = False
    
    def run(self):
        while True:
            time.sleep(10)
            if self.die:
                break
            
            self.model.save()

        print self.name, "terminated"

    def terminate(self):
        self.die = True


class Book():
    def __init__(self,title,author,genre):
        self.title = title
        self.author = author
        self.genre = genre


pageQueue = Queue.Queue()
