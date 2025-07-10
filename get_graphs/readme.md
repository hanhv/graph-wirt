# From 2-Component Links to Theta-4 Graphs

### Input
A two-component link.

### Procedure
Fuse at two crossings, `x` and `y`, where `x` and `y` appear in one component, and `-x` and `-y` appear in the other component.

### Output
A theta-4 graph.

### Examples

##### 1. Given the link:

``` 
[[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
```

By fusing at crossings `1` and `2`, we obtain the graph:

``` 
[['a1', -9, 4, -5, 3, -4, 'a2'], 
['b2', -10, 5, -3, 'b1'], 
['c1', 6, -8, 7, 'c2'], 
['d2', 10, -6, 8, -7, 9, 'd1']]
```

##### 2. Detect fusible pairs (at least `min_length_edge` distance apart) and generate graphs using those pairs:

``` 
my_link = [[1, -9, 4, -5, 3, -4, 2, -10, 5, -3], [9, -1, 6, -8, 7, -2, 10, -6, 8, -7]]
list_graphs = get_graph_by_fusing(my_link, min_length_edge=4) 
```
 
##### 3. Generate a graph table:

``` 
input_file = 'excel_files/test_input_links.xlsx'
output_file = 'excel_files/test_output_graphs.xlsx'
my_list_graphs = read_excel_and_get_list_graphs(input_file, output_file, column_index=2) 
```