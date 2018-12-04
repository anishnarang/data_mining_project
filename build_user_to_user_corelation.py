from pyspark import SparkContext
from pyspark import SparkConf
from sklearn.metrics.pairwise import cosine_similarity
import pickle


conf = (SparkConf().setAppName("Assignment3"))
conf = (conf
        .set('spark.executor.memory', '8G')
        .set('spark.driver.memory', '8G')
        .set('spark.driver.maxResultSize', '8G'))
sc = SparkContext(conf = conf)


profile_file = "util_data/sampled_user_food_profile.csv"
file = open(profile_file, "r")
file_content = list(file)
user_profile = [(line.strip().split(",")[0], [line.strip().split(",")[1:]]) for line in file_content[1:]]


main = []

for user1_index in range(len(user_profile)):
    for user2_index in range(user1_index+1,len(user_profile)):
        user1, user2 = user_profile[user1_index][0], user_profile[user2_index][0]
        user1_vec, user2_vec = user_profile[user1_index][1], user_profile[user2_index][1]

        main.append((user1,user2, user1_vec, user2_vec))

main = sc.parallelize(main, 50)
print(main.take(4))
exit(0)


def cos_similar(user):
    sim = [(user2,user_profile[user],user_profile[user2]) for user2 in user_profile if user != user2]
    sim = sc.parallelize(sim)
    sim = sim.map(lambda row: (row[0], cosine_similarity(row[1], row[2])[0][0])).collect()
    sim = sorted(sim, key=lambda x:x[1])
    return sim

user_similar = {}

i = 0
for user in user_profile:
    print(str(i)+"/"+str(len(user_profile)))


    '''
    sim = []
    for user2 in user_profile:
        if user != user2:
            sim.append((user2, cosine_similarity([user_profile[user]], [user_profile[user2]])))
    
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    '''
    user_similar[user] = cos_similar(user)

pickle.dump(user_similar, open("util_data/user_similar_data.pkl","wb"))