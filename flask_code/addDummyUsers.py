# This script adds dummy users to the database
import User
from RedisDatabase import RedisDatabase

db = RedisDatabase("Anything besides the string 'Test', which wipes the database each time for testing purposes") # our wrapper for the database

db.putUser("Asher Morgan", "1162476383780112")
db.putUser("Jonathan Jenkins", "986584014732857")

