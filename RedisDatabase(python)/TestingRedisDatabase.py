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

  def test_PutPaper(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one"]))

  def test_PutPaperAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one"]))

  def test_PutPaperTags(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one", "Tag two"]))

  def test_PutPaperTagsAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"]))

  def test_PutAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one"]))
    self.assertEqual('1', db.putPaper("Paper Two's Title", ["Author two"],["Tag one"]))
    self.assertEqual('2', db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one","Tag two"]))

  def test_PutTag(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("Tag one"))

  def test_PutTags(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("Tag one"))
    self.assertEqual('1', db.putTag("Tag two"))
    self.assertEqual('2', db.putTag("Tag three"))

  def test_GetTag(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("TagOne"))
    tag = db.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual([],tag.papers)

  def test_GetTags(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("Tag one"))
    self.assertEqual('1', db.putTag("Tag two"))
    self.assertEqual('2', db.putTag("TagThree"))
    tag = db.getTag('2')
    self.assertEqual("TagThree", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('2', tag.id)
    self.assertEqual([],tag.papers)

  def test_GetTagsPapers(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    tag = db.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual([0],tag.papers)

if __name__ == '__main__': 
  unittest.main()
