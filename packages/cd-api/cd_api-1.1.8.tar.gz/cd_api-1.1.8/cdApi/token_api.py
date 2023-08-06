'''
@说明    :草动商城管理端取得token
@时间    :2020/3/8 下午6:25:59
@作者    :任秋锴
@版本    :1.0
'''
import requests
import time
import uuid
# import cv2
from cv2 import imdecode, imshow, IMREAD_COLOR, waitKey, destroyAllWindows
import numpy as np
from urllib import request


class Token:
    code_url = ""

    def __init__(self):
        self.makeCodeUrl()

    def makeCodeUrl(self):
        self.uuid_str = str(uuid.uuid4())
        timestamp = time.time()
        self.code_url = f"https://api.icaodong.com/manager/sysuser/imagecode?uuid={self.uuid_str}&time={int(timestamp*100)}"

    def openCode(self):
        resp = request.urlopen(self.code_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = imdecode(image, IMREAD_COLOR)
        imshow('验证码', image)
        key = waitKey(0)
        if key == 113:
            destroyAllWindows()
            self.code = input("pls enter code:")
        else:
            self.openCode()

    def get(self, tenantId, acc, pwd, acc_type=0):
        # acc_type=0表示个人管理员=1表示企业管理员
        self.openCode()
        data = {
            "tenantId": tenantId,
            "mobile": acc,
            "password": pwd,
            "code": self.code,
            "uuid": self.uuid_str,
            "brandType": '1',
            "type": acc_type,
        }
        url = "https://api.icaodong.com/manager/sysuser/login"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            response_json = response.json()
            status = response_json.get('status')
            if status == 200:
                token = response_json.get("data").get("token")
                print(f"token is {token}")
                return token
            else:
                print(url, data, response_json)
                self.get(
                    tenantId=tenantId,
                    acc=acc,
                    pwd=pwd,
                    acc_type=acc_type)


def testcase():
    t = Token()
    t.get(508, "13801587423", "cd123456")


if __name__ == "__main__":
    testcase()
