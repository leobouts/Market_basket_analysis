import pandas as pd
import itertools


# computes the frequency of one or more items. (used in the apriori function)

def frequency_ap(items, user_baskets):

    times_found = [0 for basket in user_baskets if all(x in basket for x in items)]

    return len(times_found)/len(user_baskets)


# computes the frequency of one or more items. (used in the association_rules_creation function)
def frequency(items, user_baskets):

    count = 0

    out = [item for t in items for item in t]
    out = set(out)

    for basket in user_baskets:

        basket_set = set(basket)

        if out.intersection(basket_set) == out:
            count += 1

    return count/len(user_baskets)


def create_movie_baskets(movies_basket, min_score):

    ratings_csv = pd.read_csv('ratings_100users.csv')

    user_baskets = []

    # get the last value of the UserId column
    # that will be how many users exist in the df because the file is sorted
    mapped_ids = []

    for row in ratings_csv.iterrows():

        movie_id = row[1].values[1]
        assigned_id_of_movie = movies_basket.loc[movies_basket['movieId'] == movie_id, 'index'].iloc[0]

        mapped_ids.append(assigned_id_of_movie)

    # create an index for mapping every basket item to the movies
    ratings_csv['index'] = mapped_ids

    no_of_users = ratings_csv.userId.iloc[-1]

    # get each data for every user
    for user in range(no_of_users):

        # +1 to skip the headers
        user_dataframe = ratings_csv[ratings_csv.userId == user+1]
        # keep only min_score and higher movies
        user_dataframe = user_dataframe[user_dataframe.rating >= float(min_score)]

        movies_of_user = user_dataframe['index'].tolist()

        user_baskets.append(movies_of_user)

    return user_baskets


def read_movies():

    movies_csv = pd.read_csv('movies.csv')

    # create an index for mapping every basket item to an integer
    movies_csv['index'] = movies_csv.index

    return movies_csv


def subsets(arr):
    """ Note this only returns non empty subsets of arr"""
    return itertools.chain(*[itertools.combinations(arr, i + 1) for i, a in enumerate(arr)])


def k_subset(arr, k):
    s_arr = sorted(arr)
    return set([frozenset(i) for i in itertools.combinations(subsets(arr), k)
               if sorted(itertools.chain(*i)) == s_arr])

