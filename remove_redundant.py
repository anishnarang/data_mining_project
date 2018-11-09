data = {}
with open("util_data/user_to_cuicine_test.csv") as input_file:
    for row in input_file:
        user, category, rating = row.strip().split(",")
        rating = int(rating)

        if user in data:
            if category in data[user]:
                data[user][category] = (data[user][category][0]+rating, data[user][category][1]+1)
            else:
                data[user][category] = (rating, 1)
        else:
            data[user] = {}
            data[user][category] = (rating, 1)

    for user in data.keys():
        for category in data[user].keys():
            data[user][category] = float(data[user][category][0])/data[user][category][1]


with open("util_data/user_to_cuisine_unique_test.csv","w+") as output_file:

    output_file.write("User,Category,Rating\n")

    for user in data.keys():
        for category in data[user].keys():
            output_file.write(str(user) + "," + str(category) + "," + str(data[user][category]) + "\n")