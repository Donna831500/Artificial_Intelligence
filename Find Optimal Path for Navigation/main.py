import queue

def create_cost_table(wide,height):
    cost_table = []
    for i in range(0,wide):
        temp = []
        for j in range(0,height):
            temp.append(-1)
        cost_table.append(temp)
    return cost_table

def create_parent_table(wide,height):
    parent_table = []
    for i in range(0,wide):
        temp = []
        for j in range(0,height):
            temp.append((-1,-1))
        parent_table.append(temp)
    return parent_table

def get_estimate_cost(map,end_x,end_y,x,y):
    abs_x = abs(end_x-x)
    abs_y = abs(end_y - y)
    height_diff = abs(map[x][y]-map[end_x][end_y])
    result = (min(abs_x,abs_y)*14)+(10*abs(abs_x-abs_y))+height_diff
    return result



filename = 'input.txt'
with open(filename) as f:
    content = f.readlines()
content = [x.strip() for x in content]

algorithm = content[0]
temp = content[1].split()
W = int(temp[0])
H = int(temp[1])
temp = content[2].split()
start_X = int(temp[0])
start_Y = int(temp[1])
max_diff = int(content[3])
N = int(content[4])


target_location = []
for i in range(0,N):
    temp = content[5+i].split()
    temp_X = int(temp[0])
    temp_Y = int(temp[1])
    target_location.append([temp_X,temp_Y])


map = []
for i in range(0,H):
    temp = content[5+N+i].split()
    temp = [int(j) for j in temp]
    map.append(temp)
map = [*zip(*map)]

outFile = open('output.txt', 'w')



if algorithm == 'BFS':
    # (location, height, parent_location) #
    for each_target in target_location:
        target_x = each_target[0]
        target_y = each_target[1]
        findSol = False
        Q = queue.Queue()
        start_node = ((start_X,start_Y),map[start_X][start_Y],(start_X,start_Y))
        Q.put(start_node)
        explored_node = []
        explored_location = []
        explored_location.append((start_X, start_Y))
        while(not findSol and Q.qsize()!=0):
            current_node = Q.get()
            explored_node.append(current_node)
            current_x = current_node[0][0]
            current_y = current_node[0][1]
            current_height = current_node[1]
            if current_x==target_x and current_y==target_y:
                findSol = True
            else:
                for i in range(-1,2):
                    for j in range(-1,2):
                        temp_x = current_x + i
                        temp_y = current_y + j
                        is_original_location = False
                        if (i==0 and j==0):
                            is_original_location = True
                        if(0 <= temp_x < W and 0 <= temp_y < H and (abs(map[temp_x][temp_y] - current_height))<=max_diff
                            and (not (temp_x,temp_y) in explored_location) and not is_original_location):
                            temp_node = ((temp_x,temp_y),map[temp_x][temp_y],(current_x,current_y))
                            explored_location.append((temp_x, temp_y))
                            Q.put(temp_node)

        if(not findSol):
            print('FAIL', file=outFile)

        else:
            path = []
            path.append((current_x,current_y))
            counter = len(explored_node)-1
            while(current_x!=start_X or current_y!=start_Y):
                current_node = explored_node[counter]
                if(current_x == current_node[0][0] and current_y == current_node[0][1]):
                    current_x = current_node[2][0]
                    current_y = current_node[2][1]
                    path.append((current_x, current_y))
                counter = counter-1

            path = path[::-1]
            path_str = ''
            for each_location in path:
                path_str = path_str+str(each_location[0])+','+str(each_location[1])+' '
            print(str(path_str), file=outFile)




elif algorithm == 'UCS':
    # (cost, location, height) #
    for each_target in target_location:
        cost_table = create_cost_table(W,H)
        cost_table[start_X][start_Y]=0
        parent_table = create_parent_table(W,H)
        parent_table[start_X][start_Y] = (start_X,start_Y)

        target_x = each_target[0]
        target_y = each_target[1]

        findSol = False
        open_node = []
        closed_node = []
        open_location = []
        closed_location = []
        start_node = (0, (start_X, start_Y), map[start_X][start_Y])
        open_node.append(start_node)
        open_location.append((start_X, start_Y))
        while(not findSol and len(open_node)>0):
            current_node = open_node[0]
            open_node = open_node[1:]
            current_cost = current_node[0]
            current_x = current_node[1][0]
            current_y = current_node[1][1]
            current_height = current_node[2]
            if current_x==target_x and current_y==target_y:
                findSol = True
            else:   # expand children
                for i in range(-1,2):
                    for j in range(-1,2):
                        temp_x = current_x + i
                        temp_y = current_y + j
                        if 0 <= temp_x < W and 0 <= temp_y < H and (abs(map[temp_x][temp_y] - current_height))<=max_diff:
                            bonus_cost = 10
                            if abs(i)+abs(j)==2:
                                bonus_cost = 14

                            if (not (temp_x,temp_y) in open_location) and (not (temp_x,temp_y) in closed_location):
                                temp_node = (current_cost+bonus_cost,(temp_x,temp_y),map[temp_x][temp_y])
                                open_node.append(temp_node)
                                open_location.append((temp_x,temp_y))
                                cost_table[temp_x][temp_y] = current_cost+bonus_cost
                                parent_table[temp_x][temp_y] = (current_x,current_y)

                            elif (temp_x,temp_y) in open_location and (current_cost + bonus_cost)< cost_table[temp_x][temp_y]:
                                new_cost = current_cost + bonus_cost
                                if new_cost< cost_table[temp_x][temp_y]:
                                    open_node.remove((cost_table[temp_x][temp_y], (temp_x,temp_y), map[temp_x][temp_y]))
                                    open_node.append((new_cost, (temp_x,temp_y), map[temp_x][temp_y]))
                                    cost_table[temp_x][temp_y] = current_cost + bonus_cost
                                    parent_table[temp_x][temp_y] = (current_x, current_y)

                            elif (temp_x,temp_y) in closed_location and (current_cost + bonus_cost)< cost_table[temp_x][temp_y]:
                                new_cost = current_cost + bonus_cost
                                if new_cost< cost_table[temp_x][temp_y]:
                                    closed_node.remove((cost_table[temp_x][temp_y], (temp_x,temp_y), map[temp_x][temp_y]))
                                    closed_location.remove((temp_x,temp_y))
                                    open_node.append((new_cost, (temp_x,temp_y), map[temp_x][temp_y]))
                                    cost_table[temp_x][temp_y] = current_cost + bonus_cost
                                    parent_table[temp_x][temp_y] = (current_x, current_y)


                closed_node.append(current_node)
                closed_location.append((current_x,current_y))
                open_node.sort()


        if(not findSol):
            print('FAIL', file=outFile)
        else:
            path = []
            path.append((current_x,current_y))
            while(current_x!=start_X or current_y!=start_Y):
                temp_x = parent_table[current_x][current_y][0]
                temp_y = parent_table[current_x][current_y][1]
                path.append((temp_x, temp_y))
                current_x = temp_x
                current_y = temp_y
            path = path[::-1]
            path_str = ''
            for each_location in path:
                path_str = path_str+str(each_location[0])+','+str(each_location[1])+' '
            print(str(path_str), file=outFile)




elif algorithm == 'A*':
    for each_target in target_location:
        cost_table = create_cost_table(W,H)
        cost_table[start_X][start_Y]=0
        parent_table = create_parent_table(W,H)
        parent_table[start_X][start_Y] = (start_X,start_Y)

        target_x = each_target[0]
        target_y = each_target[1]

        findSol = False
        open_node = []
        closed_node = []
        open_location = []
        closed_location = []
        est_cost = get_estimate_cost(map,target_x,target_y,start_X,start_Y)
        start_node = (est_cost, 0, (start_X, start_Y), map[start_X][start_Y])
        open_node.append(start_node)
        open_location.append((start_X, start_Y))
        while(not findSol and len(open_node)>0):
            current_node = open_node[0]
            open_node = open_node[1:]
            current_cost = current_node[1]
            current_x = current_node[2][0]
            current_y = current_node[2][1]
            current_height = current_node[3]
            if current_x==target_x and current_y==target_y:
                findSol = True
            else:
                for i in range(-1,2):
                    for j in range(-1,2):
                        temp_x = current_x + i
                        temp_y = current_y + j
                        if 0 <= temp_x < W and 0 <= temp_y < H and (abs(map[temp_x][temp_y] - current_height))<=max_diff:
                            bonus_cost = 10
                            if abs(i)+abs(j)==2:
                                bonus_cost = 14
                            bonus_cost = bonus_cost+(abs(map[temp_x][temp_y] - current_height))
                            est_cost = get_estimate_cost(map,target_x,target_y,temp_x,temp_y)

                            if (not (temp_x,temp_y) in open_location) and (not (temp_x,temp_y) in closed_location):
                                temp_node = (est_cost+current_cost+bonus_cost,current_cost+bonus_cost,(temp_x,temp_y),map[temp_x][temp_y])
                                open_node.append(temp_node)
                                open_location.append((temp_x,temp_y))
                                cost_table[temp_x][temp_y] = current_cost+bonus_cost
                                parent_table[temp_x][temp_y] = (current_x,current_y)

                            elif (temp_x,temp_y) in open_location and (current_cost + bonus_cost)< cost_table[temp_x][temp_y]:
                                new_cost = current_cost + bonus_cost
                                if new_cost< cost_table[temp_x][temp_y]:
                                    open_node.remove((cost_table[temp_x][temp_y]+est_cost, cost_table[temp_x][temp_y], (temp_x,temp_y), map[temp_x][temp_y]))
                                    open_node.append((new_cost+est_cost,new_cost, (temp_x,temp_y), map[temp_x][temp_y]))
                                    cost_table[temp_x][temp_y] = current_cost + bonus_cost
                                    parent_table[temp_x][temp_y] = (current_x, current_y)

                            elif (temp_x,temp_y) in closed_location and (current_cost + bonus_cost)< cost_table[temp_x][temp_y]:
                                new_cost = current_cost + bonus_cost
                                if new_cost< cost_table[temp_x][temp_y]:
                                    closed_node.remove((cost_table[temp_x][temp_y]+est_cost, cost_table[temp_x][temp_y], (temp_x,temp_y), map[temp_x][temp_y]))
                                    closed_location.remove((temp_x,temp_y))
                                    open_node.append((new_cost+est_cost,new_cost, (temp_x,temp_y), map[temp_x][temp_y]))
                                    cost_table[temp_x][temp_y] = current_cost + bonus_cost
                                    parent_table[temp_x][temp_y] = (current_x, current_y)


                closed_node.append(current_node)
                closed_location.append((current_x,current_y))
                open_node.sort()


        if(not findSol):
            print('FAIL', file=outFile)
        else:
            path = []
            path.append((current_x,current_y))
            while(current_x!=start_X or current_y!=start_Y):
                temp_x = parent_table[current_x][current_y][0]
                temp_y = parent_table[current_x][current_y][1]
                path.append((temp_x, temp_y))
                current_x = temp_x
                current_y = temp_y
            path = path[::-1]
            path_str = ''
            for each_location in path:
                path_str = path_str+str(each_location[0])+','+str(each_location[1])+' '
            print(str(path_str), file=outFile)


outFile.close()