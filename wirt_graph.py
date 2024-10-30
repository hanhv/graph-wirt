import itertools
import string
import pandas as pd
import ast


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

##########################################################################
##########################################################################


def get_seeds_only(all_strands, num_colors, pods):
    # Generate all combinations of strands
    combinations = list(itertools.combinations(all_strands, num_colors))
    # Filter combinations to include at least one pod
    valid_combinations = []
    for combination in combinations:
        # Check if any strand in the combination is a pod
        has_pod = False
        for strand in combination:
            if strand in pods:
                has_pod = True
                break
        if has_pod:
            valid_combinations.append(list(combination))
    return valid_combinations


##########################################################################
##########################################################################


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
        end_node = current_strand[-1]
        return [strand for strand in all_strands
                if end_node in strand and strand != current_strand]


##########################################################################
##########################################################################

# NOTE: current strand ends at under node
def get_over_strand(current_strand, all_strands):
    current_under = current_strand[-1]
    over_node = -current_under
    # print("over node", over_node)
    for strand in all_strands:
        if over_node in strand:
            return strand
    return None


def check_extension(all_strands, colored_strands, pods):
    pod_endpoints = [item for sublist in pods for item in sublist]
    extendable = True
    while extendable:
        extendable = False
        for current_strand in colored_strands:
            # print("working on extending", current_strand)
            next_strands = get_next_strands(current_strand, all_strands, pods)
            # print("next_strands ", next_strands)
            for next_strand in next_strands:
                if next_strand not in colored_strands:
                    # move 1: extend at an endpoint of a tripod
                    if (current_strand in pods
                            or current_strand[-1] in pod_endpoints):
                        extendable = True
                        colored_strands.append(next_strand)
                        # print("extend using move 1 ", current_strand, "to ", next_strand)
                    # move 2: extend at an under node
                    else:
                        over_strand = get_over_strand(current_strand, all_strands)
                        # print("over_strand", over_strand)
                        if over_strand in colored_strands:
                            extendable = True
                            colored_strands.append(next_strand)
                            # print("extend using move 2 ", current_strand, "to ", next_strand)
                if lists_contain_same_elements(all_strands, colored_strands):
                    # print("Colorable")
                    return True
    return False



##########################################################################
##########################################################################


def lists_contain_same_elements(list1, list2):
    set1 = {tuple(sublist) for sublist in list1}
    set2 = {tuple(sublist) for sublist in list2}
    return set1 == set2


##########################################################################
##########################################################################


def get_wirtinger(gauss_code):
    pods = extract_pods(gauss_code)
    all_strands = get_strands(gauss_code, pods)
    # print("All strands:", all_strands)
    num_colors = 1
    while num_colors <= len(all_strands):
        list_seeds = get_seeds_only(all_strands, num_colors, pods)
        for seed in list_seeds:
            # print("\nseed ", seed)
            current_truncated = get_truncated(all_strands, seed, pods)
            # print("current_truncated ", current_truncated)
            colored_strands = []
            for strand in seed:
                colored_strands.append(strand)
            is_colorable = check_extension(current_truncated, colored_strands, pods)
            # print("is_colorable ", is_colorable)
            if is_colorable:
                # print("\nGood seed ", seed)
                return [num_colors, seed]
        num_colors += 1


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

        # Get the Wirtinger number and seed
        [wirtinger, seed] = get_wirtinger(my_gauss)

        # Append the result (my_gauss, wirtinger, seed) to the results list
        results.append([my_gauss, wirtinger, seed])

    # Convert the list of results into a DataFrame
    output_df = pd.DataFrame(results)

    # Write the DataFrame to an Excel file (without column names)
    output_df.to_excel(output_excel, header=False, index=False)
    print("Done")

# # # Example usage:
# process_wirtinger('excel/list_graphs_test.xlsx', 'excel/output_wirtinger_test.xlsx')
# # process_wirtinger('excel/list_graphs_14in2.xlsx', 'excel/output_wirtinger_list_graphs_14in2.xlsx')


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
#
# [wirtinger, seed] = get_wirtinger(my_gauss)
# print("Wirtinger ", wirtinger, "\nseed ", seed)



