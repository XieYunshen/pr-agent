"""
本地保存文件
"""
import logging
import json
import re
import time
import os

import socket
import urllib.parse
import urllib.request



def save_pr_info(file_name, pr_link, icafe_card_num, pr_info):
    """
    保存报告信息,用于展示
    """
    info_file_path = 'pr-info-dir_' + time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(info_file_path):
        os.makedirs(info_file_path)
    logging.info("pr info file will save to: " + info_file_path)
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
    info_file_path = 'pr-info-dir_' + time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(info_file_path):
        os.makedirs(info_file_path)
    logging.info("pr info file will save to: " + info_file_path)
    """
    保存格式化报告信息,后续加载
    """
    pr_info['pr_link']=pr_link
    pr_info['icafe_card_num']=','.join(icafe_card_num)
    with open(info_file_path + '/' + file_name, 'w') as f:
        json.dump(pr_info, f)
    logging.info("write to json_file done!")


def write_json(file_name, info_file_path=None, **kwargs):
    """
    保存信息到json文件
    """
    if info_file_path == None:
        info_file_path = 'pr-info-dir_' + time.strftime("%Y-%m-%d", time.localtime())
    if not os.path.exists(info_file_path):
        os.makedirs(info_file_path)
    logging.info("pr info file will save to: " + info_file_path)
    """
    保存格式化报告信息,后续加载
    """
    with open(info_file_path + '/' + file_name, 'w') as f:
        json.dump(kwargs, f)
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


class HttpService:
    def post(self, url, params, timeout=50):
        return self.__service(url, params, timeout=timeout)

    def get(self, url, timeout=50):
        return self.__service(url, timeout=timeout)

    # timeout 50s
    def __service(self, url, params=None, timeout=50):
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            # POST
            if params:
                data = urllib.parse.urlencode(params).encode('utf-8')
                request = urllib.request.Request(url, data)
            # GET
            else:
                request = urllib.request.Request(url)
            request.add_header('Accept-Language', 'zh-cn')
            with urllib.request.urlopen(request) as response:
                content = response.read().decode('utf-8')
                if response.code == 200:
                    return content, True
                return content, False
        except Exception as ex:
            return str(ex), False
        finally:
            socket.setdefaulttimeout(old_timeout)


def get_card_info(card_id):
    icafe_url = os.getenv("icafe_url")
    icafe_user = os.getenv("icafe_user")
    icafe_passwd = os.getenv("icafe_passwd")
    get_data = ''
    get_data += '&u=' + icafe_user
    get_data += '&pw=' + icafe_passwd
    get_data += '&showAssociations=false'
    http_service = HttpService()
    try:
        content, _ = http_service.get("{}/api/spaces/{}/cards/{}?{}".format(icafe_url, "DLTP", card_id, get_data))
    except Exception:
        print('time out')
        return None
    content = json.loads(content)["cards"][0]
    card_title = content['title']
    card_created_user = content['createdUser']
    card_parent_info = content['parent']
    card_responsible_people = content['responsiblePeople']
    
    return card_title, card_created_user, card_responsible_people, card_parent_info


if __name__ == "__main__":
    card_title, card_created_user, card_responsible_people, card_parent_info = get_card_info("67010")
    write_json(file_name="test.json", 
               card_title=card_title, 
               card_created_user=card_created_user, 
               card_responsible_people=card_responsible_people, 
               card_parent_info=card_parent_info)
    exit()
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