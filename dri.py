import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json

url = "http://www.glico.co.jp/navi/e07.html"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")
areas = soup.find_all("div", class_="tables_area")


def get_item(dic, index):
    for k, v in dic.items():
       if re.search(k, index):
           return v


def get_name(name):
    names = OrderedDict((
        (".*エネルギー.*", "energy"),
        (".*たんぱく質.*", "protein"),
        (".*脂質.*", "lipid"),
        (".*飽和脂肪酸.*", "saturated_fatty_acid"),
        (".*炭水化物.*", "carbohydrate"),
        (".*食物繊維.*", "dietary_fiber"),
    ))
    return get_item(names, name)
    

def get_age(age):
    age = age[:-3]
    if "以上" in age:
        return int(age[:-2]), 200
    return map(lambda n:int(n), age.split("〜"))


def get_val(val):
    val = re.sub(",", "", val)
    return val


data = []
for area in areas:
    title = get_name(area.a.string)
    if title is None:
        continue

    trs = area.table.find_all("tr")[2:13]
    for tr in trs:
        td = tr.find_all("td")
        start, end = get_age(td[0].string)
        for i in [1, 2]:
            data.append({
                "nut_type": title,
                "gender": "male" if i == 1 else "female",
                "age_start": start,
                "age_end": end,
                "val": get_val(td[i].string)
            })

print(json.dumps(data))
