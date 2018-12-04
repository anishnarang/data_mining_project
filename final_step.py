import math
import time
import sys
from operator import itemgetter
from collections import defaultdict
import pickle

class FindBusiness:

	def __init__(self, business_to_food, food_to_business):
		self.business_to_food = business_to_food
		self.food_to_business = food_to_business

	def suggestBusiness(self, foods, k):
		final_business = defaultdict()
		for food in foods:
			candidate_business = defaultdict()
			businesses = self.food_to_business[food]
			for business in businesses:
				rating = self.business_to_food[business][food]
				candidate_business[business] = rating
			final_business[food] = sorted(candidate_business, key = candidate_business.get, reverse=True)[:k]
		return final_business[foods[0]]

if __name__ == '__main__':

	foods = ["cheese", "bread", "chicken", "potato", "chocolate"]
	business_to_food = pickle.load(open( "business_to_food_mapping.pkl", "rb" ))
	food_to_business = pickle.load(open( "food_to_business_mapping.pkl", "rb" ))
	findBusiness = FindBusiness(business_to_food, food_to_business)
	businesses = findBusiness.suggestBusiness('8HMN1jABE5y7my-B8m62Cw', '-X6NbB699wt1Z2atOPgmBw', foods)