import random
from copy import deepcopy
from ast import literal_eval


#  constants
COST_INDEX = 0
PREVIOUS_NODE_INDEX = 1
PATH_INDEX = 0
PATH_COST = 1
GET_ALL_BUT_LAST = slice(None, -1, None)
GET_ALL_BUT_FIRST = slice(1, None, None)
GET_LAST = -1
GET_FIRST = 0
LOWER_BOUND_WEIGHT = 1
UPPER_BOUND_WEIGHT = 10


#  default values
nb_of_nodes: int = 2
p: float = 0.4
src: int = 0
des: int = 1
k: int = 5


#  formatting
COLORS = \
    {
        'red': '\033[91m', \
        'green': '\033[92m', \
        'yellow': '\033[93m', \
        'blue': '\033[94m', \
        'magenta': '\033[95m', \
        'cyan': '\033[96m', \
        'white': '\033[97m', \
        'reset': '\033[0m', \
    }

TEXT_STYLES = \
    {
        'bold': '\033[1m', \
        'underline': '\033[4m', \
        'italic': '\033[3m', \
    }


#  messages
EXCEPTION_MESSAGES = \
    {
        'nb_of_nodes': f'{COLORS["red"]}nb_of_nodes must be an integer greater than 1{COLORS["reset"]}', \
        'p': f'{COLORS["red"]}p must be a float between 0 and 1{COLORS["reset"]}', \
        'src': f'{COLORS["red"]}src must be an integer between 0 and the # of nodes{COLORS["reset"]}', \
        'des': f'{COLORS["red"]}des must be an integer between 0 and the # of nodes and different than src{COLORS["reset"]}', \
        'k': f'{COLORS["red"]}k must be an integer greater than 0{COLORS["reset"]}', \
        'invalid_input': f'{COLORS["red"]}Invaild input!!!{COLORS["reset"]}', \
        'matrix_0': f'{COLORS["red"]}the passed adjacency matrix is not in the form of list of list of numbers{COLORS["reset"]}', \
        'matrix_1': f'{COLORS["red"]}there has to be more than one node{COLORS["reset"]}', \
        'matrix_2': f'{COLORS["red"]}the number of rows and columns of the matrix must be equal (the size of the main list must equal the sizes of sub-lists){COLORS["reset"]}', \
        'matrix_3': f'{COLORS["red"]}all the values of the list has to be numbers{COLORS["reset"]}', \
        'matrix_4': f'{COLORS["red"]}all the weights have to be positive numbers{COLORS["reset"]}', \
        'matrix_5': f'{COLORS["red"]}the nodes should not reference itself (Hint: the top left to bottom right digonal values must be zeros){COLORS["reset"]}', \
        'matrix_6': f'{COLORS["red"]}each node must be reachable (Hint: each column has to have at least one value larger than 0){COLORS["reset"]}'  
     }

NORMAL_MESSAGES = \
    {
        'welcome': f'{COLORS["green"]}{TEXT_STYLES["bold"]}\n{" Welcome to the Shortest Path Finder ":*^60}\n\n{COLORS["reset"]}', \
        'exit': f'{COLORS["green"]}{TEXT_STYLES["bold"]}\n{" Thank you for using the Shortest Path Finder ":*^60}\n\n{COLORS["reset"]}', \
        'graph': f'{COLORS["cyan"]}{TEXT_STYLES["bold"]}Do you want to: \n[0] create random graph \n[1] create your own graph \n[Default: 0]:> {COLORS["reset"]}', \
        'start_menu': f'{COLORS["cyan"]}{TEXT_STYLES["bold"]}What do you want to perform: \
            \n[1] re-create the graph. \
            \n[2] display the adjacency matrix. \
            \n[3] find the shortest path. \
            \n[4] find the shortest k paths.\
            \n[5] display the links.\
            \n[0] exit\
            \n[Default: 0]:> {COLORS["reset"]}', \
        'graph_details': f'{COLORS["cyan"]}{TEXT_STYLES["bold"]}Do you want to: \n[0] use the default values (nb_of_nodes={nb_of_nodes},p={p}) \n[1] use your own values \n[Default: 0]:> {COLORS["reset"]}', \
        'search_details': f'{COLORS["cyan"]}{TEXT_STYLES["bold"]}Do you want to: \n[0] use the default values (src={src},des={des},k={k}) \n[1] use your own values \n[Default: 0]:> {COLORS["reset"]}', \
        'adj_matrix': f'{COLORS["blue"]}Enter the adjacency matrix in the form of list of list of positive numbers:> {COLORS["reset"]}', \
        'nb_of_nodes': f'{COLORS["blue"]}Enter the number of nodes (nb_of_nodes > 1):>{COLORS["reset"]} ', \
        'p': f'{COLORS["blue"]}Enter the probability of having a link between any two nodes (0 < p <= 1):>{COLORS["reset"]} ', \
        'src': f'{COLORS["blue"]}Enter the source node (0 <= src < nb_of_nodes):>{COLORS["reset"]} ', \
        'des': f'{COLORS["blue"]}Enter the destination node (0 <= des < nb_of_nodes) and (des != src):>{COLORS["reset"]} ', \
        'k': f'{COLORS["blue"]}Enter the number of shortest paths (k > 0):>{COLORS["reset"]} ', \
    }

WARNING_MESSAGES = \
    {
        'src_des': f'{COLORS["yellow"]}WARNING: the src and/or the des nodes becomes out of range and they will be set to the default (src=0, des=1).\nDo you want to continue? (n)o or (y)es [Default: n]:> {COLORS["reset"]}'
    }

def start() -> None:

    print(NORMAL_MESSAGES['welcome'])
    adj_matrix = create_graph_options()

    exit_flag: bool = False

    while not exit_flag:
        match (choice := input(NORMAL_MESSAGES['start_menu']).strip() or "0"):
            case "0":
                print(NORMAL_MESSAGES['exit'])
                exit_flag = True
            case "1":
                adj_matrix = create_graph_options()
            case "2":
                display_adj_matrix(adj_matrix)
            case "3":
                read_search_details(choice)
                result = dijkstra(src, des, adj_matrix)
                path, delay = trace_back(result, des)
                print(path, delay)
            case "4":
                read_search_details(choice)
                list_of_paths = find_k_path(src, des, adj_matrix, k)
                print(list_of_paths)
            case "5":
                display_links(adj_matrix)
            case _:
                print(EXCEPTION_MESSAGES['invalid_input'])

    # display_adj_matrix(adj_matrix)
    # print(display_links(adj_matrix))
    # result = dijkstra(src, des, adj_matrix)
    # path, delay = trace_back(result, des)
    # print(path, delay)
    # list_of_paths = find_k_path(src, des, adj_matrix, k)
    # print(list_of_paths)


def create_graph_options() -> list[list[int]]:
    adj_matrix: list[list[int]] = []

    #  create random graph or get input from the user
    match input(NORMAL_MESSAGES['graph']):
        case "1":
            adj_matrix = read_adj_matrix()
        case _:
            match input(NORMAL_MESSAGES['graph_details']):
                case "1":
                    read_graph_details()
            adj_matrix = create_random_graph(nb_of_nodes, p)
            if not all(adj_matrix):
                adj_matrix = fix_non_reachable_nodes(adj_matrix)
    
    return adj_matrix


def read_graph_details() -> None:
    global nb_of_nodes, p, src, des

    #  get nb_of_nodes from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            nb_of_nodes = int(input(NORMAL_MESSAGES["nb_of_nodes"]))
            if nb_of_nodes < 2:
                raise ValueError()
            elif src >= nb_of_nodes:
                match input(WARNING_MESSAGES['src_des']):
                    case "y" | "Y" | "yes" | "Yes" | "YES" | "yES" | "yEs" | "yeS" | "YeS":
                        src, des = 0, 1
                        correct_input_flag = True
                    case _:
                        continue
        except ValueError:
            print(EXCEPTION_MESSAGES["nb_of_nodes"])
    
    #  get p from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            p = float(input(f'{NORMAL_MESSAGES["p"]}'))
            if p > 1.0 or p <= 0:
                raise ValueError()
            correct_input_flag = True
        except ValueError:
            print(f'{EXCEPTION_MESSAGES["p"]}')


def check_validity(adj_matrix: list[list[int]]) -> tuple[bool, bool, bool, bool, bool, bool]:
        
    ''' This method checks the validity of the adjacency matrix in the following order:
        I. the number of rows and columns of the matrix must be greater than 1
        II. the number of rows and columns of the matrix must be equal
        III. all the values of the matrix must be numbers
        IV. all the values of the matrix must be positive
        V. all the nodes should not reference itself
        VI. all the nodes should be reachable
        (is_valid_structure, is_valid_size, is_number, is_positive, is_not_self_referencing, is_reachable)
    '''
    # CHECK 0: the passed argument must be a list of lists
    if type(adj_matrix) is not list or any([type(adj_matrix[i]) is not list for i in range(len(adj_matrix))]):
        # check 0 is failed because the passed argument is not a list of lists
        return (False, False, False, False, False, False, False)

    #  CHECK I and II: the number of rows and columns of the matrix must be greater than 1 and samiliar to each other
    if(len(adj_matrix) < 2):
        #  check I is failed because the number of nodes is less than 2
        return (True, False, False, False, False, False, False)

    for i in range(len(adj_matrix)):
        if(len(adj_matrix[i]) != len(adj_matrix)):
            #  check II is failed because the number of rows and columns are not equal
            return (True, True, False, False, False, False, False)
    
    #  CHECK III and IV: all the values of the matrix must be numbers and positives
    for i in range (len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if(not isinstance(adj_matrix[i][j], float)) and (not isinstance(adj_matrix[i][j], int)):
                #  check III failed because the value is not a number
                return (True, True, True, False, False, False, False)
            elif(adj_matrix[i][j] < 0):
                #  check VI failed because the value is negative
                return (True, True, True, True, False, False, False)

    
    #  CHECK V and VI: all the nodes should not reference itself and shuld be reachable
    for i in range(len(adj_matrix)):
        if(adj_matrix[i][i] != 0):
            # check V is failed because a node is referencing itself
            return (True, True, True, True, True, False, False)
        is_reachable: bool = False
        for j in range(len(adj_matrix)):
            if(adj_matrix[j][i] != 0):
                is_reachable = True
                break
        if(not is_reachable):
            # check VI
            break 
    
    return (True, True, True, True, True, True, is_reachable)
 

def read_adj_matrix() -> list[list[int]]:
    ''' This method reads the adjacency matrix from the user and checks its validity '''
    #  get the adjacency matrix from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            adj_matrix: list[list[int]] = literal_eval(input(f'{NORMAL_MESSAGES["adj_matrix"]}'))
            check_result = check_validity(adj_matrix)
            if(not all(check_result)):
                raise ValueError(EXCEPTION_MESSAGES[f'matrix_{check_result.index(False)}'])
            correct_input_flag = True
        except ValueError as e:
            print(e.args[0])
        except SyntaxError as e:
            print(f'{COLORS["red"]}{e.args[0]}{COLORS["reset"]}')
    
    return adj_matrix
    

def read_search_details() -> None:

    #  get src from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            src: int = int(input(f'{NORMAL_MESSAGES["src"]}'))
            if src < 0 or src >= nb_of_nodes:
                raise ValueError()
            correct_input_flag = True
        except ValueError:
            print(f'{EXCEPTION_MESSAGES["src"]}')
        except TypeError:
            print(f'{EXCEPTION_MESSAGES["src"]}')
    
    #  get des from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            des: int = int(input(f'{NORMAL_MESSAGES["des"]}'))
            if (des < 0 or des >= nb_of_nodes) or (des == src):
                raise ValueError()
            correct_input_flag = True
        except ValueError:
            print(f'{EXCEPTION_MESSAGES["des"]}')
        except TypeError:
            print(f'{EXCEPTION_MESSAGES["des"]}')
    
    #  get k from the user
    correct_input_flag: bool = False
    while not correct_input_flag:
        try:
            k: int = int(input(f'{NORMAL_MESSAGES["k"]}'))
            if k < 0 or k >= len(nb_of_nodes):
                raise ValueError()
            correct_input_flag = True
        except ValueError:
            print(f'{EXCEPTION_MESSAGES["k"]}')
        except TypeError:
            print(f'{EXCEPTION_MESSAGES["k"]}')


def get_non_reachable_nodes(adj_matrix: list[list[int]]) -> list[int]:
    ''' This method returns the list of non reachable nodes '''
    non_reachable_nodes: list[int] = []
    for i in range(len(adj_matrix)):
        is_reachable: bool = False
        for j in range(len(adj_matrix)):
            if(adj_matrix[j][i] != 0):
                is_reachable = True
                break
        if(not is_reachable):
            non_reachable_nodes.append(i)
    
    return non_reachable_nodes


def get_nodes_degree(adj_matrix: list[list[int]]) -> list[int]:
    ''' This method returns the list of degrees of the nodes '''
    nodes_degree: list[int] = []
    for i in range(len(adj_matrix)):
        degree: int = 0
        for j in range(len(adj_matrix)):
            if(adj_matrix[i][j] != 0):
                degree += 1
        nodes_degree.append(degree)
    
    return nodes_degree


def get_node_degree(adj_matrix: list[list[int]], node: int) -> int:
    ''' This method returns the degree of the node '''
    degree: int = 0
    for j in range(len(adj_matrix)):
        if(adj_matrix[node][j] != 0):
            degree += 1
    
    return degree


def fix_non_reachable_nodes(adj_matrix: list[list[int]]) -> list[list[int]]:
    ''' This method fixes the non reachable nodes by adding a random link to the node from another node '''

    non_reachable_nodes: list[int] = get_non_reachable_nodes(adj_matrix)
    all_nodes: list[int] = [x for x in range(len(adj_matrix))]
    for i in non_reachable_nodes:
        candidate_nodes = list(set(all_nodes) - set([i]))
        candidate_nodes_with_degrees = [(x, get_node_degree(adj_matrix, x)) for x in candidate_nodes]
        candidate_nodes_with_degrees.sort(key=lambda x: x[1])
        adj_matrix[candidate_nodes_with_degrees[GET_FIRST][GET_FIRST]][i] = random.randint(LOWER_BOUND_WEIGHT, UPPER_BOUND_WEIGHT)

    return adj_matrix


def create_random_graph(nodes_: int, p: float) -> list[list[int]]:
    adj_matrix: list[list[int]] = []
    for i in range(nodes_):
        adj_row: list[int] = []
        for j in range(nodes_):
            if (i == j):
                x = 0
            else:
                if (random.random() < p):
                    x = random.randint(LOWER_BOUND_WEIGHT, UPPER_BOUND_WEIGHT)
                else:
                    x = 0
            adj_row.append(x)
        adj_matrix.append(adj_row)

    return adj_matrix


def display_links(adj_matrix: list[list[int]]) -> list[list[tuple[int, int]]]:
    list_of_links: list[list[tuple[int, int]]] = []
    for i in range(len(adj_matrix)):
        node_i_links: list[tuple[int, int]] = []
        for j in range(len(adj_matrix)):
            if (adj_matrix[i][j] != 0):
                node_i_links.append((i, j))
        list_of_links.append(node_i_links)

    return list_of_links


def display_adj_matrix(adj_matrix: list[list[int]]) -> None:
    txt_header: str = "     "
    txt_body: str = ""
    for i in range(len(adj_matrix)):
        txt_header += f'{i:<5}'
        txt_body += f'{i:<5}'
        for j in range(len(adj_matrix)):
            txt_body += f'{adj_matrix[i][j]:<5}'
        txt_body += '\n'
    print(f'\n\n{txt_header}\n\n{txt_body}\n\n')


def init_phase(s: int, nb_of_elements: int) -> \
        tuple[dict[int, list[int]], list[int], list[tuple[int, int]]]:
    delays: list[tuple[int, int]] = []
    nodes: list[int] = []
    result: dict[int, list[int]] = {}
    for i in range(nb_of_elements):
        if (i != s):
            cost = 99999999
        else:
            cost = 0
        result[i] = [cost, -1]
        nodes.append(i)
        delays.append((i, cost))

    return result, nodes, delays


def dijkstra(s: int, d: int, adj_matrix: list[list[int]]) -> \
        dict[int, list[int]]:
    result: dict[int, list[int]]
    nodes: list[int]
    delays: list[tuple[int, int]]
    result, nodes, delays = init_phase(s, len(adj_matrix))

    while (nodes != []):
        delays.sort(key=lambda x: x[1], reverse=True)
        current_node, cost = delays.pop()
        nodes.remove(current_node)
        for i in nodes:
            if (not (link_cost := adj_matrix[current_node][i])):
                continue
            if (result[i][COST_INDEX] > (new_cost := cost + link_cost)):
                result[i][COST_INDEX] = new_cost
                result[i][PREVIOUS_NODE_INDEX] = current_node
                delay_idx = [delays.index(x) for x in delays if x[0] == i][0]
                delays[delay_idx] = (i, new_cost)
    return result


def find_k_path(s: int, d: int, adj_matrix: list[list[int]], k: int) \
        -> list[tuple[list[int], int]]:
    """ Using Yen's Algorithm """

    # 'A' container in Yen's Algorithm
    list_of_paths: list[tuple[list[int], int]] = []

    #  'B' container in Yen's Algorithm
    list_of_candidate_paths: list[tuple[list[int], int]] = []

    first_path: list[int]
    first_path_cost: int
    first_path, first_path_cost = trace_back(dijkstra(s, d, adj_matrix), d)
    list_of_paths.append((first_path, first_path_cost))
    counter = 1
    while counter < k:
        prefix_nodes: list[int] = []
        prefix_cost: int = 0
        idx = 0
        for i in (path := list_of_paths[GET_LAST][GET_FIRST])[GET_ALL_BUT_LAST]:
            prefix_nodes.append(i)
            tmp_adj_matrix = deepcopy(adj_matrix)
            list_of_links = [x[GET_FIRST][x[GET_FIRST].index(i):x[GET_FIRST].index(i)+2:] 
                             for x in list_of_paths if i in x[GET_FIRST][GET_ALL_BUT_LAST]] + \
                                [[i,x] for x in prefix_nodes]
            for link in list_of_links:
                tmp_adj_matrix[link[0]][link[1]] = 9999999
            for node in prefix_nodes:
                for j in range(len(tmp_adj_matrix)):
                    tmp_adj_matrix[j][node] = 9999999
            suffix_path, suffix_cost = trace_back(dijkstra(i, d, tmp_adj_matrix), d)
            new_path = prefix_nodes[GET_ALL_BUT_LAST] + suffix_path
            new_cost = prefix_cost + suffix_cost
            if (new_path, new_cost) not in list_of_candidate_paths:
                list_of_candidate_paths.append((new_path, new_cost))
            prefix_cost += adj_matrix[i][path[idx+1]]
            idx += 1
        if(list_of_candidate_paths != []):
            list_of_candidate_paths.sort(key=lambda x: x[PATH_COST], reverse=True)
            chosen_path, chosen_path_cost = list_of_candidate_paths.pop()
            if(chosen_path_cost >100000):
                break
            list_of_paths.append((chosen_path, chosen_path_cost))
            counter += 1
        else:
            break

    return list_of_paths


def trace_back(result: dict[int, list[int]], des: int) -> \
        tuple[list[int], int]:
    reversed_path_nodes: list[int] = []
    path_cost: int = result[des][COST_INDEX]
    current_node: int = des
    temp_cost: int = path_cost
    while temp_cost != 0:
        current_node = result[current_node][PREVIOUS_NODE_INDEX]
        reversed_path_nodes.append(current_node)
        temp_cost = result[current_node][COST_INDEX]
    return reversed_path_nodes[::-1], path_cost


if __name__ == '__main__':
    start()