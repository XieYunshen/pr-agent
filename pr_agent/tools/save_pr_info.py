"""
本地保存文件
"""
import logging
import json
import re
import time
import os


info_file_path = 'pr-info-dir_' + time.strftime("%Y-%m-%d", time.localtime())
# print(info_file_path)
logging.info("pr info file will save to: " + info_file_path)
if not os.path.exists(info_file_path):
    os.makedirs(info_file_path)


def save_pr_info(file_name, pr_link, icafe_card_num, pr_info):
    """
    保存报告信息,用于展示
    """
    with open(info_file_path + '/' + file_name, 'w') as f:
        f.write("======= pr link ======\n")
        f.write(pr_link)
        f.write("\n")
        f.write("======= icafe card num ======\n")
        f.write(','.join(icafe_card_num))
        f.write("\n")
        f.write("======= pr info ======\n")
        for key, value in pr_info.items():
            f.write(key + ":\t" + value + "\n")
    logging.info("write to json_file done!")


def save_pr_info_json(file_name, pr_link, icafe_card_num, pr_info):
    """
    保存格式化报告信息,后续加载
    """
    pr_info['pr_link']=pr_link
    pr_info['icafe_card_num']=','.join(icafe_card_num)
    with open(info_file_path + '/' + file_name, 'w') as f:
        json.dump(pr_info, f)
    logging.info("write to json_file done!")


def get_pr_card_num(info):
    if info is None:
        return ''
    # parttern="Pcard-\d+"
    pattern = re.compile(r'Pcard-\d+', re.IGNORECASE)
    result = pattern.findall(info)
    res = []
    try:
        for item in result:
            print(item)
            res.append(item)
    except Exception as e:
        print(e)
    return res


if __name__ == "__main__":
    test_txt="""
    ## PR Type:
Enhancement

___
## PR Description:
This PR introduces a new script named get_pr_ut.py. The script is designed to enhance the testing capabilities of the project by obtaining PR mapping unit tests.
Pcard-67005

___
## PR Main Files Walkthrough:
`get_pr_ut.py`: This is a new file added in this PR. It is likely used for obtaining PR mapping unit tests.
    """
    # res = get_pr_card_num(test_txt)
    # print(res)
    # test_list = []
    # print(','.join(test_list))
    # print(time.asctime(time.localtime()))
    print(time.strftime("%Y-%m-%d", time.localtime()))
    # print(time.strptime(time.localtime(), "%Y-%m-%d %H:%M:%S"))