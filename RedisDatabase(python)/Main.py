'''
Created on Oct 1, 2015

@author: davidsac
'''

from ValidFakeDatabase import *
from InvalidFakeDatabase import *

if __name__ == '__main__':
  fakeDB = ValidFakeDatabase()
  print fakeDB.getAuthorsMatchingAuthors(["Foo","Bar"])    
  print fakeDB.getAllTags()
  print fakeDB.getPapersMatchingTags( [12345,6789,0,111])
  print fakeDB.getPapersMatchingTitle("This is a title")
  print fakeDB.getPapersForAuthor(5525)
  print fakeDB.getPapersPublishedInYear(1921)
  print fakeDB.getPaper( 6364)
  print fakeDB.getTopAuthors()
  print fakeDB.getTopPapers()
  print fakeDB.getAuthor(527)
  
  pass