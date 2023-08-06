'''
@说明    :商品接口。
@时间    :2020/2/13 下午4:28:26
@作者    :任秋锴
@版本    :1.0
'''


from .base import base


class product(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, productCode=None, specCode=None, name=None,
             storeStatus=None, categoryIds=None, pageNum=1, pageSize=10):
        api_name = "manager/product/list"
        data = {
            "productCode": productCode,
            "specCode": specCode,
            "name": name,
            "storeStatus": storeStatus,
            "categoryIds": categoryIds,
            "pageNum": pageNum,
            "pageSize": pageSize
        }
        result = self.request(api_name, data, method="POST")
        status = result.get("status")
        if status == 200:
            return result.get("data").get("dataList")
        else:
            print(result)

    def create(self, data):
        api_name = "manager/product/add"
        return self.request(api_name, data, method="POST")

    def create_demo(self, name, specCode):
        data = {
            "name": name,
            "categoryList":
            [
                {"id": 1},
                {"id": 4},
                {"id": 7},
                {"id": 6},
                {"id": 8},
                {"id": 21},
                {"id": 52},
                {"id": 12},
                {"id": 5},
                {"id": 10},
                {"id": 11},
                {"id": 20}
            ],
            "labelList": [{"id": 78}],
            "materialMainList": [{"id": 14139, "rank": 1}],
            "materialnotMainList": [{"id": 14138}],
            "details": "测试测试",
            "showImages": "",
            "productCode": "",
            "weight": "11",
            "volume": "1",
            "virtualTotal": "1",
            "type": 1,
            "status": 0,
            "isOpen": 0,
            "commissionRulesDTO": {"empAmount": "", "empPercent": "", "empType": 1, "empSwitch": 0, "id": ""},
            "expressFree": 1, "attributeList": [
                {"key": "颜色", "value": [{"values": "红色", "img": "https://cdqn.icaodong.com/image/100_1577429535111_44253476.png"}], "isShow": 1}, {"key": "尺寸", "value": [{"values": "150cm", "img": ""}], "isShow": 1}], "specificationList": [{"id": "", "imgUrl": "https://cdqn.icaodong.com/image/100_1577429535111_44253476.png", "inventory": "100", "prePrice": "100", "price": "100", "specCode": specCode, "specContent": "红色，150cm", "status": 1}], "batch": {"prePrice": "100", "price": "100", "inventory": "100"}, "isVip": 1}
        return self.create(data)

    def read(self, _id):
        url = "manager/product/info"
        data = {
            "id": _id
        }
        result = self.request(url, data)
        status = result.get("status")
        if status == 200:
            data = result.get("data")
            return data

    def update(self, data):
        url = "manager/product/update"
        return self.request(url, data, method="POST")

    def delete(self):
        pass
