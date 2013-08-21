import threading, Queue, urllib2, time

class Crawler(threading.Thread):
    """
    Thread that downloads book summary pages from www.iblist.com
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Crawler")
        self.model = model

    def run(self):
        i = len(self.model.books) + 1
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

            #extract author:
            start = html.find("iblist.com/author")
            start = html.find(">",start) + 1
            end = html.find("<",start)
            author = html[start:end]
            
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
            
            if genre[0] == "Fiction":
                del genre[0]    #they're all meant to be fiction anyway
                #print "%s\n%s\n%s\n\n" % (title, author, genre)
                book = Book(title,author,genre)
                self.model.books.append(book)
                
class PeriodicAutosave(threading.Thread):
    """
    Triggers model.save() every 10 seconds
    """

    def __init__(self,model):
        threading.Thread.__init__(self,name="Autosave")
        self.model = model
    
    def run(self):
        while True:
            time.sleep(10)
            self.model.save()


class Book():
    def __init__(self,title,author,genre):
        self.title = title
        self.author = author
        self.genre = genre


pageQueue = Queue.Queue()
