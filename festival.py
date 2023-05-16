import requests,uuid
from datetime import datetime
proxies = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}

twenty_four_solar_list = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']
statutory_holiday = ['元旦','春节','清明节','劳动节','端午节','中秋节']
twenty_four_solar_data_list = []
festival_data_list = []
festival_data_list_other = []
almanac_data_list = []

year_now = datetime.now().year

for year in [str(year_now-1),str(year_now),str(year_now+1)]:
    for month in ['2','5','8','11']:
        url = 'https://opendata.baidu.com/api.php?tn=wisetpl&format=json&resource_id=39043&query='+year+'年'+month+'月'
        a = requests.get(url,proxies=proxies)
        day_data = a.json()['data'][0]['almanac']
        for data in day_data:
            if 'term' in data and data['term'] != '':#节日
                if data['term'] in twenty_four_solar_list:#节气
                    twenty_four_solar_data_list.append([data['term'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])
                else:
                    if data['term'] not in statutory_holiday:
                        festival_data_list.append([data['term'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])
            if 'value' in data and data['value'] != '':#其他节日
                festival_data_list_other.append([data['value'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])
            almanac_data_list.append([data['suit'],data['avoid'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])

print(twenty_four_solar_data_list)
print(festival_data_list)
print(festival_data_list_other)
print(almanac_data_list)

f = open('twenty_four_solar.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:节气\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年节气，数据来自百度\n')
for i in twenty_four_solar_data_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+str(datetime.now().date())+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('festival.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:主要节日\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年主要节日，数据来自百度\n')
for i in festival_data_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+str(datetime.now().date())+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('festival_other.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:其他节日\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年其他节日，数据来自百度\n')
for i in festival_data_list_other:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+str(datetime.now().date())+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('almanac.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:黄历\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年黄历，数据来自百度\n')
for i in almanac_data_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+str(datetime.now().date())+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[2]+'\nDTEND;VALUE=DATE:'+str(int(i[2])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+'宜：'+i[0]+'  忌：'+i[1]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()