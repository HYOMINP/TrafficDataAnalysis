import konlpy
from konlpy.tag import Hannanum
from konlpy.tag import Kkma
hannanum = Hannanum()
kkma = Kkma()
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams, style
import numpy as np
from selenium import webdriver
import time
import re
from wordcloud import WordCloud
from collections import Counter
import folium
import webbrowser
import json

#한글 글꼴 삽입
from matplotlib import font_manager, rc
font_path = "C:/Users/user/Desktop/team7/NanumGothic.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

#대중교통 현황 확인
traffic = pd.read_csv('C:/Users/user/Desktop/team7/대중교통_이용.csv', sep=',',engine='python',encoding='CP949')
traffic
traffic = traffic.set_index('구분1')

    #1주간대중교통이용횟수(회)
times_a_week = traffic.loc['1주간대중교통이용횟수(회)'].sort_values(ascending = False)
times_a_week.plot(kind='bar')
plt.title('1주간대중교통이용횟수(회)')
plt.show()

    #한달평균대중교통비용(원)
cost_average_month = traffic.loc['한달평균대중교통비용(원)'].sort_values(ascending = False)
cost_average_month.plot(kind='bar')
plt.title('한달평균대중교통비용(원)')
plt.show()

    #교통카드이용률(%)
card_use = traffic.loc['교통카드이용률(%)'].sort_values(ascending = False)
card_use.plot(kind='bar')
plt.title('교통카드이용률(%)')
plt.show()

    #정보제공서비스이용률(%)
use_info_serv = traffic.loc['정보제공서비스이용률(%)'].sort_values(ascending = False)
use_info_serv.plot(kind='bar')
plt.title('정보제공서비스이용률(%)')
plt.show()

    #접근소요시간(분)
time_coming = traffic.loc['접근소요시간(분)'].sort_values(ascending = False)
time_coming.plot(kind='bar')
plt.title('접근소요시간(분)')
plt.show()

    #환승서비스이용률(%)
use_transfer_serv = traffic.loc['환승서비스이용률(%)'].sort_values(ascending = False)
use_transfer_serv.plot(kind='bar')
plt.title('환승서비스이용률(%)')
plt.show()

    #환승횟수(회)
transfer_times = traffic.loc['환승횟수(회)'].sort_values(ascending = False)
transfer_times.plot(kind='bar')
plt.title('환승횟수(회)')
plt.show()

    #환승이동시간(분)
time_for_transfer = traffic.loc['환승이동시간(분)'].sort_values(ascending = False)
time_for_transfer.plot(kind='bar')
plt.title('환승이동시간(분)')
plt.show()

    #환승대기시간(분)
waiting_for_transfer = traffic.loc['환승대기시간(분)'].sort_values(ascending = False)
waiting_for_transfer.plot(kind='bar')
plt.title('환승대기시간(분)')
plt.show()

#평일통행량
amount = pd.read_csv('C:/Users/user/Desktop/team7/대중교통_통행량.csv', sep = ',', header = 0, engine = 'python', encoding='CP949')
amount_weekday = amount.drop(['토요일', '일요일'], axis = 1, inplace = False)
amount_x = amount_weekday.transpose()
amount = amount_x
amount = amount.rename(columns=amount.iloc[0])
amount = amount.drop(amount.index[0])
pd.set_option('mode.chained_assignment',None)
population = pd.read_csv('C:/Users/user/Desktop/team7/행정구역_시군구_별__성별_인구수_20210521190300.csv',  index_col=0, engine = 'python', encoding='CP949')
amount = amount.transpose()
amount = amount.rename({'평일': '평일통행량'}, axis=1)
am_population_merge = pd.merge(amount, population, how = 'inner', left_index = True, right_index = True)
MC_amount = am_population_merge['평일통행량']
am_population_merge['ratio'] = MC_amount.div(am_population_merge['총인구수 (명)'], axis = 0) * 10
am_population_merge
am_population_merge['행정구역별'] = am_population_merge.index
am_population_merge.to_csv('C:/Users/user/Desktop/team7/am_population_merge.csv',sep=',', na_rep='NaN')

csvFile = 'C:/Users/user/Desktop/team7/am_population_merge.csv'
SiDodf = pd.read_csv(csvFile, encoding = 'utf-8')
SiDo_geo = json.load(open('C:/Users/user/Desktop/team7/Si_Do_map_utf8.json', encoding='utf-8'))
m = folium.Map(location=[36.45, 127.42], tiles = "OpenStreetMap", zoom_start=8)
folium.Choropleth(
    geo_data = SiDo_geo,
    data=SiDodf,
    columns=['행정구역별', 'ratio'],
    key_on='feature.properties.CTP_KOR_NM',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    name='10명당 대중교통 통행량',
    legend_name='10명당 대중교통 통행량').add_to(m)
folium.LayerControl().add_to(m)
m.save('map.html')
webbrowser.open('map.html')


#대중교통 만족도 
satisfaction = pd.read_csv('C:/Users/user/Desktop/team7/대중교통_만족도.csv', sep = ',', header = 0, engine = 'python', encoding='CP949')
satisfaction = satisfaction.drop(['구분1'], axis = 1, inplace = False)
satisfaction = satisfaction.set_index('구분2')
satisfaction

    #노선체계적절성
system_adequacy = satisfaction.loc['노선체계적절성'].sort_values(ascending = False)
system_adequacy.plot(kind='bar')
plt.title('노선체계적절성')
plt.ylim([0,7])
plt.show()

    #배차간격적절성
interval_adequacy = satisfaction.loc['배차간격적절성'].sort_values(ascending = False)
interval_adequacy.plot(kind='bar')
plt.title('배차간격적절성')
plt.ylim([0,7])
plt.show()

    #이용요금합리성
price_reasonable = satisfaction.loc['이용요금합리성'].sort_values(ascending = False)
price_reasonable.plot(kind='bar')
plt.title('이용요금합리성')
plt.ylim([0,7])
plt.show()

    #대중교통운영체계구축
os = satisfaction.loc['대중교통운영체계구축'].sort_values(ascending = False)
os.plot(kind='bar')
plt.title('대중교통운영체계구축')
plt.ylim([0,7])
plt.show()

    #기사/역무원친절도
hospitality = satisfaction.loc['기사/역무원친절도'].sort_values(ascending = False)
hospitality.plot(kind='bar')
plt.title('기사/역무원친절도')
plt.ylim([0,7])
plt.show()

    #내부시설이용편리성
convenience = satisfaction.loc['내부시설이용편리성'].sort_values(ascending = False)
convenience.plot(kind='bar')
plt.title('내부시설이용편리성')
plt.ylim([0,7])
plt.show()

    #교통약자시설
facilities_handicapped = satisfaction.loc['교통약자시설'].sort_values(ascending = False)
facilities_handicapped.plot(kind='bar')
plt.title('교통약자시설')
plt.ylim([0,7])
plt.show()

    #차량내부혼잡도
congestion = satisfaction.loc['차량내부혼잡도'].sort_values(ascending = False)
congestion.plot(kind='bar')
plt.title('차량내부혼잡도')
plt.ylim([0,7])
plt.show()

    #이용시설청결성
clean = satisfaction.loc['이용시설청결성'].sort_values(ascending = False)
clean.plot(kind='bar')
plt.title('이용시설청결성')
plt.ylim([0,7])
plt.show()

    #(버스)급출발/급제동/차로변경/안전거리확보
bus_sudden_departure = satisfaction.loc['(버스)급출발/급제동/차로변경/안전거리확보'].sort_values(ascending = False)
bus_sudden_departure.plot(kind='bar')
plt.title('(버스)급출발/급제동/차로변경/안전거리확보')
plt.ylim([0,7])
plt.show()

    #(버스)비상시대처방안안내
bus_emergency_action = satisfaction.loc['(버스)비상시대처방안안내'].sort_values(ascending = False)
bus_emergency_action.plot(kind='bar')
plt.title('(버스)비상시대처방안안내')
plt.ylim([0,7])
plt.show()

    #(지하철)급출발/급정거/정확한위치정차
sub_sudden_departure = satisfaction.loc['(지하철)급출발/급정거/정확한위치정차'].sort_values(ascending = False)
sub_sudden_departure.plot(kind='bar')
plt.title('(지하철)급출발/급정거/정확한위치정차')
plt.ylim([0,7])
plt.show()

    #(지하철)비상시대처방안안내
sub_emergency_action = satisfaction.loc['(지하철)비상시대처방안안내'].sort_values(ascending = False)
sub_emergency_action.plot(kind='bar')
plt.title('(지하철)비상시대처방안안내')
plt.ylim([0,7])
plt.show()

    #대중교통정보제공시스템구축
info_system = satisfaction.loc['대중교통정보제공시스템구축'].sort_values(ascending = False)
info_system.plot(kind='bar')
plt.title('대중교통정보제공시스템구축')
plt.ylim([0,7])
plt.show()

    #대중교통제공정보정확성
info_accuracy = satisfaction.loc['대중교통제공정보정확성'].sort_values(ascending = False)
info_accuracy.plot(kind='bar')
plt.title('대중교통제공정보정확성')
plt.ylim([0,7])
plt.show()

    #대중교통변경정보제공
change_info = satisfaction.loc['대중교통변경정보제공'].sort_values(ascending = False)
change_info.plot(kind='bar')
plt.title('대중교통변경정보제공')
plt.ylim([0,7])
plt.show()

    #환승노선(체계)구축
transfer_system = satisfaction.loc['환승노선(체계)구축'].sort_values(ascending = False)
transfer_system.plot(kind='bar')
plt.title('환승노선(체계)구축')
plt.ylim([0,7])
plt.show()

    #환승정보제공적절성
info_transfer = satisfaction.loc['환승정보제공적절성'].sort_values(ascending = False)
info_transfer.plot(kind='bar')
plt.title('환승정보제공적절성')
plt.ylim([0,7])
plt.show()

    #환승요금적절성
transfer_cost = satisfaction.loc['환승요금적절성'].sort_values(ascending = False)
transfer_cost.plot(kind='bar')
plt.title('환승요금적절성')
plt.ylim([0,7])
plt.show()

    #만족도평균
transfer_cost = satisfaction.loc['만족도평균'].sort_values(ascending = False)
transfer_cost.plot(kind='bar')
plt.title('만족도평균')
plt.ylim([0,7])
plt.show()

#버스 민원 통계
bus_complaint = pd.read_excel('C:/Users/user/Desktop/team7/버스 민원 통계.xlsx')
bus_complaint = bus_complaint.set_index('Unnamed: 0')
bus_complaint

#국민신문고에서 민원내용 확인하기
driver = webdriver.Chrome(r'C:/Users/user/Desktop/team7/chromedriver.exe')
url = "https://www.epeople.go.kr/nep/pttn/gnrlPttn/pttnSmlrCaseList.npaid"
driver.get(url)
time.sleep(5)

    # 검색어 = 대중교통
element = driver.find_element_by_name('searchWord')
element.send_keys("대중교통")

    #기간 설정

        #시작날짜
element = driver.find_element_by_name('rqstStDt')
element.send_keys("2019-01-01")

        #마침날짜
element = driver.find_element_by_name('rqstEndDt')
element.send_keys("2020-12-31")

    #상세검색 열기
element = driver.find_element_by_class_name('search_open')
element.click()

    #처리기관 - '지방자치단체'로 설정 
element = driver.find_element_by_name('searchInstType')
element.send_keys('지방자치단체')

    #검색버튼 누르기
element.submit()

#335건의 민원사례를 확인했다. 


    #1페이지부터 34페이지까지 제목 크롤링
for i in range(34):
    try:
        contents=driver.find_elements_by_css_selector('td.left')
        for content in contents:
            print(content.text)
        nextpage = driver.find_element_by_css_selector('span.nep_p_next')
        nextpage.click()
        time.sleep(1)
    except:
        break

#크롤링한 내용 복사하기 붙여넣기로 엑셀에서 중복 내용 제거 후 complaint변수에 저장
    #필요없는 내용도 제거하였습니다. ex) '대중교통 불편, 대중교통 민원' 등
complaint = '''((대중 교통불편 해소 및 대안이 될 자전거 이용에 적합한 도로 정비, 확충 및 안내표지판 설치에 관한 건))
1AA-2009-0168329호 답변과 관련하여 용인시 대중교통과에 추가 질의합니다.
3-6대로 공사 이후 대중교통 증설 요청
m버스 2개 추가시 원안이었던 창의고옆 정류장 추가로 호반 3차 및 목동대중교통 불편을 해결해 주시기를 강력히 요구드리는 바입니다.이번에는 꼭 재고 부탁드립니다.
갈매동 대중교통 민원
감일지구 대중교통 문제 해결을 바랍니다
경기도 동남권 지역 대중교통망 확충
경기도 성남시 교통도로국 대중교통과 김*화 분께 보내주세요
경기도 의정부시 고산동 대중교통민원
공공기관 홈페이지 대중교통 알림서비스
관광지 대중교통 정보 제공 필요성
광교우미뉴브 신축 지식산업쎈타 앞 포은대로변 버스정류장 신설 요청(대중교통과 버스운영팀)
광주시 대중교통과!시민들위해 꼭 마을버스 해결해주시리라 응원합니다!
국토부는 운정신도시의 불편한 대중교통 문제 개선 위해 서울역행 M버스 신설확충 즉각 확정시켜 주세요!
귀 부서의 발전을 기원하며 또한 이번 시에서 추진하는 대중교통혁신 추진단에 거는 기대가 아주 큽니다.
기업도시 대중교통 너무 불편합니다. 원주시청 직원용 출근 버스도 없애주세요. 상대적 박탈감 느낍니다.
김포 고촌 신곡6지구 대중교통 추가 확보 요청드립니다.
김포시 양촌읍 학운산업2단지 대중교통
김해 율하2지구 대중교통 개선을 제안합니다.
대구광역시와 원주시 간 대중교통(고속, 시외버스) 운행을 재개해주세요
대중 교통불편 해소 및 대안이 될 자전거 이용에 적합한 도로 정비, 확충 및 안내표지판 설치에 관한 건
대중교통 기사님들 마스크 착용 의무화해주세요
대중교통 마을버스
대중교통 배차문제 이의제기
대중교통 버스 무단 결선(무성의)
대중교통 불편(시내버스), 106번, 453번버스 테크노산단 경유 요청
대중교통 시간
대중교통 운행시간연장을 건의드립니다.
대중교통 증차
대중교통 지원금 대책방안
대중교통 해결방안 필요
대중교통 환승에 관해 궁금한 점이 있습니다
대중교통 환승할인 제도의 문제점
대중교통(버스) 급정거 및 과속 등 개선 요구
대중교통(시내버스)사용시 대화강제금지의 건
대중교통(지하철,버스) 와 계단,엘레베이터,에스컬레이터, 공중화장실
대중교통과 일안하나?
대중교통과 철도기획팀 오재경 민원답변에 대해서 어이상실이네요~~
대중교통에서 마스크를 쓰기위한 환경을 마련해주세요.
대중교통은 시민들의 발이라면서 발이 시간도 안지켜요
대중교통의 감축을 완화해주세요
대중교통이 늘면 늘었지 운행을 줄이는 기이한 행동이 이재수와 대중교통과정책인가
대중교통이용환경개선
동탄2신도시 미래철도 트램관련 대중교통소외지역(문화디자인밸리)교통불편 해소 건
마북동 교동마을 대중교통 개선을 위한 용인경전철 노선 포함 요청
마스크착용후 대중교통이용 독려 재난문자 지속적 발송바랍니다.
맘현마을 안쪽(소실봉쪽) 대중교통-버스노선,정류장 신설 요청 드립니다.
물향기수목원 대중교통 편의 증대
미사신도시 고질적인 대중교통 문제 해결
미사의 고질적인 대중교통부족해결
민원 1AA-2010-0875555과 관련하여 용인시 대중교통과에 묻습니다.
밀양시장이 구만산 산림욕장 예정지의 “대중교통 이용 편이성 점수”를 1점 준 이유를 알려 주세요?
버스나 지하철등 대중교통에 칸막이 추가설치를 요청합니다
보라동 교통지옥 대중교통열악합니다. 분당선 연장 꼭 필요합니다.
보라동 세브란스 대중교통 개선해주세요
서구 아이푸드파크 대중교통 관련
서남부권-강남구간의 대중교통 개선시급
서판교로 판교원마을 대중교통 개선요청
송도 8공구 호반3차 주민의 대중교통문제 해결해주세요.
송도8공구 옥련동,용현동 연결 대중교통 증설 및 아암1교 문의
송도동 호반베르디움3차 아파트 대중교통 개선요청
수도권 동북부의 열악한 한강 이남 대중교통 개선이 시급합니다.
수원역환승센터로가는 대중교통을 늘려주세요
신규 아파트 단지 대중교통수단 확충 요청
신도시 대중교통문제
신현4리 대중교통 개선 건의
씨사이드파크 접근 대중교통 개선 및 관광활성화 요청
안녕하세요 위례신도시 주민입니다. 위례신도시가 조성된지 꽤 오랜 시간이 흘렀습니다. 하지만 대중교통시설은 아직 미비하고 위례의특성상 버스가 빙둘러가는 노선으로 되어있어 버스를타면 시간이 많이걸려고 의
안녕하세요. 대중교통 이용시 배차간격이 길어 불편함을 겪고 있습니다.
영종역 하늘신도시간 대중교통 확충 및 개선 관련
예솔초 대중교통 확충 (동탄2신도시 순환대로)
용인 세브란스 병원 대중교통 신설관련 민원
용인 한숲시티 6월 셔틀버스 종료시 그에따른 대중교통 대처 방안
용인동백 대중교통 부탁드립니다.
용인한숲시티 광역버스 및 대중교통 신설 진행상황 여부
운정3지구 휴아림 아파트 대중교통 보완요구
운정신도시 대중교통 & 행정시설의 빈익빈 부익부
울산 혁신도시 대중교통(버스) 배차 증차가 어렵다면 운행코스라도 조정해서 배차간격을 줄여주시면 좋겠습니다
의정부 고산지구 대중교통 보완 및 신규 요청
이케아 대중교통
인천 송도 6.8공구 대중교통정책
인천 송도 8공구 모든 입주민이 대중 교통을 고르게 이용 할 수 있도록 인천지하철 3개역을 신설해주세요.
인천시 대중교통 종사자에게 마스크를 지급해주세요
인천시 대중교통 취약지역 및 대중교통 사각지대 관련 문의 건
인후동 1가 안덕원로 대중교통편 관련 민원입니다.
장현동 대중교통이 불편합니다
제2판교테크노밸리 대중교통 확충 건의
증산 버스운행시간 준수/ 대중교통 효울화
진해신항 대중교통개선
창의고 옆 정류장에 잠실행 버스 정차하여 호반 3차를 비롯 목동대중교통 불편을 해결해 주시기를 강력히 요구드립니다.
청덕동 물푸레마을 대중교통 불편 해소 요청
청주시 대중교통 노동자의 깊은 한숨
청현마을 대중교통지옥에서 벗어나게 해주세요
추동공원에 갈수있는 대중교통을 만들어주세요!
출근시간대 대중교통 배차간격에 관한 불편사항
코로나 관련 9200 위례 버스 등 대중교통 이용시
코로나 대중교통 연장운행
코로나 속 대중교통 냉방기 가동에 관해 대책
코로나19 대중교통건의
코로나19로 인한 대중교통 이용시 부담스러기에 자가운행에 따른 공영주차장 개방 또는 임시 주차장 확보 건의
코로나19로인해 단축된 청주시 대중교통 노선원활화
코로나시대를 비웃는 청주시의 대중교통 행정
태전지구-포은대로간 연결도로 조속히 착공바라며, 대중교통 개선 좀 부탁드립니다.
퇴계환승센터~유봉여자고등학교(중학교, 한림대학교) 방면 대중교통 버스 추가, 혹은 개편을 요청합니다.
퇴보한 대중교통 환경 버스감차, 노선감소
파주 출근길 대중교통(특시 운정->광탄방면) 정비좀 해주세요.
파주 출판단지 행복주택 대중교통 문제를 해결해주세요
판교 테크노밸리로 들어가는 현재와 미래의 대중교통을 정리해서 알고 싶습니다.
평택 대중교통 관련
포항 버스나 대중교통시설에 손소독제를 배치해주세요.
풍무동 구도심 계양역 대중교통 확충요청
하남 - 서울 간의 대중 교통 편의 개선 요청 건
하남시 감일지구 대중교통(버스)대책 시급합니다
하남시 대중교통 적극개선요구
하남시에 대중교통을 원활하게 사용할수 있도록 도와 주세요.
한보라마을 대중교통 개선
혁신도시 대중교통 활성화 요청 - 울산시로 이관하지말고 중구청에서 답변바람
현 상지석길 대중교통 상황은 현저하게 낮은 수준입니다.
화성시 광역대중교통 개선에 의견드립니다.
화성시 동탄1 출퇴근 대중교통 배차시간 및 간격
화성시 새솔동 대중교통불편 개선요청'''

#텍스트 가공
r_symbol = re.compile('\W+') 
r_underbar = re.compile('ㅡ') 
r_title = re.compile('대중교통') 
r_title_2 = re.compile('대중') 
r_require = re.compile('요청')
r_require_2 = re.compile('해결')
r_require_3 = re.compile('해소')
r_about = re.compile('관련')
r_complaint = re.compile('민원')

   
complaint = r_symbol.sub(' ', complaint)   
complaint = r_underbar.sub(' ', complaint)    
complaint = r_title.sub(' ', complaint)    
complaint = r_title_2.sub(' ', complaint)
complaint = r_require.sub(' ', complaint)
complaint = r_require_2.sub(' ', complaint)
complaint = r_require_3.sub(' ', complaint)
complaint = r_about.sub(' ', complaint)
complaint = r_complaint.sub(' ', complaint)

#워드 클라우드

    #complaint text파일로 작성
f = open("C:/Users/user/Desktop/team7/민원내용.txt",'w')
l = [complaint]
f.writelines(l)
f.close()

    #hannanum/kkma
f_com = open("C:/Users/user/Desktop/team7/민원내용.txt",'r')
lines_com = f_com.readlines()
f_com.close()
print(lines_com)

temp_hannanum = []

temp_kkma = []

for i in range(len(lines_com)):
	temp_hannanum.append(hannanum.nouns(lines_com[i]))
	temp_kkma.append(kkma.nouns(lines_com[i]))

def flatten(l):
	flatList = []
	for elem in l:
		if type(elem) == list:
			for e in elem:
				flatList.append(e)
		else:
			flatList.append(elem)
	return flatList

word_list_hannanum = flatten(temp_hannanum)
word_list_kkma = flatten(temp_kkma)

word_list_hannanum = pd.Series([x for x in word_list_hannanum if len(x)>1])
pd.DataFrame(word_list_hannanum)

word_list_kkma = pd.Series([x for x in word_list_kkma if len(x)>1])
pd.DataFrame(word_list_kkma)

word_list_hannanum = pd.Series(word_list_hannanum)
word_list_hannanum_20 = word_list_hannanum.value_counts().head(20)
pd.DataFrame(word_list_hannanum_20)

word_list_kkma = pd.Series(word_list_kkma)
word_list_kkma_20 = word_list_kkma.value_counts().head(20)
pd.DataFrame(word_list_kkma_20)

word_list_hannanum_20[0:20].plot.bar()
plt.show()

    #워드클라우드
wordcloud = WordCloud(font_path = font_path, width = 800, height = 800, background_color = 'white')
count_kor = Counter(word_list_hannanum)
wordcloud_kor = wordcloud.generate_from_frequencies(count_kor)
fig_kor = plt.figure(figsize = (10, 10))
plt.axis('off')
plt.imshow(wordcloud)
plt.show()

#처리리관+제목 크롤링
for i in range(34):
    try:
        table = driver.find_element_by_class_name('tbl.default.brd1')
        tbody = table.find_element_by_tag_name("tbody")
        rows = tbody.find_elements_by_tag_name("tr")
        for index, value in enumerate(rows):
            org=value.find_elements_by_tag_name("td")[2]
            print(org.text)
            
        nextpage = driver.find_element_by_css_selector('span.nep_p_next')
        nextpage.click()
        time.sleep(1)            
            
       
    except:
        break

#크롤링된 것을 '지역별민원내용.txt'로 복사해서 붙여넣기


#지역별민원내용.txt 확인
f = open("C:/Users/user/Desktop/team7/지역별민원내용.txt", 'r', encoding = 'utf-8')
lines = f.readlines()
for line in lines:
    print(line)
f.close()

#lines 타입 확인
type(lines)

#처리기관(area)
area = []
for i in lines:
    a = i.split(' ')[0]
    num = len(a) + 1
    area.append(a)

#area 데이터프레임으로 변환
area = pd.DataFrame(area)
area.columns = ['지역']

#csv로 내보내기
area.to_csv("C:/Users/user/Desktop/team7/지역별민원내용.csv")

complaint_area = pd.read_csv("C:/Users/user/Desktop/team7/지역별민원내용.csv", sep=',',engine='python',encoding='utf-8')
complaint_area.set_index('지역', inplace = True)

# 엑셀로 정렬 후 지역별 민원 개수 확




   
