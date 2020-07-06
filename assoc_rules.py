from helpers import *
import pandas as pd


def association_rules_creation(itemset, user_baskets, min_confidence, min_lift, max_lift):

    rules_df = pd.DataFrame(columns=['rule', 'itemset',  'frequency', 'confidence', 'lift', 'rule ID'])
    id_counter = 0

    for item in itemset:

        if len(item) > 1:

            returned_set_of_rules = k_subset(item, 2)

            set_of_rules = [list(x) for x in returned_set_of_rules]

            for rule in set_of_rules:

                append_flag = False

                left_side = [rule[0]]
                right_side = [rule[1]]

                items_of_the_rule = left_side + right_side

                frequency_of_rule = frequency(items_of_the_rule, user_baskets)

                frequency_of_left = frequency(left_side, user_baskets)

                frequency_of_right = frequency(right_side, user_baskets)

                confidence_of_rule = frequency_of_rule / frequency_of_left

                lift_of_rule = confidence_of_rule / frequency_of_right

                # print(frequency_of_rule)
                # print(frequency_of_left)
                # print(frequency_of_right)
                # print(confidence_of_rule)
                # print(lift_of_rule)
                # print("--------------")

                if max_lift == -1 and min_lift == -1:

                    if confidence_of_rule > min_confidence:
                        append_flag = True

                if max_lift == -1:

                    if confidence_of_rule > min_confidence and lift_of_rule > min_lift:
                        append_flag = True

                if min_lift == -1:

                    if confidence_of_rule > min_confidence and lift_of_rule < max_lift:
                        append_flag = True

                if confidence_of_rule > min_confidence and min_lift < lift_of_rule < max_lift:
                    append_flag = True

                if append_flag:

                    rules_df = rules_df.append({'itemset': item, 'rule': str(left_side) + '->' + str(right_side),
                                                'frequency': frequency_of_rule, 'confidence': confidence_of_rule,
                                                'lift': lift_of_rule, 'rule ID': id_counter}, ignore_index=True)
                    id_counter += 1
    return rules_df
