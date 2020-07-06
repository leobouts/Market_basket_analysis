import itertools
import threading
import pickle
import time
import sys


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rComputing the matrix ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r...     ')
    sys.stdout.write('\rDone!     ')
    print("")


def triangular_matrix_of_pairs_counters(user_baskets, movies_basket):

    global done
    done = False

    t = threading.Thread(target=animate)
    t.start()

    no_of_movies = len(movies_basket)

    # space needed 2*n^2

    triangular_matrix = [0]*(2*no_of_movies ** 2)

    for basket in user_baskets:

        list_of_pairs = itertools.combinations(basket, 2)

        for pair in list_of_pairs:

            i = pair[0]
            j = pair[1]

            if i < j:

                # store the pair with i < j as a lower triangular matrix
                # with a dimension array

                k = (i-1) * (no_of_movies - i / 2) + j - 1

                # float to int
                k = int(k)

                # update the counter
                triangular_matrix[k] += 1

    done = True

    with open('triangular', 'wb') as fp:
        pickle.dump(triangular_matrix, fp)

    return triangular_matrix


def hashed_counters_of_pairs(user_baskets):

    global done
    done = False

    t = threading.Thread(target=animate)
    t.start()

    hash_table = {}

    for basket in user_baskets:

        # pairs of three
        list_of_pairs = itertools.combinations(basket, 2)

        for pair in list_of_pairs:

            # if exists in the hash table counter + 1, else create the entry
            # this way we dont need to store zeros, opposed to the triangular matrix

            try:

                hash_table.update({pair: hash_table[pair] + 1})

            except KeyError:

                hash_table.update({pair: 1})

    done = True

    # write to file
    with open('hash_table', 'wb') as fp:
        pickle.dump(hash_table, fp)

    return hash_table
