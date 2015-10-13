import unittest
from RedisDatabase import RedisDatabase
import datetime

class RedisIntegrationTestCase(unittest.TestCase):
  def setUp(self):
	self.redisDB = RedisDatabase()
	self.redisDB.clearDatabase()

  def test_1(self):
    authorIDs = []
    authorIDs.append(self.redisDB.putAuthor("Jimmy Fallon"))
    authorIDs.append(self.redisDB.putAuthor("Jimmy Dean"))
    authorIDs.append(self.redisDB.putAuthor("James Dean"))
    authorIDs.append(self.redisDB.putAuthor("Dean Thomas"))
    authorIDs.append(self.redisDB.putAuthor("Thomas Jefferson"))
    authorIDs.append(self.redisDB.putAuthor("Jefferson Davis"))
    publishers = []
    publishers.append(self.redisDB.putPublisher("RHIT"))
    publishers.append(self.redisDB.putPublisher("McGraw-Hill"))
    tagIDs = []
    tagIDs.append(self.redisDB.putTag("Biology"))
    tagIDs.append(self.redisDB.putTag("Nanotechnology"))
    tagIDs.append(self.redisDB.putTag("Distributed Computing"))
    tagIDs.append(self.redisDB.putTag("Big Data"))
    paperIDs = []
    paperIDs.append(self.redisDB.putPaper("MY TITLE IS IN CAPS", [authorIDs[0],authorIDs[5]], [tagIDs[0]], "This is an abstract", -1, datetime.datetime(2003, 8, 4), publishers[0], [], []))
    paperIDs.append(self.redisDB.putPaper("cheese bacon", [authorIDs[2],authorIDs[3]], [tagIDs[1],tagIDs[2]], "This is another abstract", -1, datetime.datetime(2004, 8, 4), publishers[1], [], []))
    '''for paper in self.redisDB.getTopPapers():
      print paper
    self.assertEqual('foo'.upper(), 'FOO')'''
    print self.redisDB.getPaper(paperIDs[0])

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
