'''
Created on Oct 6, 2015

@author: davidsac
'''

import redis
from datetime import datetime
from Author import Author
from Tag import Tag
from Paper import Paper
from Publisher import Publisher

class RedisDatabase():

  def __init__(self):
    self.redisDB = redis.StrictRedis(host='localhost', port=6379, db=0)
    self.redisDB.set("Tags:IDCounter",0)
    self.redisDB.set("Authors:IDCounter",0)
    self.redisDB.set("Papers:IDCounter",0)
    self.redisDB.set("Publishers:IDCounter",0)
    self.wordsToFilter = set(["the","a","an","the","with","of","for","to","from","on","my","his","her","our","is", "your","in","that","have","has", "be", "it", "not","he","she","you","me","them","us","and","do","at","this","but","by","they","if","we","say", "or","will","one","can","like","no","when"])	
    
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
    datePosted = datetime.datetime.now()
    id = self.redisDB.get("Papers:IDCounter")
    self.redisDB.set("Paper:"+id+":Publisher:", publisherID)
    self.redisDB.set("Paper:"+id+":Abstract:", abstract)
    self.redisDB.set("Paper:"+id+":Title:", title)
    self.redisDB.set("Paper:"+id+":DatePublished:", str(datePublished))
    self.redisDB.set("Paper:"+id+":DatePosted:", str(datePosted))
    self.redisDB.zadd("Papers",id,0)
    for author in authors:
      self.redisDB.addpaper("Author:"+author+":Papers", id)
	  self.redisDB.sadd("Paper:"+id+":Authors:", author)
    for tag in tags:
      self.redisDB.zadd("Tag:"+tag+":Papers", id, 0)
	  self.redisDB.sadd("Paper:"+id+":Tags:", tag)
    self.redisDB.zadd("YearPublished:"+id, id, 0)
    words = getTitleWords(title)
    for word in words:
      self.redisDB.zadd("PaperWord:"+word,id,0)
    self.redisDB.incr("Papers:IDCounter")
    return id
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = self.redisDB.get("Authors:IDCounter")
    self.redisDB.set("Author:"+id+":Name:", name)
    self.redisDB.set("Author:"+id+":ViewCount:", 0)
    self.redisDB.zadd("Authors",id,0)
    words = getAuthorWords(title)
    for word in words:
      self.redisDB.zadd("AuthorWord:"+word,id,0)
    self.redisDB.incr("Authors:IDCounter")
    return id
    
    #Takes in a string of the tag's name
    #Returns a string tagID 
  def putTag(self, name):
    id = self.redisDB.get("Tags:IDCounter")
    self.redisDB.set("Tag:"+id+":Name:", name)
    self.redisDB.set("Tag:"+id+":ViewCount:", 0)
    self.redisDB.zadd("Tags",id,0)
    self.redisDB.incr("Authors:IDCounter")
    return id
  
    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    id = self.redisDB.get("Publishers:IDCounter")
    self.redisDB.set("Publisher:"+id+":Name:", name)
    self.redisDB.set("Publisher:"+id+":ViewCount:", 0)
    self.redisDB.zadd("Publishers",id,0)
    self.redisDB.incr("Publishers:IDCounter")
    return id  
  
    #updates the view count of a paper in every location that it is stored
  def incrementPaperViews(self, paperID):
    #update paper itself, year list, each tags list, publisher list, each author, authorword, title word, publisher, authors list
	paper = getPaper(paperID)
    self.redisDB.incr("Paper:"+paperID+":ViewCount")
	self.redisDB.zincrby("Papers", paperID, 1)
    self.redisDB.zincrby("YearPublished:"+paper.datePublished.year, paperID, 1)
	self.redisDB.zincrby("Publishers", paper.publisherID, 1)
	self.redisDB.incr("Publisher:"+paper.publisherID+":ViewCount")
	titleWords = getSearchWords(paper.title)
	for titleWord in titleWords:
	  self.redisDB.zincrby("PaperWord:"+titleWord, paperID, 1)
	for authorID in paper.authors:
	  self.redisDB.incr("Author:"+authorID+":ViewCount")
	  self.redisDB.zincrby("Authors",authorID, 1)
	  author = getAuthor(authorID)
	  words = getSearchWords(author.name)
	  for word in words:
	    self.redisDB.zincrby("AuthorWord:"+word, authorID, 1)
	for tagID in paper.tagIDs:
	  self.redisDB.incr("Tag:"+tagID+":ViewCount")
	  self.redisDB.zincrby("Tag:"+tagID+":Papers", paperID, 1)
	  self.redisDB.zincrby("Tags", tagID, 1)
    return
    
    # Takes in a list of strings with names of authors to search for
    #  If only one author is given, give a list with a single element
    # Returns a list of Author objects 
  def getAuthorsMatchingAuthors(self, namesToSearch):
    words = []
    for name in namesToSearch:
      words.append(getSearchWords(name))
    authorWordKeys = []
    for word in words:
      authorWordKeys.append("AuthorWord:"+word)  
    authorIDs = getMergedSearchResults(authorWordKeys)
    authors = []
    for authorID in authorIDs:
      author = getAuthor(authorID)
      authors.append(author)
    return authors
    
    # Returns a list of all tag objects
  def getAllTags(self):
    rawTags = self.redisDB.zrange("Tags",0,-1)
    tags = []
    for rawTag in rawTags:
      tag = getTag(rawTag)
      tags.append(tag)
    return tags
  
    # Returns a list of all publisher objects
  def getAllPublishers(self):
    rawPublishers = self.redisDB.zrange("Publishers",0,-1)
    publishers = []
    for rawPublisher in rawPublishers:
      publisher = getPublisher(rawPublisher)
      publishers.append(publisher)
    return publishers  
    
    # Takes in a list of integer tagIDs
    # Returns a list of paper objects that match
  def getPapersMatchingTags(self, tagIDs):
    tagKeys = []
    for tagID in tagIDs:
      tagKeys.append("Tag:"+tagID+":Papers")
    paperIDs = getMergedSearchResults(tagKeys)
    papers = []
    for paperID in paperIDs:
      paper = getPaper(paperID)
      papers.append(paper)
    return papers
    
    # Takes in a string of the title of the paper
    # Returns a list of paper objects
  def getPapersMatchingTitle(self, title):
    titleWords = getSearchWords(title)
    titleKeys = []
    for titleWord in titleWords:
      tagKeys.append("TitleWord:"+titleWord)
    paperIDs = getMergedSearchResults(titleKeys)
    papers = []
    for paperID in paperIDs:
      paper = getPaper(paperID)
      papers.append(paper)
    return papers
    
    # Takes in an integer authorID
    # Returns a list of paper objects
  def getPapersForAuthor(self, authorID):
    rawPapers = self.redisDB.smembers("Author:"+authorID+":Papers")
    papers=[]
    for rawPaper in rawPapers:
      paper = getPaper(rawPaper.paperID)
      papers.append(paper) 
    return papers
    
    # Takes in an integer year before the current year
    # returns a list of paper objects
  def getPapersPublishedInYear(self, year):
    rawPapers = self.redisDB.zrange("YearPublished:"+year,0,-1)
    papers=[]
    for rawPaper in rawPapers:
      paper = getPaper(rawPaper)
      papers.append(paper) 
    return papers
    
    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    authors = self.redisDB.smembers("Paper:"+paperID+":Authors")
    tags = self.redisDB.smembers("Paper:"+paperID+":Tags")
    title = self.redisDB.get("Paper:"+paperID+":Title")
    abstract = self.redisDB.get("Paper:"+paperID+":Abstract")
    publisher = self.redisDB.get("Paper:"+paperID+":PublisherID")
    viewCount = self.redisDB.get("Paper:"+paperID+":ViewCount")
    datePosted = datetime.datetime.fromtimestamp(self.redisDB.get("Paper:"+paperID+":DatePosted"))
    datePublished = datetime.datetime.fromtimestamp(self.redisDB.get("Paper:"+paperID+":DatePublished"))
    postedBy = ""
    references = []
    citedBys = []
    return Paper(paperID, title, authors, tags, abstract, publisher, datePublished, datePosted, postedBy, references, viewCount, citedBys)      
    
    # Returns a list of paper objects
  def getTopAuthors(self):
    rawAuthors = self.redisDB.zrange("Authors",0,100)
    authors = []
    for a in rawAuthors:
      author = getAuthor(a);
      authors.append(author)
    return authors
    
    # Returns a list of author objects
  def getTopPapers(self):
    rawPapers = self.redisDB.zrange("Papers", 0, 100)
    papers = []
    for p in rawPapers:
      paper = getPaper(p);
      papers.append(paper)
    return papers
    
    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    papers = self.redisDB.smembers("Author:"+authorID+":Papers")
    name = self.redisDB.get("Author:"+authorID+":Name")
    viewCount = self.redisDB.get("Author:"+authorID+":ViewCount")
    return Author(authorID, name, viewCount, papers)
  
    # Takes in an integer tagID
    # Returns a tag object
  def getTag(self, tagID):
    papers = self.redisDB.smembers("Tag:"+tagID+":Papers")
    name = self.redisDB.get("Tag:"+tagID+":Name")
    viewCount = self.redisDB.get("Tag:"+tagID+":ViewCount")
    return Tag(tagID, name, viewCount, papers)  
  
    # Takes in an integer publisherID
    # Returns a publisher object
  def getPublisher(self, publisherID):
    name = self.redisDB.get("Publisher:"+publisherID+":Name")
    viewCount = self.redisDB.get("Publisher:"+publisherID+":ViewCount")
    return Publisher(publisherID, name, viewCount)
  
  def clearDatabase(self):
    self.redisDB.flushDB()
    
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
          occurences[rslt] = (1, zscore)
    groupedOccurences = {}
    for item in occurences.items():
	  occurenceCount = item[1][0]
	  viewCount = item[1][1]
	  itemID = item[0]
      if !occurenceCount in groupedOccurences:
        groupedOccurences[occurenceCount] = [(itemID,viewCount)]
      else:
        insertIndex = -1
        for i in range(0, len(groupedOccurences[occurenceCount]) ):
          if groupedOccurences[occurenceCount][i][1]<viewCount:
            insertIndex = i
            break
        if insertIndex >= 0:
          groupedOccurences[occurenceCount].insert(insertIndex,(itemID,viewCount))
        else:
          groupedOccurences[occurenceCount].append((itemID,viewCount))
    ids = []
    for ls in groupedOccurences.values():
      for tup in ls:
        ids.append(tup[0])      
    return ids
  
    #Takes in integers paperID and tagID corresponding to the tag and paper to link together
  def tagPaper(self, paperID, tagID):
    paper = getPaper(paperID)
    self.redisDB.zadd("Tag:"+tagID+":Papers", paperID, paper.viewCount)
    self.redisDB.incrby("Tag:"+tagID+":ViewCount",paper.viewCount)
    self.redisDB.zincrby("Tags", tagID,paper.viewCount)
    self.redisDB.sadd("Paper:"+paperID+":Tags", tagID)
    
  def getSearchWords(self, authorName):
    rawWords = re.sub('[^0-9a-z]+', ' ', authorName.lower()).split()
    words = []
	wordSet = set([])
    for rawWord in rawWords:
      if len(rawWord)>1 and rawWord not in self.wordsToFilter:
        wordSet.add(rawWord)
	for word in wordSet:
	  words.append(word)
    return words