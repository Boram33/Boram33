import re
import webbrowser

import folium
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json

html = requests.get('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=')
soup = BeautifulSoup(html.text, 'html.parser')

data1 = soup.find('div', {'class':'data_table midd mgt24'})
data_2 = data1.find('tbody')

data_list = []
city = []
p_sum = []
p_domestic = []
p_foreign = []
p_sum_all = []
code = ['11','26','27','28','29','30','31','36','41','42','43','44','45','46','47','48','50']
for i in range(0,17):
    data = data_2.findAll('tr')[i+1]
    data_list.append([])
    data5 = str(data.findAll('th'))
    data5 = re.sub('<.+?>', '', data5, 0).strip()
    data5 = data5.replace("[","")
    data5 = data5.replace("]","")
    city.append(data5)
    for j in range(0,4):
        data4 = str(data.findAll('td')[j])
        data4 = re.sub('<.+?>', '', data4, 0).strip()
        data4 = int(data4.replace(',',''))
        data_list[i].append(data4)
# data4 = data1.findAll('tr')[5]

for k in range(0,17):
    p_sum.append(data_list[k][0])
    p_domestic.append(data_list[k][1])
    p_foreign.append(data_list[k][2])
    p_sum_all.append(data_list[k][3])


corona_info = pd.DataFrame({'city':city, "patients_sum":p_sum, "patients_domestic":p_domestic,
                            "patients_foreign":p_foreign, "patiens_All":p_sum_all,"Code":code})
print(corona_info.dtypes)
print(corona_info)
corona_info.to_csv("corona_info.csv", encoding='cp949')


city_geo = "map.geojson"
geo_str = json.load(open(city_geo, encoding='utf-8'))
patient_data = pd.read_csv("corona_info.csv",encoding='cp949')
print(patient_data)


map = folium.Map(location=(37.470493, 127.057265),zoom_start=7)
map.choropleth(geo_data = geo_str ,
               data = patient_data,
               columns=['Code','patiens_All'],
               key_on = 'feature.properties.CTPRVN_CD',
               fill_opacity=0.7,
               line_opacity=0.3,
               fill_color='YlGn',
               legend_name = 'Patients')


folium.LayerControl().add_to(map)
map.save("./Patients.html")
webbrowser.open_new("Patients.html")



"""
print(data3)

print(data4)

info_list = [[],[],[],[],[]]
for i in range(5):
    data = data1.findAll('tr')[i]
    for j in range(5):
        info = data.findAll("td")
        info_list[j].append(info)
        

print(info_list)

for a in data1.find_all("tr"):
    list2 = [[],[],[],[],[],[]]
    i = 0
    for b in a.find_all("td"):

        info = b.get_text()
        list2[i].append(info)
        i= i+1
        print(info)
print(list2)

today_status_1 = data1.find('em',{'class':'info_num'}).text

print('오늘의 국내 확진자: '+today_status_1)

corona_info_dict = {'국내 확진자':today_status_1}
def toJson(corona_info_dict):
    with open('weather.json', 'w', encoding='utf-8') as file :
        json.dump(corona_info_dict, file, ensure_ascii=False, indent='\t')

toJson(corona_info_dict)
"""
