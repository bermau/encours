#!/bin/env python3
# file : graph_encours.py

"""Un module pour tracer des graphes sur les données des encours.

Il faut réaliser un tableau de contingence (nombre de dossiers par jour).
"""


def get_array_frequency(word_lst):
    """retourne un dictionnaire de fréquence"""
    pass
    dict_of_words = {}
    for word in word_lst:
        if word in dict_of_words:
            dict_of_words[word] = dict_of_words[word] + 1
        else:
            dict_of_words[word] = 1
    return dict_of_words


data = ['2011-03-03', '2012-06-12', '2012-07-16', '2012-07-18',
'2012-07-19', '2012-11-04', '2013-02-23', '2013-03-16', '2013-04-08',
'2013-04-26', '2013-04-29', '2013-04-29', '2013-05-01', '2013-05-03',
'2013-05-03', '2013-05-03', '2013-05-06', '2013-05-06', '2013-05-06',
'2013-05-07', '2013-05-07', '2013-05-10', '2013-05-14', '2013-05-17',
'2013-05-18']

a = get_array_frequency(data)
sorted_data = sorted(a.items())
print(data)
print(a)
print(sorted_data)



import matplotlib.pyplot as plt
# import numpy as np

x = [ sorted_data[i][0] for i in range(len(sorted_data)) ]

y = [ sorted_data[i][1] for i in range(len(sorted_data)) ]
plt.plot(x, y)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()
