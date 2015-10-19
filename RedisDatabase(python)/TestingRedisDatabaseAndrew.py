'''
Created on Oct 7, 2015

@author: jenkinjk
'''
from RedisDatabase import RedisDatabase
from Paper import Paper
import unittest
import datetime

class RedisIntegrationTestCase(unittest.TestCase):

  #1
  def test_PutAuthor(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putAuthor("Author one"))

  #2
  def test_PutAuthors(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putAuthor("Author one"))
    self.assertEqual('1', self.db.putAuthor("Author two"))
    self.assertEqual('2', self.db.putAuthor("Author three"))

  #3
  def test_PutPaper(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #4
  def test_PutPaperAuthors(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #5
  def test_PutPaperTags(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #6
  def test_PutPaperTagsAuthors(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #7
  def test_GetPaper(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    paper = self.db.getPaper('0')
    self.assertEqual(["Author one", "Author two"], paper.authors)
    self.assertEqual('0', paper.viewCount)
    self.assertEqual('0', paper.id)
    self.assertEqual("Paper One's Title", paper.title)
    self.assertTrue("Tag two" in paper.tags)
    self.assertTrue("Tag one" in paper.tags)

  #8
  def test_PutPapersAuthors(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author two"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one","Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #9
  def test_GetAuthor(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putAuthor("Author One"))
    author = self.db.getAuthor('0')
    self.assertEqual("Author One", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual([],author.papers)

  #10
  def test_GetAuthors(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putAuthor("Author One"))
    self.assertEqual('1', self.db.putAuthor("Author Two"))
    self.assertEqual('2', self.db.putAuthor("Author Three"))
    author = self.db.getAuthor('2')
    self.assertEqual("Author Three", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('2', author.id)
    self.assertEqual([],author.papers)

  #THIS TEST SHOULDN'T PASS, SHOULD IT?
  #11
  def test_GetAuthorsPapers(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    author = self.db.getAuthor('0')
    self.assertEqual("Author one", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual(['0'],author.papers)

  #12
  def test_PutTag(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putTag("Tag one"))

  #13
  def test_PutTags(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putTag("Tag one"))
    self.assertEqual('1', self.db.putTag("Tag two"))
    self.assertEqual('2', self.db.putTag("Tag three"))

  #14
  def test_GetTag(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putTag("239ck39&%$#@*&"))
    tag = self.db.getTag('0')
    self.assertEqual("239ck39&%$#@*&", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual([],tag.papers)

  #15
  def test_GetTags(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putTag("Tag one"))
    self.assertEqual('1', self.db.putTag("Tag two"))
    self.assertEqual('2', self.db.putTag("TagThree"))
    tag = self.db.getTag('2')
    self.assertEqual("TagThree", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('2', tag.id)
    self.assertEqual([],tag.papers)

  #16
  def test_putUser(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual('1', self.db.putUser("User Two"))

  #17
  def test_getUser(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual('0', result.followers)
    self.assertEqual([], result.papers)
    self.assertEqual([],result.authors)
    self.assertEqual([],result.tags)

  #18
  def test_putFavoritePaper(self):
    self.db = RedisDatabase("Test")
    self.assertEqual(1, self.db.putFavoritePaper('0','0','6'))
    self.assertEqual(2, self.db.putFavoritePaper('0','1','0'))
    self.assertEqual(2, self.db.putFavoritePaper('0','0','3'))
    self.assertEqual(1, self.db.putFavoritePaper('1','0','7'))

  #19
  def test_putFavoriteAuthor(self):
    self.db = RedisDatabase("Test")
    self.assertEqual(1, self.db.putFavoriteAuthor('0','0','6'))
    self.assertEqual(2, self.db.putFavoriteAuthor('0','1','0'))
    self.assertEqual(2, self.db.putFavoriteAuthor('0','0','3'))
    self.assertEqual(1, self.db.putFavoriteAuthor('1','0','7'))

  #20
  def test_putFavoriteTag(self):
    self.db = RedisDatabase("Test")
    self.assertEqual(1, self.db.putFavoriteTag('0','0','6'))
    self.assertEqual(2, self.db.putFavoriteTag('0','1','0'))
    self.assertEqual(2, self.db.putFavoriteTag('0','0','3'))
    self.assertEqual(1, self.db.putFavoriteTag('1','0','7'))

  #21
  def test_getUserPaper(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual(1, self.db.putFavoritePaper('0','0','6'))
    self.assertEqual(2, self.db.putFavoritePaper('0','1','8'))
    self.assertEqual(3, self.db.putFavoritePaper('0','2','4'))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual('0', result.followers)
    self.assertEqual(['2','0','1'], result.papers)
    self.assertEqual([],result.authors)
    self.assertEqual([],result.tags)
    

  #22
  def test_getUserAuthor(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual(1, self.db.putFavoriteAuthor('0','0','6'))
    self.assertEqual(2, self.db.putFavoriteAuthor('0','1','8'))
    self.assertEqual(3, self.db.putFavoriteAuthor('0','2','4'))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual('0', result.followers)
    self.assertEqual(['2','0','1'], result.authors)
    self.assertEqual([],result.papers)
    self.assertEqual([],result.tags)

  #23
  def test_getUserTag(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual(1, self.db.putFavoriteTag('0','0','6'))
    self.assertEqual(2, self.db.putFavoriteTag('0','1','8'))
    self.assertEqual(3, self.db.putFavoriteTag('0','2','4'))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual('0', result.followers)
    self.assertEqual(['2','0','1'], result.tags)
    self.assertEqual([],result.authors)
    self.assertEqual([],result.papers)

  #24
  def test_getUserAll(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual(1, self.db.putFavoritePaper('0','0','6'))
    self.assertEqual(1, self.db.putFavoriteTag('0','1','8'))
    self.assertEqual(2, self.db.putFavoritePaper('0','1','8'))
    self.assertEqual(1, self.db.putFavoriteAuthor('0','1','8'))
    self.assertEqual(2, self.db.putFavoriteTag('0','0','6'))
    self.assertEqual(3, self.db.putFavoriteTag('0','2','4'))
    self.assertEqual(2, self.db.putFavoriteAuthor('0','0','6'))
    self.assertEqual(3, self.db.putFavoriteAuthor('0','2','4'))
    self.assertEqual(3, self.db.putFavoritePaper('0','2','4'))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual('0', result.followers)
    self.assertEqual(['2','0','1'], result.papers)
    self.assertEqual(['2','0','1'],result.authors)
    self.assertEqual(['2','0','1'],result.tags)


  #25
  def test_GetTagsPapers(self):
    self.db = RedisDatabase("Test")
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    tag = self.db.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual(['0'],tag.papers)

if __name__ == '__main__': 
  unittest.main()
