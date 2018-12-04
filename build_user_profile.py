import pickle

given_ratings = open("util_data/train_sampled.csv","r")
given_ratings = list(given_ratings)
given_ratings = [line.strip().split(",") for line in given_ratings]

predicted_ratings = open("util_data/cf_result_matrix.txt","r")
predicted_ratings = list(predicted_ratings)
predicted_ratings = [line.strip().split(",") for line in predicted_ratings]

over_all_ratings = given_ratings + predicted_ratings

print("Total count:"+str(len(over_all_ratings)))

user_profile = {}
users_sampled = set()
foods_sampled = set()

for each_entry in over_all_ratings:
    user, food, rating = each_entry[0], each_entry[1], float(each_entry[2])
    user = user.strip()
    food = food.strip()

    users_sampled.add(user)
    foods_sampled.add(food)

    if user not in user_profile:
        user_profile[user] = {}

    user_profile[user][food] = rating

print("Sampled Users:"+str(len(users_sampled)))
print("Sampled Foods:"+str(len(foods_sampled)))

# Store csv user_profile

food_to_index = dict([(food,index) for index, food in enumerate(list(foods_sampled))])

with open("util_data/sampled_user_food_profile.csv","w+") as profile_file:
    profile_file.write("Users,"+(",".join(list(food_to_index.keys())))+"\n")
    for user in user_profile:
        vector = [-1] * len(food_to_index)

        for food in food_to_index:
            vector[food_to_index[food]] = user_profile[user][food]

        vector = [str(each) for each in vector]

        profile_file.write(str(user)+","+(",".join(vector))+"\n")

# Store sampled_users

pickle.dump(users_sampled, open("util_data/sampled_users.pkl","wb"))

# Store sampled foods

pickle.dump(foods_sampled, open("util_data/sampled_foods.pkl","wb"))





