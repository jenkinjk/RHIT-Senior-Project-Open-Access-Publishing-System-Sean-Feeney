'''
Created on Oct 6, 2015

@author: davidsac
'''

class Publisher():

  def __init__(self, id, name, viewCount):
    self.id = id
    self.name = name
    self.viewCount = viewCount

  def __str__(self):
    return 'id:'+self.id+'    name:'+self.name+'      viewCount:'+self.viewCount

  def __repr__(self):
    return 'id:'+self.id+'    name:'+self.name+'      viewCount:'+self.viewCount

  def __eq__(self, other):
    if not self.id ==  other.id:
      return False
    if not self.name == other.name:
      return False
    if not self.viewCount == other.viewCount:
      return False
    return True

  def eqDebug(self, other):
    if not self.id ==  other.id:
      print "id ", self.id,"!=",other.id
      return False
    if not self.name == other.name:
      print "name ", self.name,"!=",other.name
      return False
    if not self.viewCount == other.viewCount:
      print "viewCount ", self.viewCount,"!=",other.viewCount
      return False
    return True

  def __hash__(self):
    return hash(self.id) ^ hash(self.name)
