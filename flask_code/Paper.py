'''
Created on Oct 1, 2015

@author: davidsac
'''

class Paper:

  def __init__(self, id, title, authorIDs, tags, abstract, publisherID, datePublished, datePosted, postedBy, references, viewCount, citedBys, publisherName, authorNames):
    self.id = id
    self.title = title
    self.authorIDs = authorIDs
    self.tags = tags
    self.abstract = abstract
    self.publisherID = publisherID
    self.datePublished = datePublished
    self.datePosted = datePosted
    self.postedBy = postedBy
    self.references = references
    self.citedBys = citedBys
    self.viewCount = viewCount
    self.publisherName = publisherName
    self.authorNames = authorNames
    
  def __str__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   authorNames:'+str(self.authorNames)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisherID:'+self.publisherID+'   publisherName:'+self.publisherName+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedBy:'+self.postedBy+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount
  
  def __repr__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisher:'+self.publisher+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedBy:'+self.postedBy+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount
        
