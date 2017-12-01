import requests
from bs4 import BeautifulSoup
from progressbar import ProgressBar, Percentage, Bar
import re
import json

base_url = "http://calorie.slism.jp"

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
        res = requests.get("{base}/{dish_id}".format(base=base_url, dish_id=dish_id))
        soup = BeautifulSoup(res.text, "lxml")

        res_data = {}
        for type_id in ["mainData", "etc", "fat"]:
            table = soup.find("div", id=type_id).table
            res_data.update(self.__data_to_dict(table))
        
        return res_data

    def get_last_page(self, page, soup):
        """
        最後のページかどうか
        """
        pager = soup.find("div", id="pager")
        href = pager.find("a", text="Last")["href"]
        return href.rsplit("/", 1)[1]

    def get_dish_list(self, category_id, page=1):
        """
        カテゴリの食品のリストを返すよ。
        @param category_id カテゴリのid
        @return 食品の辞書
        """
        res = requests.get("{base}/category/{cat_id}/{page}".format(base=base_url, cat_id=category_id, page=page))
        soup = BeautifulSoup(res.text, "lxml")

        food_list =  soup.find("div", id="foodList")
        res = []
        all_size = len(food_list.find_all("li"))
        #progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

        for i, li in enumerate(food_list.find_all("li")):
            dish_name = li.a.string
            dish_img = re.sub("[a-z]+\.jpg", ".jpg", li.img["src"])
            dish_id = li.a["href"].strip("/")
            dish_data = self.get_dish_data(dish_id)
            res.append({"name": dish_name, "img": dish_img, "nutritions": dish_data})
            per = int((i+1) * 100 / all_size)
            #progress.update(per)

        last_page =  int(self.get_last_page(page, soup))
        if page != last_page:
            res.extend(self.get_dish_list(category_id, page=page+1))

        return res

#res = Calorieslism().get_dish_data(dish_id=200000)
res = Calorieslism().get_dish_list(category_id=16)
print(json.dumps(res))
