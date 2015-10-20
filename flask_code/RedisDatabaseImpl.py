'''
Created on Oct 6, 2015

@author: davidsac
'''

import redis
import re
from datetime import datetime
from Author import Author
from Tag import Tag
from Paper import Paper
from Publisher import Publisher
from User import User

class RedisDatabase():

  def __init__(self, Test):
    if(Test == "Test"): #We can connect to a second database, which we can clean out without losing production data
      self.redisDB = redis.Redis(host='openscholar.csse.rose-hulman.edu', port=6379, db=1)
      self.redisDB.flushdb()
      self.redisDB.set("Tags:IDCounter",0)
      self.redisDB.set("Authors:IDCounter",0)
      self.redisDB.set("Papers:IDCounter",0)
      self.redisDB.set("Users:IDCounter",0)
    else:

      self.redisDB = redis.Redis(host='openscholar.csse.rose-hulman.edu', port=6379, db=0)
    self.wordsToFilter = set(["the","a","an","the","with","of","for","to","from","on","my","his","her","our","is", "your","in","that","have","has", "be", "it", "not","he","she","you","me","them","us","and","do","at","this","but","by","they","if","we","say", "or","will","one","can","like","no","when"])	
    
  def clearDatabase(self):
    self.redisDB.flushdb()
    self.redisDB.set("Tags:IDCounter",0)
    self.redisDB.set("Authors:IDCounter",0)
    self.redisDB.set("Papers:IDCounter",0)
    self.redisDB.set("Publishers:IDCounter",0)
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = self.redisDB.get("Authors:IDCounter")
    self.redisDB.set("Author:"+id+":Name", name)
    self.redisDB.set("Author:"+id+":ViewCount", 0)
    self.redisDB.zadd("Authors",0,id)
    words = self.getSearchWords(name)
    for word in words:
      self.redisDB.zadd("AuthorWord:"+word,0,id)
    self.redisDB.incr("Authors:IDCounter")
    return id
    
    #Takes in a string of the tag's name
    #Returns a string tagID 
  def putTag(self, name):
    id = self.redisDB.get("Tags:IDCounter")
    self.redisDB.set("Tag:"+id+":Name", name)
    self.redisDB.set("Tag:"+id+":ViewCount", 0)
    self.redisDB.zadd("Tags",0,id)
    self.redisDB.incr("Tags:IDCounter")
    return id
  
    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    id = self.redisDB.get("Publishers:IDCounter")
    self.redisDB.set("Publisher:"+id+":Name", name)
    self.redisDB.set("Publisher:"+id+":ViewCount", 0)
    self.redisDB.zadd("Publishers",0,id)
    self.redisDB.incr("Publishers:IDCounter")
    return id

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
    datePosted = datetime.now()
    id = self.redisDB.get("Papers:IDCounter")
    self.redisDB.set("Paper:"+id+":PublisherID", publisherID)
    self.redisDB.set("Paper:"+id+":Abstract", abstract)
    self.redisDB.set("Paper:"+id+":Title", title)
    self.redisDB.set("Paper:"+id+":ViewCount", 0)
    self.redisDB.set("Paper:"+id+":DatePublished", str(datePublished))
    self.redisDB.set("Paper:"+id+":DatePosted", str(datePosted))
    self.redisDB.zadd("Papers",0,id)
    for author in authors:
      self.redisDB.sadd("Paper:"+id+":Authors", author)
      authorID = self.putAuthor(author)
      self.redisDB.sadd("Author:"+authorID+":Papers", id)
    for tag in tags:
      self.redisDB.sadd("Paper:"+id+":Tags", tag)
      tagID = self.putTag(tag)
      self.redisDB.zadd("Tag:"+tagID+":Papers",id,0)
    self.redisDB.zadd("YearPublished:"+str(datePublished.year), 0, id)
    words = self.getSearchWords(title)
    for word in words:
      self.redisDB.zadd("PaperWord:"+word,0,id)
    self.redisDB.incr("Papers:IDCounter")
    return id

    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    name = self.redisDB.get("Author:"+authorID+":Name")
    if name == None:
      return None
    papers = list(self.redisDB.smembers("Author:"+authorID+":Papers"))
    viewCount = self.redisDB.get("Author:"+authorID+":ViewCount")
    return Author(authorID, name, viewCount, papers)
  
    # Takes in an integer tagID
    # Returns a tag object
  def getTag(self, tagID):
    papers = self.redisDB.zrange("Tag:"+tagID+":Papers",0,-1)
    name = self.redisDB.get("Tag:"+tagID+":Name")
    viewCount = self.redisDB.get("Tag:"+tagID+":ViewCount")
    return Tag(tagID, name, viewCount, papers)  
  
    # Takes in an integer publisherID
    # Returns a publisher object
  def getPublisher(self, publisherID):
    name = self.redisDB.get("Publisher:"+publisherID+":Name")
    viewCount = self.redisDB.get("Publisher:"+publisherID+":ViewCount")
    return Publisher(publisherID, name, viewCount)

    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    authors = list(self.redisDB.smembers("Paper:"+paperID+":Authors"))
    tags = list(self.redisDB.smembers("Paper:"+paperID+":Tags"))
    title = self.redisDB.get("Paper:"+paperID+":Title")
    abstract = self.redisDB.get("Paper:"+paperID+":Abstract")
    publisherID = self.redisDB.get("Paper:"+paperID+":PublisherID")
    viewCount = self.redisDB.get("Paper:"+paperID+":ViewCount")
    datePosted = datetime.strptime(self.redisDB.get("Paper:"+paperID+":DatePosted"), "%Y-%m-%d %H:%M:%S.%f")
    datePublished = datetime.strptime(self.redisDB.get("Paper:"+paperID+":DatePublished"), "%Y-%m-%d %H:%M:%S")
    postedBy = ""
    references = []
    citedBys = []
    return Paper(paperID, title, authors, tags, abstract, publisherID, datePublished, datePosted, postedBy, references, viewCount, citedBys)

    #THIS METHOD CAN EASILY BE IMPLEMENTED OUTSIDE OF THIS CLASS.  CONSIDER REMOVING TO REMOVE COMPLEXITY FROM CODEBASE
    # Takes in an integer authorID
    # Returns a list of paper objects
  def getPapersForAuthor(self, authorID):
    rawPapers = list(self.redisDB.smembers("Author:"+authorID+":Papers"))
    papers=[]
    for rawPaper in rawPapers:
      paper = self.getPaper(rawPaper.paperID)
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
  def getTopAuthors(self):
    rawAuthors = self.redisDB.zrange("Authors",0,100)
    authors = []
    for a in rawAuthors:
      author = self.getAuthor(a);
      authors.append(author)
    return authors
    
    # Returns a list of author objects
  def getTopPapers(self):
    rawPapers = self.redisDB.zrange("Papers", 0, 100)
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
    self.redisDB.zincrby("Publishers", paper.publisher, 1)
    self.redisDB.incr("Publisher:"+paper.publisher+":ViewCount")
    titleWords = self.getSearchWords(paper.title)
    for titleWord in titleWords:
      self.redisDB.zincrby("PaperWord:"+titleWord, paperID, 1)
    for authorID in paper.authors:
      self.redisDB.incr("Author:"+authorID+":ViewCount")
      self.redisDB.zincrby("Authors",authorID, 1)
      author = self.getAuthor(authorID)
      words = self.getSearchWords(author.name)
      for word in words:
        self.redisDB.zincrby("AuthorWord:"+word, authorID, 1)
    for tagID in paper.tags:
      self.redisDB.incr("Tag:"+tagID+":ViewCount")
      self.redisDB.zincrby("Tag:"+tagID+":Papers", paperID, 1)
      self.redisDB.zincrby("Tags", tagID, 1)
    return

    #Takes in integers paperID and tagID corresponding to the tag and paper to link together
  def tagPaper(self, paperID, tagID):
    paper = self.getPaper(paperID)
    self.redisDB.zadd("Tag:"+tagID+":Papers", paper.viewCount, paperID)
    self.redisDB.incrby("Tag:"+tagID+":ViewCount",paper.viewCount)
    self.redisDB.zincrby("Tags", tagID,paper.viewCount)
    self.redisDB.sadd("Paper:"+paperID+":Tags", tagID)
    
    # Takes in a list of strings with names of authors to search for
    #  If only one author is given, give a list with a single element
    # Returns a list of Author objects 
  def getAuthorsMatchingAuthors(self, namesToSearch):
    words = []
    for name in namesToSearch:
      words += self.getSearchWords(name)
    authorWordKeys = []
    for word in words:
      authorWordKeys.append("AuthorWord:"+word)  
    authorIDs = self.getMergedSearchResults(authorWordKeys)
    authors = []
    for authorID in authorIDs:
      author = self.getAuthor(authorID)
      authors.append(author)
    return authors
    
    # Takes in a list of integer tagIDs
    # Returns a list of paper objects that match
  def getPapersMatchingTags(self, tagIDs):
    tagKeys = []
    for tagID in tagIDs:
      tagKeys.append("Tag:"+tagID+":Papers")
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
    
    #NOTE:  This is a helper function!!!  This should never be called outside of this class!!
    #Takes in a list of Redis Keys
    #Returns an ordered list of Ids for whichever resource was requested
  def getMergedSearchResults(self, keys):
    occurences = {}
    for key in keys:
      rslts = self.redisDB.zrange(key, 0, -1)
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
    ids.reverse()
    print ids
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

  #Users, username, List of favorite articles, list of favorite authors, list of interesting tags
  def putUser(self, username):
    id = self.redisDB.get("Users:IDCounter")
    self.redisDB.hmset("User:"+id, {"Username":username,"Followers":0})
    self.redisDB.zadd("Users",id,0) #To be ranked by followers
    self.redisDB.incr("Users:IDCounter")
    return id

  #Should return a new user object
  def getUser(self, id):
    resultUser = self.redisDB.hvals("User:"+id)
    username = resultUser[0]
    followers = resultUser[1]
    papers = self.redisDB.zrange("User:"+id+":FavoritePapers",0,-1)
    authors = self.redisDB.zrange("User:"+id+":FavoriteAuthors",0,-1)
    tags = self.redisDB.zrange("User:"+id+":FavoriteTags",0,-1)
    return User(username, followers,papers,authors,tags)

  #takes a user id and a paper id to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoritePaper(self, userID, paperID, favoriteLevel):
    self.redisDB.zadd("User:"+userID+":FavoritePapers",paperID,favoriteLevel)
    length = self.redisDB.zrange("User:"+userID+":FavoritePapers",0,-1)
    return len(length)


  #takes a user id and an author id to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoriteAuthor(self, userID, authorID, favoriteLevel):
    self.redisDB.zadd("User:"+userID+":FavoriteAuthors",authorID,favoriteLevel)
    length = self.redisDB.zrange("User:"+userID+":FavoriteAuthors",0,-1)
    return len(length)


  #takes a user id and a Tag id to add to this users list of favorites
  #returns the current length of the favorites
  def putFavoriteTag(self, userID, tagID, favoriteLevel):
    self.redisDB.zadd("User:"+userID+":FavoriteTags",tagID,favoriteLevel)
    length = self.redisDB.zrange("User:"+userID+":FavoriteTags",0,-1)
    return len(length)

