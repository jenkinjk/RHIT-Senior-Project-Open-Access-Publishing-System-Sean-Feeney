'''
Created on Oct 7, 2015

@author: jenkinjk
'''
from RedisDatabase import RedisDatabase
from Paper import Paper
import unittest
import datetime

class RedisIntegrationTestCase(unittest.TestCase):
  
    #use test database here instead
  def setUp(self):
    self.db = RedisDatabase()
    self.db.clearDatabase()

  #1
  def test_PutAuthor(self):
    self.assertEqual('0', self.db.putAuthor("Author one"))

  #2
  def test_PutAuthors(self):
    self.assertEqual('0', self.db.putAuthor("Author one"))
    self.assertEqual('1', self.db.putAuthor("Author two"))
    self.assertEqual('2', self.db.putAuthor("Author three"))

  #3
  def test_PutPaper(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #4
  def test_PutPaperAuthors(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #5
  def test_PutPaperTags(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #6
  def test_PutPaperTagsAuthors(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one", "Author two"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #7
  def test_GetPaper(self):
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
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author two"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.db.putPaper("Paper One's Title", ["Author one","Author two"],["Tag one","Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #9
  def test_GetAuthor(self):
    self.assertEqual('0', self.db.putAuthor("Author One"))
    author = self.db.getAuthor('0')
    self.assertEqual("Author One", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual([],author.papers)

  #10
  def test_GetAuthors(self):
    self.assertEqual('0', self.db.putAuthor("Author One"))
    self.assertEqual('1', self.db.putAuthor("Author Two"))
    self.assertEqual('2', self.db.putAuthor("Author Three"))
    author = self.db.getAuthor('2')
    self.assertEqual("Author Three", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('2', author.id)
    self.assertEqual([],author.papers)

  '''#THIS TEST SHOULDN'T PASS, SHOULD IT?
  #11
  def test_GetAuthorsPapers(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    author = self.db.getAuthor('0')
    self.assertEqual("Author one", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual(['0'],author.papers)'''

  #12
  def test_PutTag(self):
    self.assertEqual('0', self.db.putTag("Tag one"))

  #13
  def test_PutTags(self):
    self.assertEqual('0', self.db.putTag("Tag one"))
    self.assertEqual('1', self.db.putTag("Tag two"))
    self.assertEqual('2', self.db.putTag("Tag three"))

  #14
  def test_GetTag(self):
    self.assertEqual('0', self.db.putTag("239ck39&%$#@*&"))
    tag = self.db.getTag('0')
    self.assertEqual("239ck39&%$#@*&", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual([],tag.papers)

  #15
  def test_GetTags(self):
    self.assertEqual('0', self.db.putTag("Tag one"))
    self.assertEqual('1', self.db.putTag("Tag two"))
    self.assertEqual('2', self.db.putTag("TagThree"))
    tag = self.db.getTag('2')
    self.assertEqual("TagThree", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('2', tag.id)
    self.assertEqual([],tag.papers)

  '''#THIS TEST SHOULDN'T PASS, SHOULD IT?
  #16
  def test_GetTagsPapers(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    tag = self.db.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual(['0'],tag.papers)'''

  '''#17
  def test_search(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.db.putPaper("Paper Three's Title", ["Author one"],["TagTwo"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('3', self.db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    result = self.db.getPapersMatchingTitle("Paper One")
    self.assertEqual(4, len(result))
    paper = Paper('0', "Paper One's Title", set(["Author one"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#18
  def test_searchTwo(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.db.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.db.search("Paper Two")
    self.assertEqual(1, len(result))
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#19
  def test_searchTwoMiddle(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.db.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.db.search("Two")
    self.assertEqual(1, len(result))
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#20
  def test_searchThree(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.db.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.db.putPaper("Paper TwoToo's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.db.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.db.search("Paper Two")
    self.assertEqual(2, len(result))
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
    self.assertEqual(result[1].tags,paper.tags)'''

  '''#21
  def test_searchSeperated(self):
    self.assertEqual('0', self.db.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.db.putPaper("Paper Title One's", ["Author one", "Author two"],["TagOne"]))
    result = self.db.search("Paper One")
    paper = Paper('0', "Paper One's Title", set(["Author one"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(1, len(result))
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''
  #22
  def test_putUser(self):
    self.assertEqual('0', self.db.putUser("User One"))
    self.assertEqual('1', self.db.putUser("User Two"))

  #23
  def test_getUser(self):
    self.assertEqual('0', self.db.putUser("User One"))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual(set([]), result.papers)
    self.assertEqual(set([]),result.authors)
    self.assertEqual(set([]),result.tags)

  #23
  def test_favoritePaper(self):
    self.assertEqual('0', self.db.putUser("User One"))
    result = self.db.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual(set([]), result.papers)
    self.assertEqual(set([]),result.authors)
    self.assertEqual(set([]),result.tags)'''

  '''#Stress testing for performance
  def test_stress(self):
    start = datetime.datetime.now()
    for i in range(0,1000000):
      self.db.putPaper("%s" % i, ["Author one"],["TagOne"])
    finish = datetime.datetime.now()
    print finish - start
    start = datetime.datetime.now()
    result = self.db.search("100")
    finish = datetime.datetime.now()
    print finish - start'''

if __name__ == '__main__': 
  unittest.main()
