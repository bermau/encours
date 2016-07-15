#!/bin/env python3
# file : graph_encours.py

"""Un module pour tracer des graphes sur les données des encours.

Il faut réaliser un tableau de contingence (nombre de dossiers par jour).
"""
import matplotlib.pyplot as plt
import datetime
import doctest

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


def str2date_for_dt(str_date):
    """from a string, return a datetime.date
    >>> str2date_for_dt('2013-02-23')
    datetime.date(2013, 2, 23)
    """
    return datetime.date(int(str_date[0:4]),
                                    int(str_date[5:7]),
                                    int(str_date[8:10]))


def graphe(data):
    """Affiche un graphe de fréquences pour une liste de dates"""
    pass

    a = get_array_frequency(data)
    sorted_array = sorted(a.items())

    x = [ str2date_for_dt(sorted_array[i][0]) for i in range(len(sorted_array)) ]
    y = [ sorted_array[i][1] for i in range(len(sorted_array)) ]

    # Graphe
    fig, ax = plt.subplots()

    ax.plot_date(x, y, '.')
    ax.autoscale_view()

    plt.xlabel('Temps')
    plt.ylabel('Nombre')
    plt.title('Nombre de dossiers encours pour un jour donné')
    plt.grid(True)

    # Gérer l'affichage automatique
    x_min, x_max, y_min, y_max = plt.axis()
    # print("y_min, y_max", (self.y_min, self.y_max))
    # print("y mix max des axes : ",(self.y_min_ax, self.y_max_ax))
    plt.axis([x_min-10, x_max+10, 0 , y_max + 1])          
    fig.autofmt_xdate()
    plt.savefig("test.png")
    plt.show()

def _test():
    "self-test routine"

    # load the doctest module, part of the std Python API
    import doctest
    # invoke the testmod function that will parse
    # the whole content of the file, looking for
    # docstrings and run all tests they contain
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
    data = ['2011-03-03', '2012-06-12', '2012-07-16', '2012-07-18',
'2012-07-19', '2012-11-04', '2013-02-23', '2013-03-16', '2013-04-08',
'2013-04-26', '2013-04-29', '2013-04-29', '2013-05-01', '2013-05-03',
'2013-05-03', '2013-05-03', '2013-05-06', '2013-05-06', '2013-05-06',
'2013-05-07', '2013-05-07', '2013-05-10', '2013-05-14', '2013-05-17',
'2013-05-18']
    graphe(data)
