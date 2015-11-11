'''
Created on Oct 1, 2015

@author: davidsac
'''

class InvalidFakeDatabase:

  def __init__(self, mode):
    pass
   
  def clearDatabase(self):
    pass

  def putAuthor(self, name):
    return None

  def putTag(self, name):
    return None

  def putPublisher(self, name):
    return None

  def putPaper(self, title, authors, tags, abstract, postedByUserID, datePublished, publisherID, citedBys, references):
    return None

  def getAuthor(self, authorID):
    return None

  def getTag(self, tag):
    return None
  
  def getPublisher(self, publisherID):
    return None

  def getPaper(self, paperID):
    return None

  def getPapersForAuthorID(self, authorID):
    return []

  def getAllTags(self):
    return []

  def getAllPublishers(self):
    return []

  def getPapersPublishedInYear(self, year):
    return []
    
  def getTopAuthors(self, top_bound=100):
    return []
    
  def getTopPapers(self, top_bound=100):
    return []
  
  def incrementPaperViews(self, paperID):
    pass

  def tagPaper(self, paperID, tag):
    pass  

  def getAuthorsMatchingAuthorNames(self, namesToSearch):
    return []
	
  def getPapersMatchingAuthorNames(self, namesToSearch):
    return []

  def getPapersMatchingAuthorIDs(self, IDsToSearch):
    return []
    
  def getPapersMatchingTags(self, tags):
    return []
    
  def getPapersMatchingTitle(self, title):
    return []
	
  def putUser(self, Name, facebookID = None):
    return None

  def assignUserFacebookID(self, id, facebookID):
    pass

  def getUserByID(self, id):
    return None
	
  def getUserByFacebookID(self, facebookID):
    return None

  def putFavoritePaper(self, userID, paperID, favoriteLevel):
    pass
  
  def putFavoriteAuthor(self, userID, authorID, favoriteLevel):
    pass

  def putFavoriteTag(self, userID, tag, favoriteLevel):
    pass
	
  def addStalker(self, stalkerID, userIDToStalk):
    pass