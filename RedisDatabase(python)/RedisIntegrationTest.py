import unittest
import RedisDatabase
import datetime

class RedisIntegrationTestCase(unittest.TestCase):
  def setUp(self):
	self.redisDB = RedisDatabase()
	self.redisDB.clearDataBase()

  def test_1(self):
    authorIDs = []
	authorIds.append(self.redisDB.putAuthor("Jimmy Fallon"))
	authorIds.append(self.redisDB.putAuthor("Jimmy Dean"))
	authorIds.append(self.redisDB.putAuthor("James Dean"))
	authorIds.append(self.redisDB.putAuthor("Dean Thomas"))
	authorIds.append(self.redisDB.putAuthor("Thomas Jefferson"))
	authorIds.append(self.redisDB.putAuthor("Jefferson Davis"))
	
	publishers = []
	publishers.append(self.redisDB.putPublisher("RHIT"))
	publishers.append(self.redisDB.putPublisher("McGraw-Hill"))
	
	tagIDs = []
	tagIDs.append(self.redisDB.putTag("Biology"))
	tagIDs.append(self.redisDB.putTag("Nanotechnology"))
	tagIDs.append(self.redisDB.putTag("Distributed Computing"))
	tagIDs.append(self.redisDB.putTag("Big Data"))
	
	paperIDs = []
	paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [authorIDs[0],authorIDs[5]], [tagIDs[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4, 12, 30, 45), publishers[0], [], []))
	paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [authorIDs[2],authorIDs[3]], [tagIDs[1],tagIDs[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4, 12, 30, 45), publishers[1], [], []))
	
	for paper in self.redisDB.getTopPapers():
	  print paper
	
	
  
						 
  def tearDown(self):
    pass
	
if __name__ == '__main__':
    unittest.main()