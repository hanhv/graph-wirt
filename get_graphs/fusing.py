# input: a 2-component link
# output: a theta-4 graph
# from 2 crossings to 2 vertices
import pandas as pd

def cyclic_distance(idx1, idx2, my_length):
    if idx1 <= idx2:
        return min(idx2 - idx1, my_length - idx2 + idx1)
    else:
        return min(idx1 - idx2, my_length - idx1 + idx2)


# test_cyclic_distance = cyclic_distance(1, 5, 6)
# test_cyclic_distance = cyclic_distance(5, 1, 6)
# print("test_cyclic_distance ", test_cyclic_distance)

##########################################################################
##########################################################################


def find_fusible_pairs(my_link):
    component_1 = my_link[0]
    component_2 = my_link[1]

    fusible_pairs = []
    len_component_1 = len(component_1)
    # Iterate through all pairs of elements in component 1
    for idx in range(len_component_1-3):
        for jdx in range(idx + 3, len_component_1):
            fuse1 = component_1[idx]
            fuse2 = component_1[jdx]
            # Check if the negation of both x and y are in component 2
            if -fuse1 in component_2 and -fuse2 in component_2:
                fusible_pairs.append((fuse1, fuse2))
    return fusible_pairs

# # # # Input data
# my_link = [[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
# pairs = find_fusible_pairs(my_link)
# print("my link ", my_link, "\nfusible pairs (x, y):", pairs)


##########################################################################
##########################################################################


def split_cyclic_list(lst, start, end):
    # Find the indices of the start and end elements
    start_idx = lst.index(start)
    end_idx = lst.index(end)

    # Create the first list: from start to end
    if start_idx <= end_idx:
        list1 = lst[start_idx:end_idx + 1]
    else:  # cyclic case
        list1 = lst[start_idx:] + lst[:end_idx + 1]

    # Create the second list: from end to start (cyclic)
    if end_idx <= start_idx:
        list2 = lst[end_idx:start_idx + 1]
    else:  # cyclic case
        list2 = lst[end_idx:] + lst[:start_idx + 1]

    return list1, list2

# # Example
# original_list = [1, -9, 4, -5, 3, -4, 2, -10, 5, -3]
# start_element = 1
# end_element = -10

# list1, list2 = split_cyclic_list(original_list, start_element, end_element)
# print("original_list ", original_list)
# print("List 1:", list1)
# print("List 2:", list2)


##########################################################################
##########################################################################


def transform_to_theta4_format(lst_of_lsts):
    # Letters to prepend (a, b, c, d, ...)
    letters = ['a', 'b', 'c', 'd']  # You can extend this if there are more directions

    transformed = []

    for i, sublist in enumerate(lst_of_lsts):
        # Extract the first and last elements
        first = sublist[0]
        last = sublist[-1]

        # Replace them with the corresponding letter and absolute value
        transformed_first = f"{letters[i]}{abs(first)}"
        transformed_last = f"{letters[i]}{abs(last)}"

        # Create the transformed sublist
        new_sublist = [transformed_first] + sublist[1:-1] + [transformed_last]
        transformed.append(new_sublist)

    return transformed


# # Example
# original_list = [[-9, 4, -5, 3, -4, 2, -10],
#                  [-10, 5, -3, 1, -9],
#                  [9, -1, 6, -8, 7, -2, 10],
#                  [10, -6, 8, -7, 9]]
#
# result = transform_to_theta4_format(original_list)
# print("original_list\n", original_list, "\nresult\n", result)
##########################################################################
##########################################################################


def check_sublists_length(list_of_lists, min_length_edge):
    return all(len(sublist) >= min_length_edge for sublist in list_of_lists)

# # Example usage:
# list_of_lists = [[1, 2, 3], [4, 5, 6, 7], [8, 9]]
# min_length_edge = 3
# if check_sublists_length(list_of_lists, min_length_edge):
#     print("True")
# else:
#     print("False")
##########################################################################
##########################################################################

# Split each component of a 2-component-link
def get_graph_by_fusing(my_link, min_length_edge=4):
    my_graphs = []
    fusible_pairs = find_fusible_pairs(my_link)
    for current_fusing_pair in fusible_pairs:
        current_graph = []
        note1 = current_fusing_pair[0]
        note2 = current_fusing_pair[1]
        for current_component in my_link:
            current_graph.extend(split_cyclic_list(current_component, note1, note2))
            note1 = -note1
            note2 = -note2
        if check_sublists_length(current_graph, min_length_edge):
            print("\ngood graph ", current_graph)
            theta_format = transform_to_theta4_format(current_graph)
            print("using fusing_pair ", current_fusing_pair, "\ntheta_format ", theta_format)
            my_graphs.append(theta_format)
    return my_graphs

# # # # # TEST
# # # # # # # Input data
# my_link = [[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
# # # my_link = [[1, 13, -2, -12, 3, -14, 4, -10, 5, -6], [6, -1, -7, 2, 8, -3, 9, -4, 10, -5, 11, -8, 12, 7, -13, -11, 14, -9]]
# list_graphs = get_graph_by_fusing(my_link, min_length_edge=4)
# # # print("list_graphs ", list_graphs)
# ##########################################################################
# ##########################################################################


def read_excel_and_get_list_graphs(input_file_path, output_file_path, column_index=2):
    df = pd.read_excel(input_file_path, header=None)  # header=None tells pandas there are no column names

    # Get the third column (index 2, because Python is 0-indexed)
    column_data = df.iloc[:, column_index].tolist()

    # Parse each row into a list of two components (separated by ';')
    list_graphs = []
    for row in column_data:
        # Check if the cell has exactly one ';'
        if row.count(';') == 1:
            # Split the string by ';' to separate into two components
            components = row.split(';')
            # For each component, split by commas, convert to integers, and create the list of lists
            list1 = [int(x) for x in components[0].split(',')]
            list2 = [int(x) for x in components[1].split(',')]
            good_link = [list1, list2]
            current_list_graphs = get_graph_by_fusing(good_link, min_length_edge=4)
            if current_list_graphs:
                print("good_link ", good_link)
                list_graphs.extend(current_list_graphs)
                print("\n", current_list_graphs)
    # Save to Excel
    # Convert each sublist in list_graphs to a string to fit in one cell
    data = [[str(sublist)] for sublist in list_graphs]
    df = pd.DataFrame(data)
    df.to_excel(output_file_path, index=False, header=False)
    print("list_graphs has been saved to ", output_file_path)
    return list_graphs


# # Example
# # input_file_path = 'link14in2.xlsx'
# input_file = 'test_input_links.xlsx'
# output_file = 'test_output_graphs.xlsx'
# my_list_graphs = read_excel_and_get_list_graphs(input_file, output_file, column_index=2)
# print("done my_list_graphs")