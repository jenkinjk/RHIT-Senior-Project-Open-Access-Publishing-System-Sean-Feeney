'''
Created on Oct 1, 2015

@author: davidsac
'''

class Tag:

  def __init__(self, name, viewCount, paperIDs):
    self.name = name
    self.viewCount = viewCount
    self.paperIDs = paperIDs

  def __str__(self):
    return 'name:'+self.name+'   paperIDs:'+str(self.paperIDs)+'      viewCount:'+self.viewCount

  def __repr__(self):
    return 'name:'+self.name+'   paperIDs:'+str(self.paperIDs)+'      viewCount:'+self.viewCount

  def __eq__(self, other):
    if other == None:
      return False
    if not self.name == other.name:
      return False
    if not self.viewCount == other.viewCount:
      return False
    if not self.paperIDs == other.paperIDs:
      return False
    return True

  def eqDebug(self, other):
    if not self.name ==  other.name:
      print "name ", self.name,"!=",other.name
      return False
    if not self.viewCount == other.viewCount:
      print "viewCount ", self.viewCount,"!=",other.viewCount
      return False
    if not self.paperIDs == other.paperIDs:
      print "paperIDs ", self.paperIDs,"!=",other.paperIDs
      return False
    return True

  def __hash__(self):
    return hash(self.name) ^ hash(self.viewCount)      
