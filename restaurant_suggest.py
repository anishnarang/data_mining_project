from pyspark import SparkContext
from pyspark import SparkConf
import math
import time
import sys
from operator import itemgetter
import pickle

class predictBusiness:

	def __init__(self, items_user, items_foods_business, items_business_food, items_foods_user):
		self.items_user = items_user
		self.items_foods_business = items_foods_business
		self.items_business_food = items_business_food
		self.items_foods_user = items_foods_user

	def userToFood(self):
		candidate_foods = {}
		for user in self.items_user:
			foods = self.items_user[user]
			if user not in candidate_foods:
				candidate_foods[user] = []
			foods.sort(key=itemgetter(1), reverse=True)
			food = [x[0] for x in foods]
			candidate_foods[user] = food[:5]
		return candidate_foods

	def foodToBusiness(self, candidate_foods):
		candidate_business = {}
		for user in candidate_foods:
			foods = candidate_foods[user]
			if user not in candidate_business:
				candidate_business[user] = set()
			for food in foods:
				candidate_business[user].union(self.items_foods_business[food])
		return candidate_business

	def businessToFoods(self, candidate_business):
		candidate_foods = {}
		for user in candidate_business:
			businesses = candidate_business[user]
			if user not in candidate_foods:
				candidate_foods[user] = set()
			for business in businesses:
				candidate_foods[user].union(self.items_business_food[business])
		return candidate_foods

	def foodsToUsers(self, candidate_foods):
		candidate_users = {}
		for user in candidate_foods:
			foods = candidate_foods[user]
			if user not in candidate_users:
				candidate_users[user] = set()
			for food in foods:
				candidate_users[user].union(self.items_foods_user[food])
		return candidate_users

if __name__ == '__main__':
	conf = (SparkConf().setAppName("Assignment3"))
	conf = (conf
			.set('spark.executor.memory', '8G')
			.set('spark.driver.memory', '8G')
			.set('spark.driver.maxResultSize', '8G'))
	sc = SparkContext(conf = conf)
	#sc = SparkContext("local", "Assignment Task 2")
	#sc.setLogLevel(logLevel = "ERROR")
	f = sc.textFile('user_to_food_interest.txt', 40)
	f2 = sc.textFile('business_to_food_mapping.txt', 40)
	f3 = sc.textFile('food_to_business_mapping.txt', 40)

	# rdd for user to food
	items = f.map(lambda line: line.strip().split(","))
	items = items.map(lambda x: (x[0], [(x[1], x[2])])).reduceByKey(lambda x,y:x+y).collectAsMap()
	#rdd for food to user
	items_foods_user = f.map(lambda line: line.strip().split(","))
	items_foods_user = items_foods_user.map(lambda x: (x[1], [x[0]])).reduceByKey(lambda x,y:x+y).collectAsMap()

	# rdd for food to business
	items_foods_business = f3.map(lambda line: line.strip().split(","))
	items_foods_business = items_foods_business.map(lambda x: (x[0], [x[1]])).reduceByKey(lambda x,y:x+y).collectAsMap()

	# rdd for business to food
	items_business_food = f2.map(lambda line: line.strip().split(","))
	items_business_food = items_business_food.map(lambda x: (x[0], [x[1]])).reduceByKey(lambda x,y:x+y).collectAsMap()

	predictBusiness = predictBusiness(items, items_foods_business, items_business_food, items_foods_user)
	user_to_food = predictBusiness.userToFood()
	d = {user_to_food.keys()[0]: user_to_food[list(user_to_food.keys())[0]]}
	food_to_business = predictBusiness.foodToBusiness(d)																																																				
	full_foods = predictBusiness.businessToFoods(food_to_business)
	user_neighbors = predictBusiness.foodsToUsers(full_foods)
	print(len(user_neighbors))												

