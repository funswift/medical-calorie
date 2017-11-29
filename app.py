import requests
from bs4 import BeautifulSoup
import json

base_url = "http://calorie.slism.jp/"

class Calorieslism:
    def __data_to_dict(self, table):
        try:
            return { tr.find_all("td")[0].string : tr.find_all("td")[1].string for i,tr in enumerate(table.find_all("tr")) if i%2==0 }
        except AttributeError:
            return {}

    def get_dish_data(self, dish_id):
        """
        一般的な栄養価を返すよ。
        @param dish_id 料理のid
        @return 栄養価の辞書
        """
        res = requests.get(base_url + str(dish_id))
        soup = BeautifulSoup(res.text, "lxml")

        res_data = {}
        for type_id in ["mainData", "etc", "fat"]:
            table = soup.find("div", id=type_id).table
            res_data.update(self.__data_to_dict(table))
        
        return res_data

    def get_dish_list(self):
        """
        カテゴリの食品のリストを返すよ。
        @param category_id カテゴリのid
        @return 食品の辞書
        """
        res = requests.get(base_url + "category/16")
        soup = BeautifulSoup(res.text, "lxml")

        food_list =  soup.find("div", id="foodList")
        res = {}
        for li in food_list.find_all("li"):
            dish_name = li.a.string
            dish_id = li.a["href"].strip("/")
            dish_data = self.get_dish_data(dish_id)
            res.update({dish_name: dish_data})

        return res

#res = Calorieslism().get_dish_data(dish_id=200000)
res = Calorieslism().get_dish_list()
print(json.dumps(res))
