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
    if other == None:
      return False
    if not self.id ==  other.id:
      return False
    if not self.name == other.name:
      return False
    if not self.viewCount == other.viewCount:
      return False

    if not len(self.paperIDs) == len(other.paperIDs):
      return False

    if not len(self.paperIDs) == len(self.paperTitles):
      return False
    if not len(other.paperIDs) == len(other.paperTitles):
      return False

    if not len(self.paperIDs) == len(self.paperAuthorNames):
      return False
    if not len(other.paperIDs) == len(other.paperAuthorNames):
      return False

    if not len(self.paperIDs) == len(self.paperDatesPublished):
      return False
    if not len(other.paperIDs) == len(other.paperDatesPublished):
      return False
    
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.paperIDs)):
      tuplesA.add(str([self.paperIDs[i], self.paperTitles[i], set(self.paperAuthorNames[i]), self.paperDatesPublished[i]]))
      tuplesB.add(str([other.paperIDs[i], other.paperTitles[i], set(other.paperAuthorNames[i]), other.paperDatesPublished[i]]))
    if not tuplesA == tuplesB:
      print "tuples don't match ", tuplesA,"!=",tuplesB
      return False
    return True

  def eqDebug(self, other):
    if other == None:
      print "other is None"
      return False
    if not self.id ==  other.id:
      print "id ", self.id,"!=",other.id
      return False
    if not self.name == other.name:
      print "name ", self.name,"!=",other.name
      return False
    if not self.viewCount == other.viewCount:
      print "viewCount ", self.viewCount,"!=",other.viewCount
      return False

    if not len(self.paperIDs) == len(other.paperIDs):
      print "len of self and other paperIDs inconsistent", len(self.paperIDs),"!=",len(other.paperIDs)
      return False

    if not len(self.paperIDs) == len(self.paperTitles):
      print "len of self paperIDs and paperTitles inconsistent", len(self.paperIDs),"!=",len(self.paperTitles)
      return False
    if not len(other.paperIDs) == len(other.paperTitles):
      print "len of other paperIDs and paperTitles inconsistent", len(other.paperIDs),"!=",len(other.paperTitles)
      return False

    if not len(self.paperIDs) == len(self.paperAuthorNames):
      print "len of self paperIDs and paperAuthorNames inconsistent", len(self.paperIDs),"!=",len(self.paperAuthorNames)
      return False
    if not len(other.paperIDs) == len(other.paperAuthorNames):
      print "len of other paperIDs and paperAuthorNames inconsistent", len(other.paperIDs),"!=",len(other.paperAuthorNames)
      return False

    if not len(self.paperIDs) == len(self.paperDatesPublished):
      print "len of self paperIDs and paperDatesPublished inconsistent", len(self.paperIDs),"!=",len(self.paperDatesPublished)
      return False
    if not len(other.paperIDs) == len(other.paperDatesPublished):
      print "len of other paperIDs and paperDatesPublished inconsistent", len(other.paperIDs),"!=",len(other.paperDatesPublished)
      return False
    
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.paperIDs)):
      tuplesA.add(str([self.paperIDs[i], self.paperTitles[i], set(self.paperAuthorNames[i]), self.paperDatesPublished[i]]))
      tuplesB.add(str([other.paperIDs[i], other.paperTitles[i], set(other.paperAuthorNames[i]), other.paperDatesPublished[i]]))
    if not tuplesA == tuplesB:
      print "tuples don't match ", tuplesA,"!=",tuplesB
      return False
    return True

  def __hash__(self):
    return hash(self.id) ^ hash(self.name)
