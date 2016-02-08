'''
Created on Oct 6, 2015
@author: davidsac
'''

import redis
import re
from datetime import datetime, date
from Author import Author
from Tag import Tag
from Paper import Paper
from Publisher import Publisher
from User import User

class RedisDatabase():

  def __init__(self, mode):
    if(mode == "Test"): #We can connect to a second database, which we can clean out without losing production data
      self.redisDB = redis.StrictRedis(host='openscholar.csse.rose-hulman.edu', port=6379, db=2)
      self.clearDatabase()
    elif(mode == "Development"): #We can connect to a second database, which we can clean out without losing production data
      self.redisDB = redis.StrictRedis(host='openscholar.csse.rose-hulman.edu', port=6379, db=1)
    elif(mode == "Production"): #We can connect to a second database, which we can clean out without losing production data
      self.redisDB = redis.StrictRedis(host='openscholar.csse.rose-hulman.edu', port=6379, db=0)
      
    self.wordsToFilter = set(["the","a","an","the","with","of","for","to","from","on","my","his","her","our","is", "your","in","that","have","has", "be", "it", "not","he","she","you","me","them","us","and","do","at","this","but","by","they","if","we","say", "or","will","one","can","like","no","when"])	
    
  def clearDatabase(self):
    self.redisDB.flushdb()
    self.redisDB.set("Authors:IDCounter",0)
    self.redisDB.set("Papers:IDCounter",0)
    self.redisDB.set("Publishers:IDCounter",0)
    self.redisDB.set("Users:IDCounter",0)
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = self.redisDB.get("Authors:IDCounter")
    self.redisDB.set("Author:"+id+":Name", name)
    self.redisDB.set("Author:"+id+":ViewCount", 0)
    self.redisDB.zadd("Authors",0, id)
    words = self.getSearchWords(name)
    for word in words:
      self.redisDB.zadd("AuthorWord:"+word,0, id)
    self.redisDB.incr("Authors:IDCounter")
    return id
    
    #Takes in a string of the tag's name
  def putTag(self, name):
    if self.getTag(name)==None:
      self.redisDB.set("Tag:"+name+":ViewCount", 0)
      self.redisDB.zadd("Tags",0, name)
    return
  
    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    id = self.redisDB.get("Publishers:IDCounter")
    self.redisDB.set("Publisher:"+id+":Name", name)
    self.redisDB.set("Publisher:"+id+":ViewCount", 0)
    self.redisDB.zadd("Publishers",0, id)
    self.redisDB.incr("Publishers:IDCounter")
    return id

    #Takes in:
    #  - a string of the paper's title
    #  - a list of string authorIDs
    #  - a list of string tags
    #  - a string of the paper's abstract
    #  - a string of the userID:  NOT IMPLEMENTED YET
    #  - a string of the date that the article was published:  FORMAT UNDECIDED SO FAR
    #  - a string of the publisherID
    #  - a list of strings of other papers that cite it:  FORMAT UNDECIDED SO FAR
    #  - a list of references to other papers :  FORMAT UNDECIDED SO FAR 
    #Returns a string paperID
  def putPaper(self, title, authors, tags, abstract, postedByUserID, datePublished, publisherID, isUploaded):
    datePosted = datetime.now()
    #print "putting paper with timestamp", datePosted
    id = self.redisDB.get("Papers:IDCounter")
    self.redisDB.set("Paper:"+id+":PublisherID", publisherID)
    self.redisDB.set("Paper:"+id+":Abstract", abstract)
    self.redisDB.set("Paper:"+id+":Title", title)
    self.redisDB.set("Paper:"+id+":PostedByUserID", postedByUserID)
    self.redisDB.set("Paper:"+id+":ViewCount", 0)
    print "datePublished:", datePublished
    self.redisDB.set("Paper:"+id+":DatePublished", str(datePublished))
    self.redisDB.set("Paper:"+id+":DatePosted", str(datePosted))
    self.redisDB.set("Paper:"+id+":IsUploaded", isUploaded)
    self.redisDB.zadd("Papers",0, id)
    for author in authors:
      self.redisDB.sadd("Author:"+author+":Papers", id)
      self.redisDB.sadd("Paper:"+id+":Authors", author)
    for tag in tags:
      self.putTag(tag)
      self.redisDB.zadd("Tag:"+tag+":Papers", 0, id)
      self.redisDB.sadd("Paper:"+id+":Tags", tag)
    self.redisDB.zadd("YearPublished:"+str(datePublished.year), 0, id)
    words = self.getSearchWords(title)
    for word in words:
      self.redisDB.zadd("PaperWord:"+word,0, id)
    self.redisDB.incr("Papers:IDCounter")
    return id

  def updatePaper(self, id, title, authors, tags, abstract, postedByUserID, datePublished, publisherID, isUploaded):
    paper = self.getPaper(id)
    self.redisDB.set("Paper:"+id+":PublisherID", publisherID)
    self.redisDB.set("Paper:"+id+":Abstract", abstract)
    self.redisDB.set("Paper:"+id+":Title", title)
    self.redisDB.set("Paper:"+id+":PostedByUserID", postedByUserID)
    self.redisDB.set("Paper:"+id+":DatePublished", str(datePublished))
    self.redisDB.set("Paper:"+id+":IsUploaded", isUploaded)

    authorsToRem = set([])
    authorsToAdd = set([])

    for author in authors:
      authorsToAdd.add(author)
    for author in paper.authorIDs:
      if author in authorsToAdd:
        authorsToAdd.remove(author)
      else:
        authorsToRem.add(author)

    for author in authorsToRem:
      self.redisDB.srem("Author:"+author+":Papers", id)
      self.redisDB.srem("Paper:"+id+":Authors", author)
    for author in authorsToAdd:
      self.redisDB.sadd("Author:"+author+":Papers", id)
      self.redisDB.sadd("Paper:"+id+":Authors", author)

    tagsToRem = set([])
    tagsToAdd = set([])

    for tag in tags:
      self.putTag(tag)
      tagsToAdd.add(tag)
    for tag in paper.tags:
      if tag in tagsToAdd:
        tagsToAdd.remove(tag)
      else:
        tagsToRem.add(tag)
    for tag in tagsToAdd:
      self.redisDB.zadd("Tag:"+tag+":Papers", paper.viewCount, id)
      self.redisDB.sadd("Paper:"+id+":Tags", tag)
    for tag in tagsToRem:
      self.redisDB.zrem("Tag:"+tag+":Papers", id)
      self.redisDB.srem("Paper:"+id+":Tags", tag)

    if not datePublished.year == paper.datePublished.year:
      self.redisDB.zadd("YearPublished:"+str(datePublished.year), paper.viewCount, id)
      self.redisDB.zrem("YearPublished:"+str(paper.datePublished.year), id)

    newWords = self.getSearchWords(title)
    oldWords = self.getSearchWords(paper.title)

    wordsToRem = set([])
    wordsToAdd = set([])

    for word in newWords:
      wordsToAdd.add(word)
    for word in oldWords:
      if word in wordsToAdd:
        wordsToAdd.remove(word)
      else:
        wordsToRem.add(word)

    for word in wordsToAdd:
      self.redisDB.zadd("PaperWord:"+word,paper.viewCount, id)
    for word in wordsToRem:
      self.redisDB.zrem("PaperWord:"+word, id)

    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    name = self.redisDB.get("Author:"+authorID+":Name")
    if name == None:
      return None
    paperIDs = list(self.redisDB.smembers("Author:"+authorID+":Papers"))
    paperAuthorNames = []
    paperTitles = []
    paperDatesPublished = []
    for paperID in paperIDs:
      paper = self.getPaper(paperID)
      paperAuthorNames.append(paper.authorNames)
      paperTitles.append(paper.title)
      paperDatesPublished.append(paper.datePublished)
    viewCount = self.redisDB.get("Author:"+authorID+":ViewCount")
    return Author(authorID, name, viewCount, paperIDs, paperTitles, paperAuthorNames, paperDatesPublished)
  
    # Takes in a string tag
    # Returns a tag object
  def getTag(self, tag):
    viewCount = self.redisDB.get("Tag:"+tag+":ViewCount")
    if viewCount == None:
      return None
    paperIDs = self.redisDB.zrange("Tag:"+tag+":Papers",0,-1)
    return Tag(tag, viewCount, paperIDs)  
  
    # Takes in an integer publisherID
    # Returns a publisher object
  def getPublisher(self, publisherID):
    name = self.redisDB.get("Publisher:"+publisherID+":Name")
    if name == None:
      return None
    viewCount = self.redisDB.get("Publisher:"+publisherID+":ViewCount")
    return Publisher(publisherID, name, viewCount)

    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    title = self.redisDB.get("Paper:"+paperID+":Title")
    if title == None:
      return None
    authorIDs = list(self.redisDB.smembers("Paper:"+paperID+":Authors"))
    tags = list(self.redisDB.smembers("Paper:"+paperID+":Tags"))
    abstract = self.redisDB.get("Paper:"+paperID+":Abstract")
    publisherID = self.redisDB.get("Paper:"+paperID+":PublisherID")
    viewCount = self.redisDB.get("Paper:"+paperID+":ViewCount")
    datePosted = datetime.strptime(self.redisDB.get("Paper:"+paperID+":DatePosted"), "%Y-%m-%d %H:%M:%S.%f")
    # TODO: fix this later
    datePublished = self.redisDB.get("Paper:"+paperID+":DatePublished")
    print "datePublished for paper", paperID, title, ":", datePublished
    datePublished = date(int(datePublished[0:4]), int(datePublished[5:7]), int(datePublished[8:10]))
    postedByUserID = self.redisDB.get("Paper:"+paperID+":PostedByUserID")
    references = list(self.redisDB.smembers("Paper:"+paperID+":References"))
    citedBys = list(self.redisDB.smembers("Paper:"+paperID+":CitedBys"))
    isUploaded = self.redisDB.get("Paper:"+paperID+":IsUploaded") =='True'
    authorNames = []
    for authorID in authorIDs:
      authorNames.append(self.redisDB.get("Author:"+authorID+":Name"))
    publisherGuy = self.getPublisher(publisherID)
    if publisherGuy is None:
      publisherName = "No Publisher Name"
    else:
      publisherName = publisherGuy.name
    return Paper(paperID, title, authorIDs, tags, abstract, publisherID, datePublished, datePosted, postedByUserID, references, viewCount, citedBys, publisherName, authorNames, isUploaded)

    #THIS METHOD CAN EASILY BE IMPLEMENTED OUTSIDE OF THIS CLASS.  CONSIDER REMOVING TO REMOVE COMPLEXITY FROM CODEBASE
    # Takes in an integer authorID
    # Returns a list of paper objects
  def getPapersForAuthorID(self, authorID):
    rawPapers = list(self.redisDB.smembers("Author:"+authorID+":Papers"))
    papers=[]
    for rawPaper in rawPapers:
      paper = self.getPaper(rawPaper)
      papers.append(paper) 
    return papers

    # Returns a list of all tag objects
  def getAllTags(self):
    rawTags = self.redisDB.zrange("Tags",0,-1)
    tags = []
    for rawTag in rawTags:
      tag = self.getTag(rawTag)
      tags.append(tag)
    return tags
  
    # Returns a list of all publisher objects
  def getAllPublishers(self):
    rawPublishers = self.redisDB.zrange("Publishers",0,-1)
    publishers = []
    for rawPublisher in rawPublishers:
      publisher = self.getPublisher(rawPublisher)
      publishers.append(publisher)
    return publishers
    
    # Takes in an integer year before the current year
    # returns a list of paper objects
  def getPapersPublishedInYear(self, year):
    rawPapers = self.redisDB.zrange("YearPublished:"+year,0,-1)
    papers=[]
    for rawPaper in rawPapers:
      paper = self.getPaper(rawPaper)
      papers.append(paper) 
    return papers
    
    # Returns a list of paper objects
  def getTopAuthors(self, top_bound=100):
    rawAuthors = self.redisDB.zrange("Authors",0,top_bound)
    authors = []
    for a in rawAuthors:
      author = self.getAuthor(a);
      authors.append(author)
    return authors
    
    # Returns a list of author objects
  def getTopPapers(self, top_bound=100):
    rawPapers = self.redisDB.zrange("Papers", 0, top_bound)
    papers = []
    for p in rawPapers:
      paper = self.getPaper(p);
      papers.append(paper)
    return papers
  
    #updates the view count of a paper in every location that it is stored:
    # - the paper's own view count
    # - the paper's zscore in the list of all papers
    # - the paper's zscore in the list of papers in its published year
    # - the paper's publisher's zscore in the list of all publishers
    # - the paper's publisher's view count
    # - the paper's zscore in each of the paper's titleWords' lists
    # - the paper's authors' view counts
    # - the paper's authors' zscores in the list of all authors
    # - the paper's zscore in each of the paper's authors' authorwords' lists
    # - the paper's tags' view counts
    # - the paper's zscore in each of the paper's tags' lists
    # - the paper's tags' zscores in the list of all tags
  def incrementPaperViews(self, paperID):
    paper = self.getPaper(paperID)
    self.redisDB.incr("Paper:"+paperID+":ViewCount")
    self.redisDB.zincrby("Papers", paperID, 1)
    self.redisDB.zincrby("YearPublished:"+str(paper.datePublished.year), paperID, 1)
    self.redisDB.zincrby("Publishers", paper.publisherID, 1)
    self.redisDB.incr("Publisher:"+paper.publisherID+":ViewCount")
    titleWords = self.getSearchWords(paper.title)
    for titleWord in titleWords:
      self.redisDB.zincrby("PaperWord:"+titleWord, paperID, 1)
    for authorID in paper.authorIDs:
      self.redisDB.incr("Author:"+authorID+":ViewCount")
      self.redisDB.zincrby("Authors",authorID, 1)
      author = self.getAuthor(authorID)
      words = self.getSearchWords(author.name)
      for word in words:
        self.redisDB.zincrby("AuthorWord:"+word, authorID, 1)
    for tag in paper.tags:
      self.redisDB.incr("Tag:"+tag+":ViewCount")
      self.redisDB.zincrby("Tag:"+tag+":Papers", paperID, 1)
      self.redisDB.zincrby("Tags", tag, 1)
    return

    #Takes in integers paperID and tag corresponding to the tag and paper to link together
  def tagPaper(self, paperID, tag):
    paper = self.getPaper(paperID)
    self.redisDB.zadd("Tag:"+tag+":Papers", paper.viewCount, paperID)
    self.redisDB.incrby("Tag:"+tag+":ViewCount",paper.viewCount)
    self.redisDB.zincrby("Tags", tag,paper.viewCount)
    self.redisDB.sadd("Paper:"+paperID+":Tags", tag)
    
    # Takes in a list of strings with names of authors to search for
    #  If only one author is given, give a list with a single element
    # Returns a list of Author objects 
  def getAuthorsMatchingAuthorNames(self, namesToSearch): 
    authorIDs = self.getAuthorIDsMatchingAuthorNames(namesToSearch)
    authors = []
    for authorID in authorIDs:
      author = self.getAuthor(authorID)
      authors.append(author)
    return authors
	
  def getAuthorIDsMatchingAuthorNames(self, namesToSearch):
    words = []
    for name in namesToSearch:
      words += self.getSearchWords(name)
    authorWordKeys = []
    for word in words:
      authorWordKeys.append("AuthorWord:"+word)  
    authorIDs = self.getMergedSearchResults(authorWordKeys)
    return authorIDs
	
  def getPapersMatchingAuthorNames(self, namesToSearch):
    authorIDs = self.getAuthorIDsMatchingAuthorNames(namesToSearch)
    return self.getPapersMatchingAuthorIDs(authorIDs)

  def getPapersMatchingAuthorIDs(self, IDsToSearch):
    papers = []
    paperIDs = self.getPaperIDsMatchingAuthorIDs(IDsToSearch)
    for paperID in paperIDs:
      papers.append(self.getPaper(paperID))
    return papers

  def getPaperIDsMatchingAuthorIDs(self, IDsToSearch):
    paperIDs = set([])
    for authorID in IDsToSearch:
      author = self.getAuthor(authorID)
      for paperID in author.paperIDs:
        paperIDs.add(paperID)
    return paperIDs
    
    # Takes in a list of string tags
    # Returns a list of paper objects that match
  def getPapersMatchingTags(self, tags):
    tagKeys = []
    for tag in tags:
      tagKeys.append("Tag:"+tag+":Papers")
    paperIDs = self.getMergedSearchResults(tagKeys)
    papers = []
    for paperID in paperIDs:
      paper = self.getPaper(paperID)
      papers.append(paper)
    return papers
    
    # Takes in a string of the title of the paper
    # Returns a list of paper objects
  def getPapersMatchingTitle(self, title):
    titleWords = self.getSearchWords(title)
    titleKeys = []
    for titleWord in titleWords:
      titleKeys.append("PaperWord:"+titleWord)
    paperIDs = self.getMergedSearchResults(titleKeys)
    papers = []
    for paperID in paperIDs:
      paper = self.getPaper(paperID)
      papers.append(paper)
    return papers
	
  def getPapersAdvancedSearch(self, titles, tags, authorNamesToSearch):
    authorIDs = self.getAuthorIDsMatchingAuthorNames(authorNamesToSearch)
    return self.getPapersAdvancedAuthorIDSearch(titles, tags, authorIDs)
	
  def getPapersAdvancedSearchRealOnly(self, titles, tags, authorNamesToSearch):
    authorIDs = self.getAuthorIDsMatchingAuthorNames(authorNamesToSearch)
    papers = self.getPapersAdvancedAuthorIDSearch(titles, tags, authorIDs)
    papersToReturn = []
    for paper in papers:
      if paper.isUploaded:
        papersToReturn.append(paper)
    return papersToReturn
	
  def getPapersAdvancedSearchFakeOnly(self, titles, tags, authorNamesToSearch):
    authorIDs = self.getAuthorIDsMatchingAuthorNames(authorNamesToSearch)
    papers = self.getPapersAdvancedAuthorIDSearch(titles, tags, authorIDs)
    papersToReturn = []

    for paper in papers:
      if not paper.isUploaded:
        papersToReturn.append(paper)
    return papersToReturn
  
  def getPapersAdvancedAuthorIDSearch(self, titles, tags, authorIDs):
    searchKeys = []
    for title in titles:
      titleWords = self.getSearchWords(title)
      for titleWord in titleWords:
        searchKeys.append("PaperWord:"+titleWord)
    for tag in tags:
      searchKeys.append("Tag:"+tag+":Papers")
    paperIDs = self.getMergedSearchResults(searchKeys)
    #TODO consider having this append papers that only match by author in order of views, perhaps by using hashes.
    authorPaperIDs = self.getPaperIDsMatchingAuthorIDs(authorIDs)
    adjustedPaperIDs = []
    addedIDs = set([])
    for paperID in paperIDs:
      if paperID in authorPaperIDs:
        adjustedPaperIDs.append(paperID)
        addedIDs.add(paperID)
        authorPaperIDs.remove(paperID)
    for paperID in paperIDs:
      if paperID not in addedIDs:
        adjustedPaperIDs.append(paperID)
    for paperID in authorPaperIDs:
      adjustedPaperIDs.append(paperID)
    papers = []
    for paperID in adjustedPaperIDs:
      paper = self.getPaper(paperID)
      papers.append(paper)
    return papers
  
  def getPaperRecsForUserID(self, userID):
    user = self.getUserByID(userID)
    authorIDs = []
    for author in user.authors:
      authorIDs.append(author.id)
    return self.getPapersAdvancedAuthorIDSearch([],user.tags,authorIDs)
    
    #NOTE:  This is a helper function!!!  This should never be called outside of this class!!
    #Takes in a list of Redis Keys
    #Returns an ordered list of Ids for whichever resource was requested
  def getMergedSearchResults(self, keys, maxResultsCount = 30, keyRange = -1):
    occurences = {}
    for key in keys:
      rslts = self.redisDB.zrange(key, 0, keyRange)
      for rslt in rslts:
        if rslt in occurences:
          occurences[rslt] = (occurences[rslt][0]+1,occurences[rslt][1])
        else:
          occurences[rslt] = (1, self.redisDB.zscore(key, rslt))
    groupedOccurences = {}
    for item in occurences.items():
      occurenceCount = item[1][0]
      viewCount = item[1][1]
      itemID = item[0]
      if occurenceCount not in groupedOccurences:
        groupedOccurences[occurenceCount] = [(itemID,viewCount)]
      else:
        insertIndex = -1
        for i in range(0, len(groupedOccurences[occurenceCount]) ):
          if groupedOccurences[occurenceCount][i][1]>viewCount:
            insertIndex = i
            break
        if insertIndex >= 0:
          groupedOccurences[occurenceCount].insert(insertIndex,(itemID,viewCount))
        else:
          groupedOccurences[occurenceCount].append((itemID,viewCount))
    ids = []
    
    for key in sorted(groupedOccurences.iterkeys()):
      for tup in groupedOccurences[key]:
        ids.append(tup[0])
        if len(ids) >= maxResultsCount:
          ids.reverse()
          return ids
    ids.reverse()
    return ids
  
  def getSearchWords(self, string):
    rawWords = re.sub('[^0-9a-z]+', ' ', string.lower()).split()
    words = []
    wordSet = set([])
    for rawWord in rawWords:
      if len(rawWord)>1 and rawWord not in self.wordsToFilter:
        wordSet.add(rawWord)
    for word in wordSet:
      words.append(word)
    return words
	
  def putUser(self, Name, facebookID = None):
    id = self.redisDB.get("Users:IDCounter")
    self.redisDB.set("User:"+id+":UserName",Name)

    self.redisDB.zadd("Users", 0, id) #To be ranked by followers
    self.redisDB.set("User:"+id+":FollowerCount", 0)
    if not facebookID == None:
      self.assignUserFacebookID(id, facebookID)
    self.redisDB.incr("Users:IDCounter")
    return id

  def assignUserFacebookID(self, id, facebookID):
    self.redisDB.set("User:"+id+":FacebookID", facebookID)
    self.redisDB.set("FacebookID:"+facebookID+":id", id)	

  #Should return a new user object
  def getUserByID(self, id):
    userName = self.redisDB.get("User:"+id+":UserName")
    followerCount = self.redisDB.get("User:"+id+":FollowerCount")
    followingIDs = list(self.redisDB.smembers("User:"+id+":FollowingUserIDs"))
    if(followingIDs == None):
      followingIDs = []
    followingNames = []
    for followingID in followingIDs:
      followingNames.append(self.redisDB.get("User:"+followingID+":UserName"))
    paperIDs = self.redisDB.zrange("User:"+id+":FavoritePapers",0,-1)
    if(paperIDs == None):
       paperIDs = []
    papers = []
    for paperID in paperIDs:
      papers.append(self.getPaper(paperID))
    authorIDs = self.redisDB.zrange("User:"+id+":FavoriteAuthors",0,-1)
    if(authorIDs == None):
      authorIDs = []
    authors = []
    for authorID in authorIDs:
      authors.append(self.getAuthor(authorID))
    tags = self.redisDB.zrange("User:"+id+":FavoriteTags",0,-1)
    if(tags == None):
      tags = []
    facebookID = self.redisDB.get("User:"+id+":FacebookID")
    return User(id, userName, followingIDs, followingNames, papers, authors, tags, followerCount, facebookID)

  def facebookToRegularID(self, facebookID):
      return self.redisDB.get("FacebookID:"+facebookID+":id")

  #takes a user id and a paper id to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoritePaper(self, userID, paperID, favoriteLevel):
    if not self.getPaper(paperID) == None:
      if favoriteLevel < 0 or favoriteLevel > 10:
        #raise Exception("Favorite level must be between 0 and 10")
        return
      else:
        self.redisDB.zadd("User:"+userID+":FavoritePapers",favoriteLevel, paperID)

  #takes a user id and an author id to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoriteAuthor(self, userID, authorID, favoriteLevel):
    if not self.getAuthor(authorID) == None:
      if favoriteLevel < 0 or favoriteLevel > 10:
        #raise Exception("Favorite level must be between 0 and 10")
        return
      else:
        self.redisDB.zadd("User:"+userID+":FavoriteAuthors",favoriteLevel, authorID)

  #takes a user id and a Tag name to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoriteTag(self, userID, tag, favoriteLevel):
    if not self.getTag(tag) == None:
      if favoriteLevel < 0 or favoriteLevel > 10:
        #raise Exception("Favorite level must be between 0 and 10")
        return
      else:
        self.redisDB.zadd("User:"+userID+":FavoriteTags", favoriteLevel, tag)
	  
  #takes a user id and a paper id to search for in this users list of favorites
  #returns true if the paper is in the user's favorites list
  def hasFavoritePaper(self, userID, paperID):
    rslt = self.redisDB.zscore("User:"+userID+":FavoritePapers", paperID)
    if rslt == None:
      return False
    return True

  #takes a user id and an author id to search for in this users list of favorites
  #returns true if the author is in the user's favorites list
  def hasFavoriteAuthor(self, userID, authorID):
    rslt = self.redisDB.zscore("User:"+userID+":FavoriteAuthors", authorID)
    if rslt == None:
      return False
    return True

  #takes a user id and a Tag name to search for in this users list of favorites
  #returns true if the tag is in the user's favorites list
  def hasFavoriteTag(self, userID, tag):
    rslt = self.redisDB.zscore("User:"+userID+":FavoriteTags", tag)
    if rslt == None:
      return False
    return True
	
  #takes a user id and a paper id to delete from this users list of favorites
  def removeFavoritePaper(self, userID, paperID):
    self.redisDB.zrem("User:"+userID+":FavoritePapers", paperID)

  #takes a user id and an author id to delete from this users list of favorites
  def removeFavoriteAuthor(self, userID, authorID):
    self.redisDB.zrem("User:"+userID+":FavoriteAuthors", authorID)

  #takes a user id and a Tag name to delete from this users list of favorites
  def removeFavoriteTag(self, userID, tag):
    self.redisDB.zrem("User:"+userID+":FavoriteTags", tag)
	
  def addStalker(self, stalkerID, userIDToStalk):
    if stalkerID == userIDToStalk:
      return
    self.redisDB.sadd("User:"+stalkerID+":FollowingUserIDs", userIDToStalk)
    self.redisDB.zincrby("Users",userIDToStalk, 1)
    self.redisDB.incr("User:"+userIDToStalk+":FollowerCount")

  def removeStalker(self, stalkerID, userIDToUnstalk):
    self.redisDB.srem("User:"+stalkerID+":FollowingUserIDs", userIDToUnstalk)
    self.redisDB.zincrby("Users",userIDToUnstalk, -1)
    self.redisDB.decr("User:"+userIDToUnstalk+":FollowerCount")

  def isStalking(self, stalkerID, userIDToCheck):
    return self.redisDB.sismember("User:"+stalkerID+":FollowingUserIDs", userIDToCheck)

  def addReference(self, paperCitingID, paperCitedID):
    self.redisDB.sadd("Paper:"+paperCitingID+":References", paperCitedID)
    self.redisDB.sadd("Paper:"+paperCitedID+":CitedBys", paperCitingID)

  def setReferences(self, paperCitingID, papersCitedIDs):
    # TODO: this function should remove any existing references (if any) from paperCitingID (paperCitingID may not even exist as a key yet)
    # then call addReference(paperCitingID, paperCitedID) for all paperCitedID in papersCitedIDs
    pass
    
  def markPaperUploaded(self, paperToMarkID):
    #TODO double check.  This is probably broken.
    self.redisDB.set("Paper:"+paperToMarkID+":IsUploaded", True)
	
  def isPaperUploaded(self, paperToCheckID):
    return self.redisDB.get("Paper:"+paperToCheckID+":IsUploaded")




