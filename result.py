from apriori import *
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def print_console_options():

    options = {"(a) List ALL discovered rules": "[format: a]",
               "(b) List all rules containing a BAG of movies:": "[format:",
               "in their <ITEMSET|HYPOTHESIS|CONCLUSION>": "b,<i,h,c>,<comma-sep. movie IDs>]",
               "(c) COMPARE rules with <CONFIDENCE,LIFT>": "[format: c]",
               "(h) Print the HISTOGRAM of <CONFIDENCE|LIFT >": "[format: h,<c,l >]",
               "(m) Show details of a MOVIE": "[format: m,<movie ID>]",
               "(r) Show a particular RULE": "[format: r,<rule ID>]",
               "(s) SORT rules by increasing <CONFIDENCE|LIFT >": "[format: s,<c,l >]",
               "(v) Visualise association rules of top 10": "[format: v]",
               "(e) EXIT": "[format: e]"}

    print(format("#", "#^90s"))

    for o in options:
        print("{option:48}: {format:40}".format(option=o, format=options[o]))

    print(format("#", "#^90s"))


def draw_graph(rules):

    G = nx.DiGraph()

    color_map = []
    final_node_sizes = []

    color_iter = 0
    edge_colors_iter = ["#4e79a9", "#59a14f", "#9c755f", "#f28e2b", "#edc948", "#bab0ac", "#e15759", "#b07aa1",
                        "#76b7b2", "#ff9da7"]

    # bigger confidence, bigger node size

    node_sizes = {}

    for index, row in rules.iterrows():

        color_of_rule = edge_colors_iter[color_iter]

        rule = row['rule']
        rule_id = row['rule ID']

        G.add_nodes_from(["R"+str(rule_id)])

        confidence_of_rule = row['confidence']

        node_sizes.update({"R"+str(rule_id): float(confidence_of_rule)})

        rule_splitted = rule.split("->")

        left_side = rule_splitted[0]
        right_side = rule_splitted[1]

        # remove [(
        left_side = left_side[2:]
        # remove ])
        left_side = left_side[:-2]

        # remove [(
        right_side = right_side[2:]
        # remove ])
        right_side = right_side[:-2]

        # split the items
        left_side_items = [item for item in left_side.split(",")]

        # replace whitespaces
        left_side_items = [item.replace(' ', '') for item in left_side_items]

        left_side_items = [int(i) for i in left_side_items if i]

        # split the items
        right_side_items = [item for item in right_side.split(",")]

        # replace whitespaces
        right_side_items = [item.replace(' ', '') for item in right_side_items]

        right_side_items = [int(i) for i in right_side_items if i]

        for item in left_side_items:
            G.add_edge(str(item), "R"+str(rule_id), color=color_of_rule)

        for item in right_side_items:
            G.add_edge("R"+str(rule_id), str(item), color=color_of_rule)

        color_iter += 1

    for node in G:

        if str(node).startswith("R"):
            color_map.append('#f9dc4c')

            # default node size is 300, multiply with a constant to amplify the confidence

            conf = node_sizes[str(node)]

            if conf > 0.75:
                conf = conf * 1300
                final_node_sizes.append(300+conf)

            elif conf > 0.5:

                conf = conf * 400
                final_node_sizes.append(700 + conf)
            else:
                final_node_sizes.append(700 + conf)
        else:
            color_map.append('#339e34')
            final_node_sizes.append(700)

    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]

    nx.draw_circular(G, edge_color=colors, node_size=final_node_sizes, node_color=color_map, with_labels=True)
    plt.show()


def user_option(option, rules, movies_basket, min_lift, max_lift):

    try:

        first_arg = option[0]
        second_arg = option[1]
        movie_ids = option[2:]
        movie_ids = [int(movie) for movie in movie_ids]

    except IndexError:
        pass

    if first_arg == 'a':

        print(rules)

    elif first_arg == 'b':

        rows_list = []

        if second_arg == 'i':

            for index, row in rules.iterrows():
                itemset = row['itemset']

                if set(movie_ids).issubset(itemset):
                    rows_list.append(row)

        elif second_arg == 'h':

            for index, row in rules.iterrows():
                itemset = row['rule']

                item_splitted = itemset.split("->")

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

                if set(movie_ids).issubset(left_side_items):
                    rows_list.append(row)

        else:

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

                if set(movie_ids).issubset(right_side_items):
                    rows_list.append(row)

        df = pd.DataFrame(rows_list)
        print(df)

    elif first_arg == 'c':

        d = {'lift': rules['lift'], 'confidence': rules['confidence']}

        df = pd.DataFrame(d)

        df.plot(x='lift', y='confidence', style='o')
        plt.title('Confidence vs Lift')
        plt.legend('', frameon=False)
        plt.xticks(np.arange(min_lift, max_lift+1, 1.0))
        plt.ylabel('Confidence')
        plt.show()

    elif first_arg == 'h':

        if second_arg == 'c':
            rules.hist(column='confidence')
            plt.title('Histogram of confidence')
            plt.legend('', frameon=False)
            plt.show()

        elif second_arg == 'l':
            rules.hist(column='lift')
            plt.title('Histogram of Lift')
            plt.legend('', frameon=False)
            plt.show()

    elif first_arg == 'm':

        movie = second_arg
        print(movies_basket[movies_basket['index'] == int(movie)])

    elif first_arg == 'r':

        rule = second_arg
        print(rules[rules['rule ID'] == int(rule)])

    elif first_arg == 's':

        if second_arg == 'c':

            final_df = rules.sort_values(by=['confidence'], ascending=True)
            print(final_df)

        elif second_arg == 'l':

            final_df = rules.sort_values(by=['lift'], ascending=True)
            print(final_df)

    elif first_arg == 'v':

        df = rules.sort_values(by=['lift'], ascending=False)
        final_df = df.head(10)

        draw_graph(final_df)
