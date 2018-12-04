import pickle
from compute_similarity import SimilarityMeasure
from food_recommendation import FoodRecommender
from final_step import FindBusiness
class FlowHandler():
    def __init__(self):
        try:
            self.top_k = 5

            # Load all mappings

            self.user_id_to_name = pickle.load(open("util_data/sampled_user_id_to_name.pkl","rb"))
            self.user_name_to_id = pickle.load(open("util_data/sampled_user_name_to_id.pkl","rb"))
            self.business_id_to_name = pickle.load(open("util_data/sampled_business_id_to_name.pkl","rb"))
            self.business_name_to_id = pickle.load(open("util_data/sampled_business_name_to_id.pkl","rb"))
            #self.user_to_neighbors = pickle.load(open("util_data/user_neighbors.pkl","rb"))

            # Inialitalize Similarity Measure object to calculate cosine similarity

            self.similarity_obj = SimilarityMeasure(k=self.top_k)

            # Initialize FoodRecommender object used to get top rated food for users

            self.food_recommender = FoodRecommender(self.similarity_obj, k=self.top_k)

            # Initialize HotelRecommender object user to get hotel recommentdations

            business_to_food = pickle.load(open("util_data/sampled_business_to_food_mapping.pkl", "rb"))
            food_to_business = pickle.load(open("util_data/sampled_food_to_business_mapping.pkl", "rb"))
            self.hotel_recommender = FindBusiness(business_to_food, food_to_business)

        except Exception as e:
            raise Exception("Error in init FlowHandler:"+str(e))

    def exists_user(self, user_name):
        try:
            return user_name in self.user_name_to_id
        except Exception as e:
            raise Exception("Error in exists_user:"+str(e))

    def get_all_users(self):
        try:
            # Done - get user_to_id pickle

            users = list(self.user_name_to_id.keys())

            return users
        except Exception as e:
            raise Exception("Exception in get_all_users:"+str(e))

    def get_similar_users(self, user_name):
        try:
            # Done - Fix user_to_neighbors pickle

            user_id = self.user_name_to_id[user_name]
            #similar_users = self.similarity_obj.cosine_similar_users(user_id, self.user_to_neighbors[user_id])
            similar_users = self.similarity_obj.cosine_similar_users(user_id, set(self.user_id_to_name.keys()))

            similar_users = [self.user_id_to_name[similar_user_id[0]] for similar_user_id in similar_users]

            return similar_users
        except Exception as e:
            raise Exception("Exception in get_similar_useers:"+str(e))

    def get_food_recommendation(self, user1_name, user2_name):
        try:
            user1_id = self.user_name_to_id[user1_name]
            user2_id = self.user_name_to_id[user2_name]

            recommended_food = self.food_recommender.get_top_rated_food(user1_id, user2_id)

            return recommended_food
        except Exception as e:
            raise Exception("Exception in get_food_recommendation:"+str(e))

    def get_hotel_recommendation(self, food_name):
        try:
            # Get inputs from arjun

            recommended_hotel = self.hotel_recommender.suggestBusiness([food_name], self.top_k)
            recommended_hotel = [self.business_id_to_name[hotel] for hotel in recommended_hotel]

            return recommended_hotel
        except Exception as e:
            raise Exception("Exception in get_hotel_recommendation:"+str(e))




if __name__=="__main__":
    f = FlowHandler()
    print(list(f.user_name_to_id.keys())[10])
    print("-------------------")
    logged_in_user = input("Enter your name: ")
    while not f.exists_user(logged_in_user):
        print("User ID not found!!")
        logged_in_user = input("Please enter your name: ")
    print("-------------------")

    print("-------------------")
    choosen_user = input("We recommend these users to go out with: (please pick one)\n"+str(f.get_similar_users(
                                                                                logged_in_user))+"\n:")
    print("-------------------")

    print("-------------------")
    choosen_food = input("We recommend the following food for you and "+str(choosen_user)+": (please pick one)\n"+
                         str(f.get_food_recommendation(logged_in_user, choosen_user))+"\n:")
    print("-------------------")

    print("-------------------")
    print("We recommend these hotels based on both of you preference")
    print(f.get_hotel_recommendation(choosen_food))
    print("-------------------")



