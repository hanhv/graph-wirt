from fusing import *

# # # # Example excel file of graphs
# # input_file_path = 'excel_files/link14in2.xlsx'
# input_file = 'excel_files/test_input_links.xlsx'
# output_file = 'excel_files/test_output_graphs.xlsx'
# my_list_graphs = read_excel_and_get_list_graphs(input_file, output_file, column_index=2)
# print("done my_list_graphs")


# ##########################################################################
# ##########################################################################

# # # # # # # # Input data
my_link = [[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
# # my_link = [[1, 13, -2, -12, 3, -14, 4, -10, 5, -6], [6, -1, -7, 2, 8, -3, 9, -4, 10, -5, 11, -8, 12, 7, -13, -11, 14, -9]]
list_graphs = get_graph_by_fusing(my_link, min_length_edge=4)
# # print("list_graphs ", list_graphs)