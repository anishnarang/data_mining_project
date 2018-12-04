import numpy as np
import matplotlib.pyplot as plt


food_freq = open("util_data/food_frequency.txt","r")
food_freq = list(food_freq)
food_freq = [line.strip().split(":") for line in food_freq]
food_freq = [(line[0],float(line[1])) for line in food_freq]
food_freq = food_freq[:10]
food_freq = dict(food_freq)


pos = np.arange(len(list(food_freq.keys())))
width = 1.0

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(food_freq.keys())

plt.bar(list(food_freq.keys()), list(food_freq.values()), width, color='g')
#
plt.show()