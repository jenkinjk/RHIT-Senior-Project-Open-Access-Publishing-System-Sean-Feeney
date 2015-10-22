'''
Created on Oct 1, 2015

@author: davidsac
'''

class Tag:

  def __init__(self, name, viewCount, papers):
    self.name = name
    self.viewCount = viewCount
    self.papers = papers

  def __str__(self):
    return 'name:'+self.name+'   papers:'+str(self.papers)+'      viewCount:'+self.viewCount

  def __repr__(self):
    return 'name:'+self.name+'   papers:'+str(self.papers)+'      viewCount:'+self.viewCount      