'''
Created on Oct 1, 2015

@author: davidsac
'''

class Paper:

  #TODO made isUploaded a not optional parameter?
  def __init__(self, id, title, authorIDs, tags, abstract, publisherID, datePublished, datePosted, postedByUserID, references, viewCount, citedBys, publisherName, authorNames, isUploaded = True):
    self.id = id
    self.title = title
    self.authorIDs = authorIDs
    self.tags = tags
    self.abstract = abstract
    self.publisherID = publisherID
    self.datePublished = datePublished
    self.datePosted = datePosted
    self.postedByUserID = postedByUserID
    self.references = references
    self.citedBys = citedBys
    self.viewCount = viewCount
    self.publisherName = publisherName
    self.authorNames = authorNames
    self.thumbnail = None
    self.isUploaded = isUploaded
    
  def __str__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   authorNames:'+str(self.authorNames)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisherID:'+self.publisherID+'   publisherName:'+self.publisherName+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedByUserID:'+self.postedByUserID+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount+'      isUploaded:'+ str(self.isUploaded)
  
  def __repr__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisher:'+self.publisherID+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedByUserID:'+self.postedByUserID+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount+'      isUploaded:'+ str(self.isUploaded)


  def __eq__(self, other):
    if other == None:
      return False
    if not self.id ==  other.id:
      return False
    if not self.title == other.title:
      return False
    if not set(self.tags) ==  set(other.tags):
      return False
    if not self.abstract == other.abstract:
      return False
    if not self.publisherID == other.publisherID:
      return False
    if not self.datePublished == other.datePublished:
      return False
    if not self.postedByUserID == other.postedByUserID:
      return False
    if not self.references == other.references:
      return False
    if not self.viewCount == other.viewCount:
      return False
    if not self.citedBys == other.citedBys:
      return False
    if not self.publisherName == other.publisherName:
      return False
    if not len(self.authorIDs) == len(other.authorIDs):
      return False
    if not len(self.authorNames) == len(other.authorNames):
      return False
    if not len(self.authorNames) == len(self.authorIDs):
      return False     
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.authorIDs)):
      tuplesA.add((self.authorIDs[i], self.authorNames[i]))
      tuplesB.add((other.authorIDs[i], other.authorNames[i]))
    if not tuplesA == tuplesB:
      return False
    return True
    
  def eqDebug(self, other):
    if other == None:
      print "other is None"
      return False
    if not self.id ==  other.id:
      print "id ", self.id,"!=",other.id
      return False
    if not self.title == other.title:
      print "title ", self.title,"!=",other.title
      return False
    if not self.tags ==  other.tags:
      print "tags ", self.tags,"!=",other.tags
      return False
    if not self.abstract == other.abstract:
      print "abstract ", self.abstract,"!=",other.abstract
      return False
    if not self.publisherID == other.publisherID:
      print "publisherID ", self.publisherID,"!=",other.publisherID
      return False
    if not self.datePublished == other.datePublished:
      print "datePublished ", self.datePublished,"!=",other.datePublished
      return False
    if not self.postedByUserID == other.postedByUserID:
      print "postedByUserID ", self.postedByUserID,"!=",other.postedByUserID
      return False
    if not self.references == other.references:
      print "references ", self.references,"!=",other.references
      return False
    if not self.viewCount == other.viewCount:
      print "viewCount ", self.viewCount,"!=",other.viewCount
      return False
    if not self.citedBys == other.citedBys:
      print "citedBys ", self.citedBys,"!=",other.citedBys
      return False
    if not self.publisherName == other.publisherName:
      print "publisherName ", self.publisherName,"!=",other.publisherName
      return False
    if not len(self.authorIDs) == len(other.authorIDs):
      print "len(self.authorIDs) ", len(self.authorIDs),"!=",len(other.authorIDs)
      return False
    if not len(self.authorNames) == len(other.authorNames):
      print "len(self.authorNames) ", len(self.authorNames),"!=",len(other.authorNames)
      return False
    if not len(self.authorNames) == len(self.authorIDs):
      print "len of author names and ids inconsistent ", len(self.authorNames),"!=",len(self.authorIDs)
      return False     
    tuplesA = set([])
    tuplesB = set([])
    for i in range(0,len(self.authorIDs)):
      tuplesA.add((self.authorIDs[i], self.authorNames[i]))
      tuplesB.add((other.authorIDs[i], other.authorNames[i]))
    if not tuplesA == tuplesB:
      print "tuples don't match ", tuplesA,"!=",tuplesB
      return False
    return True

  def __hash__(self):
    return hash(self.id) ^ hash(self.title)
