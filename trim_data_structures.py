import pickle

# Load Sampled Users

sampled_users = pickle.load(open("util_data/sampled_users.pkl","rb"))

# Load Sampled Food

sampled_foods = pickle.load(open("util_data/sampled_foods.pkl","rb"))

# Load old mappings

user_id_to_name = pickle.load(open("util_data/user_id_to_name_trimmed.pkl", "rb"))
business_id_to_name = pickle.load(open("util_data/business_id_to_name.pkl", "rb"))

# Retain only sampled ones

user_id_to_name = dict([(id,name) for id,name in user_id_to_name.items() if id in sampled_users])
user_name_to_id = dict([(b,a) for a,b in user_id_to_name.items()])

print("Length of user_id_to_name:"+str(len(user_id_to_name)))
print("Length of user_name_to_id:"+str(len(user_name_to_id)))

# Sampled business

food_to_business = pickle.load(open("util_data/food_to_business_mapping.pkl","rb"))
food_to_business = dict([(food, business)  for food,business in food_to_business.items() if food in sampled_foods])

print("Length of food_to_business:"+str(len(food_to_business)))

business_to_food = {}

for food, business_list in food_to_business.items():
    for business in business_list:
        if business not in business_to_food:
            business_to_food[business] = {}

        business_to_food[business][food] = food_to_business[food][business]

print("Length of business_to_food:"+str(len(business_to_food)))

sampled_business = set(business_to_food.keys())

print("List of sampled_business:"+str(len(sampled_business)))

# business_id

stamp = 0
h_set = set()
for id,name in business_id_to_name.items():
    if name in h_set:
        business_id_to_name[id] = business_id_to_name[id] + str(stamp)
        stamp += 1
    else:
        h_set.add(name)


business_id_to_name = dict([(id,name) for id,name in business_id_to_name.items() if id in sampled_business])
business_name_to_id = dict([(b,a) for a,b in business_id_to_name.items()])

print("Length of business_id_to_name:"+str(len(business_id_to_name)))
print("length of business_name_to_id:"+str(len(business_name_to_id)))

# User to food and food to user

user_to_food = pickle.load(open("util_data/user_to_food_mapping.pkl","rb"))
food_to_user = {}

user_to_food = dict([(user, food) for user, food in user_to_food.items() if user in sampled_users])

for user in user_to_food:
    current = user_to_food[user]

    new = dict([(food,rating) for food, rating in current.items() if food in sampled_foods])

    user_to_food[user] = new

for user in user_to_food:
    for food in user_to_food[user]:
        if food not in food_to_user:
            food_to_user[food] = {}

        food_to_user[food][user] = user_to_food[user][food]

print("Length of user_to_food:"+str(len(user_to_food)))
print("Length of food_to_user:"+str(len(food_to_user)))

# Store new sampled

pickle.dump(user_id_to_name,open("util_data/sampled_user_id_to_name.pkl","wb"))
pickle.dump(user_name_to_id,open("util_data/sampled_user_name_to_id.pkl","wb"))
pickle.dump(food_to_business,open("util_data/sampled_food_to_business_mapping.pkl","wb"))
pickle.dump(business_to_food,open("util_data/sampled_business_to_food_mapping.pkl","wb"))
pickle.dump(sampled_business,open("util_data/sampled_business.pkl","wb"))
pickle.dump(business_id_to_name,open("util_data/sampled_business_id_to_name.pkl","wb"))
pickle.dump(business_name_to_id,open("util_data/sampled_business_name_to_id.pkl","wb"))
pickle.dump(user_to_food,open("util_data/sampled_user_to_food_mapping.pkl","wb"))
pickle.dump(food_to_user,open("util_data/sampled_food_to_user_mapping.pkl","wb"))


# Generate text files

with open("util_data/sampled_user_to_food_mapping.txt","w+") as mapping_file:
    for user in user_to_food:
        for food in user_to_food[user]:
            mapping_file.write(str(user)+","+str(food)+","+str(user_to_food[user][food])+"\n")


with open("util_data/sampled_business_to_food_mapping.txt","w+") as mapping_file:
    for business in business_to_food:
        for food in business_to_food[business]:
            mapping_file.write(str(business)+","+str(food)+","+str(business_to_food[business][food])+"\n")


with open("util_data/sampled_food_to_business_mapping.txt","w+") as mapping_file:
    for food in food_to_business:
        for business in food_to_business[food]:
            mapping_file.write(str(food)+","+str(business)+","+str(food_to_business[food][business])+"\n")
