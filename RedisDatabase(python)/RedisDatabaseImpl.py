'''
Created on Oct 11, 2015

@author: jenkinjk
Note, this is a class that is designed to be a working, tested database. It takes code from RedisDatabase, written by davidsac, as well as implementing its own functions.
'''

import redis
from Author import Author
from Tag import Tag
from Paper import Paper

class RedisDatabaseImpl():

  def __init__(self):
    self.redisDB = redis.Redis(host='localhost', port=6379, db=0)
    self.redisDB.set("Tags:IDCounter",0)
    self.redisDB.set("Authors:IDCounter",0)
    self.redisDB.set("Papers:IDCounter",0)

    #Takes in a string of the author's name
    #Returns a string authorID
  def putAuthor(self, name):
    id = self.redisDB.get("Authors:IDCounter")
    self.redisDB.set("Author:"+id+":Name:", name)
    self.redisDB.set("Author:"+id+":ViewCount:", 0)
    self.redisDB.zadd("Authors",id,0) #Note that authors are ranked by view count, hence the 0
    self.redisDB.incr("Authors:IDCounter")
    return id



  
