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
