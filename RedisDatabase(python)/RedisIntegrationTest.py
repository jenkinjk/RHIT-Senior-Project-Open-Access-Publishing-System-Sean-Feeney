import unittest
from RedisDatabase import RedisDatabase
import datetime
from difflib import Differ

class RedisIntegrationTestCase(unittest.TestCase):
  def setUp(self):
    self.redisDB = RedisDatabase()
    self.redisDB.clearDatabase()
    self.tagIDs = []
    self.authorIDs = []
    self.publisherIDs = []
    self.paperIDs = []

  def loadTestData(self):

    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Dean"))
    self.authorIDs.append(self.redisDB.putAuthor("James Dean"))
    self.authorIDs.append(self.redisDB.putAuthor("Dean Thomas"))
    self.authorIDs.append(self.redisDB.putAuthor("Thomas Jefferson"))
    self.authorIDs.append(self.redisDB.putAuthor("Jefferson Davis"))

    self.publisherIDs.append(self.redisDB.putPublisher("RHIT"))
    self.publisherIDs.append(self.redisDB.putPublisher("McGraw-Hill"))
    
    self.tagIDs.append(self.redisDB.putTag("Biology"))
    self.tagIDs.append(self.redisDB.putTag("Nanotechnology"))
    self.tagIDs.append(self.redisDB.putTag("Distributed Computing"))
    self.tagIDs.append(self.redisDB.putTag("Big Data"))

    self.paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [self.authorIDs[0], self.authorIDs[5]], [self.tagIDs[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], [], []))
    self.paperIDs.append(self.redisDB.putPaper("cheese bacon", [self.authorIDs[2], self.authorIDs[3]], [self.tagIDs[1], self.tagIDs[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))

  def loadMoreTestData(self):
    self.paperIDs.append(self.redisDB.putPaper("Foo foo fOo Bar Bar bAR", [self.authorIDs[0], self.authorIDs[5]], [self.tagIDs[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], [], []))
    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    self.paperIDs.append(self.redisDB.putPaper("The Pirates of the Carribean", [self.authorIDs[0], self.authorIDs[6]], [self.tagIDs[1], self.tagIDs[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))

  def testClearDatabase(self):
    id = self.redisDB.putAuthor("Jimmy Fallon")
    author = self.redisDB.getAuthor(id)
    self.assertEqual("id:0    name:Jimmy Fallon   papers:[]      viewCount:0", str(author))
    self.redisDB.clearDatabase()
    author = self.redisDB.getAuthor(id)
    self.assertEqual(None, author)

  def testGetAuthor(self):
    self.loadTestData()
    self.assertEqual("id:0    name:Jimmy Fallon   papers:['0']      viewCount:0", str(self.redisDB.getAuthor(self.authorIDs[0])))

  def testGetTag(self):
    self.loadTestData()
    self.assertEqual("id:0    name:Biology   papers:['0']      viewCount:0", str(self.redisDB.getTag(self.tagIDs[0])))

  def testGetPublisher(self):
    self.loadTestData()
    self.assertEqual("id:0    name:RHIT      viewCount:0", str(self.redisDB.getPublisher(self.publisherIDs[0])))

  def testGetPaper(self):
    self.loadTestData()
    paper = self.redisDB.getPaper(self.paperIDs[0])
    self.assertEqual("id:0    title:MY TITLE IS IN CAPS   authors:['0', '5']   tags:['0']   abstract:This is an abstract   publisher:0   datePublished:2003-08-04 00:00:00   datePosted:TruepostedBy:   references:[]   citedBys:[]      viewCount:0",self.getPaperStringCheckedPostedDate(paper))    

  def testGetAllTags(self):
    self.loadTestData()
    expecteds = ["id:0    name:Biology   papers:['0']      viewCount:0", "id:1    name:Nanotechnology   papers:['1']      viewCount:0", "id:2    name:Distributed Computing   papers:['1']      viewCount:0", "id:3    name:Big Data   papers:[]      viewCount:0"]
    rawActuals = self.redisDB.getAllTags()
    self.assertEqual(len(expecteds),len(rawActuals)) 
    actuals = set([])
    for rawActual in rawActuals:
      actuals.add(str(rawActual))
    for expected in expecteds:
      if expected not in actuals:
        self.assertEqual(expected,False)

  def testGetAllPublishers(self):
    self.loadTestData()
    expecteds = ["id:0    name:RHIT      viewCount:0", "id:1    name:McGraw-Hill      viewCount:0"]
    rawActuals = self.redisDB.getAllPublishers()
    self.assertEqual(len(expecteds),len(rawActuals)) 
    actuals = set([])
    for rawActual in rawActuals:
      actuals.add(str(rawActual))
    for expected in expecteds:
      if expected not in actuals:
        self.assertEqual(expected,False)

  def testGetTopPapers(self):
    self.loadTestData()
    rawActuals = self.redisDB.getTopPapers()
    actuals = []
    expecteds = "[\"id:0    title:MY TITLE IS IN CAPS   authors:[\'0\', \'5\']   tags:[\'0\']   abstract:This is an abstract   publisher:0   datePublished:2003-08-04 00:00:00   datePosted:TruepostedBy:   references:[]   citedBys:[]      viewCount:0\", \"id:1    title:cheese bacon   authors:[\'3\', \'2\']   tags:[\'1\', \'2\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:   references:[]   citedBys:[]      viewCount:0\"]"
    for rawActual in rawActuals:
      actuals.append(self.getPaperStringCheckedPostedDate(rawActual))
    self.assertEqual(expecteds,str(actuals))

  def testGetTopAuthors(self):
    self.loadTestData()
    self.assertEqual("[id:0    name:Jimmy Fallon   papers:['0']      viewCount:0, id:1    name:Jimmy Dean   papers:[]      viewCount:0, id:2    name:James Dean   papers:['1']      viewCount:0, id:3    name:Dean Thomas   papers:['1']      viewCount:0, id:4    name:Thomas Jefferson   papers:[]      viewCount:0, id:5    name:Jefferson Davis   papers:['0']      viewCount:0]", str(self.redisDB.getTopAuthors()))

  def testGetPapersByYearValid(self):
    self.loadTestData()
    rawActuals = self.redisDB.getPapersPublishedInYear("2003")
    actuals = []
    expecteds = "[\"id:0    title:MY TITLE IS IN CAPS   authors:[\'0\', \'5\']   tags:[\'0\']   abstract:This is an abstract   publisher:0   datePublished:2003-08-04 00:00:00   datePosted:TruepostedBy:   references:[]   citedBys:[]      viewCount:0\"]"
    for rawActual in rawActuals:
      actuals.append(self.getPaperStringCheckedPostedDate(rawActual))
    self.assertEqual(expecteds,str(actuals))

  def testGetPapersByYearEmpty(self):
    self.loadTestData()
    rawActuals = self.redisDB.getPapersPublishedInYear("1972")
    self.assertEquals([],rawActuals)

    #Test that nothing bad was changed
  def testIncrementViews(self):
    self.loadTestData()
    self.redisDB.incrementPaperViews("0")
    paper = self.redisDB.getPaper("0")
    self.assertEqual(paper.viewCount, 1)
    for rawAuthor in paper.authors:
      author = self.redisDB.getAuthor(rawAuthor)
      self.assertEqual(author.viewCount, 1)
    for rawTag in paper.tags:
      tag = self.redisDB.getTag(rawTag)
      self.assertEqual(tag.viewCount, 1)
    self.assertTrue(False)

  def testIncrementViewsDoesntIncrementPaperWithRepetitiveWordsMultipleTimes(self):
    self.loadTestData()
    self.assertTrue(False)

  def testIncrementViewsDoesntIncrementAuthorsWithSameNameOnSamePaperMultipleTimes(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("3")
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:jimmy", 0))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:jimmy", 6))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:fallon", 0))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:fallon", 6))


  def testTagPaper(self):
    self.loadTestData()
    for i in range(0,28):
      self.redisDB.incrementPaperViews("0")
    for i in range(0,5):
      self.redisDB.incrementPaperViews("1")
    self.assertEqual(self.redisDB.getTag("0").viewCount, "28")
    self.assertEqual(self.redisDB.getTag("1").viewCount, "5")
    self.redisDB.tagPaper("0","1")
    self.assertEqual(self.redisDB.getTag("1").viewCount, "33")
    self.assertTrue("1" in self.redisDB.getPaper("0").tags)
    self.assertEqual(self.redisDB.getPaper("0").viewCount, "28")
    self.assertEqual(28, self.redisDB.redisDB.zscore("Tag:1:Papers", "0"))
    self.assertEqual(33, self.redisDB.redisDB.zscore("Tags", "1"))


  def testGetAuthorsMatchingAuthorsSingle(self):
    self.loadTestData()
    self.assertEqual("[id:1    name:Jimmy Dean   papers:[]      viewCount:0, id:0    name:Jimmy Fallon   papers:['0']      viewCount:0]",str(self.redisDB.getAuthorsMatchingAuthors(["Jimmy"])))
    self.assertEqual("[id:1    name:Jimmy Dean   papers:[]      viewCount:0, id:3    name:Dean Thomas   papers:['1']      viewCount:0, id:2    name:James Dean   papers:['1']      viewCount:0]",str(self.redisDB.getAuthorsMatchingAuthors(["Dean"])))
    self.assertEqual("[id:2    name:James Dean   papers:['1']      viewCount:0]",str(self.redisDB.getAuthorsMatchingAuthors(["James"])))
    self.assertEqual("[]",str(self.redisDB.getAuthorsMatchingAuthors(["Poop"])))

  def testGetAuthorsMatchingAuthorsMultiple(self):
    self.loadTestData()
    self.assertEqual("[id:0    name:Jimmy Fallon   papers:['0']      viewCount:0, id:2    name:James Dean   papers:['1']      viewCount:0, id:5    name:Jefferson Davis   papers:['0']      viewCount:0, id:1    name:Jimmy Dean   papers:[]      viewCount:0, id:3    name:Dean Thomas   papers:['1']      viewCount:0, id:4    name:Thomas Jefferson   papers:[]      viewCount:0]",str(self.redisDB.getAuthorsMatchingAuthors(["Jimmy Dean","Thomas Jefferson", "Poop"])))

  def testTrivialAuthorWordsFilteredOutBeforePutAuthor(self):
    self.loadTestData()
    self.assertTrue(False)

  def testGetPapersMatchingTitle(self):
    self.loadTestData()
    self.assertTrue(False)

  #This test was removed because it tests the implementation, not the correctness of the results
  '''def testTrivialTitleWordsFilteredOutBeforePutPaper(self):
    self.loadTestData()
    self.assertTrue(False)'''

  def testGetPapersMatchingTags(self):
    self.loadTestData()
    self.assertTrue(False)


  def getPaperStringCheckedPostedDate(self, paper):
    validDateTime = False
    if isinstance(paper.datePosted, datetime.datetime):
      validDateTime = True
    s = str(paper)
    oneEnd = s.find("datePosted:")
    twoStart = s.find("postedBy:") 
    return s[:oneEnd+11]+str(validDateTime)+s[twoStart:]


  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
