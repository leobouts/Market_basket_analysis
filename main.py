import threading
import time
import sys
from assoc_rules import  *
from result import *


def main():

    print(format("*", "*^23s"))
    print("* Main script started *")
    print(format("*", "*^23s"))
    print("")

    itemsets = {}

    while True:
        minimum_confidence = input("Please enter the minimum confidence:")
        try:
            minimum_confidence = float(minimum_confidence)
            if float(minimum_confidence) <= 0 or float(minimum_confidence) >= 1:
                print("Confidence ranges from (0,1). Try again")
                continue
            break
        except ValueError:
            print("This is not a number. Try again")

    while True:
        minimum_lift = input("Please enter the minimum lift:")
        try:
            minimum_lift = int(minimum_lift)
            break
        except ValueError:
            try:
                minimum_lift = float(minimum_lift)
                break
            except ValueError:
                print("This is not a number. Try again")

    while True:
        maximum_lift = input("Please enter the maximum lift:")
        try:
            maximum_lift = int(maximum_lift)
            break
        except ValueError:
            try:
                maximum_lift = float(maximum_lift)
                break
            except ValueError:
                print("This is not a number. Try again")

    while True:
        minimum_length = input("Please enter the minimum length:")
        try:
            minimum_length = int(minimum_length)
            break
        except ValueError:
            print("This is not a number. Try again")

    while True:
        print("Minimum score options: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5")
        min_score = input("Please enter the minimum movie score:")

        if str(min_score) not in ['1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']:
            min_score = input("Please try again with a valid option:")
            continue

        break

    # use a terminal animation while loading the data

    global done
    done = False

    t = threading.Thread(target=animate)
    t.start()

    # load the data

    movies_basket = read_movies()

    user_baskets = create_movie_baskets(movies_basket, min_score)

    initial_item_movies = [[i] for i in range(len(movies_basket))]

    my_apriori(user_baskets, initial_item_movies, itemsets)

    items = [list(item) for item in itemsets.keys()]

    # write itemset in a file
    with open('itemeset_generated_from_apriori.txt', 'w+') as f:
        for item in items:
            f.write("%s\n" % item)

    # returns a pandas dataframe with association rules, last arguments are, min_confidence, min_lift, max_lift
    rules = association_rules_creation(items, user_baskets, minimum_confidence, minimum_lift, maximum_lift)

    rules_list = []

    # ensure the rules have a minimum length
    for index, row in rules.iterrows():

        itemset = row['rule']

        item_splitted = itemset.split("->")

        right_side = item_splitted[1]
        # remove [(
        right_side = right_side[2:]
        # remove ])
        right_side = right_side[:-2]

        # split the items
        right_side_items = [item for item in right_side.split(",")]

        # replace whitespaces
        right_side_items = [item.replace(' ', '') for item in right_side_items]

        right_side_items = [int(i) for i in right_side_items if i]

        left_side = item_splitted[0]
        # remove [(
        left_side = left_side[2:]
        # remove ])
        left_side = left_side[:-2]

        # split the items
        left_side_items = [item for item in left_side.split(",")]

        # replace whitespaces
        left_side_items = [item.replace(' ', '') for item in left_side_items]

        left_side_items = [int(i) for i in left_side_items if i]

        if len(right_side_items)+len(left_side_items) >= minimum_length:
            rules_list.append(row)

    rules = pd.DataFrame(rules_list)

    rules.to_csv(r'association_rules.csv')

    done = True
    print("")
    time.sleep(2)

    option = input("Please enter an option:")

    option_splited = option.split(",")

    while option_splited[0].lower() != 'e':

        if option_splited[0].lower() not in ['a', 'b', 'c', 'h', 'm', 'r', 's', 'v']:
            option = input("please try again with a valid option:")
            option_splited = option.split(",")
            continue

        if option_splited[0].lower() == 'b':

            if option_splited[1].lower() not in ['i', 'h', 'c']:
                print("Second argument wrong. Available parameters: 'i,h,c' example: b,i,movie ids")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

            ids = option_splited[2:]

            for movie in ids:

                try:
                    int(movie)

                except ValueError:
                    print("One of the movie ids is not an integer.")
                    option = input("please try again with a valid option:")
                    option_splited = option.split(",")
                    continue

        if option_splited[0].lower() == 'h':

            if option_splited[1].lower() not in ['l', 'c']:
                print("Second argument wrong. Available parameters: 'c,l' example: h,c")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

        if option_splited[0].lower() == 's':

            if option_splited[1].lower() not in ['c', 'l']:
                print("Second argument wrong. Available parameters: 'c,l' example: s,c")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

        if option_splited[0].lower() == 'r':

            try:
                int(option_splited[1])

            except ValueError:
                print("The rule id is not an integer.")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

        if option_splited[0].lower() == 'm':

            try:
                int(option_splited[1])

            except ValueError:
                print("The movie id is not an integer.")
                option = input("please try again with a valid option:")
                option_splited = option.split(",")
                continue

        user_option(option_splited, rules, movies_basket, 3, 6)

        print(format("-", "-^35s"))
        print("| Selected results were presented |")
        print(format("-", "-^35s"))

        option = input("Choose another option to continue:")
        option_splited = option.split(",")


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
    print_console_options()


if __name__ == "__main__":
    main()
