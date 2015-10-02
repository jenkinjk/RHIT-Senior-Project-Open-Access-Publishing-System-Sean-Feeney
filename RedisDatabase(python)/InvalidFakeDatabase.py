'''
Created on Oct 1, 2015

@author: davidsac
'''

class InvalidFakeClass:

  def __init__(self):
    
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
  def putPaper(self, title, authors, tags, abstract, userID, datePublished, publisher, citedBys, references):
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
   
    #Takes in a string of the tag's name
    #Returns a string tagID 
  def putTag(self, name):
    
    #Takes in a list of strings with names of authors to search for
    #  If only one author is given, give a list with a single element
    #Returns an empty list
  def getAuthorsMatchingAuthors(self, namesToSearch):  
    return []
    
    #Returns an empty list
  def getAllTags(self):
    return[]
    
    #Takes in a list of integer tagIDs
    #Returns an empty list
  def getPapersMatchingTags(self, tags):
    return[]
    
    #Takes in a string of the title of the paper
    #Returns None
  def getPapersMatchingTitle(self, title):
    return None
    
    #Takes in an integer authorID
    #Returns an empty list
  def getPapersForAuthor(self, authorID):
    return []
    
    #Takes in an integer year before the current year
    #returns an empty list
  def getPapersPublishedInYear(self, year):
    return []
    
    #Takes in an integer paperID
    #Returns None
  def getPaper(self, paperID):
    return None
    
    #Returns an empty list
  def getTopAuthors(self):
    return []
    
    #Returns an empty list
  def getTopPapers(self):
    return []
    
    #Takes in an integer authorID
    #Returns None
  def getAuthor(self, authorID):
    return None