from helpers import *
import random
import pickle


def sampled_apriori(sampling_number, user_baskets, movies_basket, second_passing):

    reservoir_array = [0] * sampling_number

    no_of_movies = len(movies_basket)

    min_frequency = 0.1

    iteration = 0

    commons = []

    # iterate one by one on the basket arrays to imitate the flow of a stream.
    for next_item in user_baskets:

        # fill the reservoir array with 'sampling_number' first items

        if iteration < sampling_number:
            reservoir_array[iteration] = next_item

        # 'sampling_number'+1 iteration to n
        else:
            position_to_be_replaced = random.randint(0, iteration)
            if position_to_be_replaced < sampling_number:

                reservoir_array[position_to_be_replaced] = next_item

                # sampling chose to replace a basket, redo an apriori first pass

                # keeps track of counters
                counter_of_items = [0] * no_of_movies

                # first pass

                for basket in reservoir_array:
                    for item in basket:

                        index = movies_basket[movies_basket['index'] == item].index
                        index = list(index)
                        counter_of_items[index[0]] += 1

                # intermediate between passes

                common_items = [counter_of_items.index(item) for item in counter_of_items
                                if (frequency_ap([item], reservoir_array)) > min_frequency]

                # create a list with the new ordering of 1->m
                # if common item then it has a numberL 1<number<m else it has the number 0

                estimated_common_items = [0] * no_of_movies

                for item in common_items:

                    index = counter_of_items[item]
                    estimated_common_items[index] = counter_of_items[item]

                # Note: if entry is zero item of this index is not common.
                commons = [i for i, e in enumerate(estimated_common_items) if e != 0]

                if not second_passing:

                    print("Sample changed...")
                    # for a only-common list just print the non zero indexes of this list.
                    print("Current common items:", commons)

        iteration += 1

    #####################
    # end of the stream #
    #####################

    # the user can add a mode to do a second passing at the end of the stream

    if second_passing:

        second_passing_items = []

        # create pairs for the second passing
        list_of_pairs = list(itertools.combinations(commons, 2))

        for pair in list_of_pairs:

            if frequency_ap(pair, reservoir_array) > min_frequency:
                second_passing_items.append(pair)
        print("-------------")
        print("stream ended")
        print("common pairs:")
        print(second_passing_items)

        # write to file
        with open('sampled_apriori', 'wb') as fp:
            pickle.dump(second_passing_items, fp)

        return second_passing_items
