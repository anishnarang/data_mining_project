from sklearn.metrics.pairwise import cosine_similarity
import random

class SimilarityMeasure():
    def __init__(self,k=5):
        try:
            self.user_profile = self.load_user_profile()
            self.k = k
        except Exception as e:
            raise Exception("Exception in init SimilarityMeasure class:"+str(e))

    def load_user_profile(self):
        try:
            profile_file = "util_data/sampled_user_food_profile.csv"
            file = open(profile_file, "r")
            file_content = list(file)
            file_content = dict([(line.strip().split(",")[0],line.strip().split(",")[1:]) for line in file_content[1:]])

            return file_content
        except Exception as e:
            raise Exception("Exception in loader_user_profile:"+str(e))

    def cosine_similar_users(self, user, neighbors):
        try:
            similar_users = neighbors

            #similar_users = random.sample(similar_users, 5000)

            # compute score for similar_users

            similar_users = [(other_user,cosine_similarity([list(map(float,self.user_profile[user]))], [
                        list(map(float,self.user_profile[other_user]))])[0][0]) for other_user in similar_users]

            similar_users = sorted(similar_users, key=lambda x:x[1], reverse=True)

            similar_users = similar_users[:self.k]

            return similar_users
        except Exception as e:
            raise Exception("Error in cosine_similar_users:"+str(e))