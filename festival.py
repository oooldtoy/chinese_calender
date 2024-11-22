import requests,cnlunar,uuid
from datetime import datetime, timedelta,timezone

twenty_four_solar_list = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']
statutory_holiday = ['元旦','春节','清明节','劳动节','端午节','中秋节']
twenty_four_solar_data_list = []
festival_data_list = []
festival_data_list_other = []
almanac_data_list_suit = []
almanac_data_list_avoid = []
almanac_data_list_suitavoid = []
good_bad_time_list = []
pengzu_100_taboos_list = []
auspicious_direction_list = []
today_fetal_god_list = []
year_now = datetime.now().year

for year in [str(year_now-1),str(year_now),str(year_now+1)]:
    for month in ['2','5','8','11']:
        url = 'https://opendata.baidu.com/api.php?tn=wisetpl&format=json&resource_id=39043&query='+year+'年'+month+'月'
        a = requests.get(url)
        day_data = a.json()['data'][0]['almanac']
        for data in day_data:
            if 'term' in data and data['term'] != '':#节日
                if data['term'] not in statutory_holiday and data['term'] not in twenty_four_solar_list:#一般性节日
                        festival_data_list.append([data['term'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])
            if 'value' in data and data['value'] != '':#其他节日
                festival_data_list_other.append([data['value'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])
            almanac_data_list_suit.append([data['suit'], str(year) + data['month'].zfill(2) + data['day'].zfill(2)])
            almanac_data_list_avoid.append([data['avoid'], str(year) + data['month'].zfill(2) + data['day'].zfill(2)])
            almanac_data_list_suitavoid.append([data['suit'],data['avoid'],str(year)+data['month'].zfill(2)+data['day'].zfill(2)])

start_date = datetime(year_now-1, 1, 1)
end_date = datetime(year_now+1, 12, 31)
all_datetimes = [(start_date + timedelta(days=i)).replace(hour=0, minute=0)for i in range((end_date - start_date).days + 1)]
for i in all_datetimes:
    a = cnlunar.Lunar(i, godType='8char')  # 常规算法
    # a = cnlunar.Lunar(datetime.datetime(2022, 2, 3, 10, 30), godType='8char', year8Char='beginningOfSpring')  # 八字立春切换算法
    dic = {
        '日期': a.date,
        '农历数字': (a.lunarYear, a.lunarMonth, a.lunarDay, '闰' if a.isLunarLeapMonth else ''),
        '农历': '%s %s[%s]年 %s%s' % (a.lunarYearCn, a.year8Char, a.chineseYearZodiac, a.lunarMonthCn, a.lunarDayCn),
        '星期': a.weekDayCn,
        # 未增加除夕
        '今日节日': (a.get_legalHolidays(), a.get_otherHolidays(), a.get_otherLunarHolidays()),
        '八字': ' '.join([a.year8Char, a.month8Char, a.day8Char, a.twohour8Char]),
        '今日节气': a.todaySolarTerms,
        '下一节气': (a.nextSolarTerm, a.nextSolarTermDate, a.nextSolarTermYear),
        '今年节气表': a.thisYearSolarTermsDic,
        '季节': a.lunarSeason,

        '今日时辰': a.twohour8CharList,
        '时辰凶吉': a.get_twohourLuckyList(),
        '生肖冲煞': a.chineseZodiacClash,
        '星座': a.starZodiac,
        '星次': a.todayEastZodiac,

        '彭祖百忌': a.get_pengTaboo(),
        '彭祖百忌精简': a.get_pengTaboo(long=4, delimit='<br>'),
        '十二神': a.get_today12DayOfficer(),
        '廿八宿': a.get_the28Stars(),

        '今日三合': a.zodiacMark3List,
        '今日六合': a.zodiacMark6,
        '今日五行': a.get_today5Elements(),

        '纳音': a.get_nayin(),
        '九宫飞星': a.get_the9FlyStar(),
        '吉神方位': a.get_luckyGodsDirection(),
        '今日胎神': a.get_fetalGod(),
        '神煞宜忌': a.angelDemon,
        '今日吉神': a.goodGodName,
        '今日凶煞': a.badGodName,
        '宜忌等第': a.todayLevelName,
        '宜': a.goodThing,
        '忌': a.badThing,
        '时辰经络': a.meridians
    }
    if dic['今日节气'] != '无':
        twenty_four_solar_data_list.append([dic['今日节气'],i.strftime("%Y%m%d")])
    good_bad_time_list.append([' '.join(f"{a}{b}" for a, b in zip(dic['今日时辰'], dic['时辰凶吉'])), i.strftime("%Y%m%d")])
    pengzu_100_taboos_list.append([dic['彭祖百忌'], i.strftime("%Y%m%d")])
    auspicious_direction_list.append([' '.join(dic['吉神方位']), i.strftime("%Y%m%d")])
    today_fetal_god_list.append([dic['今日胎神'], i.strftime("%Y%m%d")])

print(twenty_four_solar_data_list)
print(festival_data_list)
print(festival_data_list_other)
print(almanac_data_list_suitavoid)

f = open('twenty_four_solar.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:节气\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年节气\n')
for i in twenty_four_solar_data_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('festival.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:主要节日\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年主要节日，数据来自百度\n')
for i in festival_data_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('festival_other.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:其他节日\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年其他节日，数据来自百度\n')
for i in festival_data_list_other:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('almanac.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:黄历\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年黄历，数据来自百度\n')
for i in almanac_data_list_suitavoid:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[2]+'\nDTEND;VALUE=DATE:'+str(int(i[2])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+'宜：'+i[0]+'  忌：'+i[1]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('good_bad_time.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:时辰吉凶\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年时辰吉凶\n')
for i in good_bad_time_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('pengzu_100_taboos.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:彭祖百忌\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年彭祖百忌\n')
for i in pengzu_100_taboos_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('auspicious_direction.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:吉神方位\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年吉神方位\n')
for i in auspicious_direction_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()

f = open('today_fetal_god.ics','w',encoding='utf-8')
f.write('BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//github//Chinese Calendar//oooldtoy\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:今日胎神\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:近三年今日胎神\n')
for i in today_fetal_god_list:
    f.write('BEGIN:VEVENT\nDTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'\nUID:'+str(uuid.uuid4())+'\nDTSTART;VALUE=DATE:'+i[1]+'\nDTEND;VALUE=DATE:'+str(int(i[1])+1)+'\nSTATUS:CONFIRMED\nSUMMARY:'+i[0]+'\nEND:VEVENT\n')
f.write('END:VCALENDAR')
f.close()
