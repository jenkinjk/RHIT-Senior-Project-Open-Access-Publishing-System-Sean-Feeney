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