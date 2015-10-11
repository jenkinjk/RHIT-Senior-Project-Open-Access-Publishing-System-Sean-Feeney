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
    self.redisDB.set("Paper:"+id+":Authors:", authors)
    self.redisDB.set("Paper:"+id+":Tags:", tags)
    self.redisDB.set("Paper:"+id+":DatePublished:", str(datePublished))
    self.redisDB.set("Paper:"+id+":DatePosted:", str(datePosted))
    self.redisDB.set("Papers",id,0)
    for author in authors:
      self.redisDB.addpaper("Author:"+author+":Papers", id)
    for tag in tags:
      self.redisDB.addpaper("Tag:"+tag+":Papers", id, 0)
    self.redisDB.addpaper("YearPublished:"+id, id, 0)
    words = getTitleWords(title)
    for word in words:
      self.redisDB.addpaper("PaperWord:"+word,id,0)
    self.redisDB.incr("Papers:IDCounter")
    return id
    
    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = self.redisDB.get("Authors:IDCounter")
    self.redisDB.set("Author:"+id+":Name:", name)
    self.redisDB.set("Author:"+id+":ViewCount:", 0)
    self.redisDB.set("Authors",id,0) #Note that authors are ranked by view count, hence the 0.
    words = getAuthorWords(title) #title?
    for word in words:
      self.redisDB.addpaper("AuthorWord:"+word,id,0)
    self.redisDB.incr("Authors:IDCounter")
    return id
    
    #Takes in a string of the tag's name
    #Returns a string tagID 
  def putTag(self, name):
    id = self.redisDB.get("Tags:IDCounter")
    self.redisDB.set("Tag:"+id+":Name:", name)
    self.redisDB.set("Tag:"+id+":ViewCount:", 0)
    self.redisDB.set("Tags",id,0)
    self.redisDB.incr("Authors:IDCounter")
    return id
  
    #Takes in a string of the publisher's name
    #Returns a string publisherID
  def putPublisher(self, name):
    id = self.redisDB.get("Publishers:IDCounter")
    self.redisDB.set("Publisher:"+id+":Name:", name)
    self.redisDB.set("Publisher:"+id+":ViewCount:", 0)
    self.redisDB.set("Publishers",id,0)
    self.redisDB.incr("Publishers:IDCounter")
    return id  
  
    #updates the view count of a paper in every location that it is stored
  def incrementPaperViews(self, paperID):
    "update paper itself, year list, each tags list, publisher list, each author, authorword, title word, publisher, authors list,"
    self.redisDB.incr("Paper:"+paperID+":ViewCount")
    "Screw this, let's worry about implementing this later!"
    #self.redisDB.incr("YearPublished:")
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
      authors.push(author)
    return authors
    
    # Returns a list of all tag objects
  def getAllTags(self):
    rawTags = self.redisDB.get("Tags")
    tags = []
    for rawTag in rawTags:
      tag = getTag(rawTag.tagID)
      tags.push(tag)
    return tags
  
    # Returns a list of all publisher objects
  def getAllPublishers(self):
    rawPublishers = self.redisDB.get("Publishers")
    publishers = []
    for rawPublisher in rawPublishers:
      publisher = getPublisher(rawPublisher.publisherID)
      publishers.push(publisher)
    return publishers  
    
    # Takes in a list of integer tagIDs
    # Returns a list of paper objects that match
  def getPapersMatchingTags(self, tagIDs):
    tagKeys = []
    for tagID in tagIDs:
      tagKeys.push("Tag:"+tagID+":Papers")
    paperIDs = getMergedSearchResults(tagKeys)
    papers = []
    for paperID in paperIDs:
      paper = getPaper(paperID)
      papers.push(paper)
    return papers
    
    # Takes in a string of the title of the paper
    # Returns a list of paper objects
  def getPapersMatchingTitle(self, title):
    titleWords = getSearchWords(title)
    titleKeys = []
    for titleWord in titleWords:
      tagKeys.push("TitleWord:"+titleWord)
    paperIDs = getMergedSearchResults(titleKeys)
    papers = []
    for paperID in paperIDs:
      paper = getPaper(paperID)
      papers.push(paper)
    return papers
    
    # Takes in an integer authorID
    # Returns a list of paper objects
  def getPapersForAuthor(self, authorID):
    rawPapers = self.redisDB.get("Author:"+authorID+":Papers")
    papers=[]
    for rawPaper in rawPapers:
      paper = getPaper(rawPaper.paperID)
      papers.push(paper) 
    return papers
    
    # Takes in an integer year before the current year
    # returns a list of paper objects
  def getPapersPublishedInYear(self, year):
    rawPapers = self.redisDB.get("YearPublished:"+year)
    papers=[]
    for rawPaper in rawPapers:
      paper = getPaper(rawPaper.paperID)
      papers.push(paper) 
    return papers
    
    # Takes in an integer paperID
    # Returns a paper object
  def getPaper(self, paperID):
    authors = self.redisDB.get("Paper:"+paperID+":Authors")
    tags = self.redisDB.get("Paper:"+paperID+":Authors")
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
    rawAuthors = self.redisDB.lrange(0,100)
    authors = []
    for a in rawAuthors:
      author = getAuthor(a.authorID);
      authors.push(author)
    return authors
    
    # Returns a list of author objects
  def getTopPapers(self):
    rawPapers = self.redisDB.lrange(0,100)
    papers = []
    for p in rawPapers:
      paper = getPaper(p.paperID);
      papers.push(paper)
    return papers
    
    # Takes in an integer authorID
    # Returns an author object
  def getAuthor(self, authorID):
    papers = self.redisDB.get("Author:"+authorID+":Papers")
    name = self.redisDB.get("Author:"+authorID+":Name")
    viewCount = self.redisDB.get("Author:"+authorID+":ViewCount")
    return Author(authorID, name, viewCount, papers)
  
    # Takes in an integer tagID
    # Returns a tag object
  def getTag(self, tagID):
    papers = self.redisDB.get("Tag:"+tagID+":Papers")
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
      rslts = self.redisDB.get(key)
      for rslt in rslts:
        if rslt in occurences:
          occurences[rslt] = (occurences[rslt][0]+1,occurences[rslt][1)
        else:
          occurences[rslt] = (1, zscore)
    groupedOccurences = {}
    for item in occurences.items():
      if !item[1][0] in groupedOccurences:
        groupedOccurences[item[1][0]] = [(item[0],item[1][1])]
      else:
        viewCount = item[1][1]
        insertIndex = -1
        for i in range(0, len(groupedOccurences[item[1][0]]) ):
          if groupedOccurences[item[1][0]][i][1]<viewCount:
            insertIndex = i
            break
        if insertIndex >= 0:
          groupedOccurences[item[1][0]].insert(insertIndex,(item[0],item[1][1]))
        else:
          groupedOccurences[item[1][0]].append((item[0],item[1][1]))
    ids = []
    for ls in groupedOccurences.values():
      for tup in ls:
        ids.append(tup[0])        
    return ids
  
    #Takes in integers paperID and tagID corresponding to the tag and paper to link together
  def tagPaper(self, paperID, tagID):
    paper = getPaper(paperID)
    self.redisDB.addpaper("Tag:"+tagID+":Papers", paperID, paper.viewCount)
    self.redisDB.incr("Tag:"+tagID+":ViewCount",paper.viewCount)
    self.redisDB.zincr("Tags", tagID,paper.viewCount)
    self.redisDB.sadd("Paper:"+paperID+":Tags", tagID)
    
  def getSearchWords(self, authorName):
    rawWords = re.sub('[^0-9a-z]+', ' ', authorName.lower()).split()
    words = []
    for rawWord in rawWords:
      if len(rawWord)>1:
        words.append(rawWord)
    return words
 
  
      
        
