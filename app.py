import requests
from bs4 import BeautifulSoup

base_url = "http://calorie.slism.jp/"

class Calorieslism:
    def __data_to_dict(self, table):
        return { tr.find_all("td")[0].string : tr.find_all("td")[1].string for i,tr in enumerate(table.find_all("tr")) if i%2==0 }

    def get_dish_data(self, dish_id):
        res = requests.get(base_url + str(dish_id))
        self.soup = BeautifulSoup(res.text, "lxml")

        res_data = {}
        for type_id in ["mainData", "etc", "fat"]:
            table = self.soup.find("div", id=type_id).table
            res_data.update(self.__data_to_dict(table))
        
        return res_data


res = Calorieslism().get_dish_data(dish_id=200000)
print(res)
