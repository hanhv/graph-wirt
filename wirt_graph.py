import itertools
import string
import pandas as pd
import ast
import math


def flatten_current_seed(current_seed_groups):
    flattened_colored_seed = []
    for seed_group in current_seed_groups:
        if isinstance(seed_group[0], list):
            # Assume it's a list of strands (list of lists)
            flattened_colored_seed.extend(seed_group)
        else:
            # It's just a single strand
            flattened_colored_seed.append(seed_group)
    return flattened_colored_seed


def check_all_pods_extend_to_one(this_pod_extension, all_pods):
    if all(pod in this_pod_extension for pod in all_pods):
        return True
    return False


def extend_all_pods(all_strands, all_pods):
    extended_pods = []
    for this_pod in all_pods:
        list_of_current_pods = [this_pod]
        this_pod_extension = extend_at_pod(all_strands, list_of_current_pods, all_pods)
        extended_pods.append(this_pod_extension)
        if check_all_pods_extend_to_one(this_pod_extension, all_pods):
            return extended_pods
    return extended_pods


def seed_candidates(all_strands, all_pods):
    extended_pods = extend_all_pods(all_strands, all_pods)
    left_over = [strand for strand in all_strands if is_normal_arc(strand)]
    return extended_pods + left_over


def get_seeds(seeds_candidates, num_colors):
    # Convert each combination tuple to a list and print it
    valid_combinations = [list(comb) for comb in itertools.combinations(seeds_candidates, num_colors)]
    flat_seeds_list = []
    for current_seed in valid_combinations:
        flat_seeds_list.append(flatten_current_seed(current_seed))
    return flat_seeds_list


def get_weight(current_seed):
    count = 0
    for sublist in current_seed:
        for item in sublist:
            if isinstance(item, int) and item < 0:
                count += 1
    return count / 2


def contains_negative(strand):
    return any(isinstance(x, int) and x < 0 for x in strand)


def get_pod_ends(strand):
    return [item for item in strand if isinstance(item, str)]


def extend_at_pod(all_strands, list_of_current_pods, pods):
    extendable = True
    while extendable:
        extendable = False
        appeared_pod_endpoints = list(
            {item for strand in list_of_current_pods for item in strand if isinstance(item, str)})
        for current_strand in list_of_current_pods:
            next_strands = get_next_strands(current_strand, all_strands, pods)
            for next_strand in next_strands:
                if next_strand not in list_of_current_pods:
                    list_pod_ends = get_pod_ends(next_strand)
                    # move 1: extend at an endpoint of a pod
                    if any(item in appeared_pod_endpoints for item in list_pod_ends):
                        list_of_current_pods.append(next_strand)
                        appeared_pod_endpoints = list(
                            {item for strand in list_of_current_pods for item in strand if isinstance(item, str)})
                        extendable = True
    return list_of_current_pods


def is_normal_arc(strand):
    if all(isinstance(item, int) for item in strand):
        return True
    return False


def extract_pods(gauss):
    # Determine the number of branches and get corresponding letters from the alphabet
    num_branches = len(gauss)
    letters = string.ascii_lowercase[:num_branches]  # Get the first 'num_branches' letters from the alphabet

    first_list = []  # To store the first set of pods (like 'a1', 'b1', etc.)
    second_list = []  # To store the second set of pods (like 'a2', 'b2', etc.)

    found_numbers = []  # List to store found numbers
    for sublist in gauss:  # Loop through each sublist in gauss
        for item in sublist:  # Loop through each item in the sublist
            if isinstance(item, str):
                number_str = item[1:]  # Slice to get the part after the first character
                number = int(number_str)  # Convert the remaining part to an integer

                # Add the number to found_numbers if it's not already present
                if number not in found_numbers:
                    found_numbers.append(number)

                # Stop searching if we have found both numbers
                if len(found_numbers) == 2:
                    break  # Break the inner loop
        if len(found_numbers) == 2:
            break  # Break the outer loop if both numbers are found

    # If we have found exactly 2 numbers, create the pod lists
    if len(found_numbers) == 2:
        num1, num2 = found_numbers
        first_list = [f"{letter}{num1}" for letter in letters]
        second_list = [f"{letter}{num2}" for letter in letters]

    return [first_list, second_list]  # Return both lists


##########################################################################
##########################################################################


def get_strands(gauss_code, pods):
    # Initialize lists to hold strands
    all_strands = []
    all_strands.extend(pods)  # Add pods to the strands list

    for edge in gauss_code:
        current_strand = [edge[0]]  # Start a new strand from a pod end
        for node in edge[1:]:
            if isinstance(node, int) and node > 0:
                current_strand.append(node)  # Add overcrossing to the current strand
            if isinstance(node, int) and node < 0:
                current_strand.append(node)  # Add undercrossing to the current strand
                all_strands.append(current_strand)
                current_strand = [node]
                # if we see under node then add to the END of the current strand, then create next strand
            if isinstance(node, str):
                current_strand.append(node)  # Add pod to current strand
                all_strands.append(current_strand)
                current_strand = []
                # if we see end of a pod then add to the END of the current strand, then DONE the current branch
    return all_strands  # Return the complete list of strands


def get_truncated(all_strands, seed, pods):
    # truncate pods that are NOT in seed
    pods_in_seed = [strand for strand in seed if strand in pods]
    # print("pods_in_seed ", pods_in_seed)
    pods_to_be_deleted = [strand for strand in pods if strand not in pods_in_seed]
    # print("pods_not_in_seed ", pods_not_in_seed)
    truncated_graph = [strand for strand in all_strands if strand not in pods_to_be_deleted]
    # print("truncated_graph ", truncated_graph)
    return truncated_graph


##########################################################################
##########################################################################


def get_next_strands(current_strand, all_strands, pods):
    if current_strand in pods:
        return [strand for strand in all_strands
                if any(node in strand for node in current_strand)
                and strand != current_strand]
    else:
        end_node0 = current_strand[0]
        end_node1 = current_strand[-1]
        return [strand for strand in all_strands
                if (end_node0 in strand or end_node1 in strand) and strand != current_strand]


def get_over_strand_between_current_next(current_strand, next_strand, all_strands):
    # Step 1: Find common under node (negative integer) in both strands
    under_nodes = set(x for x in current_strand if isinstance(x, int) and x < 0)
    next_under_nodes = set(x for x in next_strand if isinstance(x, int) and x < 0)
    common_under_nodes = under_nodes & next_under_nodes

    if not common_under_nodes:
        return []  # No common under node, return empty list

    # Assume only one common under node is needed
    under_node = common_under_nodes.pop()
    over_node = -under_node  # Positive counterpart

    # Step 2: Search for strand containing the over node
    for strand in all_strands:
        if over_node in strand:
            return strand  # Return as a list

    return []  # No matching over strand found


##########################################################################
##########################################################################


def lists_contain_same_elements(list1, list2):
    set1 = {tuple(sublist) for sublist in list1}
    set2 = {tuple(sublist) for sublist in list2}
    return set1 == set2


def check_extension(all_strands, seed, pods):
    colored_strands = [strand for strand in seed]
    extendable = True
    while extendable:
        extendable = False
        for current_strand in colored_strands:
            next_strands = get_next_strands(current_strand, all_strands, pods)
            for next_strand in next_strands:
                if next_strand not in colored_strands:
                    # extension using move 2
                    over_strand = get_over_strand_between_current_next(current_strand, next_strand, all_strands)
                    if over_strand in colored_strands:
                        extendable = True
                        colored_strands.append(next_strand)
                if lists_contain_same_elements(all_strands, colored_strands):
                    return True
    return False


def get_wirtinger(gauss_code):
    pods = extract_pods(gauss_code)
    all_strands = get_strands(gauss_code, pods)
    candidate_for_seeds = seed_candidates(all_strands, pods)
    num_colors = 1
    max_num_colors = len(all_strands)
    min_wirt = max_num_colors * len(pods[0]) * 2
    list_good_seeds = []
    while True:
        if num_colors > max_num_colors:
            break
        if num_colors > math.ceil(min_wirt):
            break

        list_seeds = get_seeds(candidate_for_seeds, num_colors)
        for current_seed_group in list_seeds:
            current_truncated = get_truncated(all_strands, current_seed_group, pods)
            is_colorable = check_extension(current_truncated, current_seed_group, pods)
            if is_colorable:
                current_wirt = get_weight(current_seed_group)
                if current_wirt <= min_wirt:
                    min_wirt = current_wirt
                    list_good_seeds.append([current_wirt, current_seed_group])

        num_colors += 1
    output_seeds = []
    for item in list_good_seeds:
        if item[0] == min_wirt:
            output_seeds.append(item[1])
    return [min_wirt, output_seeds]


##########################################################################
##########################################################################


def process_wirtinger(input_excel, output_excel):
    """
    Function to process a list of graphs from an Excel file and compute Wirtinger numbers.

    Parameters:
    input_excel (str): Path to the input Excel file.
    output_excel (str): Path to save the output Excel file.

    Returns:
    None
    """
    # Read the Excel file with pandas
    df = pd.read_excel(input_excel, header=None)

    # Initialize a list to store the results
    results = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Convert the string representation of the list to an actual list
        graph_as_string = row[0]  # Get the content of the only cell in the row
        my_gauss = ast.literal_eval(graph_as_string)  # Convert string to list of lists
        print("gauss code", my_gauss)
        # Get the Wirtinger number and seed
        [wirtinger, seed] = get_wirtinger(my_gauss)
        print(wirtinger, seed)

        # Append the result (my_gauss, wirtinger, seed) to the results list
        results.append([my_gauss, wirtinger, seed])

    # Convert the list of results into a DataFrame
    output_df = pd.DataFrame(results)

    # Write the DataFrame to an Excel file (without column names)
    output_df.to_excel(output_excel, header=False, index=False)
    print("Done")


# # # # Example usage:
# process_wirtinger('excel/list_graphs_test.xlsx', 'excel/output_wirtinger_test.xlsx')
# process_wirtinger('excel/list_graphs_14in2.xlsx', 'excel/output_wirtinger_list_graphs_14in2.xlsx')


##########################################################################
##########################################################################


# Example Gauss code input
# my_gauss = [
#     ['a1', -13, -2, 'a12'],
#     ['b12', -3, 14, 4, -10, 5, -6, 'b1'],
#     ['c1', -7, 2, -8, 3, -9, -4, 10, -5, 11, 8, 'c12'],
#     ['d12', 7, 13, -11, -14, 9, 6, 'd1']
# ]

# my_gauss = [
#     ['a1', -13, -2, 12, 'a3'],
#     ['b3', 14, 4, -10, 5, -6, 'b1'],
#     ['c1', -7, 2, -8, 'c3'],
#     ['d3', -9, -4, 10, -5, 11, 8, -12, 7, 13, -11, -14, 9, 6, 'd1']
# ]


# my_gauss = [['a1', -13, -2, 12, -3, 'a14'],
#             ['b14', 4, -10, 5, -6, 'b1'],
#             ['c1', -7, 2, -8, 3, -9, -4, 10, -5, 11, 8, -12, 7, 13, -11, 'c14'],
#             ['d14', 9, 6, 'd1']]

# my_gauss = [['a1', 3, -4, 'a2'],
#             ['b1', -5, 6, 7, -8, 9, -7, 10, -11, 12, -10, -13, 14, 'b2'],
#             ['c1', -9, 8, -3, 5, -6, 13, -14, 4, -12, 11, 'c2']]

# my_gauss = [
#     ['a1', 3, -4, 'a2'],
#     ['b1', -5, 6, 7, -8, 9, -7, 10, -11, 12, -10, -13, 14, 'b2'],
#     ['c1', -9, 8, -3, 5, -6, 13, -14, 4, -12, 11, 'c2']
# ]

# my_gauss = [
#     ['a1', 3, 4, 'a2'],
#     ['b1', -5, 6, 7, -8, 9, -7, 10, -11, 12, -10, -13, 14, 'b2'],
#     ['c1', -9, 8, -3, 5, -6, 13, -14, -4, -12, 11, 'c2']
# ]

# [wirtinger, good_seeds] = get_wirtinger(my_gauss)
# print("\nList of colorable seeds:")
# for item in good_seeds:
#     print(item)
# print("Wirtinger ", wirtinger, "\nDone")
