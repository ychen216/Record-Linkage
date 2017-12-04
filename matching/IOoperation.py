import os
import pandas

def load_people_record_test():
    return _load_record_data('record_test.csv')

def load_people_record():
    return _load_record_data('record_title.csv')

def _load_record_data(filename):

    filepath = os.path.join(filename)

    record_data = pandas.read_csv(filepath,
                                  index_col="ID",
                                  sep=",",
                                  engine='python',
                                  skipinitialspace=True,
                                  encoding='utf-8',
                                  dtype={
                                      "STNUM": object,
                                      "EmplyeeID": object,
                                      "SSN": object,
                                      "ZIP": object
                                  })

    return record_data

def write_result(filename, class_list):
    '''
    
    :param filename: result filename
    :param class_list: include result id set,format like id1,id2,id3...
    :return: 
    '''
    write_path = os.path.join(filename)
    outfile = open(write_path, 'w')
    for same_class in class_list:
        list_len = len(same_class)
        line = str(same_class[0])
        for i in range(1, list_len):
            line = line + ',' + str(same_class[i])
        line = line + '\n'
        outfile.write(line)
    outfile.close()

def write_pair(filename, pair_list):
    '''
    write similar pair id list to file
    :param filename: result_pair filename
    :param pair_list: [[4, 5], [0, 1], [8, 9]]
    :return:
    '''
    write_path = os.path.join(filename)
    outfile = open(write_path, 'w')
    for pair in pair_list:
        outfile.write(str(pair[0])+","+str(pair[1])+'\n')
    outfile.close()

def get_result_list(cluster_list):
    '''

    :param cluster_list: similar pair list [[4, 5], [0, 1], [8, 9]]
    :return:type list and each element is set which contains elements belonging to same class
    '''
    # TODO
    # index == i need to be added into with list
    res_list = []
    index_dict = dict()
    for pair in cluster_list:
        if pair[0] in index_dict:
            res_list[index_dict[pair[0]]].add(pair[0])
            res_list[index_dict[pair[0]]].add(pair[1])
            if pair[1] not in index_dict:
                index_dict[pair[1]] = index_dict[pair[0]]
            else:
                res_list[index_dict[pair[1]]].add(pair[0])
                res_list[index_dict[pair[1]]].add(pair[1])

        elif pair[1] in index_dict:
            res_list[index_dict[pair[1]]].add(pair[0])
            res_list[index_dict[pair[1]]].add(pair[1])
            if pair[0] not in index_dict:
                index_dict[pair[0]] = index_dict[pair[1]]
            else:
                res_list[index_dict[pair[0]]].add(pair[0])
                res_list[index_dict[pair[0]]].add(pair[1])
        else:
            index_dict[pair[0]] = index_dict[pair[1]] = len(res_list)
            res_list.append(set())
            res_list[index_dict[pair[0]]].add(pair[0])
            res_list[index_dict[pair[0]]].add(pair[1])
    # each element inside is ordered
    final_list = []
    for item in res_list:
        final_list.append(sorted(item))
    final_list.sort(cmp=cmp_fist_element)
    # print final_list
    return final_list

def cmp_fist_element(list1, list2):
    return list1[0] - list2[0]

if  __name__  ==  "__main__":
    x = [[8,7],[5,1],[2,5],[1,3]]
    get_result_list(x)