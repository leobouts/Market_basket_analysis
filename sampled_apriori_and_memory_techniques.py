from sampled_apriori import *
from memory_loading import *
import threading
import time
import sys


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rCrunching the data ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r...     ')
    sys.stdout.write('\rDone!     ')
    print("")


def options():

    print("(t): Compute triangular matrix and save to file")
    print("(h): Compute hash table and save to file")
    print("(a,c,n): Run the apriori-stream and display every change in the stream, where n is the reservoir size e.g. 50")
    print("(a,s,n): Run the apriori-stream and display the final results with a second pass, where n is the reservoir size e.g. 50")
    print("(e): Exit")


print(format("*", "*^25s"))
print("* Second script started *")
print(format("*", "*^25s"))
print("")


global done
done = False

t = threading.Thread(target=animate)
t.start()

# load the data

movies_basket = read_movies()
user_baskets = create_movie_baskets(movies_basket, 1)


done = True

print("")
time.sleep(2)

options()

option = input("Please enter an option:")

option_splited = option.split(",")


while option_splited[0].lower() != 'e':

    if option_splited[0].lower() not in ['t', 'h', 'a', 'e']:
        option = input("please try again with a valid option:")
        option_splited = option.split(",")
        continue

    if option_splited[0].lower() == 't':
        triangular_matrix_of_pairs_counters(user_baskets, movies_basket)

    if option_splited[0].lower() == 'h':
        hashed_counters_of_pairs(user_baskets)

    if option_splited[0].lower() == 'a':

        try:

            if option_splited[1].lower() not in ['c', 's']:
                print("Second argument wrong.")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

            if option_splited[1].lower() == 'c':
                try:
                    sampling_size = int(option_splited[2])
                    sampled_apriori(sampling_size, user_baskets, movies_basket, False)
                except ValueError:
                    print("This is not a number. Try again")
                    option = input("please try again with a valid option:")
                    option_splited = option.split(",")
                    continue
            else:
                try:
                    sampling_size = int(option_splited[2])
                    sampled_apriori(sampling_size, user_baskets, movies_basket, True)
                except ValueError:
                    print("This is not a number. Try again")
                    option = input("please try again with a valid option:")
                    option_splited = option.split(",")
                    continue

        except IndexError:
            print("Second argument missing.")
            option = input("Please try again with a valid option:")
            option_splited = option.split(",")
            continue

    time.sleep(0.8)
    print(format("-", "-^20s"))
    print("| Action completed |")
    print(format("-", "-^20s"))

    option = input("Choose another option to continue:")
    option_splited = option.split(",")
