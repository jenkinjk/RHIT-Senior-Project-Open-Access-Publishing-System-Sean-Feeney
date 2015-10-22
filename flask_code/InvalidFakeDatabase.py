'''
Created on Oct 1, 2015

@author: davidsac
'''

class InvalidFakeDatabase:

  def __init__(self):
    pass
    
  
  def putPaper(self, title, authors, tags, abstract, userID, datePublished, publisher, citedBys, references):
    return None

  def putAuthor(self, name):
    return None

  def putTag(self, name):
    return None

  def tagPaper(self, paperID, tagID):
    pass

  def getPublisher(self, publisherID):
    return None

  def incrementPaperViews(self, paperID):
    pass
    
  def putPublisher(self, name):
    return None
  
  def getAllPublishers(self):
    return []
    
  def getTag(self, tagID):  
    return None
    
  def getAuthorsMatchingAuthors(self, namesToSearch):  
    return []
    
  def getAllTags(self):
    return[]
    
  def getPapersMatchingTags(self, tags):
    return[]
    
  def getPapersMatchingTitle(self, title):
    return []
    
  def getPapersForAuthor(self, authorID):
    return []
    
  def getPapersPublishedInYear(self, year):
    return []
    
  def getPaper(self, paperID):
    return None

  def getTopAuthors(self):
    return []

  def getTopPapers(self):
    return []

  def getAuthor(self, authorID):
    return None

  def clearDatabase(self):
    pass
    
    
    
    