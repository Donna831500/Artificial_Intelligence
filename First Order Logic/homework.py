import filecmp

def get_negate_query(s):
    if s[len(s) - 1] == True:
        result = s[:len(s) - 1] + [False]
    else:
        result = s[:len(s) - 1] + [True]
    return result


def is_Variable(s):
    if len(s) == 1 and s.islower():
        return True
    else:
        return False


def get_predicate(s):
    temp = s.split('(')
    predicate_name = temp[0]
    temp2 = temp[1][:len(temp[1]) - 1]
    parameters = temp2.split(',')

    if predicate_name[0] == '~':
        result = [predicate_name[1:]] + parameters + [False]
    else:
        result = [predicate_name] + parameters + [True]
    return result


def get_CNF_KB(s_list):
    KB_i = []
    KB_p = []
    for i in range(0, len(s_list)):
        s = s_list[i]
        temp = s.split('=>')
        if len(temp) == 1:
            result = get_predicate(temp[0].strip())
            KB_p.append(result)
        else:
            condition = temp[0]
            conclusion = get_predicate(temp[1].strip())
            all_condition = condition.split('&')
            result = []
            for i in range(0, len(all_condition)):
                temp_condition = get_negate_query(get_predicate(all_condition[i].strip()))
                result.append(temp_condition)
            result.append(conclusion)
            KB_i.append(result)
    return KB_p, KB_i


def variable_match(p1, p2):
    parameter_match = True
    substitution_list_1_variable = []
    substitution_list_1_constant = []
    substitution_list_1 = []
    substitution_list_2 = []
    substitution_list_2_variable = []
    substitution_list_2_constant = []
    variable_match_variable = []
    for k in range(1, len(p1) - 1):
        # 1. if first and last contain different constant
        if p1[k] != p2[k] and not is_Variable(p1[k]) and not is_Variable(p2[k]):
            parameter_match = False
        # 2. if first is variable and second is constant
        if is_Variable(p1[k]) and not is_Variable(p2[k]):
            if (p1[k], p2[k]) not in substitution_list_1 and p1[k] not in substitution_list_1_variable:
                substitution_list_1.append((p1[k], p2[k]))
                substitution_list_1_variable.append(p1[k])
                substitution_list_1_constant.append(p2[k])
            elif (p1[k], p2[k]) not in substitution_list_1 and p1[k] in substitution_list_1_variable:
                parameter_match = False

        # 3. if first is constant and second is variable
        if not is_Variable(p1[k]) and is_Variable(p2[k]):
            if (p2[k], p1[k]) not in substitution_list_2 and p2[k] not in substitution_list_2_variable:
                substitution_list_2.append((p2[k], p1[k]))
                substitution_list_2_variable.append(p2[k])
                substitution_list_2_constant.append(p1[k])
            elif (p2[k], p1[k]) not in substitution_list_2 and p2[k] in substitution_list_2_variable:
                parameter_match = False

        # 4. if both first and second are variable
        if is_Variable(p1[k]) and is_Variable(p2[k]):
            if (p1[k], p2[k]) not in variable_match_variable:
                variable_match_variable.append((p1[k], p2[k]))

    if parameter_match:
        for i in range(0, len(variable_match_variable)):
            first_v = variable_match_variable[i][0]
            second_v = variable_match_variable[i][1]
            if first_v in substitution_list_1_variable and second_v in substitution_list_2_variable:
                index = substitution_list_1_variable.index(first_v)
                if substitution_list_1_constant[index] != substitution_list_2_constant[index]:
                    parameter_match = False

    return parameter_match


def is_contradiction(KB_p):
    for i in range(0, len(KB_p) - 1):
        for j in range(i + 1, len(KB_p)):
            first = KB_p[i]
            second = KB_p[j]
            if first[0] == second[0] and first[len(first) - 1] != second[len(first) - 1] and variable_match(first,
                                                                                                            second):
                return True
    return False


def substitude_variable_in_imp(variable, constant, imp):
    imp_copy = imp[:]
    result = []
    for i in range(0, len(imp_copy)):
        temp = imp_copy[i]
        temp_result = [constant if x == variable else x for x in temp]
        result.append(temp_result)
    return result


def substitude_variable_in_pre(variable, constant, pre):
    pre_copy = pre[:]
    result = [constant if x == variable else x for x in pre_copy]
    return result


def i_and_p_infer(pre, imp):
    result = []
    for i in range(0, len(imp)):
        imp_copy = imp[:]
        pre_copy = pre[:]

        if pre_copy[0] == imp_copy[i][0] and pre_copy[len(pre_copy) - 1] != imp_copy[i][len(pre_copy) - 1]:
            p1 = pre_copy
            p2 = imp_copy[i]
            if variable_match(p1, p2):
                for j in range(1, len(pre_copy) - 1):
                    for repeat in range(0, 2):
                        # if pre is variable and imp is constant
                        if not is_Variable(imp_copy[i][j]) and is_Variable(pre_copy[j]):
                            variable = pre_copy[j]
                            constant = imp_copy[i][j]
                            pre_copy = substitude_variable_in_pre(variable, constant, pre_copy)

                        # if pre is constant and imp is variable
                        elif is_Variable(imp_copy[i][j]) and not is_Variable(pre_copy[j]):
                            constant = pre_copy[j]
                            variable = imp_copy[i][j]
                            imp_copy = substitude_variable_in_imp(variable, constant, imp_copy)

                result.append(imp_copy[:i] + imp_copy[i + 1:])
    # print(result)
    return result


def KBI_and_KBP(KB_i, KB_p):
    new_message = []
    for i in range(0, len(KB_p)):
        for j in range(0, len(KB_i)):
            pre = KB_p[i]
            imp = KB_i[j]
            new_message = new_message + i_and_p_infer(pre, imp)

    # return new_message
    new_i = []
    new_p = []
    for i in range(0, len(new_message)):
        if len(new_message[i]) == 1:
            new_p.append(new_message[i])
        elif len(new_message[i]) > 1:
            new_i.append(new_message[i])

    return new_i, new_p




def drop_duplication_imp(imp):
    imp_copy = imp[:]
    dup_i = 0
    while dup_i > -1 and len(imp_copy) > 0:
        dup_i = -1
        dup_j = -1
        for i in range(0, len(imp_copy) - 1):
            for j in range(i + 1, len(imp_copy)):
                p1 = imp_copy[i]
                p2 = imp_copy[j]
                if p1[0] == p2[0] and p1[len(p1) - 1] == p2[len(p1) - 1] and variable_match(p1, p2):
                    dup_i = i
                    dup_j = j
        if dup_i > -1:
            imp_copy = imp_copy[:dup_j] + imp_copy[dup_j + 1:]
            imp_copy = imp_copy[:dup_i] + imp_copy[dup_i + 1:]

    return imp_copy




def file_are_same(file1,file2):
    result = True
    with open(file1) as f:
        content1 = f.readlines()
    content1 = [x.strip() for x in content1]
    with open(file2) as f2:
        content2 = f2.readlines()
    content2 = [x.strip() for x in content2]

    for i in range(0,len(content1)):
        if content1[i]!=content2[i]:
            result=False
    return result



for testfile in range(25,26):

    filename = 'input_'+str(testfile)+'.txt'
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    number_of_query = int(content[0])
    query_list = []
    for i in range(0, number_of_query):
        temp = content[1 + i]
        query_list.append(temp)

    number_of_sentence = int(content[number_of_query + 1])
    sentence_list = []
    for i in range(0, number_of_sentence):
        temp = content[number_of_query + 2 + i]
        sentence_list.append(temp)

    original_KB_p, original_KB_i = get_CNF_KB(sentence_list)

    outFile = open('output.txt', 'w')
    for i in range(0, number_of_query):
        KB_p = original_KB_p[:]
        KB_i = original_KB_i[:]
        current_query = query_list[i]
        query = get_predicate(current_query)
        negate_query = get_negate_query(query)
        KB_p.append(negate_query)
        find_contradiction = is_contradiction(KB_p)

        total_new_infer = 1

        #print('query: '+str(i))
        while total_new_infer > 0 and not find_contradiction:
            #print('stuck first???')
            new_i, new_p = KBI_and_KBP(KB_i, KB_p)
            # adding new predicate
            for j in range(0, len(new_p)):
                KB_p.append(new_p[j][0])
            find_contradiction = is_contradiction(KB_p)
            total_new_infer = len(new_i) + len(new_p)
            KB_i = new_i[:]


        if not find_contradiction:
            KB_i = original_KB_i[:]
            total_new_infer = 1

            while total_new_infer > 0 and not find_contradiction:
                #print('stuck second???')
                new_i, new_p = KBI_and_KBP(KB_i, KB_p)
                # adding new predicate
                for j in range(0, len(new_p)):
                    KB_p.append(new_p[j][0])
                find_contradiction = is_contradiction(KB_p)
                total_new_infer = len(new_i) + len(new_p)
                KB_i = new_i[:]



        if find_contradiction:
            print(str('TRUE'), file=outFile)
        else:
            print(str('FALSE'), file=outFile)
    outFile.close()


    answerfile = 'output_'+str(testfile)+'.txt'
    compare_result = file_are_same(answerfile,'output.txt')
    if compare_result:
        print('test '+str(testfile)+' : PASS')
    else:
        print('test ' + str(testfile) + ' : FAIL')

        # print outputfile
        with open('output.txt') as f3:
            content3 = f3.readlines()
        content3 = [x.strip() for x in content3]

        print('output: ')
        for hhh in range(0,len(content3)):
             print(content3[hhh])
