'''
Created on Oct 11, 2015

@author: jenkinjk
Note, this is a class that is designed to be a working, tested database. It takes code from RedisDatabase, written by davidsac, as well as implementing its own functions.
'''

import re
import redis
from Author import Author
from Tag import Tag
from Paper import Paper

class RedisDatabaseImpl():
  
  def __init__(self, Test):
    if(Test == "Test"): #We can connect to a second database, which we can clean out without losing production data
      self.redisDB = redis.Redis(host='localhost', port=6379, db=1)
      self.redisDB.flushdb()
      self.redisDB.set("Tags:IDCounter",0)
      self.redisDB.set("Authors:IDCounter",0)
      self.redisDB.set("Papers:IDCounter",0)
      self.redisDB.set("Users:IDCounter",0)
    else:
      self.redisDB = redis.Redis(host='localhost', port=6379, db=0)

    
    #Takes in a string 
    #returns a list of paper objects where the title contains that string
  def search(self, searchTerm):
    result = []
    for paperID in self.redisDB.zrange("Papers",0,-1):
      paperStuff = self.redisDB.hvals("Paper:"+paperID)
      title = paperStuff[1]
      if(bool(searchTerm in title)):
        result.append(self.getPaper(paperID))
    return result

    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = '%s' % self.redisDB.get("Authors:IDCounter")
    self.redisDB.hmset("Author:"+id, {"Name":name,"ViewCount":0})
    self.redisDB.zadd("Authors",id,0) #Note that authors are ranked by view count, hence the 0
    self.redisDB.incr("Authors:IDCounter")
    return id

    #Takes in a string of the author's ID
    #Returns an author object
  def getAuthor(self, id):
    resultAuthor = self.redisDB.hvals("Author:"+id) #It returns [viewCount, name]
    name = resultAuthor[1]
    authorPapers = "Author:"+name+":Papers"
    return Author(id,name,resultAuthor[0],self.redisDB.zrange(authorPapers,0,-1))

    #Takes a string title and two string lists authors and tags
    #Returns a string, PaperID
  def putPaper(self, title, authors, tags):
    id = self.redisDB.get("Papers:IDCounter")
    self.redisDB.hmset("Paper:"+id, {"Title":title,"ViewCount":0})
    self.redisDB.zadd("Papers",id,0)
    for author in authors:
      self.redisDB.zadd("Author:"+author+":Papers", id,0)
      self.redisDB.sadd("Paper:"+id+":Authors", author)
      self.putAuthor(author)
    for tag in tags:
      self.redisDB.zadd("Tag:"+tag+":Papers", id, 0)
      self.redisDB.sadd("Paper:"+id+":Tags", tag)
      self.putTag(tag)
    self.redisDB.incr("Papers:IDCounter")
    return id

  def getPaper(self, id):
    resultPaper = self.redisDB.hvals("Paper:"+id) #It returns [viewCount, title]
    title = resultPaper[1]
    viewCount = resultPaper[0]
    authors = self.redisDB.smembers("Paper:"+id+":Authors")
    tags = self.redisDB.smembers("Paper:"+id+":Tags")
    return Paper(id, title, authors, tags, '','','','','','',viewCount,'')

   #Takes in a string of the tag's name
   #Returns a string tagID 
  def putTag(self, name):
    id = self.redisDB.get("Tags:IDCounter")
    self.redisDB.hmset("Tag:"+id, {"Name":name,"ViewCount":0})
    self.redisDB.zadd("Tags",id,0)
    self.redisDB.incr("Tags:IDCounter")
    return id

    #Takes a string id to a tag
    #Returns a tag object
  def getTag(self, id):
    resultTag = self.redisDB.hvals("Tag:"+id) #It returns [viewCount, name]
    name = resultTag[1]
    tagPapers = "Tag:"+name+":Papers"
    return Tag(id,name,resultTag[0],self.redisDB.zrange(tagPapers,0,-1))

#Users, username, List of favorite articles, list of favorite authors, list of interesting tags
  def createUser(self, username):
    id = self.redisDB.get("Users:IDCounter")
    self.redisDB.hmset("User:"+id, {"Username":username,"Followers":0})
    self.redisDB.zadd("Users",id,0) #To be ranked by followers
    self.redisDB.incr("Users:IDCounter")
    return id

  
