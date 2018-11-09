import pickle

business_to_category = pickle.load(open("business_to_category.pkl", "rb"))

for bus in business_to_category:
    business_to_category[bus] = set([i.lower() for i in business_to_category[bus]])


categories = {}

with open("cusine_categories.txt","r") as file:
    for line in file:
        cat, count = line.strip().split(",")
        categories[cat] = int(count)

business_frequenc_of_category = {}

for cat in categories:
    business_frequenc_of_category[cat] = 0
    for bus in business_to_category:
        if cat in business_to_category[bus]:
            business_frequenc_of_category[cat] += 1

with open("category_in_business.txt", "w+") as file:
    for cat,val in sorted(business_frequenc_of_category.items(), key=lambda x: x[1], reverse=True):
        file.write(str(cat) + "=" + str(val) + "\n")

