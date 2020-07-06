from helpers import *
import itertools


def my_apriori(user_baskets, movies_basket, apriori_hash_table):

    no_of_movies = len(movies_basket)

    # 1% as suggested in the textbook
    min_frequency = 0.1
    min_length = 2

    number_of_current_iteration = 1

    while True:

        # first pass, count items

        # keep track of counters
        counter_of_items = [0] * no_of_movies

        for movie in movies_basket:

            for basket in user_baskets:

                # sets are used to count all singletons, pairs of two, three etc

                movie_set = set(movie)
                basket_set = set(basket)

                items_intersecting = movie_set.intersection(basket_set)

                # condition is true when all items of a pair of two, three etc are inside a basket
                if items_intersecting == movie_set:

                    index = movies_basket.index(movie)

                    counter_of_items[index] += 1

        # intermediate between passes

        # items that stay are those that their frequency are above a minimum
        # threshold frequency that we set

        # create a list with the new ordering of 1->m
        # if common item then it has a number 1<number<m else it has the number 0

        # print(counter_of_items)

        for item in counter_of_items:

            if item < min_length:

                counter_of_items[item] = 0

        # second pass

        items_to_pair = []

        # use a counter, .index() can return a list of items with the same occurence
        index_counter = 0

        for item in counter_of_items:

            index_counter += 1

            if item > 0:

                try:

                    index = counter_of_items.index(index_counter)

                    pair = movies_basket[index]

                    # compute frequency for every singleton or pair of two, three etc

                    if frequency_ap(pair, user_baskets) > min_frequency:
                        items_to_pair.append(pair)

                except ValueError:
                    pass

        # flatten the list of pairs that were selected so we can do a pair of n+1
        unique_items_to_pair = set(x for l in items_to_pair for x in l)

        # pairs, at first singletons and then dup, trip etc
        list_of_pairs = list(itertools.combinations(unique_items_to_pair, number_of_current_iteration))

        # Check the pairs, if we didnt found any we are done
        if len(list_of_pairs) == 0:
            # print("pass:", number_of_current_iteration)
            # print("All common pairs explored")
            # print("=========================")
            break

        # create or update the hash table that reports all common pairs and their findings
        for pair in list_of_pairs:
            current_pair = apriori_hash_table.get(pair)

            if current_pair:
                apriori_hash_table.update({pair: apriori_hash_table[pair] + 1})
            else:
                apriori_hash_table.update({pair: 1})

        # print("pass:", number_of_current_iteration)
        # print("common pairs:", list_of_pairs)
        # print("===================")

        number_of_current_iteration += 1
        movies_basket = list_of_pairs
