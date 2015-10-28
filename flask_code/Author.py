'''
Created on Oct 1, 2015

@author: davidsac
'''

class Author:

  def __init__(self, id, name, viewCount, paperIDs, paperTitles, paperAuthorNames, paperDatesPublished):
    self.id = id
    self.name = name
    self.viewCount = viewCount
    self.paperIDs = paperIDs
    self.paperTitles = paperTitles
    self.paperAuthorNames = paperAuthorNames
    self.paperDatesPublished = paperDatesPublished

  def __str__(self):
    return 'id:'+self.id+'    name:'+self.name+'   paperIDs:'+str(self.paperIDs)+'      viewCount:'+self.viewCount+'      paperTitles:'+str(self.paperTitles)+'      paperAuthorNames:'+str(self.paperAuthorNames)+'      paperDatesPublished:'+str(self.paperDatesPublished)

  def __repr__(self):
    return 'id:'+self.id+'    name:'+self.name+'   paperIDs:'+str(self.paperIDs)+'      viewCount:'+self.viewCount+'      paperTitles:'+str(self.paperTitles)+'      paperAuthorNames:'+str(self.paperAuthorNames)+'      paperDatesPublished:'+str(self.paperDatesPublished)

  def __eq__(self, other):
    if not self.id ==  other.id:
      return False
    if not self.name == other.name:
      return False
    if not self.viewCount == other.viewCount:
      return False
    if not self.paperIDs == other.paperIDs:
      return False
    if not self.paperTitles == other.paperTitles:
      return False
    if not self.paperAuthorNames == other.paperAuthorNames:
      return False
    if not self.paperDatesPublished == other.paperDatesPublished:
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
    if not self.paperIDs == other.paperIDs:
      print "paperIDs ", self.paperIDs,"!=",other.paperIDs
      return False
    if not self.paperTitles == other.paperTitles:
      print "paperTitles ", self.paperTitles,"!=",other.paperTitles
      return False
    if not self.paperAuthorNames == other.paperAuthorNames:
      print "paperAuthorNames ", self.paperAuthorNames,"!=",other.paperAuthorNames
      return False
    if not self.paperDatesPublished == other.paperDatesPublished:
      print "paperDatesPublished ", self.paperDatesPublished,"!=",other.paperDatesPublished
      return False
    return True

  def __hash__(self):
    return hash(self.id) ^ hash(self.name)
