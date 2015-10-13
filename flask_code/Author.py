'''
Created on Oct 1, 2015

@author: davidsac
'''

class Author:

  def __init__(self, id, name, viewCount, papers):
    self.id = id
    self.name = name
    self.viewCount = viewCount
    self.papers = papers

  def __str__(self):
    return 'id:'+self.id+'    name:'+self.name+'   papers:'+str(self.papers)+'      viewCount:'+self.viewCount

  def __repr__(self):
    return 'id:'+self.id+'    name:'+self.name+'   papers:'+str(self.papers)+'      viewCount:'+self.viewCount
        