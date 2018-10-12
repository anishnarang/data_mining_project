import ijson

def businessToCategories(f_categories, f_business):
	business_category = {}
	categories = []
	for i in f_categories.readlines():
		i = i.strip().split(',')
		categories.append(i[0])

	for i in f_business.readlines():
		i = i.strip().split(',')
		catgories_id = i[1].strip().lower()
		business_id = i[2]
		if catgories_id in categories:
			if business_id not in business_category:
				business_category[business_id] = []
			business_category[business_id].append(catgories_id)
	return business_category

def userProfiles(business_category, f_review):
	user_restaurants = {}
	for i in f_review:
		i = eval(i)
		review_id = i['review_id']
		business_id = i['business_id']
		user_id = i['user_id']
		rating = i['stars']
		if business_id in business_category:
			if user_id not in user_restaurants:		
				user_restaurants[user_id] = []
			if business_id not in user_restaurants[user_id]:
				if business_category[business_id]:
					for category in business_category[business_id]:
						user_restaurants[user_id].append((business_id, category, rating))
				else:
					user_restaurants[user_id].append((business_id, "General", rating))

	return user_restaurants

if __name__ == '__main__':
	f_review = open("yelp_dataset/yelp_academic_dataset_review.json","r")	
	f_categories = open("cuisine_categories_mapping.txt", "r")
	f_business = open('categories_to_business.csv', 'r')
	business_category_mapping = businessToCategories(f_categories, f_business)
	user_profiles = userProfiles(business_category_mapping, f_review)

