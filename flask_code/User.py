'''
Created on Oct 14, 2015

@author: jenkinjk
'''

class User():

  def __init__(self, username, followingIDs, followingNames, papers, authors, tags, followerCount):
    self.username = username
    self.followingIDs = followingIDs
    self.followingNames = followingNames
    self.papers = papers
    self.tags = tags
    self.authors = authors
    self.followerCount = followerCount
    #encrypted password
    #facebookID

  def __str__(self):
    return 'username:'+self.username+'      followingIDs:'+self.followingIDs+'      followingNames:'+self.followingNames+'      papers:'+self.papers+'      tags:'+self.tags+'      authors:'+self.authors+'      followerCount:'+self.followerCount

  def __repr__(self):
    return 'username:'+self.username+'      followingIDs:'+self.followingIDs+'      followingNames:'+self.followingNames+'      papers:'+self.papers+'      tags:'+self.tags+'      authors:'+self.authors+'      followerCount:'+self.followerCount


  def __eq__(self, other):
    if not self.username ==  other.username:
      return False
    if not self.followingIDs ==  other.followingIDs:
      return False
    if not self.followingNames ==  other.followingNames:
      return False
    if not self.papers ==  other.papers:
      return False
    if not self.authors ==  other.authors:
      return False
    if not self.tags ==  other.tags:
      return False
    if not self.followerCount ==  other.followerCount:
      return False
    return True

  def eqDebug(self, other):
    if not self.username ==  other.username:
      print "username ", self.username,"!=",other.username
      return False
    if not self.followingIDs ==  other.followingIDs:
      print "followingIDs ", self.followingIDs,"!=",other.followingIDs
      return False
    if not self.followingNames ==  other.followingNames:
      print "followingNames ", self.followingNames,"!=",other.followingNames
      return False
    if not self.papers ==  other.papers:
      print "papers ", self.papers,"!=",other.papers
      return False
    if not self.authors ==  other.authors:
      print "authors ", self.authors,"!=",other.authors
      return False
    if not self.tags ==  other.tags:
      print "tags ", self.tags,"!=",other.tags
      return False
    if not self.followerCount ==  other.followerCount:
      print "followerCount ", self.followerCount,"!=",other.followerCount
      return False
    return True

  def __hash__(self):
    return hash(self.username)
