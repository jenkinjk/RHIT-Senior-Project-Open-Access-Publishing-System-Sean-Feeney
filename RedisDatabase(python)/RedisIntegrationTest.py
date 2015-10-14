import unittest
from RedisDatabase import RedisDatabase
import datetime

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

  def testClearDatabase(self):
    id = self.redisDB.putAuthor("Jimmy Fallon")
    author = self.redisDB.getAuthor(id)
    self.assertEqual("id:0    name:Jimmy Fallon   papers:[]      viewCount:0", str(author))
    self.redisDB.clearDatabase()
    author = self.redisDB.getAuthor(id)
    self.assertEqual(None, author)
    #test that the counters are reset

  def testGetAuthor(self):
    self.loadTestData()

    self.assertEqual("id:0    name:Jimmy Fallon   papers:['0']      viewCount:0", str(self.redisDB.getAuthor(self.authorIDs[0])))
    #print self.redisDB.getAuthor(authorIDs[0])
    #print self.redisDB.getAuthor(authorIDs[2])
    #print self.redisDB.getPublisher(publishers[0])
    #print self.redisDB.getTag(tagIDs[0])
    #print self.redisDB.getTag(tagIDs[3])
    #tags = self.redisDB.getAllTags()
    #for tag in tags:
    #  print tag
    #print self.redisDB.getPaper(paperIDs[0])

  def testGetTag(self):
    self.loadTestData()

  def testGetPublisher(self):
    self.loadTestData()

  def testGetPaper(self):
    self.loadTestData()

  def testGetAllTags(self):
    expecteds = []
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

  def testGetTopPapers(self):
    self.loadTestData()

  def testGetTopAuthors(self):
    self.loadTestData()

  def testGetPapersByYearValid(self):
    self.loadTestData()
    rawActuals = self.redisDB.getPapersPublishedInYear("2003")
    rawPapers = self.redisDB.redisDB.zrange("YearPublished:2003",0,-1)
    self.assertEquals("id:0    title:MY TITLE IS IN CAPS   authors:['0', '5']   tags:['0']   abstract:This is an abstract   publisher:0   datePublished:2003-08-04 00:00:00   datePosted:2015-10-14 02:43:19.674070   postedBy:   references:[]   citedBys:[]      viewCount:0",str(rawActuals[0]))

  def testGetPapersByYearEmpty(self):
    self.loadTestData()
    rawActuals = self.redisDB.getPapersPublishedInYear("1972")
    self.assertEquals([],rawActuals)

  def testIncrementViews(self):
    self.loadTestData()

  def testIncrementViewsDoesntIncrementPaperWithRepetitiveWordsMultipleTimes(self):
    self.loadTestData()

  def testIncrementViewsDoesntIncrementAuthorsWithSameNameOnSamePaperMultipleTimes(self):
    self.loadTestData()

  def testTagPaper(self):
    self.loadTestData()

  def testGetAuthorsMatchingAuthorsSingle(self):
    self.loadTestData()

  def testGetAuthorsMatchingAuthorsMultiple(self):
    self.loadTestData()

  def testTrivialAuthorWordsFilteredOutBeforePutAuthor(self):
    self.loadTestData()

  def testGetPapersMatchingTitle(self):
    self.loadTestData()

  def testTrivialTitleWordsFilteredOutBeforePutPaper(self):
    self.loadTestData()

  def testGetPapersMatchingTags(self):
    self.loadTestData()


  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
