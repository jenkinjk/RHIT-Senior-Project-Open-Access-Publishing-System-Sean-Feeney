import unittest
from RedisDatabase import RedisDatabase
import datetime
from difflib import Differ
from Paper import Paper
from Author import Author
from Tag import Tag
from Publisher import Publisher
from User import User

class RedisIntegrationTestCase(unittest.TestCase):

  def setUp(self):
    self.redisDB = RedisDatabase("Test")
    self.redisDB.clearDatabase()
    self.tags = []
    self.authorIDs = []
    self.publisherIDs = []
    self.paperIDs = []
    date = datetime.datetime(2003, 8, 4)
    date2 = datetime.datetime(2004, 8, 4)
    self.jimmyFallon = Author("0", "Jimmy Fallon", '0', ['0'], ["MY TITLE IS IN CAPS"], [['Jimmy Fallon', "Jefferson Davis"]], [date])
    self.jimmyDean = Author("1", "Jimmy Dean", '0', [], [], [], [])
    self.jamesDean = Author("2", "James Dean", '0', ['1'], ["cheese bacon"], [['Dean Thomas', "James Dean"]], [date2])
    self.deanThomas = Author("3", "Dean Thomas", '0', ['1'], ["cheese bacon"], [['Dean Thomas', "James Dean"]], [date2])
    self.thomasJefferson = Author("4", "Thomas Jefferson", '0', [], [], [], [])
    self.jeffersonDavis = Author("5", "Jefferson Davis", '0', ['0'], ["MY TITLE IS IN CAPS"], [['Jimmy Fallon', "Jefferson Davis"]], [date])
    self.jimmyFallonEmpty = Author("0", "Jimmy Fallon", '0', [], [], [], [])
    self.bioTag = Tag("Biology","0",['0'])
    self.nanoTag = Tag("Nanotechnology","0",['1'])
    self.distTag = Tag("Distributed Computing","0",['1'])
    self.bigDataTag = Tag("Big Data","0",[])
    self.rhitPublisher = Publisher("0","RHIT","0")
    self.mcGrawPublisher = Publisher("1","McGraw-Hill","0")
    self.allCapsPaper = Paper("0", "MY TITLE IS IN CAPS",['0', '5'],['Biology'],"This is an abstract","0",date,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jefferson Davis"])
    self.cheesePaper = Paper("1", "cheese bacon",['3', '2'],['Nanotechnology', 'Distributed Computing'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Dean Thomas", "James Dean"])
    self.fpcPaper = Paper("5", "The Friendly Pirates of the Carribean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.fpmPaper = Paper("4", "The Friendly Pirates of the Mediterranean",['0', '6'],['Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.apcPaper = Paper("3", "The Angry Pirates of the Carribean",['0', '6'],['Dieting', 'Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.apmPaper = Paper("6", "The Angry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.hpmPaper = Paper("7", "The Hungry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.fpcViewedPaper = Paper("5", "The Friendly Pirates of the Carribean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"1",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.fpmViewedPaper = Paper("4", "The Friendly Pirates of the Mediterranean",['0', '6'],['Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"7",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.apcViewedPaper = Paper("3", "The Angry Pirates of the Carribean",['0', '6'],['Dieting', 'Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"15",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.apmViewedPaper = Paper("6", "The Angry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"8",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.hpmViewedPaper = Paper("7", "The Hungry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"5",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.hpaViewedPaper = Paper("8", "The Happy Planet of the Apes",['0', '6'],['Dieting', 'Pirates'],"This is another abstract","1",date2,None,"-1",[],"18",[],"McGraw-Hill",["Jimmy Fallon", "Jimmy Fallon"])
    self.fooBarPaper = Paper("2", "Foo foo fOo Bar Bar bAR",['0', '5'],["Biology"],"This is an abstract","0",date,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jefferson Davis"])

  def loadTestData(self):

    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Dean"))
    self.authorIDs.append(self.redisDB.putAuthor("James Dean"))
    self.authorIDs.append(self.redisDB.putAuthor("Dean Thomas"))
    self.authorIDs.append(self.redisDB.putAuthor("Thomas Jefferson"))
    self.authorIDs.append(self.redisDB.putAuthor("Jefferson Davis"))

    self.publisherIDs.append(self.redisDB.putPublisher("RHIT"))
    self.publisherIDs.append(self.redisDB.putPublisher("McGraw-Hill"))
    
    self.redisDB.putTag("Biology")
    self.redisDB.putTag("Nanotechnology")
    self.redisDB.putTag("Distributed Computing")
    self.redisDB.putTag("Big Data")
	
    self.tags.append("Biology")
    self.tags.append("Nanotechnology")
    self.tags.append("Distributed Computing")
    self.tags.append("Big Data")

    self.paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [self.authorIDs[0], self.authorIDs[5]], [self.tags[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], True))
    self.paperIDs.append(self.redisDB.putPaper("cheese bacon", [self.authorIDs[2], self.authorIDs[3]], [self.tags[1], self.tags[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))

  def loadMoreTestData(self):
    self.redisDB.putTag("Pirates")
    self.redisDB.putTag("Dieting")

    self.tags.append("Pirates")
    self.tags.append("Dieting")

    self.paperIDs.append(self.redisDB.putPaper("Foo foo fOo Bar Bar bAR", [self.authorIDs[0], self.authorIDs[5]], [self.tags[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], True))
    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    self.paperIDs.append(self.redisDB.putPaper("The Angry Pirates of the Carribean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[4], self.tags[3],self.tags[5]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))
    self.paperIDs.append(self.redisDB.putPaper("The Friendly Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3],self.tags[4]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))
    self.paperIDs.append(self.redisDB.putPaper("The Friendly Pirates of the Carribean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))
    self.paperIDs.append(self.redisDB.putPaper("The Angry Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))
    self.paperIDs.append(self.redisDB.putPaper("The Hungry Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))
    self.paperIDs.append(self.redisDB.putPaper("The Happy Planet of the Apes", [self.authorIDs[0], self.authorIDs[6]], [self.tags[4],self.tags[5]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], True))

  def viewPiratePapers(self):
    for i in range(0,15):
      self.redisDB.incrementPaperViews("3")
    for i in range(0,7):
      self.redisDB.incrementPaperViews("4")
    for i in range(0,1):
      self.redisDB.incrementPaperViews("5")
    for i in range(0,8):
      self.redisDB.incrementPaperViews("6")
    for i in range(0,5):
      self.redisDB.incrementPaperViews("7")
    for i in range(0,18):
      self.redisDB.incrementPaperViews("8")

  #1
  def testClearDatabase(self):
    id = self.redisDB.putAuthor("Jimmy Fallon")
    self.assertEqual(self.jimmyFallonEmpty, self.redisDB.getAuthor(id))
    self.redisDB.clearDatabase()
    self.assertEqual(None, self.redisDB.getAuthor(id))

  #2
  def testGetAuthor(self):
    self.loadTestData()
    self.assertEqual(self.jimmyFallon, self.redisDB.getAuthor(self.authorIDs[0]))

  #3
  def testGetTag(self):
    self.loadTestData()
    self.assertEqual(self.bioTag, self.redisDB.getTag(self.tags[0]))

  #4
  def testGetPublisher(self):
    self.loadTestData()
    self.assertEqual(self.rhitPublisher, self.redisDB.getPublisher(self.publisherIDs[0]))

  #5
  def testGetPaper(self):
    self.loadTestData()
    self.assertEqual(self.allCapsPaper,self.redisDB.getPaper(self.paperIDs[0]))    

  #6
  def testGetUnviewedAllTags(self):
    self.loadTestData()
    expecteds = set([self.bioTag,self.nanoTag,self.distTag,self.bigDataTag])
    actuals = set(self.redisDB.getAllTags())
    self.assertEqual(len(expecteds),len(actuals)) 
    self.assertEqual(expecteds,actuals)

  #7
  def testGetUnviewedAllPublishers(self):
    self.loadTestData()
    expecteds = set([self.rhitPublisher,self.mcGrawPublisher])
    actuals = set(self.redisDB.getAllPublishers())
    self.assertEqual(len(expecteds),len(actuals)) 
    self.assertEqual(expecteds,actuals)

  #8
  def testGetUnviewedTopPapers(self):
    self.loadTestData()
    actuals = set(self.redisDB.getTopPapers())
    expecteds = set([self.allCapsPaper,self.cheesePaper])
    self.assertEqual(expecteds,actuals)

  #9
  def testGetUnviewedTopAuthors(self):
    self.loadTestData()
    actuals = set(self.redisDB.getTopAuthors())
    expecteds = set([self.jimmyFallon,self.jimmyDean,self.jamesDean, self.deanThomas, self.thomasJefferson, self.jeffersonDavis])
    self.assertEqual(expecteds, actuals)

  #10
  def testGetUnviewedPapersByYearValid(self):
    self.loadTestData()
    actuals = self.redisDB.getPapersPublishedInYear("2003")
    expecteds = []
    expecteds.append(self.allCapsPaper)
    self.assertEqual(expecteds,actuals)

  #11
  def testGetPapersByYearEmpty(self):
    self.loadTestData()
    actuals = self.redisDB.getPapersPublishedInYear("1972")
    self.assertEquals([],actuals)

  #12
  def testIncrementViews(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("0")
    self.checkPaperViewCountUpdated(1, "0")

  #13
  def testIncrementViewsDoesntIncrementPaperWithRepetitiveWordsMultipleTimes(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("3")
    self.redisDB.incrementPaperViews("3")
    self.redisDB.incrementPaperViews("3")
    self.checkPaperViewCountUpdated(3, "3")    

  #14
  def testIncrementViewsDoesntIncrementAuthorsWithSameNameOnSamePaperMultipleTimes(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("3")
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:jimmy", 0))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:jimmy", 6))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:fallon", 0))
    self.assertEqual(1,self.redisDB.redisDB.zscore("AuthorWord:fallon", 6))

  #15
  def testTagPaper(self):
    self.loadTestData()
    for i in range(0,28):
      self.redisDB.incrementPaperViews("0")
    for i in range(0,5):
      self.redisDB.incrementPaperViews("1")
    self.assertEqual(self.redisDB.getTag("Biology").viewCount, "28")
    self.assertEqual(self.redisDB.getTag("Nanotechnology").viewCount, "5")
    self.redisDB.tagPaper("0","Nanotechnology")
    self.assertEqual(self.redisDB.getTag("Nanotechnology").viewCount, "33")
    self.assertTrue("Nanotechnology" in self.redisDB.getPaper("0").tags)
    self.assertEqual(self.redisDB.getPaper("0").viewCount, "28")
    self.assertEqual(28, self.redisDB.redisDB.zscore("Tag:Nanotechnology:Papers", "0"))
    self.assertEqual(33, self.redisDB.redisDB.zscore("Tags", "Nanotechnology"))

  #16
  def testGetAuthorsMatchingAuthorNamesSingle(self):
    self.loadTestData()
    actuals1 = set(self.redisDB.getAuthorsMatchingAuthorNames(["Jimmy"]))
    self.assertEqual(len(actuals1),2)
    expecteds1 = set([self.jimmyDean, self.jimmyFallon])
    self.assertEqual(expecteds1, actuals1)

    actuals2 = set(self.redisDB.getAuthorsMatchingAuthorNames(["Dean"]))
    self.assertEqual(len(actuals2),3)
    expecteds2 = set([self.jimmyDean, self.jamesDean, self.deanThomas])
    self.assertEqual(expecteds2, actuals2)

    actuals3 = set(self.redisDB.getAuthorsMatchingAuthorNames(["James"]))
    self.assertEqual(len(actuals3),1)
    expecteds3 = set([self.jamesDean])
    self.assertEqual(expecteds3, actuals3)

    self.assertEqual([],self.redisDB.getAuthorsMatchingAuthorNames(["Poop"]))

  #17
  def testGetAuthorsMatchingAuthorNamesMultiple(self):
    self.loadTestData()
    s = self.redisDB.getAuthorsMatchingAuthorNames(["Jimmy Dean","Thomas Jefferson", "Poop"])
    self.assertEqual(len(s),6)
    actuals1 = set([s[0], s[1], s[2]])
    actuals2 = set([s[3], s[4], s[5]])
    expecteds1 = set([self.thomasJefferson, self.deanThomas, self.jimmyDean])
    expecteds2 = set([self.jimmyFallon, self.jeffersonDavis, self.jamesDean])
    self.assertEqual(actuals1, expecteds1)
    self.assertEqual(actuals2, expecteds2)

  #18
  def testGetUnviewedPapersMatchingTitle(self):
    self.loadTestData()
    self.loadMoreTestData()
    actuals = self.redisDB.getPapersMatchingTitle("The Friendly Pirates of the Carribean")
    self.assertEqual(5,len(actuals))
    actuals1 = set([actuals[0]])
    actuals2 = set([actuals[1],actuals[2]])
    actuals3 = set([actuals[3],actuals[4]])
	
    expecteds1 = set([self.fpcPaper])
    expecteds2 = set([self.fpmPaper, self.apcPaper])
    expecteds3 = set([self.apmPaper, self.hpmPaper])

    self.assertEqual(actuals1,expecteds1)
    self.assertEqual(actuals2,expecteds2)
    self.assertEqual(actuals3,expecteds3)

  #19
  def testGetViewedPapersMatchingTitle(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    actuals = self.redisDB.getPapersMatchingTitle("The Friendly Pirates of the Carribean")
    expecteds = [self.fpcViewedPaper,self.apcViewedPaper,self.fpmViewedPaper, self.apmViewedPaper, self.hpmViewedPaper]
    self.assertEqual(actuals, expecteds)

  #20
  def testGetViewedPapersMatchingTags(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    actuals = self.redisDB.getPapersMatchingTags(["Pirates","Big Data","Dieting"])
    expecteds = [self.apcViewedPaper,self.hpaViewedPaper, self.fpmViewedPaper, self.apmViewedPaper, self.hpmViewedPaper, self.fpcViewedPaper]
    self.assertEqual(expecteds,actuals)

  #TODO make this not a set	  
  #21	  
  def testGetViewedPapersMatchingAuthorNames(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    actuals = set(self.redisDB.getPapersMatchingAuthorNames(["Jimmy Fallon","Jefferson Davis", "Poop"]))
    expecteds = set([self.apcViewedPaper, self.hpaViewedPaper,self.fpmViewedPaper,self.apmViewedPaper, self.hpmViewedPaper,self.fpcViewedPaper, self.allCapsPaper, self.fooBarPaper])
    self.assertEqual(len(expecteds),len(actuals))	
    self.assertEqual(expecteds,actuals)

  #22
  def test_PutAuthor(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author one"))

  #23
  def test_PutAuthors(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author one"))
    self.assertEqual('1', self.redisDB.putAuthor("Author two"))
    self.assertEqual('2', self.redisDB.putAuthor("Author three"))

  #24
  def test_PutPaper(self):
    self.redisDB.putAuthor("Author one")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))

  #25
  def test_PutPaperAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))

  #26
  def test_PutPaperTags(self):
    self.redisDB.putAuthor("Author one")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one", "Tag two"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))

  #27
  def test_PutPaperTagsAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0", "1"],["Tag one", "Tag two"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))

  #28
  def test_GetPaper(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.redisDB.putPublisher("RHIT")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0", "1"],["Tag one", "Tag two"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))
    actual = self.redisDB.getPaper('0')
    expected = Paper('0', "Paper One's Title", ["1", "0"], ["Tag two", "Tag one"], "This is an abstract", "0", datetime.datetime(2003, 8, 4), None, "0", [], '0', [], "RHIT", ["Author two","Author one"])
    self.assertEqual(actual, expected)

  #29
  def test_PutPapersAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["1"],["Tag one"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))
    self.assertEqual('2', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one","Tag two"],"This is an abstract", "0", datetime.datetime(2003, 8, 4), "0", True))

  #30
  def test_GetAuthor(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author One"))
    actual = self.redisDB.getAuthor('0')
    expected = Author('0', "Author One", '0', [], [], [], [])

  #31
  def test_GetAuthors(self):
    self.redisDB.putAuthor("Author One")
    self.redisDB.putAuthor("Author Two")
    self.redisDB.putAuthor("Author Three")
    actual = self.redisDB.getAuthor('2')
    expected = Author('2', "Author Three", '0', [], [], [], [])

  #32	  
  def testGetUnviewedPapersMatchingAuthorIDs(self):
    self.loadTestData()
    self.loadMoreTestData()
    actuals = set(self.redisDB.getPapersMatchingAuthorIDs(["2","5"]))
    expecteds = set([self.cheesePaper, self.allCapsPaper, self.fooBarPaper])
    self.assertEqual(len(expecteds),len(actuals))	
    self.assertEqual(expecteds,actuals)

  #33
  def test_GetTag(self):
    self.redisDB.putTag("239ck39&%$#@*&")
    tag = self.redisDB.getTag("239ck39&%$#@*&")
    self.assertEqual(tag, Tag("239ck39&%$#@*&",'0', []))

  #34
  def test_GetTags(self):
    self.redisDB.putTag("Tag one")
    self.redisDB.putTag("Tag two")
    self.redisDB.putTag("TagThree")
    tag = self.redisDB.getTag("TagThree")
    self.assertEqual(tag, Tag("TagThree",'0', []))

  #35
  def test_GetTagsPapers(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, True))
    tag = self.redisDB.getTag('TagOne')
    self.assertEqual(tag, Tag("TagOne",'0', ['0']))

  
  #36
  def testPutUser(self):
    self.assertEqual('0', self.redisDB.putUser("Andrew Davidson"))
    self.assertEqual('1', self.redisDB.putUser("Andrew Carnegie"))
  #37
  def testGetUser(self):
    self.redisDB.putUser("Andrew Davidson")
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], [], "0")
    self.assertEqual(actual, expected)

  #38
  def testFavoritePapers(self):
    self.loadTestData()
    self.redisDB.putUser("Andrew Davidson")

    self.redisDB.putFavoritePaper("0","0",0)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertFalse(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.putFavoritePaper("0","1",11)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertFalse(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.putFavoritePaper("0","1",-1)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertFalse(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.putFavoritePaper("0","1",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.cheesePaper, self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.removeFavoritePaper("0","1")
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertFalse(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.putFavoritePaper("0","1",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.cheesePaper, self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"1"))

    self.redisDB.putFavoritePaper("0","45",3)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [self.cheesePaper, self.allCapsPaper], [], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"0"))
    self.assertTrue(self.redisDB.hasFavoritePaper('0',"1"))
    self.assertFalse(self.redisDB.hasFavoritePaper('0',"45"))
	
  #39
  def testFavoriteTags(self):
    self.loadTestData()
    self.redisDB.putUser("Andrew Davidson")

    self.redisDB.putFavoriteTag("0","Big Data",0)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertFalse(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.putFavoriteTag("0","Biology",-1)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertFalse(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.putFavoriteTag("0","Biology",11)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertFalse(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.putFavoriteTag("0","Biology",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Biology", "Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.removeFavoriteTag("0","Biology")
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertFalse(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.putFavoriteTag("0","Biology",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Biology", "Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Biology"))

    self.redisDB.putFavoriteTag("0","poop",3)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [], ["Biology", "Big Data"], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Big Data"))
    self.assertTrue(self.redisDB.hasFavoriteTag('0',"Biology"))
    self.assertFalse(self.redisDB.hasFavoriteTag('0',"poop"))
	
  #40
  def testFavoriteAuthors(self):
    self.loadTestData()
    self.redisDB.putUser("Andrew Davidson")

    self.redisDB.putFavoriteAuthor("0","0",0)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertFalse(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.putFavoriteAuthor("0","3",-1)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertFalse(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.putFavoriteAuthor("0","3",11)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertFalse(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.putFavoriteAuthor("0","3",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon, self.deanThomas], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.removeFavoriteAuthor("0","3")
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertFalse(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.putFavoriteAuthor("0","3",10)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon, self.deanThomas], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"3"))

    self.redisDB.putFavoriteAuthor("0","45",3)
    actual = self.redisDB.getUserByID('0')
    expected = User("0", "Andrew Davidson", [], [], [], [self.jimmyFallon, self.deanThomas], [], "0")
    self.assertEqual(actual, expected)
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"0"))
    self.assertTrue(self.redisDB.hasFavoriteAuthor('0',"3"))
    self.assertFalse(self.redisDB.hasFavoriteAuthor('0',"45"))
	
  #41
  def test_stalker(self):
    ids = []
    ids.append(self.redisDB.putUser("Andrew Davidson"))
    ids.append(self.redisDB.putUser("Barbra Streissand"))
    ids.append(self.redisDB.putUser("Andrew Carnegie"))
    self.redisDB.addStalker(ids[1], ids[0])
    self.redisDB.addStalker(ids[1], ids[2])
    self.redisDB.addStalker(ids[0], ids[2])
    self.redisDB.addStalker(ids[0], ids[0])
    actualA = self.redisDB.getUserByID(ids[0])
    actualB = self.redisDB.getUserByID(ids[1])
    actualC = self.redisDB.getUserByID(ids[2])
    expectedA = User("0", "Andrew Davidson", ["2"], ["Andrew Carnegie"], [], [], [], "1")
    expectedB = User("1", "Barbra Streissand", ["2", "0"], ["Andrew Carnegie", "Andrew Davidson"], [], [], [], "0")
    expectedC = User("2", "Andrew Carnegie", [], [], [], [], [], "2")
    self.assertEqual(actualA, expectedA)
    self.assertEqual(actualB, expectedB)
    self.assertEqual(actualC, expectedC)
    self.assertTrue(self.redisDB.isStalking("0", "2"))
    self.assertTrue(self.redisDB.isStalking("1", "2"))
    self.assertTrue(self.redisDB.isStalking("1", "0"))
    self.assertFalse(self.redisDB.isStalking("0", "1"))
    self.assertFalse(self.redisDB.isStalking("0", "0"))
    self.assertFalse(self.redisDB.isStalking("2", "0"))
    self.assertFalse(self.redisDB.isStalking("2", "1"))

    self.redisDB.removeStalker(ids[1], ids[0])
    actualA = self.redisDB.getUserByID(ids[0])
    actualB = self.redisDB.getUserByID(ids[1])
    expectedA = User("0", "Andrew Davidson", ["2"], ["Andrew Carnegie"], [], [], [], "0")
    expectedB = User("1", "Barbra Streissand", ["2"], ["Andrew Carnegie"], [], [], [], "0")
    self.assertEqual(actualA, expectedA)
    self.assertEqual(actualB, expectedB)
    self.assertTrue(self.redisDB.isStalking("1", "2"))
    self.assertFalse(self.redisDB.isStalking("1", "0"))
  
  #42
  def testUserIntegration(self):
    self.loadTestData()

    ids = []
    ids.append(self.redisDB.putUser("Andrew Davidson"))
    ids.append(self.redisDB.putUser("Barbra Streissand"))
    ids.append(self.redisDB.putUser("Andrew Carnegie"))

    self.redisDB.addStalker(ids[1], ids[0])
    self.redisDB.addStalker(ids[1], ids[2])
    self.redisDB.addStalker(ids[0], ids[2])

    self.redisDB.putFavoriteAuthor("0","0",3)
    self.redisDB.putFavoriteAuthor("0","3",3)
    self.redisDB.putFavoriteAuthor("0","45",3)

    self.redisDB.putFavoriteTag("0","Big Data",3)
    self.redisDB.putFavoriteTag("0","Biology",3)
    self.redisDB.putFavoriteTag("0","poop",3)

    self.redisDB.putFavoritePaper("0","0",3)
    self.redisDB.putFavoritePaper("0","1",3)
    self.redisDB.putFavoritePaper("0","45",3)

    actualA = self.redisDB.getUserByID(ids[0])
    actualB = self.redisDB.getUserByID(ids[1])
    actualC = self.redisDB.getUserByID(ids[2])
    expectedA = User("0", "Andrew Davidson", ["2"], ["Andrew Carnegie"], [self.cheesePaper, self.allCapsPaper], [self.jimmyFallon, self.deanThomas], ["Biology", "Big Data"], "1")
    expectedB = User("1", "Barbra Streissand", ["2", "0"], ["Andrew Carnegie", "Andrew Davidson"], [], [], [], "0")
    expectedC = User("2", "Andrew Carnegie", [], [], [], [], [], "2")
    self.assertEqual(actualA, expectedA)
    self.assertEqual(actualB, expectedB)
    self.assertEqual(actualC, expectedC)

  #43
  def testAdvancedSearch(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
 
    self.redisDB.putPaper("The Friendly Friendlier Pirates of the Carribean", ['2', '3'], ['Pirates', 'Big Data'], "This is another abstract", -1, datetime.datetime(2003, 8, 4),self.publisherIDs[1], True)
    ffpmPaper = Paper("9", "The Friendly Friendlier Pirates of the Carribean",['2', '3'],['Pirates', 'Big Data'],"This is another abstract","1",datetime.datetime(2003, 8, 4),None,"-1",[],"0",[],"McGraw-Hill",["James Dean", "Dean Thomas"])

    actuals = self.redisDB.getPapersAdvancedSearch(["The Friendly Pirates of the Carribean"],["Dieting"],["Jimmy Fulton"])

    # apc matches 2 title words and 1 tag and an author with 18 views
    # fpc matches 3 title words and an author with 1 view
    # fpm matches 2 title words and an author with 7 views
    # hpa matches 1 tag and an author with 18 views
    # apm matches 1 title word and an author with 8 views
    # hpm matches 1 title word and an author with 5 views
    # ffpc matches 3 title words but not an author with 0 view
    # allCaps matches only the author
    # foo matches only the author
    # cheese matches nothing and is not found in the results 

    #The advanced search algorithm first shows all results that match both author(s) and title-word(s)/tag(s), then results that just match title-word(s)/tag(s), then results that just match author(s).  Between these first two groups, results come first based on the number of matches between title words/tags (a matched title word is weighted the same as a matched tag in the advanced search).  Among papers with the same number of matches, they are further ordered by view count.  At the end, the results that only match authors but not tag(s)/title-word(s) come in a random order.  

    actuals0123456 = [actuals[0],actuals[1],actuals[2],actuals[3],actuals[4],actuals[5],actuals[6]]
    expecteds0123456 = [self.apcViewedPaper, self.fpcViewedPaper, self.fpmViewedPaper, self.hpaViewedPaper, self.apmViewedPaper, self.hpmViewedPaper, ffpmPaper]
    self.assertEqual(actuals0123456,expecteds0123456)

    actuals78 = set([actuals[7],actuals[8]])
    expecteds78 = set([self.fooBarPaper, self.allCapsPaper])
    self.assertEqual(actuals78,expecteds78)

  '''#44
  def testPaperRecsForUserID(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    self.redisDB.putUser("Andrew Davidson")
    self.redisDB.putFavoriteAuthor("0","0",2)

    self.redisDB.putFavoriteTag("0","Distributed Computing",2)
    self.redisDB.putFavoriteTag("0","Biology",1)
    self.redisDB.putFavoriteTag("0","Dieting",4)

    actuals = self.redisDB.getPaperRecsForUserID("0")
    self.assertEqual(actuals[0], self.hpaViewedPaper)
    self.assertEqual(actuals[1], self.apcViewedPaper)

    actuals23 = set([actuals[2],actuals[3]])
    expecteds23 = set([self.fooBarPaper, self.allCapsPaper])
    self.assertEqual(actuals23, expecteds23)

    self.assertEqual(actuals[4], self.cheesePaper)

    actuals5678 = set([actuals[5],actuals[6],actuals[7],actuals[8]])
    expecteds5678 = set([self.apmViewedPaper,self.hpmViewedPaper, self.fpmViewedPaper,self.fpcViewedPaper])
    self.assertEqual(actuals5678, expecteds5678)
  
  #Stress testing for performance
  def testSearchStress(self):
    self.loadTestData()
    self.redisDB.putUser("Andrew Davidson")

    listA = []
    listB = []
    listC = []

    for i in range(0,6):
      for j in range(0,26):
        listA.append(str(unichr(i+97))+str(unichr(97+j)))
        listB.append(str(unichr(i+6+97))+str(unichr(97+j)))
        listC.append(str(unichr(i+12+97))+str(unichr(97+j)))

    startInsert = datetime.datetime.now()
    print "beginning to insert papers into the DB: ",startInsert

    for a in listA:
      for b in listB:
        for c in listC:
          self.redisDB.putPaper(a+" "+b+" "+c, ["0"], [], "abstract", "0", datetime.datetime.now(), "0", [], [])

    endInsert = datetime.datetime.now()
    print "ended inserting papers into the DB: ",endInsert
    print "total time elapsed: ", endInsert - startInsert

    startSearch = datetime.datetime.now()
    print "searching for paper with title \"\": ", startSearch

    rslt = self.redisDB.getPapersMatchingTitle("ab hk oz")

    endSearch = datetime.datetime.now()
    print "ended searching for paper with title \"\": ",endSearch
    print "total time elapsed: ", endSearch - startSearch
    print "total time for both steps: ", endSearch - startInsert
    print "rslt:"
    print rslt'''

  def checkPaperViewCountUpdated(self, views, id):
    paper = self.redisDB.getPaper(id)
    self.assertEqual(paper.viewCount, str(views))
    self.assertEqual(views, self.redisDB.redisDB.zscore("Papers",id))
    self.assertEqual(views, self.redisDB.redisDB.zscore("YearPublished:"+str(paper.datePublished.year),id))
    self.assertEqual(views, self.redisDB.redisDB.zscore("Publishers",paper.publisherID))
    self.assertEqual(str(views), self.redisDB.getPublisher(paper.publisherID).viewCount)
    for word in self.redisDB.getSearchWords(paper.title):
      self.assertEqual(views, self.redisDB.redisDB.zscore("PaperWord:"+word,id))
    for rawAuthor in paper.authorIDs:
      author = self.redisDB.getAuthor(rawAuthor)
      self.assertEqual(author.viewCount, str(views))
      self.assertEqual(views, self.redisDB.redisDB.zscore("Authors",rawAuthor))
      for word in self.redisDB.getSearchWords(author.name):
        self.assertEqual(views, self.redisDB.redisDB.zscore("AuthorWord:"+word, rawAuthor))        
    for rawTag in paper.tags:
      tag = self.redisDB.getTag(rawTag)
      self.assertEqual(tag.viewCount, str(views))
      self.assertEqual(views, self.redisDB.redisDB.zscore("Tags",rawTag))
      self.assertEqual(views, self.redisDB.redisDB.zscore("Tag:"+rawTag+":Papers",id))

  #TODO test getAll methods after viewing papers
  #TODO test putting in a duplicate author name

  #These tests were cancelled because they test the implementation, not the correctness, of the results.
  #TODO we should still do these tests anyways
  '''def testTrivialTitleWordsFilteredOutBeforePutPaper(self):
    self.loadTestData()
    self.assertTrue(False)'''

  '''def testTrivialAuthorWordsFilteredOutBeforePutAuthor(self):
    self.loadTestData()
    self.assertTrue(False)'''

  #44
  def testAdvancedSearchBoth(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
 
    self.redisDB.putPaper("The Friendly Friendlier Pirates of the Carribean", ['2', '3'], ['Pirates', 'Big Data'], "This is another abstract", -1, datetime.datetime(2003, 8, 4),self.publisherIDs[1], False)
    ffpmPaper = Paper("9", "The Friendly Friendlier Pirates of the Carribean",['2', '3'],['Pirates', 'Big Data'],"This is another abstract","1",datetime.datetime(2003, 8, 4),None,"-1",[],"0",[],"McGraw-Hill",["James Dean", "Dean Thomas"])

    actuals = self.redisDB.getPapersAdvancedSearch(["The Friendly Pirates of the Carribean"],["Dieting"],["Jimmy Fulton"])  

    actuals0123456 = [actuals[0],actuals[1],actuals[2],actuals[3],actuals[4],actuals[5],actuals[6]]
    expecteds0123456 = [self.apcViewedPaper, self.fpcViewedPaper, self.fpmViewedPaper, self.hpaViewedPaper, self.apmViewedPaper, self.hpmViewedPaper, ffpmPaper]
    self.assertEqual(actuals0123456,expecteds0123456)

    actuals78 = set([actuals[7],actuals[8]])
    expecteds78 = set([self.fooBarPaper, self.allCapsPaper])
    self.assertEqual(actuals78,expecteds78)

  #45
  def testAdvancedSearchFake(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
 
    self.redisDB.putPaper("The Friendly Friendlier Pirates of the Carribean", ['2', '3'], ['Pirates', 'Big Data'], "This is another abstract", -1, datetime.datetime(2003, 8, 4),self.publisherIDs[1], False)
    ffpmPaper = Paper("9", "The Friendly Friendlier Pirates of the Carribean",['2', '3'],['Pirates', 'Big Data'],"This is another abstract","1",datetime.datetime(2003, 8, 4),None,"-1",[],"0",[],"McGraw-Hill",["James Dean", "Dean Thomas"])

    actuals = self.redisDB.getPapersAdvancedSearchFakeOnly(["The Friendly Pirates of the Carribean"],["Dieting"],["Jimmy Fulton"])

    self.assertEqual(len(actuals),1)
    self.assertEqual(actuals[0],ffpmPaper)

  #46
  def testAdvancedSearchReal(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
 
    self.redisDB.putPaper("The Friendly Friendlier Pirates of the Carribean", ['2', '3'], ['Pirates', 'Big Data'], "This is another abstract", -1, datetime.datetime(2003, 8, 4),self.publisherIDs[1], False)
    ffpmPaper = Paper("9", "The Friendly Friendlier Pirates of the Carribean",['2', '3'],['Pirates', 'Big Data'],"This is another abstract","1",datetime.datetime(2003, 8, 4),None,"-1",[],"0",[],"McGraw-Hill",["James Dean", "Dean Thomas"])

    actuals = self.redisDB.getPapersAdvancedSearchRealOnly(["The Friendly Pirates of the Carribean"],["Dieting"],["Jimmy Fulton"])

    actuals012345 = [actuals[0],actuals[1],actuals[2],actuals[3],actuals[4],actuals[5]]
    expecteds012345 = [self.apcViewedPaper, self.fpcViewedPaper, self.fpmViewedPaper, self.hpaViewedPaper, self.apmViewedPaper, self.hpmViewedPaper]
    self.assertEqual(actuals012345,expecteds012345)

    actuals67 = set([actuals[6],actuals[7]])
    expecteds67 = set([self.fooBarPaper, self.allCapsPaper])
    self.assertEqual(actuals67,expecteds67)

  #47
  def testUpdatePaper(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()

    date = datetime.datetime(2003, 8, 4)
    self.redisDB.updatePaper("3", "The Red Hot Chili Peppers",['1', '6'],['Dieting', 'Biology'],"This is not another abstract","-1",date,"0", False)

    expected = Paper("3", "The Red Hot Chili Peppers",['1', '6'],['Dieting', 'Biology'],"This is not another abstract","0",date,None,"-1",[],"15",[],"RHIT",["Jimmy Dean", "Jimmy Fallon"], False)
    actual = self.redisDB.getPaper("3")
    self.assertEqual(expected, actual)

    yearNew = self.redisDB.getPapersPublishedInYear("2003")
    valid1 = False
    for paper in yearNew:
      if paper.id == "3":
        valid1 = True

    yearOld = self.redisDB.getPapersPublishedInYear("2004")
    valid2 = True
    for paper in yearOld:
      if paper.id == "3":
        valid2 = False

    tagOld1 = self.redisDB.getTag("Pirates").paperIDs
    valid3 = "3" not in tagOld1
    tagOld2 = self.redisDB.getTag("Big Data").paperIDs
    valid4 = "3" not in tagOld2

    titleOld = self.redisDB.getPapersMatchingTitle("The Angry Pirates of the Carribean")
    valid5 = True
    for paper in titleOld:
      if paper.id == "3":
        valid5 = False

    authorOld = self.redisDB.getPapersForAuthorID("0")
    valid6 = True
    for paper in authorOld:
      if paper.id == "3":
        valid6 = False

    self.assertTrue(valid1 and valid2 and valid3 and valid4 and valid5 and valid6)

if __name__ == '__main__':
  unittest.main()
