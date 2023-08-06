'''
@Author: Rqk
@Date: 2020-04-30 14:08:52
@Description: 
@说明    :商品接口。
@时间    :2020/2/13 下午4:28:26
@作者    :任秋锴
@版本    :1.0
'''

from .base import base


class storeProduct(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, productCode=None, companyId=None, specCode=None, name=None,
             storeStatus=None, categoryIds=None, pageNum=1, pageSize=10):
        api_name = "manager/storeproduct/list"
        data = {
            "productCode": productCode,
            "companyId": companyId,
            "specCode": specCode,
            "name": name,
            "storeStatus": storeStatus,
            "categoryIds": categoryIds,
            "pageNum": pageNum,
            "pageSize": pageSize
        }
        result = self.request(api_name, data, method="GET")
        status = result.get("status")
        if status == 200:
            return result.get("data").get("dataList")
        else:
            print(result)

    def create(self, data):
        api_name = "manager/storeproduct/add"
        return self.request(api_name, data, method="POST")

    def read(self, _id):
        url = "manager/storeproduct/info"
        data = {
            "id": _id
        }
        return self.request(url, data)

    def update(self, data):
        url = "manager/storeproduct/edit"
        return self.request(url, data, method="POST")

    def delete(self):
        pass

    def updatebatchproduct(self, _id, price):
        api_name = "manager/storeproduct/updatebatchproduct"
        data = {"pidList": [_id], "price": price}
        return self.request(api_name, data, method="POST")

    def update_price(self, store_product_id, price, spec_code=None):
        data = self.read(store_product_id)
        data = data.get("data")
        if data:
            if spec_code:
                for d in data["specificationList"]:
                    if d["specCode"] == spec_code:
                        d["price"] = price
            else:
                for d in data["specificationList"]:
                    d["price"] = price
        return self.update(data)
