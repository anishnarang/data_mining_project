class FoodRecommender():
    def __init__(self, similarity_measure_object, k=5):
        try:
            self.k = k
            self.similarity_measure_object = similarity_measure_object
            self.ordered_food_names = self.get_ordered_food_names()
        except Exception as e:
            raise Exception("Exception in init of FoodRecommender class:"+str(e))

    def get_top_rated_food(self, user_id_1, user_id_2):
        try:
            user_1_food_details = list(self.get_users_food_rating(user_id_1).items())
            user_2_food_details = list(self.get_users_food_rating(user_id_2).items())

            #hash_val = hash(user_id_1 + user_id_2) % len(user_2_food_details)

            zipped_ratings = []

            for user1_details, user2_details in zip(user_1_food_details, user_2_food_details):
                zipped_ratings.append((user1_details[0],user1_details[1]+user2_details[1]))

            zipped_ratings = sorted(zipped_ratings, key=lambda x: x[1], reverse=True)
            top_food_names = zipped_ratings[:self.k]
            #top_food_names = zipped_ratings[hash_val:hash_val+(self.k/2)]
            top_food_names = [food[0] for food in top_food_names]

            return top_food_names


        except Exception as e:
            raise Exception("Exception in get_top_rated_food:"+str(e))

    def get_users_food_rating(self, user_id):
        try:
            profile = list(map(float,self.similarity_measure_object.user_profile[user_id]))

            result = dict(zip(self.ordered_food_names, profile))
            return result
        except Exception as e:
            raise Exception("Exception in get_users_food_rating:"+str(e))

    def get_ordered_food_names(self):
        try:
            file_name = "util_data/sampled_user_food_profile.csv"

            file_content = open(file_name, "r")
            file_content = list(file_content)

            heading = file_content[0].strip().split(",")[1:]

            return heading
        except Exception as e:
            raise Exception("Exception in get_ordered_food_names:"+str(e))