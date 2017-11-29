import requests
from bs4 import BeautifulSoup

url = "http://calorie.slism.jp/200000/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

def data_to_dict(table):
    return { tr.find_all("td")[0].string : tr.find_all("td")[1].string for i,tr in enumerate(table.find_all("tr")) if i%2==0 }
 

main_table = soup.find("div", id="mainData").table
main_data = data_to_dict(main_table)

etc_table = soup.find("div", id="etc").table
etc_data = data_to_dict(etc_table)

fat_table = soup.find("div", id="fat").table
fat_data = data_to_dict(fat_table)

data = {**main_data, **etc_data, **fat_data}
print(data)
