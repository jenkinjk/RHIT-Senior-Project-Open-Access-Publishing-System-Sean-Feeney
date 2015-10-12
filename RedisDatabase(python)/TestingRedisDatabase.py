'''
Created on Oct 7, 2015

@author: jenkinjk
'''
from RedisDatabaseImpl import RedisDatabaseImpl
from Paper import Paper
import unittest

class MyTests(unittest.TestCase):

  #1
  def test_PutAuthor(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author one"))

  #2
  def test_PutAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author one"))
    self.assertEqual('1', db.putAuthor("Author two"))
    self.assertEqual('2', db.putAuthor("Author three"))

  #3
  def test_PutPaper(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one"]))

  #4
  def test_PutPaperAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one"]))

  #5
  def test_PutPaperTags(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one", "Tag two"]))

  #6
  def test_PutPaperTagsAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"]))

  #7
  def test_GetPaper(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"]))
    paper = db.getPaper('0')
    self.assertEqual(set(["Author one", "Author two"]), paper.authors)
    self.assertEqual('0', paper.viewCount)
    self.assertEqual('0', paper.id)
    self.assertEqual("Paper One's Title", paper.title)
    self.assertEqual(set(["Tag one","Tag two"]),paper.tags)

  #8
  def test_PutPapersAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["Tag one"]))
    self.assertEqual('1', db.putPaper("Paper Two's Title", ["Author two"],["Tag one"]))
    self.assertEqual('2', db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one","Tag two"]))

  #9
  def test_GetAuthor(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author One"))
    author = db.getAuthor('0')
    self.assertEqual("Author One", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual([],author.papers)

  #10
  def test_GetAuthors(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putAuthor("Author One"))
    self.assertEqual('1', db.putAuthor("Author Two"))
    self.assertEqual('2', db.putAuthor("Author Three"))
    author = db.getAuthor('2')
    self.assertEqual("Author Three", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('2', author.id)
    self.assertEqual([],author.papers)

  #11
  def test_GetAuthorsPapers(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    author = db.getAuthor('0')
    self.assertEqual("Author one", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual(['0'],author.papers)

  #12
  def test_PutTag(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("Tag one"))

  #13
  def test_PutTags(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("Tag one"))
    self.assertEqual('1', db.putTag("Tag two"))
    self.assertEqual('2', db.putTag("Tag three"))

  #14
  def test_GetTag(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putTag("239ck39&%$#@*&"))
    tag = db.getTag('0')
    self.assertEqual("239ck39&%$#@*&", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual([],tag.papers)

  #15
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

  #16
  def test_GetTagsPapers(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    tag = db.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual(['0'],tag.papers)

  #17
  def test_search(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', db.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = db.search("Paper One")
    paper = Paper('0', "Paper One's Title", set(["Author one"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)

  #18
  def test_searchtwo(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', db.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = db.search("Paper Two")
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)

  #18
  def test_searchthree(self):
    db = RedisDatabaseImpl()
    self.assertEqual('0', db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', db.putPaper("Paper TwoToo's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = db.search("Paper Two")
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)
    paper = Paper('2', "Paper TwoToo's Title", set(["Author one"]), set(["TagTwo"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[1].id)
    self.assertEqual(result[1].authors, paper.authors)
    self.assertEqual(result[1].viewCount, paper.viewCount)
    self.assertEqual(result[1].title, paper.title)
    self.assertEqual(result[1].tags,paper.tags)

if __name__ == '__main__': 
  unittest.main()
