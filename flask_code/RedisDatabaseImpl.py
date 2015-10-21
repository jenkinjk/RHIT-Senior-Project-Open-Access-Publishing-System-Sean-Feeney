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
    id = str(id)
    self.redisDB.hmset("Author:"+id, {"Name":name, "ViewCount":0})
    self.redisDB.zadd("Authors",id,0)
    words = self.getSearchWords(name)
    for word in words:
      self.redisDB.zadd("AuthorWord:"+word,id,0)
    self.redisDB.incr("Authors:IDCounter")
    return id
    
    #Takes in a string of the tag's name
    #Returns a string tagID 
  def putTag(self, name):
    id = self.redisDB.get("Tags:IDCounter")
    id = str(id)
    self.redisDB.hmset("Tag:"+id,{"Name":name, "ViewCount":0})
    self.redisDB.zadd("Tags",id,0)
    self.redisDB.incr("Tags:IDCounter")
    return id
  
    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    id = self.redisDB.get("Publishers:IDCounter")
    id = str(id)
    self.redisDB.hmset("Publisher:"+id,{"Name":name,"ViewCount":0})
    self.redisDB.zadd("Publishers",id,0)
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
  def putPaper(self, title, authorIDs, authorNames, tags, abstract, userID, datePublished, publisherID, citedBys, references):
    datePosted = datetime.now()
    id = self.redisDB.get("Papers:IDCounter")
    id = str(id)
    self.redisDB.hmset("Paper:"+id,{"PublisherID":publisherID,"Abstract":abstract, "Title":title, "DatePublished":str(datePublished), "DatePosted":str(datePosted), "ViewCount":0})
    self.redisDB.zadd("Papers",id,0)
    for authorID in authorIDs:
      self.redisDB.sadd("Paper:"+id+":Authors", author)
      authorID = self.putAuthor(author)
      self.redisDB.sadd("Author:"+authorID+":Papers", id)
    for tag in tags:
      if self.getTag(tag) == None:
        self.putTag(tag)
      self.redisDB.sadd("Paper:"+id+":Tags", tag)
      tagID = self.putTag(tag)
      self.redisDB.zadd("Tag:"+tagID+":Papers",id,0)
    self.redisDB.zadd("YearPublished:"+str(datePublished.year),id,0)
    words = self.getSearchWords(title)
    for word in words:
      self.redisDB.zadd("PaperWord:"+word,id,0)
    self.redisDB.incr("Papers:IDCounter")
    return id

    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    author = self.redisDB.hvals("Author:"+authorID) #[viewCount, name]
    if(len(author)==0):
      return None;
    papers = list(self.redisDB.smembers("Author:"+authorID+":Papers"))
    return Author(authorID, author[1], author[0], papers)
  
    # Takes in an integer tagID
    # Returns a tag object
  def getTag(self, tagID):
    tag = self.redisDB.hvals("Tag:"+tagID) #[viewCount, name]
    if(len(tag)==0):
      return None;
    papers = self.redisDB.zrange("Tag:"+tagID+":Papers",0,-1)
    return Tag(tagID, tag[1], tag[0], papers)  
  
    # Takes in an integer publisherID
    # Returns a publisher object
  def getPublisher(self, publisherID):
    publisher = self.redisDB.hvals("Publisher:"+publisherID) #[viewCount, name]
    return Publisher(publisherID, publisher[1], publisher[0])

    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    authors = list(self.redisDB.smembers("Paper:"+paperID+":Authors"))
    tags = list(self.redisDB.smembers("Paper:"+paperID+":Tags"))
    paper = self.redisDB.hvals("Paper:"+paperID) #[viewCount, title, abstract, posted, published, publisher]
    datePosted = datetime.strptime(paper[3], "%Y-%m-%d %H:%M:%S.%f")
    datePublished = datetime.strptime(paper[4], "%Y-%m-%d %H:%M:%S") # NOTE: this format needs to be updated once we stop using a datetime object 
    postedBy = ""
    references = []
    citedBys = []
    return Paper(paperID, paper[1], authors, tags, paper[2], datePublished, datePosted, paper[3], postedBy, references, paper[0], citedBys)

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
    self.redisDB.zadd("Tag:"+tagID+":Papers", paperID, paper.viewCount)
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
    

  def getPapersMatchingAuthors(self, namesToSearch):
    papers = []
    paperIDs = set([])
    authors = self.getAuthorsMatchingAuthors(namesToSearch)
    for author in authors:
      for paper in author.papers:
        paperIDs.add(paper)
    for paperID in paperIDs:
      papers.append(self.getPaper(paperID))
    return papers

  # Takes in a list of integer tagNames
  # Returns a list of paper objects that match
  def getPapersMatchingTagNames(self, tagNames):
    allTags = self.getAllTags()
    tagIDs = []
    for tagName in tagNames:
      for tag in allTags:
        if tag.name == tagName:
          tagIDs.append(tagID)
    return self.getPapersMatchingTagIDs(tagIDs)

    # Takes in a list of integer tagIDs
    # Returns a list of paper objects that match
  def getPapersMatchingTagIDs(self, tagIDs):
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
    id = str(id)
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

