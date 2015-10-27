import unittest
from RedisDatabase import RedisDatabase
import datetime
from difflib import Differ
from Paper import Paper
from Author import Author
from Tag import Tag
from Publisher import Publisher

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
    self.cheesePaper = Paper("1", "cheese bacon",['3', '2'],['Nanotechnology', 'Distributed Computing'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jefferson Davis"])
    self.fpcPaper = Paper("5", "The Friendly Pirates of the Carribean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.fpmPaper = Paper("4", "The Friendly Pirates of the Mediterranean",['0', '6'],['Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.apcPaper = Paper("3", "The Angry Pirates of the Carribean",['0', '6'],['Dieting', 'Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.apmPaper = Paper("6", "The Angry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.hpmPaper = Paper("7", "The Hungry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"0",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
	self.fpcViewedPaper = Paper("5", "The Friendly Pirates of the Carribean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"1",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.fpmViewedPaper = Paper("4", "The Friendly Pirates of the Mediterranean",['0', '6'],['Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"7",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.apcViewedPaper = Paper("3", "The Angry Pirates of the Carribean",['0', '6'],['Dieting', 'Pirates', 'Big Data'],"This is another abstract","1",date2,None,"-1",[],"15",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.apmViewedPaper = Paper("6", "The Angry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"8",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
    self.hpmViewedPaper = Paper("7", "The Hungry Pirates of the Mediterranean",['0', '6'],['Big Data'],"This is another abstract","1",date2,None,"-1",[],"5",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
	self.hpaViewedPaper = Paper("8", "The Happy Planet of the Apes",['0', '6'],['Dieting', 'Pirates'],"This is another abstract","1",date2,None,"-1",[],"18",[],"RHIT",["Jimmy Fallon", "Jimmy Fallon"])
	
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

    self.paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [self.authorIDs[0], self.authorIDs[5]], [self.tags[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], [], []))
    self.paperIDs.append(self.redisDB.putPaper("cheese bacon", [self.authorIDs[2], self.authorIDs[3]], [self.tags[1], self.tags[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))

  def loadMoreTestData(self):
    self.redisDB.putTag("Pirates")
    self.redisDB.putTag("Dieting")

    self.tags.append("Pirates")
    self.tags.append("Dieting")

    self.paperIDs.append(self.redisDB.putPaper("Foo foo fOo Bar Bar bAR", [self.authorIDs[0], self.authorIDs[5]], [self.tags[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), self.publisherIDs[0], [], []))
    self.authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    self.paperIDs.append(self.redisDB.putPaper("The Angry Pirates of the Carribean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[4], self.tags[3],self.tags[5]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))
    self.paperIDs.append(self.redisDB.putPaper("The Friendly Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3],self.tags[4]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))
    self.paperIDs.append(self.redisDB.putPaper("The Friendly Pirates of the Carribean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))
    self.paperIDs.append(self.redisDB.putPaper("The Angry Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))
    self.paperIDs.append(self.redisDB.putPaper("The Hungry Pirates of the Mediterranean", [self.authorIDs[0], self.authorIDs[6]], [self.tags[3]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))
    self.paperIDs.append(self.redisDB.putPaper("The Happy Planet of the Apes", [self.authorIDs[0], self.authorIDs[6]], [self.tags[4],self.tags[5]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), self.publisherIDs[1], [], []))

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
    self.assertEqual(len(expecteds),len(rawActuals)) 
    self.assertEqual(expecteds,actuals)

  #7
  def testGetUnviewedAllPublishers(self):
    self.loadTestData()
    expecteds = set([self.rhitPublisher,self.mcGrawPublisher])
    rawActuals = set(self.redisDB.getAllPublishers())
    self.assertEqual(len(expecteds),len(rawActuals)) 
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

  '''def testTrivialAuthorWordsFilteredOutBeforePutAuthor(self):
    self.loadTestData()
    self.assertTrue(False)'''


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
	
  #This test was removed because it tests the implementation, not the correctness of the results
  '''def testTrivialTitleWordsFilteredOutBeforePutPaper(self):
    self.loadTestData()
    self.assertTrue(False)'''

  #20
  def testGetViewedPapersMatchingTags(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    actuals = self.redisDB.getPapersMatchingTags(["Pirates","Big Data","Dieting"])
    expecteds = [self.apcViewedPaper,self.hpaViewedPaper, self.fpmViewedPaper, self.apmViewedPaper, self.hpmViewedPaper, self.fpcViewedPaper]
    self.assertEqual(expecteds,actuals)
	  
  #21	  
  def testGetViewedPapersMatchingAuthorNames(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    actuals = self.redisDB.getPapersMatchingAuthorNames(["Jimmy Dean","Thomas Jefferson", "Poop"])
    expecteds = [self.apcViewedPaper, self.hpaViewedPaper,self.fpmViewedPaper,self.apmViewedPaper, self.hpmViewedPaper,self.fpcViewedPaper]
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
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #25
  def test_PutPaperAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #26
  def test_PutPaperTags(self):
    self.redisDB.putAuthor("Author one")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #27
  def test_PutPaperTagsAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0", "1"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #28
  def test_GetPaper(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0", "1"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    paper = self.redisDB.getPaper('0')
    self.assertEqual(set(["0", "1"]), set(paper.authorIDs))
    self.assertEqual('0', paper.viewCount)
    self.assertEqual('0', paper.id)
    self.assertEqual("Paper One's Title", paper.title)
    self.assertEqual(set(["Tag two", "Tag one"]) ,set(paper.tags))

  #29
  def test_PutPapersAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["1"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one","Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #30
  def test_GetAuthor(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author One"))
    author = self.redisDB.getAuthor('0')
    self.assertEqual("Author One", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual([],author.paperIDs)

  #31
  def test_GetAuthors(self):
    self.redisDB.putAuthor("Author One")
    self.redisDB.putAuthor("Author Two")
    self.redisDB.putAuthor("Author Three")
    author = self.redisDB.getAuthor('2')
    self.assertEqual("Author Three", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('2', author.id)
    self.assertEqual([],author.paperIDs)

  '''#THIS TEST SHOULDN'T PASS, SHOULD IT?
  #11
  def test_GetAuthorsPapers(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    author = self.redisDB.getAuthor('0')
    self.assertEqual("Author one", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual(['0'],author.papers)'''

  '''#12
  def test_PutTag(self):
    self.assertEqual('0', self.redisDB.putTag("Tag one"))

  #13
  def test_PutTags(self):
    self.assertEqual('0', self.redisDB.putTag("Tag one"))
    self.assertEqual('1', self.redisDB.putTag("Tag two"))
    self.assertEqual('2', self.redisDB.putTag("Tag three"))'''

  '''#14
  def test_GetTag(self):
    #self.assertEqual('0', self.redisDB.putTag("239ck39&%$#@*&"))   
    self.redisDB.putTag("239ck39&%$#@*&")
    tag = self.redisDB.getTag("239ck39&%$#@*&")
    self.assertEqual("239ck39&%$#@*&", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual([],tag.paperIDs)'''

  '''#15
  def test_GetTags(self):
    #self.assertEqual('0', self.redisDB.putTag("Tag one"))
    #self.assertEqual('1', self.redisDB.putTag("Tag two"))
    #self.assertEqual('2', self.redisDB.putTag("TagThree"))
	
    self.redisDB.putTag("Tag one")
    self.redisDB.putTag("Tag two")
    self.redisDB.putTag("TagThree")
	
    tag = self.redisDB.getTag("TagThree")
    self.assertEqual("TagThree", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual([],tag.paperIDs)'''

  '''#THIS TEST SHOULDN'T PASS, SHOULD IT?
  #16
  def test_GetTagsPapers(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    tag = self.redisDB.getTag('0')
    self.assertEqual("TagOne", tag.name)
    self.assertEqual('0', tag.viewCount)
    self.assertEqual('0', tag.id)
    self.assertEqual(['0'],tag.papers)'''

  '''#17
  def test_search(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.redisDB.putPaper("Paper Three's Title", ["Author one"],["TagTwo"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('3', self.redisDB.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    result = self.redisDB.getPapersMatchingTitle("Paper One")
    self.assertEqual(4, len(result))
    paper = Paper('0', "Paper One's Title", set(["Author one"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#18
  def test_searchTwo(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.redisDB.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.redisDB.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.redisDB.search("Paper Two")
    self.assertEqual(1, len(result))
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#19
  def test_searchTwoMiddle(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.redisDB.putPaper("Paper Three's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.redisDB.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.redisDB.getPapersMatchingTitle("Two")
    self.assertEqual(1, len(result))
    paper = Paper('1', "Paper Two's Title", set(["Author one", "Author two"]), set(["TagOne"]), '','','','','','','0','')
    self.assertEqual(paper.id,result[0].id)
    self.assertEqual(result[0].authors, paper.authors)
    self.assertEqual(result[0].viewCount, paper.viewCount)
    self.assertEqual(result[0].title, paper.title)
    self.assertEqual(result[0].tags,paper.tags)'''

  '''#20
  def test_searchThree(self):
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["Author one", "Author two"],["TagOne"]))
    self.assertEqual('2', self.redisDB.putPaper("Paper TwoToo's Title", ["Author one"],["TagTwo"]))
    self.assertEqual('3', self.redisDB.putPaper("Paper Four's Title", ["Author one"],["TagThree","TagFour"]))
    result = self.redisDB.getPapersMatchingTitle("Paper Two")
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
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["Author one"],["TagOne"]))
    self.assertEqual('1', self.redisDB.putPaper("Paper Title One's", ["Author one", "Author two"],["TagOne"]))
    result = self.redisDB.search("Paper One")
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
    self.assertEqual('0', self.redisDB.putUser("User One"))
    self.assertEqual('1', self.redisDB.putUser("User Two"))
  #23
  def test_getUser(self):
    self.assertEqual('0', self.redisDB.putUser("User One"))
    result = self.redisDB.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual(set([]), result.papers)
    self.assertEqual(set([]),result.authors)
    self.assertEqual(set([]),result.tags)
  #23
  def test_favoritePaper(self):
    self.assertEqual('0', self.redisDB.putUser("User One"))
    result = self.redisDB.getUser('0')
    self.assertEqual("User One", result.username)
    self.assertEqual(set([]), result.papers)
    self.assertEqual(set([]),result.authors)
    self.assertEqual(set([]),result.tags)'''

  '''#Stress testing for performance
  def test_stress(self):
    start = datetime.datetime.now()
    for i in range(0,1000000):
      self.redisDB.putPaper("%s" % i, ["Author one"],["TagOne"])
    finish = datetime.datetime.now()
    print finish - start
    start = datetime.datetime.now()
    result = self.redisDB.search("100")
    finish = datetime.datetime.now()
    print finish - start'''
	

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



if __name__ == '__main__':
  unittest.main()
