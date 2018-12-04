import pickle
import random

sample_size = 10000

user_to_food = pickle.load(open("util_data/user_to_food_mapping.pkl", "rb"))
user_to_food = list(user_to_food.items())
user_to_food = random.sample(user_to_food, sample_size)
user_to_food = dict(user_to_food)

# Get all food from user_profile
'''
user_profile = open("util_data/user_food_profile.csv", "r")
user_profile = list(user_profile)[0]
all_food = user_profile.strip().split(",")[1:]
'''
# Get all food from user_to_food selected

all_food = set()

for user in user_to_food:
    for food in user_to_food[user]:
        all_food.add(food)

print("Sampled users hav food:"+str(len(all_food)))

train_count = 0
with open("util_data/train_sampled.csv", "w+") as train_file:
    for user in user_to_food:
        for food in user_to_food[user]:
            if food in all_food:
                new_rat = ((user_to_food[user][food] - (-5)) / ((5) - (-5))) * (5 - 0) + 0
                train_file.write(str(user) + "," + str(food) + "," + str(new_rat) + "\n")
                train_count += 1

test_count = 0
with open("util_data/test_sampled.csv", "w+") as test_file:
    for user in user_to_food:
        for food in all_food:
            if food not in user_to_food[user]:
                test_file.write(str(user) + "," + str(food) + "," + str(2.5) + "\n")
                test_count += 1

print("Training count: " +str(train_count))
print("Test Count: "+str(test_count))
print("Totally :"+str(train_count + test_count))
print("Expected:"+str(len(all_food) * sample_size))
