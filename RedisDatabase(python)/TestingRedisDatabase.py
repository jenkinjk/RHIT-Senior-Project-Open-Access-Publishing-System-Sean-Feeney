'''
Created on Oct 7, 2015

@author: jenkinjk
'''

from RedisDatabaseImpl import RedisDatabaseImpl
import datetime
import unittest

class MyTests(unittest.TestCase):

  def test_PutAuthor(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author one"))

  def test_PutAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author one"))
    self.assertEqual('1', db.putAuthor("Author two"))
    self.assertEqual('2', db.putAuthor("Author three"))

if __name__ == '__main__': 
  unittest.main()
