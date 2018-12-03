from pyspark import SparkContext
from pyspark import SparkConf
import math
import time
import sys
from operator import itemgetter
import pickle
from collections import defaultdict

class predictBusiness:

	def __init__(self, items_user, items_foods_business, items_business_food, items_foods_user, business_stars):
		self.items_user = items_user
		self.items_foods_business = items_foods_business
		self.items_business_food = items_business_food
		self.items_foods_user = items_foods_user	
		self.business_stars = business_stars

	def userToFood(self):
		candidate_foods = {}
		for user in self.items_user:
			foods = self.items_user[user]
			if user not in candidate_foods:
				candidate_foods[user] = set()
			foods.sort(key=itemgetter(1), reverse=True)
			food = [x[0] for x in foods]
			candidate_foods[user] = list(set(food[:5]))
		return candidate_foods

	def foodToBusiness(self, candidate_foods):
		candidate_business = {}
		final_business = {}
		pruned_business = []
		for user in candidate_foods:
			foods = candidate_foods[user]
			if user not in candidate_business:
				candidate_business[user] = set()
			for food in foods:
				candidate_business[user] = candidate_business[user].union(self.items_foods_business[food])
		for user in candidate_business:
			min_star = 0.0
			min_review = 0.0
			min_key = ""
			if user not in final_business:
				final_business[user] = []
			businesses = candidate_business[user]
			for business in businesses:
				if business in self.business_stars:
					if(self.business_stars[business]['review_count'] > 40):
						if len(final_business[user]) == 0:
							final_business[user] = [business, self.business_stars[business]['stars'], self.business_stars[business]['review_count']]
							min_star = self.business_stars[business]['stars']
							min_review = self.business_stars[business]['review_count']

						elif self.business_stars[business]['stars'] > min_star:
							final_business[user] = [business, self.business_stars[business]['stars'], self.business_stars[business]['review_count']]
							min_star = self.business_stars[business]['stars']
							min_review = self.business_stars[business]['review_count']

						elif self.business_stars[business]['stars'] == min_star:
							if self.business_stars[business]['review_count'] > min_review:
								final_business[user] = [business, self.business_stars[business]['stars'], self.business_stars[business]['review_count']]
								min_star = self.business_stars[business]['stars']
								min_review = self.business_stars[business]['review_count']
			candidate_business[user] = final_business[user][0]


			'''for business in businesses:
				final_business[user][business] = defaultdict()
				if business in self.business_stars:
					if len(final_business[user]) == 0:
						final_business[user][business]['stars'] = self.business_stars[business]['stars']
						final_business[user][business]['review_count'] = self.business_stars[business]['review_count']
					elif len(final_business[user]) == 5:
						if(self.business_stars[business]['stars'] > min_val):
							del final_business[user][min_key]
							final_business[user][business]['stars'] = self.business_stars[business]['stars']
							final_business[user][business]['review_count'] = self.business_stars[business]['review_count']
					else:
						final_business[user][business]['stars'] = self.business_stars[business]['stars']
						final_business[user][business]['review_count'] = self.business_stars[business]['review_count']
					min_val = min(final_business[user]['stars'].values())
					min_key = min(final_business[user]['stars'], key = final_business[user]['stars'].get)'''
						
			#businesses = sorted(candidate_business, key = candidate_business.get, reverse = True)
			#final_business[user] = businesses[:5]
		return candidate_business

	def businessToFoods(self, candidate_business):
		candidate_foods = {}
		for user in candidate_business:
			business = candidate_business[user]
			if user not in candidate_foods:
				candidate_foods[user] = set()
			#for business in businesses:
			candidate_foods[user] = set(self.items_business_food[business])#candidate_foods[user].union(self.items_business_food[business])
		return candidate_foods

	def foodsToUsers(self, candidate_foods):
		candidate_users = {}
		for user in candidate_foods:
			foods = candidate_foods[user]
			if user not in candidate_users:
				candidate_users[user] = set()
			for food in foods:
				candidate_users[user] = candidate_users[user].union(self.items_foods_user[food])
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
	f = sc.textFile('sampled_user_to_food_mapping.txt', 40)
	f2 = sc.textFile('sampled_business_to_food_mapping.txt', 40)
	f3 = sc.textFile('sampled_food_to_business_mapping.txt', 40)

	business_stars = defaultdict()
	#business_review = defaultdict()
	business = pickle.load(open( "las_vegas_business_ids.p", "rb" ))

	for i in business['business_details']:
		business_stars[i] = defaultdict()
		business_stars[i]['stars'] = business['business_details'][i]['stars']
		business_stars[i]['review_count'] = business['business_details'][i]['review_count']

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

	predictBusiness = predictBusiness(items, items_foods_business, items_business_food, items_foods_user, business_stars)
	user_to_food = predictBusiness.userToFood()
	food_to_business = predictBusiness.foodToBusiness(user_to_food)																																																		
	full_foods = predictBusiness.businessToFoods(food_to_business)
	user_neighbors = predictBusiness.foodsToUsers(full_foods)
	print(len(user_neighbors))							

