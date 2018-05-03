#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import get_my_friends
import get_moods
import get_qq_number


if __name__ == '__main__':

    # 先获取包含好友QQ号码的文件
    get_friends_obj = get_my_friends.Get_friends_number()
    get_friends_obj.get_friends()

    # Second, deal with this data, clean it
    # From the get_friends result get the useful data
    # And save it to file qqnumber.inc
    # The format of this file just a list
    # 然后，从这些文件里面提取出QQ号码
    get_qq_item_obj = get_qq_number.exact_data_from_result()
    get_qq_item_obj.exact_qq_number()

    # Finally, use the cleaned data to get mood
    # Base on last step's qqnumber.inc file
    # exact the qq number and start to get their moods
    # 最后，根据每一个QQ号码去获取对应的动态
    get_moods_obj = get_moods.Get_moods_start()
    get_moods_obj.get_moods_start()
