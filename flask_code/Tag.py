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