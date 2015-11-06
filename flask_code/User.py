'''
Created on Oct 14, 2015

@author: jenkinjk
'''

class User():

  def __init__(self, id, username, followingIDs, followingNames, papers, authors, tags, followerCount, facebookID = None):
    self.id = id
    self.username = username
    self.followingIDs = followingIDs
    self.followingNames = followingNames
    self.papers = papers
    self.authors = authors
    self.tags = tags
    self.followerCount = followerCount
    self.facebookID = facebookID
    #encrypted password

  def __str__(self):
    return 'id:'+self.id+'		username:'+self.username+'		facebookID:'+self.facebookID+'      followingIDs:'+self.followingIDs+'      followingNames:'+self.followingNames+'      papers:'+self.papers+'      tags:'+self.tags+'      authors:'+self.authors+'      followerCount:'+self.followerCount

  def __repr__(self):
    return 'id:'+self.id+'		username:'+self.username+'		facebookID:'+self.facebookID+'      followingIDs:'+self.followingIDs+'      followingNames:'+self.followingNames+'      papers:'+self.papers+'      tags:'+self.tags+'      authors:'+self.authors+'      followerCount:'+self.followerCount


  def __eq__(self, other):
    if other == None:
      return False
    if not self.id ==  other.id:
      return False
    if not self.username ==  other.username:
      return False
    if not len(self.followingNames) == len(self.followingIDs):
      return False
    if not len(other.followingNames) == len(other.followingIDs):
      return False 
    if not len(self.followingNames) == len(self.followingIDs):
      return False   
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.followingIDs)):
      tuplesA.add((self.followingIDs[i], self.followingNames[i]))
      tuplesB.add((other.followingIDs[i], other.followingNames[i]))
    if not tuplesA == tuplesB:
      return False
    if not set(self.papers) ==  set(other.papers):
      return False
    if not set(self.authors) ==  set(other.authors):
      return False
    if not set(self.tags) ==  set(other.tags):
      return False
    if not self.followerCount ==  other.followerCount:
      return False
    if not self.facebookID ==  other.facebookID:
      return False
    return True

  def eqDebug(self, other):
    if other == None:
      print "other is None"
      return False
    if not self.id ==  other.id:
      print "id ", self.id,"!=",other.id
      return False
    if not self.username ==  other.username:
      print "username ", self.username,"!=",other.username
      return False
    if not len(self.followingNames) == len(self.followingIDs):
      print "len of self following names and ids inconsistent ", len(self.followingNames),"!=",len(self.followingIDs)
      return False
    if not len(other.followingNames) == len(other.followingIDs):
      print "len of other following names and ids inconsistent ", len(other.followingNames),"!=",len(other.followingIDs)
      return False 
    if not len(self.followingNames) == len(self.followingIDs):
      print "len of self and other following names and ids inconsistent ", len(self.followingIDs),"!=",len(other.followingIDs)
      return False   
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.followingIDs)):
      tuplesA.add((self.followingIDs[i], self.followingNames[i]))
      tuplesB.add((other.followingIDs[i], other.followingNames[i]))
    if not tuplesA == tuplesB:
      print "tuples don't match ", tuplesA,"!=",tuplesB
      return False
    if not set(self.papers) ==  set(other.papers):
      print "papers ", set(self.papers),"!=",set(other.papers)
      return False
    if not set(self.authors) ==  set(other.authors):
      print "authors ", set(self.authors),"!=",set(other.authors)
      return False
    if not set(self.tags) ==  set(other.tags):
      print "tags ", set(self.tags),"!=",set(other.tags)
      return False
    if not self.followerCount ==  other.followerCount:
      print "followerCount ", self.followerCount,"!=",other.followerCount
      return False
    if not self.facebookID ==  other.facebookID:
      print "facebookID ", self.facebookID,"!=",other.facebookID
      return False
    return True

  def __hash__(self):
    return hash(self.username)
