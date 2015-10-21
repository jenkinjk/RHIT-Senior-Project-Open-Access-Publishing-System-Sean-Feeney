'''
Created on Oct 1, 2015

@author: davidsac
'''

class Paper:

  def __init__(self, id, title, authorIDs, authorNames, tags, abstract, publisher, datePublished, datePosted, postedBy, references, viewCount, citedBys):
    self.id = id
    self.title = title
    self.authorIDs = authorIDs
    self.authorNames = authorNames
    self.tags = tags
    self.abstract = abstract
    self.publisher = publisher
    self.datePublished = datePublished
    self.datePosted = datePosted
    self.postedBy = postedBy
    self.references = references
    self.citedBys = citedBys
    self.viewCount = viewCount
    
  def __str__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   authorNames:'+str(self.authorNames)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisher:'+self.publisher+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedBy:'+self.postedBy+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount
  
  def __repr__(self):
    return 'id:'+self.id+'    title:'+self.title+'   authorIDs:'+str(self.authorIDs)+'   authorNames:'+str(self.authorNames)+'   tags:'+str(self.tags)+'   abstract:'+self.abstract+'   publisher:'+self.publisher+'   datePublished:'+str(self.datePublished)+'   datePosted:'+str(self.datePosted)+'   postedBy:'+self.postedBy+'   references:'+str(self.references)+'   citedBys:'+str(self.citedBys)+'      viewCount:'+self.viewCount
        