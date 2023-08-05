from DobotEDU import DobotEDU
import requests
import json
import base64


def test_shili():
    do = DobotEDU()
    assert do.__init__


def test_shili2():
    do = DobotEDU('222', '333')
    assert do.__init__


def test_shili3():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    assert dobotEdu.__init__


def test_tx():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    r = dobotEdu.nlp.topic('警方通报女游客无故推倒景区设施：由于个人生活发生重大变故导致情绪行为')
    # print(r)
    assert type(r) is str


def test_settoken():
    dobotEdu = DobotEDU()
    url = "https://dobotlab.dobot.cc/api/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {"account": "yuejiang", "password": "YJ123456"}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    token = json.loads(r.content.decode())["data"]["token"]
    dobotEdu.token = token
    print(token)
    r = dobotEdu.nlp.topic('警方通报女游客无故推倒景区设施：由于个人生活发生重大变故导致情绪行为')
    # print(r)
    assert type(r) is str


def test_sy():
    dobotEdu = DobotEDU('yuejiang', 'YJ123456')
    r = dobotEdu.speech.synthesis('你好', 1)
    # print(r)
    assert type(r) is bytes


def ToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        return base64_data


def test_voice():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = ToBase64('D:/gitttt/dobotedu/test/222.mp3')
    # print(res)
    res1 = do.speech.asr(res)
    # print(res1)
    assert type(res1) is str


def test_image():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = ToBase64('D:/gitttt/dobotedu/test/4.jpg')
    # print(res)
    res2 = do.face.create_person(group_id="123",
                                 person_name="shua",
                                 person_id="333",
                                 image=res)
    assert res2 is not True
    # print(res2)


def test_magicbox():
    do = DobotEDU('yuejiang', 'YJ123456')
    res = do.magicbox.search_dobot()
    port = res[0]["portName"]
    do.magicbox.connect_dobot(port)
    do.m_lite.set_homecmd(port)
    do.magicbox.set_ptpwith_lcmd(port, 0)


def test_urlone():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    url = "https://dobotlab.dobot.cc"
    dobotEdu.url = url
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


def test_urltwo():
    dobotEdu = DobotEDU("yuyuyu", "yuyu78YU")
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


def test_urlthree():
    dobotEdu = DobotEDU("huang", "huangHUANG123")
    url = "https://dev.dobotlab.dobot.cc"
    dobotEdu.url = url
    r = dobotEdu.speech.synthesis('你好', 1)
    print(r)


# dobotEdu.speech.asr()
# dobotEdu.speech.ToBase64("test.mp3", "1.txt")
# r = dobotEdu.nlp.topic('警方通报女游客无故推倒景区设施：由于个人生活发生重大变故导致情绪行为')

# print(r)
# session_id = ""
# res = dobotEdu.robot.conversation('你好', session_id)
# print(res)
# res = dobotEdu.magicbox.search_dobot()
# port_name = res[0]["portName"]

# result1 = ""
# with open('4.txt', 'r') as f:
#     for line in f:
#         result1 = result1 + line

# result2 = ""
# with open('5.txt', 'r') as f:
#     for line in f:
#         result2 = result2 + line
# group_s = ['666']
# res = dobotEdu.face.search(group_s, result2)
# res = dobotEdu.tmt.translation('你好', 'zh','en')
# print(res)
# dobotEdu.magicbox.connect_dobot(port_name=port_name)
# #回零
# dobotEdu.m_lite.set_homecmd(port_name)
# dobotEdu.log.set_use_file(True)

# res = dobotEdu.magician.search_dobot()
# port_name = res[0]["portName"]
# dobotEdu.magician.connect_dobot(port_name=port_name)
# #回零
# dobotEdu.magician.set_homecmd(port_name)
# #打开光电传感器
# #port2：1，enable：True,version:1
# #port:0-5
# #version:0-1
# dobotEdu.magicbox.set_infrared_sensor(port_name, 1, True, 1)
# #打开颜色传感器
# #port3：2，enable：True,version:1
# #port:0-5
# #version:0-1
# dobotEdu.magicbox.set_color_sensor(port_name, 2, True, 1)
# #设置末端为手抓
# #set_type 1：吸盘，2：手抓，3：笔
# dobotEdu.m_lite.set_endeffector_type(port_name, 2)

# #等待光电检测到水果
# while True:
#     time.sleep(0.01)
#     if dobotEdu.magicbox.get_infrared_sensor(
#             port_name, 1)['status'] == 1:  #光电检测函数返回字典形式数据，值保存在status中
#         dobotEdu.m_lite.set_endeffector_gripper(
#             port_name,
#             True,
#             False,
#         )  #打开手爪： enable:True 使能， on:False 张开
#         time.sleep(0.5)
#         dobotEdu.m_lite.set_ptpcmd(port_name, 0, 250, 0, 0, 0)  #检测到水果后运动至水果处抓取
#         dobotEdu.m_lite.set_endeffector_gripper(
#             port_name, True, True)  #打开手爪： enable:True 使能， on:True 闭合
#         time.sleep(0.5)
#         dobotEdu.m_lite.set_ptpcmd(port_name, 0, 250, -20, 10, 0)  #运动至检测水果处
#         time.sleep(0.5)
#         color = dobotEdu.magicbox.get_color_sensor(
#             port_name)  #得到检测结果  {'blue': 1, 'green': 0, 'red': 0}
#         print(color)
#         if color['red'] == 1:  #如果检测结果为'red':1,则是红色
#             print('red:', color['red'])
#             print('红色水果')
#             dobotEdu.m_lite.set_ptpcmd(port_name, 0, 250, 150, 50, 0)  #放置到放置区
#             dobotEdu.m_lite.set_endeffector_gripper(port_name, True, False)
#         elif color['green'] == 1:  #如果检测结果为'green':1,则是绿色
#             print('green:', color['green'])
#             print('绿色水果')
#             dobotEdu.m_lite.set_ptpcmd(port_name, 0, 250, -150, 50, 0)  #放置到放置区
#             dobotEdu.m_lite.set_endeffector_gripper(port_name, True, False)
#         time.sleep(0.5)
#         dobotEdu.m_lite.set_endeffector_gripper(port_name, False, False)
#         dobotEdu.m_lite.set_ptpcmd(port_name, 0, 250, 0, 50, 0)  #回到初始位置等待
