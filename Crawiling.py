import urllib.request as ul
import xmltodict
import pymysql.cursors
import sys
import pprint

conn = pymysql.connect(
    #host='localhost',
    host = 'dailyoasisbackend.cbzjw5cm6v1b.ap-northeast-2.rds.amazonaws.com',
    user='root',
    password='00000000',
    db='daily_oasis',
    charset='utf8'
)

cursor = conn.cursor()

#DB 버전 확인
cursor.execute("SELECT VERSION()")
data=cursor.fetchone()
print(data)

# #기존 테이블 데이터 삭제
# sql = "call del_activity()" # mysql에 정의해둔 프로시저 사용
# cursor.execute(sql)
# conn.commit()

numOfData = 0
numOfRows=100
pageNo=1
areaCode = 1 #서울
#(A=제목순, B=조회순,C=수정일순, D=생성일순) / 대표이미지가 반드시 있는 정렬 (O=제목순, P=조회순, Q=수정일순, R=생성일순)
arrange = 'R' #최신순으로 조회

#포털기관 습득물 데이터 받아오기
while 1:
    #지역기반 리스트 조회(서울)
    areaBasedList_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=TkWnKo4m9%2Bg22VKIj4%2B8C6Y%2BGwnrqO6QbFL5gvsi97hijXief5DvTU5rwE79p9wmY%2BpZVwwfqWBPT%2Fs9e%2BxvVQ%3D%3D&areaCode={areaCode}&MobileOS=ETC&MobileApp=DailyOasis&numOfRows={numOfRows}&pageNo={pageNo}&arrange={arrange}"
    request = ul.Request(areaBasedList_url)
    response = ul.urlopen(request)
    rescode = response.getcode()

    if(rescode == 200):
        responseData = response.read()  # 요청받은 데이터를 읽음
        areaBasedList = xmltodict.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
        #pprint.pprint(areaBasedList) #정상적으로 데이터가 출력되는지 확인

        try :
            A_items = areaBasedList["response"]["body"]["items"]["item"]  # item 데이터만 정제
        except:
            print("수집완료")
            sys.exit()

        totalCount = areaBasedList["response"]["body"]["totalCount"]
        pageNo += 1
        print("총 데이터 개수 : \n"+totalCount+"\n")


        for A_item in A_items:  # 다수의 item들을 하나씩 뽑아온다.
            numOfData += 1
            print(numOfData)
            print(pageNo)

            #이미지 있는 것만 추출
            if'firstimage' in A_item and 'firstimage' in A_item: #이미지 태그가 존재하면서 none이 아닐경우
                print("이미지 정보가 있음")
                #pprint.pprint(A_item)
                # print(pageNo)
                # print(numOfData)

                name = None
                eventTime = ''
                eventStartDate = ''
                eventEndDate = None
                eventPlace = None
                discription = ''
                mapx = None
                mapy = None
                tel = ''
                img = None

                try:
                    mapx = A_item["mapx"]
                except(KeyError, TypeError):
                    print("mapx : 조회불가")
                try:
                    mapy = A_item["mapy"]
                except(KeyError, TypeError):
                    print("mapy : 조회불가")

                name = A_item["title"]
                img = A_item["firstimage"]

                print(name)
                #컨텐츠 ID 추출
                contentid = A_item["contentid"]
                # 서울에 있는 총 관광정보 약 291,600개
                # 관광지 12(238개) / 문화시설 14(211 개) / 축제-공연-행사 15(187개)/ 여행코스 25(0개-상세정보없음) / 레포츠 28(0개-상세정보없음) / 숙박 32 / 쇼핑 38 / 음식 39
                contentTypeId = 12

                #컨텐츠 ID를 사용하여 상세조회 (서울)
                detailIntro_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailIntro?ServiceKey=TkWnKo4m9%2Bg22VKIj4%2B8C6Y%2BGwnrqO6QbFL5gvsi97hijXief5DvTU5rwE79p9wmY%2BpZVwwfqWBPT%2Fs9e%2BxvVQ%3D%3D&contentId={contentid}&contentTypeId={contentTypeId}&MobileOS=ETC&MobileApp=AppTest"
                request = ul.Request(detailIntro_url)
                response = ul.urlopen(request)
                rescode = response.getcode()

                if(rescode == 200):
                    responseData2 = response.read()
                    detailIntro = xmltodict.parse(responseData2)
                    #pprint.pprint(detailIntro)
                    # 컨텐츠타입(contentTypeId)에 대한 상세정보
                    if detailIntro["response"]["body"]["items"] is not None: #상세정보가 존재할 경우
                        B_item = detailIntro["response"]["body"]["items"]["item"]
                        print("상세 정보가 있음")
                        pprint.pprint(B_item)

                        print("-----------------------------------------------")

                        print("[지역기반조회]")
                        print("제목 : " + A_item["title"])
                        print("컨텐츠ID : " + A_item["contentid"])
                        print("firstimage  : " + A_item["firstimage"])
                        try:
                            mapx = A_item["mapx"]
                        except(KeyError, TypeError):
                            print("mapx : 조회불가")
                        try:
                            mapy = A_item["mapy"]
                        except(KeyError, TypeError):
                            print("mapy : 조회불가")
                        print('\n')
                        print("[소개상세정보조회]")
                        '''날짜'''
                        try:
                            print("행사날짜 : " + B_item["eventstartdate"] + "~" + B_item["eventenddate"])
                            eventStartDate = B_item["eventstartdate"]
                            eventEndDate = B_item["eventenddate"]
                        except(KeyError, TypeError):
                            print("행사기관 : 조회불가")
                        try:
                            print("행사시작일(opendate) : " + B_item["opendate"])
                            eventStartDate += B_item["opendate"]
                        except(KeyError, TypeError):
                            print("행사시작일 : 조회불가")

                        '''장소'''
                        try:
                            print("행사장소 : " + B_item["eventplace"])
                            eventPlace = B_item["eventplace"]
                        except(KeyError, TypeError):
                            print("행사장소 : 조회불가")

                        '''시간'''
                        try:
                            print("행사시간(playtime) : " + B_item["playtime"])
                            eventTime = B_item["playtime"]
                        except (KeyError, TypeError):
                            print("행사시간(playtime) : 조회불가")
                        try:
                            print("행사시간(usetime) : " + B_item["usetime"])
                            eventTime += B_item["usetime"]
                        except (KeyError, TypeError):
                            print("행사시간(usetime) : 조회불가")
                        try:
                            print("행사시간(usetimeculture) : " + B_item["usetimeculture"])
                            eventTime += B_item["usetimeculture"]
                        except (KeyError, TypeError):
                            print("행사시간(usetimeculture) : 조회불가")
                        try:
                            print("휴무여부(restdate) : " + B_item["restdate"])
                            eventTime += B_item["restdate"]
                        except (KeyError, TypeError):
                            print("휴무여부(restdate) : 조회불가")
                        try:
                            print("휴무여부(restdateculture) : " + B_item["restdateculture"])
                            eventTime += B_item["restdateculture"]
                        except (KeyError, TypeError):
                            print("휴무여부(restdateculture) : 조회불가")

                        '''전화번호'''
                        try:
                            print("전화번호(sponsor1tel) : " + B_item["sponsor1tel"])
                            tel = B_item["sponsor1tel"]
                        except(KeyError, TypeError):
                            print("전화번호(sponsor1tel) : 조회불가")
                        try:
                            print("전화번호(sponsor2tel) : " + B_item["sponsor2tel"])
                            tel = B_item["sponsor2tel"]
                        except(KeyError, TypeError):
                            print("전화번호(sponsor2tel) : 조회불가")
                        try:
                            print("전화번호(infocenterleports) : " + B_item["infocenterleports"])
                            tel += B_item["infocenterleports"]
                        except(KeyError, TypeError):
                            print("전화번호(infocenterleports) : 조회불가")
                        try:
                            print("전화번호(infocenter) : " + B_item["infocenter"])
                            tel += B_item["infocenter"]
                        except(KeyError, TypeError):
                            print("전화번호(infocenter) : 조회불가")
                        try:
                            print("전화번호(infocenterculture) : " + B_item["infocenterculture"])
                            tel += B_item["infocenterculture"]
                        except(KeyError, TypeError):
                            print("전화번호(infocenterculture) : 조회불가")


                        '''설명'''
                        try:
                            print("설명(subevent) : " + B_item["subevent"])
                            discription = B_item["subevent"]
                        except (KeyError, TypeError):
                            print("설명(subevent) : 조회불가")
                        try:
                            print("설명(program) : " + B_item["program"])
                            discription += B_item["program"]
                        except (KeyError, TypeError):
                            print("설명(program) : 조회불가")
                        try:
                            print("설명(expguide) : " + B_item["expguide"])
                            discription += B_item["expguide"]
                        except (KeyError, TypeError):
                            print("설명(expguide) : 조회불가")
                        try:
                            print("주차정보(parking) : " + B_item["parking"])
                            discription += '주차장 정보 : ' + B_item["parking"] + ' '
                        except (KeyError, TypeError):
                            print("주차정보(parking) : 조회불가")
                        try:
                            print("주차정보(parkingculture) : " + B_item["parkingculture"])
                            discription += '주차장 정보 : ' + B_item["parkingculture"] + ' '
                        except (KeyError, TypeError):
                            print("주차정보(parkingculture) : 조회불가")
                        try:
                            print("주차요금(parkingfee) : " + B_item["parkingfee"])
                            discription += '주차장 요금 : ' + B_item["parkingfee"] + ' '
                        except (KeyError, TypeError):
                            print("주차요금(parkingfee) : 조회불가")
                        try:
                            print("요금(usefee) : " + B_item["usefee"])
                            discription += ' 요금 : ' + B_item["usefee"] + ' '
                        except (KeyError, TypeError):
                            print("요금(usefee) : 조회불가")
                        try:
                            print("나이제한(expagerange) : " + B_item["expagerange"])
                            discription += '연령 정보 : '+B_item["expagerange"] + ' '
                        except (KeyError, TypeError):
                            print("나이제한(expagerange) : 조회불가")
                        try:
                            print("인원제한(accomcount) : " + B_item["accomcount"])
                            discription += '인원수 정보 :' + B_item["accomcount"]
                        except (KeyError, TypeError):
                            print("인원제한(accomcount) : 조회불가")
                        try:
                            print("인원제한(scale) : " + B_item["scale"])
                            discription += '장소 정보 :' + B_item["scale"]
                        except (KeyError, TypeError):
                            print("인원제한(scale) : 조회불가")

                        print("-----------------------------------------------")
                        print("\n")
                        # print("[DB에 들어갈 정제된 데이터]")
                        # print("엑티비티 이름 : "+name)
                        # print("엑티비티 시간: "+eventTime)
                        # print("엑티비티 장소 : "+eventPlace)
                        # print(discription)
                        # print("엑티비티 x좌표 : "+mapx)
                        # print("엑티비티 y좌표: "+mapy)
                        # print("엑티비티 전화번호: "+tel)
                        # print("엑티비티 이미지 : "+img)
                        print("-----------------------------------------------")

                        longitude = mapx
                        latitude =mapy
                        sql = "insert into daily_oasis.main_activity(name, discription, eventStartDate, eventEndDate, eventTime, eventPlace ,longitude ,latitude, tel, img) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (name, discription, eventStartDate, eventEndDate, eventTime, eventPlace, longitude, latitude, tel, img))
                        conn.commit()
    pageNo += 1

    # if(numOfData >= int(totalCount)):
    #     print("데이터 수집이 완료 되었습니다!")
    #     sys.exit()



#if 'subevent' in B_item and 'sponsor1tel' in B_item and B_item["subevent"] is not None: #subevent 설명이 있을경우



