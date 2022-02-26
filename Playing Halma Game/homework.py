
BLACK_CAMPUS = [(0,0),(1,0),(2,0),(3,0),(4,0),
                (0,1),(1,1),(2,1),(3,1),(4,1),
                (0,2),(1,2),(2,2),(3,2),
                (0,3),(1,3),(2,3),
                (0,4),(1,4)]

WHITE_CAMPUS = [(11,15),(12,15),(13,15),(14,15),(15,15),
                (11,14),(12,14),(13,14),(14,14),(15,14),
                (12,13),(13,13),(14,13),(15,13),
                (13,12),(14,12),(15,12),
                (14,11),(15,11)]

EIGHT_NEIGHBOR = [(-1,-1),(-1,0),(-1,1),(0,1),(0,-1),(1,-1),(1,0),(1,1)]
EIGHT_JUMP = [(-2,-2),(-2,0),(-2,2),(0,2),(0,-2),(2,-2),(2,0),(2,2)]



def eval(current_location,target_center):
    if target_center==(15,15):
        special = [(0,5),(5,0)]
    else:
        special = [(10, 15), (15, 10)]
    evaluation = 0
    for i in range(0,len(current_location)):
        if current_location[i] in special:
            d=319
        else:
            x = abs(current_location[i][0] - target_center[0])
            y = abs(current_location[i][1] - target_center[1])
            d = (min(x,y)*28)+(abs(x-y)*10)

        evaluation = evaluation+d
    return evaluation



def is_valid_move(campus,start_x,start_y,end_x,end_y):
    if (start_x,start_y) not in campus and (end_x,end_y) in campus:
        return False
    else:
        return True


def is_move_out_campus(campus,start_x,start_y,end_x,end_y):
    if (start_x,start_y) in campus and (end_x,end_y) not in campus:
        return True
    else:
        return False



def one_step_jump(board,start_x,start_y,previous_position):
    all_jumps = []
    for temp in range(0,8):
        target = (start_x + EIGHT_JUMP[temp][0],start_y + EIGHT_JUMP[temp][1])
        cover = (start_x + EIGHT_NEIGHBOR[temp][0],start_y + EIGHT_NEIGHBOR[temp][1])
        if 0 <= target[0] <= 15 and 0 <= target[1] <= 15 and board[target[0]][target[1]]=='.' and \
                board[cover[0]][cover[1]]!='.' and target not in previous_position:
            all_jumps.append(target)
            previous_position.append(target)

    return all_jumps,previous_position



def one_step_jump_three(board,start_x,start_y,previous_position,THREE_NEIGHBOR,THREE_JUMP):
    all_jumps = []
    for temp in range(0,3):
        target = (start_x + THREE_JUMP[temp][0],start_y + THREE_JUMP[temp][1])
        cover = (start_x + THREE_NEIGHBOR[temp][0],start_y + THREE_NEIGHBOR[temp][1])
        if 0 <= target[0] <= 15 and 0 <= target[1] <= 15 and board[target[0]][target[1]]=='.' and \
                board[cover[0]][cover[1]]!='.' and target not in previous_position:
            all_jumps.append(target)
            previous_position.append(target)

    return all_jumps,previous_position



def reform_hash_jump(hash_jump_list,campus):
    all_jumps = []
    start_x = hash_jump_list[0][0]
    start_y = hash_jump_list[0][1]
    for i in range(0,len(hash_jump_list)):
        path = []
        if is_valid_move(campus,start_x,start_y,hash_jump_list[i][2],hash_jump_list[i][3]):
            previous_x = hash_jump_list[i][0]
            previous_y = hash_jump_list[i][1]
            path.append((hash_jump_list[i][2],hash_jump_list[i][3]))

            for j in range(i,-1,-1):
                current = hash_jump_list[j]
                if current[2]==previous_x and current[3]==previous_y:
                    path.append((current[2],current[3]))
                    previous_x = current[0]
                    previous_y = current[1]

            path.append((start_x,start_y))
            path = path[::-1]
            path = tuple(path)
            path = ('J',) + path
            all_jumps.append(path)

    return all_jumps



def reform_hash_jump_ismoveout(hash_jump_list,campus):
    all_jumps = []
    start_x = hash_jump_list[0][0]
    start_y = hash_jump_list[0][1]
    for i in range(0,len(hash_jump_list)):
        path = []
        if is_move_out_campus(campus,start_x,start_y,hash_jump_list[i][2],hash_jump_list[i][3]):
            previous_x = hash_jump_list[i][0]
            previous_y = hash_jump_list[i][1]
            path.append((hash_jump_list[i][2],hash_jump_list[i][3]))

            for j in range(i,-1,-1):
                current = hash_jump_list[j]
                if current[2]==previous_x and current[3]==previous_y:
                    path.append((current[2],current[3]))
                    previous_x = current[0]
                    previous_y = current[1]

            path.append((start_x,start_y))
            path = path[::-1]
            path = tuple(path)
            path = ('J',) + path
            all_jumps.append(path)

    return all_jumps



def move_away(board,color,intersection):
    next_move = []
    THREE_NEIGHBOR = []
    THREE_JUMP = []
    if color == 'W':
        THREE_NEIGHBOR = [(-1, -1), (-1, 0), (0, -1)]
        THREE_JUMP = [(-2, -2), (-2, 0), (0, -2)]
    else:
        THREE_NEIGHBOR = [(1, 1), (1, 0), (0, 1)]
        THREE_JUMP = [(2, 2), (2, 0), (0, 2)]

    for each_piece in intersection:
        current_x = each_piece[0]
        current_y = each_piece[1]
        # add moves
        for n in THREE_NEIGHBOR:
            if 0 <= current_x + n[0] <= 15 and 0 <= current_y + n[1] <= 15 and \
                    board[current_x + n[0]][current_y + n[1]] == '.' and \
                    is_valid_move(campus, current_x, current_y, current_x + n[0], current_y + n[1]):
                next_move.append(('E', current_x, current_y, current_x + n[0], current_y + n[1]))

        # add jumps     one_step_jump(board,start_x,start_y,previous_position)
        previous_position = [(current_x, current_y)]
        jump_list = [(current_x, current_y)]
        hash_jumps = []

        while (len(jump_list) > 0):
            current_piece = jump_list[0]
            jump_list = jump_list[1:]
            itr_jumps, previous_position = one_step_jump_three(board, current_piece[0], current_piece[1],
                                                         previous_position,THREE_NEIGHBOR,THREE_JUMP)

            for each_jump in itr_jumps:
                hash_jumps.append((current_piece[0], current_piece[1], each_jump[0], each_jump[1]))
                jump_list.append((each_jump[0], each_jump[1]))

        if len(hash_jumps) > 0:
            jumps = reform_hash_jump(hash_jumps, campus)
            next_move = next_move + jumps

    return next_move



def get_possible_move(board,color,current_positions,campus):
    next_move=[]
    intersection = list(set(campus) & set(current_positions))
    #print(intersection)

    # moving pieces in campus
    if len(intersection)>0:
        # start search move
        for each_piece in intersection:
            current_x = each_piece[0]
            current_y = each_piece[1]
            # add moves
            for n in EIGHT_NEIGHBOR:
                if 0 <= current_x + n[0] <= 15 and 0 <= current_y + n[1] <= 15 and board[current_x + n[0]][
                    current_y + n[1]] == '.' and \
                        is_move_out_campus(campus, current_x, current_y, current_x + n[0], current_y + n[1]):
                    next_move.append(('E', current_x, current_y, current_x + n[0], current_y + n[1]))

            # add jumps
            previous_position = [(current_x, current_y)]
            jump_list = [(current_x, current_y)]
            hash_jumps = []

            while (len(jump_list) > 0):
                current_piece = jump_list[0]
                jump_list = jump_list[1:]
                itr_jumps, previous_position = one_step_jump(board, current_piece[0], current_piece[1],
                                                             previous_position)

                for each_jump in itr_jumps:
                    hash_jumps.append((current_piece[0], current_piece[1], each_jump[0], each_jump[1]))
                    jump_list.append((each_jump[0], each_jump[1]))

            if len(hash_jumps) > 0:
                jumps = reform_hash_jump_ismoveout(hash_jumps, campus)
                next_move = next_move + jumps


        # move piece farther from center of campus
        if len(next_move)==0:
            next_move = move_away(board,color,intersection)


    # moving pieces out of campus
    if len(intersection) == 0 or len(next_move) == 0:

        # start search move
        for each_piece in current_positions:
            current_x = each_piece[0]
            current_y = each_piece[1]
            # add moves
            for n in EIGHT_NEIGHBOR:
                if 0 <= current_x + n[0] <= 15 and 0 <= current_y + n[1] <= 15 and board[current_x + n[0]][
                    current_y + n[1]] == '.' and \
                        is_valid_move(campus, current_x, current_y, current_x + n[0], current_y + n[1]):
                    next_move.append(('E', current_x, current_y, current_x + n[0], current_y + n[1]))

            # add jumps     one_step_jump(board,start_x,start_y,previous_position)
            previous_position = [(current_x, current_y)]
            jump_list = [(current_x, current_y)]
            hash_jumps = []

            while (len(jump_list) > 0):
                current_piece = jump_list[0]
                jump_list = jump_list[1:]
                itr_jumps, previous_position = one_step_jump(board, current_piece[0], current_piece[1],
                                                             previous_position)

                for each_jump in itr_jumps:
                    hash_jumps.append((current_piece[0], current_piece[1], each_jump[0], each_jump[1]))
                    jump_list.append((each_jump[0], each_jump[1]))

            if len(hash_jumps) > 0:
                jumps = reform_hash_jump(hash_jumps, campus)
                next_move = next_move + jumps

    return next_move





def alpha_beta(depth_limit, board, my_color, my_campus, my_positions, corner, oppo_color, oppo_campus,
              oppo_positions):
    depth = 0
    alpha = 0
    beta = 99999

    action = max_value(depth_limit, depth, board, my_color, my_campus, my_positions, corner, oppo_color, oppo_campus,
              oppo_positions, alpha, beta)

    return action[1]


def max_value(depth_limit,depth,board,my_color,my_campus,my_positions, corner,oppo_color,oppo_campus,oppo_positions,alpha,beta):

    if depth == depth_limit:
        value = eval(my_positions, corner)
        return value

    moves = get_possible_move(board, my_color, my_positions,my_campus)

    all_values = []
    v=0
    for i in range(0, len(moves)):
        possible_position = my_positions
        one_move = moves[i]

        if one_move[0] == 'E':
            start_position = (one_move[1], one_move[2])
            end_position = (one_move[3], one_move[4])
        else:
            start_position = (one_move[1][0], one_move[1][1])
            temp = len(one_move)-1
            end_position = (one_move[temp][0], one_move[temp][1])
        index = possible_position.index(start_position)

        possible_position = possible_position[:index] + [end_position] + possible_position[index + 1:]


        value = min_value(depth_limit,depth+1,board, oppo_color, oppo_campus, oppo_positions, corner, my_color, my_campus, possible_position,alpha,beta)

        if type(value) is tuple:
            value = value[0]

        v = max(v,value)
        if v>=beta:
            return (v,one_move)
        alpha = max(alpha,v)
        all_values.append(value)
        if value>7000:
            print(one_move)
            print(value)

    index = all_values.index(v)
    return (v,moves[index])






def min_value(depth_limit, depth, board, my_color, my_campus, my_positions, corner, oppo_color, oppo_campus,
              oppo_positions, alpha, beta):
    if depth == depth_limit:
        value = eval(oppo_positions, corner)
        return value

    moves = get_possible_move(board, my_color, my_positions, my_campus)
    all_values = []
    v = 99999
    for i in range(0, len(moves)):
        possible_position = my_positions
        one_move = moves[i]
        if one_move[0] == 'E':
            start_position = (one_move[1], one_move[2])
            end_position = (one_move[3], one_move[4])
        else:
            start_position = (one_move[1][0], one_move[1][1])
            temp = len(one_move) - 1
            end_position = (one_move[temp][0], one_move[temp][1])
        index = possible_position.index(start_position)
        possible_position = possible_position[:index] + [end_position] + possible_position[index + 1:]

        value = max_value(depth_limit, depth + 1, board, oppo_color, oppo_campus, oppo_positions, corner, my_color,
                          my_campus, possible_position, alpha, beta)

        if type(value) is tuple:
            value = value[0]

        v = min(v, value)
        if v <= alpha:
            return (v, one_move)
        beta = min(beta, v)
        all_values.append(value)

    index = all_values.index(v)
    return (v, moves[index])





# main
filename = 'input.txt'
with open(filename) as f:
    content = f.readlines()
content = [x.strip() for x in content]

mode = content[0]
color = content[1]
total_time = float(content[2])

board = []
for i in range(0,16):
    temp = content[3+i]
    temp1 = [j for j in temp]
    board.append(temp1)
board = [*zip(*board)]


campus = []
target_campus = []
oppo_campus = []
target_corner = ()
if color == 'WHITE':
    color = 'W'
    oppo_color = 'B'
    campus = WHITE_CAMPUS
    target_campus = BLACK_CAMPUS
    oppo_campus = BLACK_CAMPUS
    target_corner = (15,15)
else:
    color = 'B'
    oppo_color = 'W'
    campus = BLACK_CAMPUS
    target_campus = WHITE_CAMPUS
    oppo_campus = WHITE_CAMPUS
    target_corner = (0, 0)


# get current position
current_positions = []
oppo_positions = []
for i in range(0, 16):
    for j in range(0, 16):
        if board[i][j] == color:
            current_positions.append((i,j))
        elif board[i][j]!='.':
            oppo_positions.append((i,j))



outFile = open('output.txt', 'w')
# single mode
if mode == 'SINGLE':
    #moves = get_possible_move(board,color,current_positions,campus)
    #one_turn = moves[0]
    depth_limit = 1
    action = alpha_beta(depth_limit, board, color, campus, current_positions, target_corner, oppo_color, oppo_campus,
                        oppo_positions)

    if action[0]=='E':
        print('E '+str(action[1])+','+str(action[2])+' '+str(action[3])+','+str(action[4]), file=outFile)
    else:
        for i in range(1,len(action)-1):
            print_string = 'J '+str(action[i][0])+','+str(action[i][1])+' '+str(action[i+1][0])+','+str(action[i+1][1])
            print(print_string,file=outFile)

    #print(action)

# game mode
else:
    # Determine depth
    depth_limit = 3

    if len(list(set(oppo_campus) & set(current_positions)))>16:
        depth_limit=3
        temp = list(set(current_positions) - set(oppo_campus))
        last_piece = temp[0]
        temp = list(set(oppo_campus) - set(current_positions))
        last_hole = temp[0]
        if abs(last_piece[0]-last_hole[0])==1 or abs(last_piece[1]-last_hole[1])==1:
            depth_limit=1

    else:
        filename = 'calibration.txt'
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        suggest_time = float(content[0])
        if suggest_time>total_time*0.05:
            depth_limit=1
        elif total_time*0.01<suggest_time<=total_time*0.05:
            depth_limit = 2



    action = alpha_beta(depth_limit, board, color, campus, current_positions, target_corner, oppo_color, oppo_campus,
               oppo_positions)


    if action[0]=='E':
        print('E '+str(action[1])+','+str(action[2])+' '+str(action[3])+','+str(action[4]), file=outFile)
    else:
        for i in range(1,len(action)-1):
            print_string = 'J '+str(action[i][0])+','+str(action[i][1])+' '+str(action[i+1][0])+','+str(action[i+1][1])
            print(print_string,file=outFile)


outFile.close()



