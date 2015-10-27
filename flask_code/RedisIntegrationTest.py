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

  def testClearDatabase(self):
    id = self.redisDB.putAuthor("Jimmy Fallon")
    self.assertEqual(self.jimmyFallonEmpty, self.redisDB.getAuthor(id))
    self.redisDB.clearDatabase()
    self.assertEqual(None, self.redisDB.getAuthor(id))

  def testGetAuthor(self):
    self.loadTestData()
    self.assertEqual(self.jimmyFallon, self.redisDB.getAuthor(self.authorIDs[0]))

  def testGetTag(self):
    self.loadTestData()
    self.assertEqual(self.bioTag, self.redisDB.getTag(self.tags[0]))

  def testGetPublisher(self):
    self.loadTestData()
    self.assertEqual(self.rhitPublisher, self.redisDB.getPublisher(self.publisherIDs[0]))

  def testGetPaper(self):
    self.loadTestData()
    self.assertEqual(self.allCapsPaper,self.redisDB.getPaper(self.paperIDs[0]))    

  def testGetAllTags(self):
    self.loadTestData()

    expecteds = set([])
    expecteds.add(self.bioTag)
    expecteds.add(self.nanoTag)
    expecteds.add(self.distTag)
    expecteds.add(self.bigDataTag)
    rawActuals = self.redisDB.getAllTags()
    self.assertEqual(len(expecteds),len(rawActuals)) 
    actuals = set([])
    for rawActual in rawActuals:
      actuals.add(rawActual)
    self.assertEqual(expecteds,actuals)

  def testGetAllPublishers(self):
    self.loadTestData()
    expecteds = set([])
    expecteds.add(self.rhitPublisher)
    expecteds.add(self.mcGrawPublisher)
    rawActuals = self.redisDB.getAllPublishers()
    self.assertEqual(len(expecteds),len(rawActuals)) 
    actuals = set([])
    for rawActual in rawActuals:
      actuals.add(rawActual)
    self.assertEqual(expecteds,actuals)

  def testGetTopPapers(self):
    self.loadTestData()
    actuals = self.redisDB.getTopPapers()
    expecteds = [self.allCapsPaper,self.cheesePaper]
    self.assertEqual(expecteds,actuals)

  def testGetTopAuthors(self):
    self.loadTestData()
    actuals = self.redisDB.getTopAuthors()
    expecteds = [self.jimmyFallon,self.jimmyDean,self.jamesDean, self.deanThomas, self.thomasJefferson, self.jeffersonDavis]
    self.assertEqual(expecteds, actuals)

  def testGetPapersByYearValid(self):
    self.loadTestData()
    actuals = self.redisDB.getPapersPublishedInYear("2003")
    expecteds = []
    expecteds.append(self.allCapsPaper)
    self.assertEqual(expecteds,actuals)

  def testGetPapersByYearEmpty(self):
    self.loadTestData()
    actuals = self.redisDB.getPapersPublishedInYear("1972")
    self.assertEquals([],actuals)

  def testIncrementViews(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("0")
    self.checkPaperViewCountUpdated(1, "0")


  def testIncrementViewsDoesntIncrementPaperWithRepetitiveWordsMultipleTimes(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.redisDB.incrementPaperViews("3")
    self.redisDB.incrementPaperViews("3")
    self.redisDB.incrementPaperViews("3")
    self.checkPaperViewCountUpdated(3, "3")    

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
    self.assertEqual(self.redisDB.getTag("Biology").viewCount, "28")
    self.assertEqual(self.redisDB.getTag("Nanotechnology").viewCount, "5")
    self.redisDB.tagPaper("0","Nanotechnology")
    self.assertEqual(self.redisDB.getTag("Nanotechnology").viewCount, "33")
    self.assertTrue("Nanotechnology" in self.redisDB.getPaper("0").tags)
    self.assertEqual(self.redisDB.getPaper("0").viewCount, "28")
    self.assertEqual(28, self.redisDB.redisDB.zscore("Tag:Nanotechnology:Papers", "0"))
    self.assertEqual(33, self.redisDB.redisDB.zscore("Tags", "Nanotechnology"))


  def testGetAuthorsMatchingAuthorNamesSingle(self):
    self.loadTestData()
    actuals = set(self.redisDB.getAuthorsMatchingAuthorNames(["Jimmy"]))
    self.assertEqual(len(actuals),2)
    expecteds = set([self.jimmyDean, self.jimmyFallon])
    self.assertEqual(expecteds, actuals)

    actuals2 = set(self.redisDB.getAuthorsMatchingAuthorNames(["Dean"]))
    self.assertEqual(len(actuals2),3)
    expecteds2 = set([self.jimmyDean, self.jamesDean, self.deanThomas])
    self.assertEqual(expecteds2, actuals2)

    actuals3 = set(self.redisDB.getAuthorsMatchingAuthorNames(["James"]))
    self.assertEqual(len(actuals3),1)
    expecteds3 = set([self.jamesDean])
    self.assertEqual(expecteds3, actuals3)	
	
    self.assertEqual([],self.redisDB.getAuthorsMatchingAuthorNames(["Poop"]))

  def testGetAuthorsMatchingAuthorNamesMultiple(self):
    self.loadTestData()
    s = self.redisDB.getAuthorsMatchingAuthorNames(["Jimmy Dean","Thomas Jefferson", "Poop"])
    s1 = [str(s[0]),str(s[1]),str(s[2])]
    s2 = [str(s[3]),str(s[4]),str(s[5])]
    self.assertEqual(len(s),6)
    #setofAuthorsCompare
    self.assertTrue("id:4    name:Thomas Jefferson   papers:[]      viewCount:0" in s1)
    self.assertTrue("id:1    name:Jimmy Dean   papers:[]      viewCount:0" in s1)
    self.assertTrue("id:3    name:Dean Thomas   papers:['1']      viewCount:0" in s1)
    self.assertTrue("id:2    name:James Dean   papers:['1']      viewCount:0" in s2)
    self.assertTrue("id:5    name:Jefferson Davis   papers:['0']      viewCount:0" in s2)
    self.assertTrue("id:0    name:Jimmy Fallon   papers:['0']      viewCount:0" in s2)

  '''def testTrivialAuthorWordsFilteredOutBeforePutAuthor(self):
    self.loadTestData()
    self.assertTrue(False)'''

  def testGetPapersMatchingTitle(self):
    self.loadTestData()
    self.loadMoreTestData()
    papers = self.redisDB.getPapersMatchingTitle("The Friendly Pirates of the Carribean")
    s = []
    for p in papers:
      s.append(p)
    s1 = [s[0]]
    s2 = [s[1],s[2]]
    s3 = [s[3],s[4]]
    self.assertEqual(5,len(s))
	#setofPapersEqual
    self.assertEqual(str(s1),"[\"id:5    title:The Friendly Pirates of the Carribean   authors:[\'0\', \'6\']   tags:[\'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:0\"]")
    self.assertTrue("id:4    title:The Friendly Pirates of the Mediterranean   authors:['0', '6']   tags:['Pirates', 'Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:0" in s2)
    self.assertTrue("id:3    title:The Angry Pirates of the Carribean   authors:['0', '6']   tags:['Dieting', 'Pirates', 'Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:0" in s2)
    self.assertTrue("id:6    title:The Angry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:0" in s3)
    self.assertTrue("id:7    title:The Hungry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:0" in s3)

  def testGetViewedPapersMatchingTitle(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    papers = self.redisDB.getPapersMatchingTitle("The Friendly Pirates of the Carribean")
    s = []
    for p in papers:
      s.append(p)
	  #SetofPapersComp
    self.assertEqual("[\"id:5    title:The Friendly Pirates of the Carribean   authors:[\'0\', \'6\']   tags:[\'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:1\", \"id:3    title:The Angry Pirates of the Carribean   authors:[\'0\', \'6\']   tags:[\'Dieting\', \'Pirates\', \'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:15\", \"id:4    title:The Friendly Pirates of the Mediterranean   authors:[\'0\', \'6\']   tags:[\'Pirates\', \'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:7\", \"id:6    title:The Angry Pirates of the Mediterranean   authors:[\'0\', \'6\']   tags:[\'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:8\", \"id:7    title:The Hungry Pirates of the Mediterranean   authors:[\'0\', \'6\']   tags:[\'Big Data\']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:5\"]",str(s))

  #This test was removed because it tests the implementation, not the correctness of the results
  '''def testTrivialTitleWordsFilteredOutBeforePutPaper(self):
    self.loadTestData()
    self.assertTrue(False)'''

  def testGetPapersMatchingTags(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    papers = self.redisDB.getPapersMatchingTags(["Pirates","Big Data","Dieting"])
    s = []
    for p in papers:
      s.append(p)
	  #SetofPapersComp
    expecteds = ["id:3    title:The Angry Pirates of the Carribean   authors:['0', '6']   tags:['Dieting', 'Pirates', 'Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:15", "id:8    title:The Happy Planet of the Apes   authors:['0', '6']   tags:['Dieting', 'Pirates']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:18", "id:4    title:The Friendly Pirates of the Mediterranean   authors:['0', '6']   tags:['Pirates', 'Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:7", "id:6    title:The Angry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:8", "id:7    title:The Hungry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:5", "id:5    title:The Friendly Pirates of the Carribean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:1"]
    for i in range(0,len(expecteds)):
      self.assertEqual(expecteds[i],s[i])
	  
	  
  def testGetPapersMatchingAuthorNames(self):
    self.loadTestData()
    self.loadMoreTestData()
    self.viewPiratePapers()
    papers = self.redisDB.getPapersMatchingAuthorNames(["Jimmy Dean","Thomas Jefferson", "Poop"])
    s = []
    for p in papers:
      s.append(p)
    #expecteds = ["id:3    title:The Angry Pirates of the Carribean   authors:['0', '6']   tags:['Big Data', 'Dieting', 'Pirates']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:15", "id:8    title:The Happy Planet of the Apes   authors:['0', '6']   tags:['Dieting', 'Pirates']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:18", "id:4    title:The Friendly Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data', 'Pirates']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:7", "id:6    title:The Angry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:8", "id:7    title:The Hungry Pirates of the Mediterranean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:5", "id:5    title:The Friendly Pirates of the Carribean   authors:['0', '6']   tags:['Big Data']   abstract:This is another abstract   publisher:1   datePublished:2004-08-04 00:00:00   datePosted:TruepostedBy:-1   references:[]   citedBys:[]      viewCount:1"]
    #print "!!!!!!!!!"+str(s)+"!!!!!!!!!!!"
	#for i in range(0,len(expecteds)):
    #  self.assertEqual(expecteds[i],s[i])	  

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


  #1
  def test_PutAuthor(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author one"))

  #2
  def test_PutAuthors(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author one"))
    self.assertEqual('1', self.redisDB.putAuthor("Author two"))
    self.assertEqual('2', self.redisDB.putAuthor("Author three"))

  #3
  def test_PutPaper(self):
    self.redisDB.putAuthor("Author one")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #4
  def test_PutPaperAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #5
  def test_PutPaperTags(self):
    self.redisDB.putAuthor("Author one")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #6
  def test_PutPaperTagsAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0", "1"],["Tag one", "Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #7
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

  #8
  def test_PutPapersAuthors(self):
    self.redisDB.putAuthor("Author one")
    self.redisDB.putAuthor("Author two")
    self.assertEqual('0', self.redisDB.putPaper("Paper One's Title", ["0"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('1', self.redisDB.putPaper("Paper Two's Title", ["1"],["Tag one"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))
    self.assertEqual('2', self.redisDB.putPaper("Paper One's Title", ["0","1"],["Tag one","Tag two"],"This is an abstract", -1, datetime.datetime(2003, 8, 4), -1, [], []))

  #9
  def test_GetAuthor(self):
    self.assertEqual('0', self.redisDB.putAuthor("Author One"))
    author = self.redisDB.getAuthor('0')
    self.assertEqual("Author One", author.name)
    self.assertEqual('0', author.viewCount)
    self.assertEqual('0', author.id)
    self.assertEqual([],author.paperIDs)

  #10
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

if __name__ == '__main__':
  unittest.main()
