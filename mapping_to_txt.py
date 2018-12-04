import pickle

mapping = pickle.load(open("util_data/food_to_business_mapping.pkl","rb"))


with open("util_data/food_to_business_mapping.txt","w+") as mapping_file:
    for business in mapping:
        for food in mapping[business]:
            mapping_file.write(str(business)+","+str(food)+","+str(mapping[business][food])+"\n")

     
