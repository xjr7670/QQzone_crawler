
import json
import os

class exact_data_from_result(object):
    '''Define method to get my qq friends data from result
       and get my mood data from result'''

    def __init__(self):
        print("Start to exact the qq number item from get_friends result")

    def exact_qq_number(self):
        '''Get qq number data from json file'''
        friendsFiles = [x for x in os.listdir('friends') if x.endswith("json")]

        qqnumber_item = []
        i = 0
        for each_file in friendsFiles:
            with open('friends/' + each_file) as f:
                source = f.read()
                con_dict = source[75:-4].replace('\n', '')
                con_json = json.loads(con_dict)
                friends_list = con_json['uinlist']

                # Get each item from friends list, each item is a dict
                for item in friends_list:
                    i = i + 1
                    qqnumber_item.append(item)
        else:
            with open('qqnumber.inc', 'w') as qqfile:
                qqfile.write(str(qqnumber_item))
