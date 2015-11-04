'''
Created on Oct 1, 2015

@author: davidsac
'''

import datetime
from Paper import Paper
from Author import Author
from Tag import Tag
from Publisher import Publisher

class ValidFakeDatabase:

    # initializes dummy data to return
  def __init__(self):
    self.paperA = Paper("12345", "The Health Benefits of the All-Bacon Diet", ["4445", "666", "123"], ["487", "448", "3", "27"], "Bacon is actually one of the healthiest foods of all time.  This is an abstract!  For the full article, download the PDF.", "1234", datetime.datetime(2013, 8, 4, 12, 30, 45), datetime.datetime.now(), "Name", ["ref1", "ref2", "ref3"], "14000", ["citation link 1", "citation link 2", "citation link 2"])
    self.paperB = Paper("90210", "The Dangers of Coding While Hungry", ["12068", "7797", "4326"], ["6", "48", "366", "2257"], " Abstracts never seem to be simple or contain useful information.", "444", datetime.datetime(2013, 8, 4, 12, 30, 45), datetime.datetime.now(), "Name", ["ref1", "ref2", "ref3"], "14000", ["citation link 1", "citation link 2", "citation link 2"])
    self.paperC = Paper("666", "The Struggles of Eating a Giordano's Pizza Alone", ["567", "2213", "989"], ["6237", "3177", "432"], "Abstracts are the SparkNotes of the academic world.", "12534434", datetime.datetime(1999, 7, 6, 12, 30, 45), datetime.datetime.now(), "Name", ["ref1", "ref2", "ref3"], "14000", ["citation link 1", "citation link 2", "citation link 2"])
    
    self.authorA = Author("55555", "Shia Leboeuf", "4444", [])
    self.authorB = Author("43216", "Andrew Davidson", "1", [])
    self.authorC = Author("6542", "William Shakespeare", "11542", [])
    self.authorD = Author("64632", "Edsger Dijkstra", "147", [])
    self.authorE = Author("63421", "Alan Turing", "40000", [])
    
    self.tagA = Tag("112", "Genetics", "40000", [])
    self.tagB = Tag("775", "Bioinformatics", "12345", [])
    self.tagC = Tag("842", "Search Engines", "5555", [])
    self.tagD = Tag("973", "Artificial Intelligence", "42", [])
    
    self.publisherA = Publisher("1233", "Your Favorite Publisher",0)
    self.publisherB = Publisher("3468", "Prentice Hall",0)
    self.publisherC = Publisher("8372", "Rose-Hulman",0)
    
    #Takes in:
    #  - a string of the paper's title
    #  - a list of string authorIDs
    #  - a list of string tagIDs
    #  - a string of the paper's abstract
    #  - a string of the userID:  NOT IMPLEMENTED YET
    #  - a string of the date that the article was published:  FORMAT UNDECIDED SO FAR
    #  - a string of the publisherID
    #  - a list of strings of other papers that cite it:  FORMAT UNDECIDED SO FAR
    #  - a list of references to other papers :  FORMAT UNDECIDED SO FAR 
    #Returns a string paperID
  def putPaper(self, title, authors, tags, abstract, userID, datePublished, publisherID, citedBys, references):
    if not isinstance(title, basestring):
      raise Exception("title must be a string")
    if not isinstance(abstract, basestring):
      raise Exception("abstract must be a string")
    if not isinstance(datePublished, datetime.datetime):
      raise Exception("datePublished must be a datetime")
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")
    if not isinstance(tags, list):
      raise Exception("tags must be a list")
    if not self.representsInt(publisherID):
      raise Exception("publisherID must currently be either an integer or a string that represents an integer")
    for tag in tags:
      if not self.representsInt(tag):
        raise Exception("This method takes a list of tagIDs.  TagIds must currently be either an integer or a string that represents an integer") 
    if not isinstance(authors, list):
      raise Exception("authors must be a list")
    for author in authors:
      if not self.representsInt(author):
        raise Exception("This method takes a list of authorIDs.  AuthorIds must currently be either an integer or a string that represents an integer")   
    return "12345"

    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    if not isinstance(name, basestring):
      raise Exception("name must be a string")
    return "12345"
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    if not isinstance(name, basestring):
      raise Exception("name must be a string")       
    return "23456"
  
    #Takes in a string of the tag's name
  def putTag(self, tag):
    if not isinstance(tag, basestring):
      raise Exception("tag must be a string")    
    return
  
    #Takes in integer paperID and string tag name corresponding to the tag and paper to link together
  def tagPaper(self, paperID, tag):
    if not self.representsInt(paperID):
      raise Exception("paperID must currently be either an integer or a string that represents an integer")
    if not isinstance(tag, basestring):
      raise Exception("tag must be a string")   
    
    # Takes in an integer publisherID
    # Returns a publisher object
  def getPublisher(self, publisherID):
    if not self.representsInt(publisherID):
      raise Exception("publisherID must currently be either an integer or a string that represents an integer")
    return self.publisherA

    #Takes in an integer paperID of the paper to increment
  def incrementPaperViews(self, paperID):
    if not self.representsInt(paperID):
      raise Exception("paperID must currently be either an integer or a string that represents an integer")
  
    # Returns a list of all publisher objects
  def getAllPublishers(self):
    return [self.publisherA, self.publisherB, self.publisherC] 
    
    # Takes in a string of the tag's name
    # Returns a tag object
  def getTag(self, tag):  
    if not isinstance(tag, basestring):
      raise Exception("tag must be a string") 
    return self.tagA     
    
    # Takes in a list of strings with names of authors to search for
    #  If only one author is needed, please pass in a list with a single element
    # Returns a list of Author objects 
  def getAuthorsMatchingAuthorNames(self, namesToSearch):
    if not isinstance(namesToSearch, list):
      raise Exception("namesToSearch must be a list")
    for name in namesToSearch:
      if not isinstance(name, basestring):
        raise Exception("This method takes a list of author names, which must be strings.")     
    return [self.authorA, self.authorB, self.authorC, self.authorD, self.authorE] 
    
    # Returns a list of all tag objects
  def getAllTags(self):
    return [self.tagA, self.tagC, self.tagB, self.tagD]
	
  def getPapersMatchingAuthorNames(self, namesToSearch):
    if not isinstance(namesToSearch, list):
      raise Exception("namesToSearch must be a list")
    for name in namesToSearch:
      if not isinstance(name, basestring):
        raise Exception("This method takes a list of author names, which must be strings.")     
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in a list of string tag names
    # Returns a list of paper objects that match
  def getPapersMatchingTags(self, tags):
    if not isinstance(tags, list):
      raise Exception("tags must be a list")
    for tag in tags:
      if not isinstance(tag, basestring):
        raise Exception("This method takes a list of tag names, which must be strings.")          
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in a string of the title of the paper
    # Returns a list of paper objects
  def getPapersMatchingTitle(self, title):
    if not isinstance(title, basestring):
      raise Exception("title must be a string")
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in a list of integer authorIDs
    # Returns a list of paper objects
  def getPapersMatchingAuthorIDs(self, authorIDs):
     if not isinstance(authorIDs, list):
      raise Exception("authorIDs must be a list")
    for authorID in authorIDs:
      if not self.representsInt(authorID):
        raise Exception("This method takes a list of authorIDs, which must be ints, or strings representing ints.")  
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in an integer year before the current year
    # returns a list of paper objects
  def getPapersPublishedInYear(self, year):
    if not self.representsInt(year):
      raise Exception("year must currently be either an integer or a string that represents an integer")
    if not isinstance(year, int):
      year= int(year)
    if year > datetime.datetime.today().year:
      raise Exception("the publishing year must not be in the future!")
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    if not self.representsInt(paperID):
      raise Exception("paperID must currently be either an integer or a string that represents an integer")
    return self.paperA
    
    # Returns a list of paper objects
  def getTopAuthors(self, top_bound=100):
    if not isinstance(top_bound, int):
      raise Exception("top_bound must be an int")
    if top_bound < 1:
      raise Exception("top_bound must be greater than zero")
    return [self.authorA, self.authorB, self.authorC, self.authorD, self.authorE] 
    
    # Returns a list of author objects
  def getTopPapers(self, top_bound=100):
    if not isinstance(top_bound, int):
      raise Exception("top_bound must be an int")
    if top_bound < 1:
      raise Exception("top_bound must be greater than zero")
    return [self.paperA,self.paperB,self.paperC]
    
    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    if not self.representsInt(authorID):
      raise Exception("authorID must currently be either an integer or a string that represents an integer")
    return self.authorA
	
  def putUser(self, Name, facebookID = None):
    if not isinstance(Name, basestring):
	  raise Exception("Name must currently be a string")
    if not facebookID == None:
      if not isinstance(facebookID, basestring):
	    raise Exception("facebookID must currently be a string")
    return 0

  def assignUserFacebookID(self, userID, facebookID):
    if not isinstance(facebookID, basestring):
	  raise Exception("facebookID must currently be a string")
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")

  def getUserByID(self, userID):
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")
	return self.userA
	
  def getUserByFacebookID(self, facebookID):
    if not isinstance(facebookID, basestring):
	  raise Exception("facebookID must currently be a string")
    return self.userA

  def putFavoritePaper(self, userID, paperID, favoriteLevel):
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")
    if not self.representsInt(paperID):
      raise Exception("paperID must currently be either an integer or a string that represents an integer")
    if not isinstance(favoriteLevel, int):
      raise Exception("favoriteLevel must be an int")
    return 3
  
  def putFavoriteAuthor(self, userID, authorID, favoriteLevel):
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")
    if not self.representsInt(authorID):
      raise Exception("authorID must currently be either an integer or a string that represents an integer")
    if not isinstance(favoriteLevel, int):
      raise Exception("favoriteLevel must be an int")
    return 3

  def putFavoriteTag(self, userID, tag, favoriteLevel):
    if not self.representsInt(userID):
      raise Exception("userID must currently be either an integer or a string that represents an integer")
    if not isinstance(tag, basestring):
      raise Exception("tag must be a string")
    if not isinstance(favoriteLevel, int):
      raise Exception("favoriteLevel must be an int")
    return 3

  def addStalker(self, stalkerID, userIDToStalk):
    if not self.representsInt(stalkerID):
      raise Exception("stalkerID must currently be either an integer or a string that represents an integer")
    if not self.representsInt(userIDToStalk):
      raise Exception("userIDToStalk must currently be either an integer or a string that represents an integer")
  
    #does nothing in this case
  def clearDatabase(self):
    pass
    
    #DO NOT INTERFACE WITH THIS METHOD!  This should only be used in this class.
    #A helper method to check that various fields passed in are ints or represent ints
  def representsInt(self, s):
    if isinstance(s, int):
      return True
    if isinstance(s, basestring):
      try: 
        int(s)
        return True
      except ValueError:
        return False
    return False
	

    
  
        
