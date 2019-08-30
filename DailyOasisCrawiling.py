# #관광공사 API로 데이터가져오기
#
# import urllib.request as ul
# import xmltodict
#
# #데이터를 받을 url
# url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=XkqweN6T4XhKJwYFZTcyVC2BYwqckYugERg6R%2FMu26u96JtR7X8ifsqv5AWZQsHcRAty%2FAYkQflO%2FC3SAm5OEw%3D%3D&areaCode=1&MobileOS=ETC&MobileApp=DailyOasis&numOfRows=100&modifiedtime=2019"
# request = ul.Request(url) #요청 메세지를 보낸다.
# response = ul.urlopen(request) #응답 메세지를 오픈한다.
# rescode = response.getcode() #제대로 데이터가 수신됐는지 확인하는 코드 성공시 200
#
# if (rescode == 200):
#     responseData = response.read() #요청받은 데이터를 읽음
#     rD = xmltodict.parse(responseData) #XML형식의 데이터를 dict형식으로 변환시켜줌
#
#     #  print(rD) #정상적으로 데이터가 출력되는지 확인
#
#     w_data = rD["response"]["body"]["items"]["item"] #item 데이터만 정제
#
#
#     for i in w_data:
#         print(i)
#
#
#     # for i in w_data: #다수의 item들을 하나씩 뽑아온다.
#     #     if 'addr1' in i: # item에 'addr1'이란 키가 있으면,
#     #         print("관광명 : "+i["title"])
#     #         print("주소 : "+i["addr1"]+"\n")

#경찰청 API로 분실물 데이터 가져오기(MySQL연동)










#관광지 12 / 문화시설 14 / 축제-공연-행사 15/ 여행코스 25 / 레포츠 28 / 숙박 32 / 쇼핑 38 / 음식 39


import urllib.request as ul
import xmltodict
import pymysql.cursors
import sys
import pprint

# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='0000',
#     db='findlost',
#     charset='utf8'
# )
#
# cursor = conn.cursor()
#
# #DB 버전 확인
#
# # cursor.execute("SELECT VERSION()")
# # data=cursor.fetchone()
# # print(data)
#
# #insert 예제
#
# # itemName = 'sextoy'
# # lostPlace = 'myhome'
# # sql = 'insert into lost_items(itemName, lostPlace) values(%s, %s)'
# # cursor.execute(sql, (itemName,lostPlace))
# # conn.commit()
#
#
# #기존 테이블 데이터 삭제
# sql = "call del()" # mysql에 정의해둔 프로시저 사용
# cursor.execute(sql)
# conn.commit()

numOfData = 0
numOfRows=100
pageNo=1
contentTypeId = 15
areaCode = 1 #서울


#포털기관 습득물 데이터 받아오기
while 1:
    areaBasedList_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey=TkWnKo4m9%2Bg22VKIj4%2B8C6Y%2BGwnrqO6QbFL5gvsi97hijXief5DvTU5rwE79p9wmY%2BpZVwwfqWBPT%2Fs9e%2BxvVQ%3D%3D&areaCode={areaCode}&MobileOS=ETC&MobileApp=DailyOasis&numOfRows={numOfRows}&pageNo={pageNo}&modifiedtime=2019"
    request = ul.Request(areaBasedList_url)  # 요청
    # 메세지를 보낸다.
    response = ul.urlopen(request)  # 응답 메세지를 오픈한다.
    rescode = response.getcode()  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200


    if (rescode == 200):
        responseData = response.read()  # 요청받은 데이터를 읽음
        rD = xmltodict.parse(responseData)  # XML형식의 데이터를 dict형식으로 변환시켜줌
        print(rD) #정상적으로 데이터가 출력되는지 확인
        w_data = rD["response"]["body"]["items"]["item"]  # item 데이터만 정제
        totalCount = rD["response"]["body"]["totalCount"]
        pageNo += 1

        for i in w_data:  # 다수의 item들을 하나씩 뽑아온다.
            numOfData += 1
            print("지역기반조회")
            print(pageNo)
            print(numOfData)
            print("제목 : " + i["title"])
            print("컨텐츠ID : " + i["contentid"])
            #print("firstimage  : " + i["firstimage"])
            #print("mapx : " + i["mapx"])
            #print("mapy: " + i["mapy"])


            # sql = "insert into main_lostitems(managementID, findYmd, productName, keepPlace, productImg, productDesc, productClass) values(%s, %s, %s, %s, %s, %s, %s)"
            # cursor.execute(sql, (i["atcId"], i["fdYmd"], i["fdPrdtNm"], i["depPlace"], i["fdFilePathImg"], i["fdSbjt"], i["prdtClNm"]))
            # conn.commit()

            contentid = i["contentid"]

            detailIntro_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailIntro?ServiceKey=TkWnKo4m9%2Bg22VKIj4%2B8C6Y%2BGwnrqO6QbFL5gvsi97hijXief5DvTU5rwE79p9wmY%2BpZVwwfqWBPT%2Fs9e%2BxvVQ%3D%3D&contentId={contentid}&contentTypeId={contentTypeId}&MobileOS=ETC&MobileApp=AppTest"

            #detailCommon_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey=XkqweN6T4XhKJwYFZTcyVC2BYwqckYugERg6R%2FMu26u96JtR7X8ifsqv5AWZQsHcRAty%2FAYkQflO%2FC3SAm5OEw%3D%3D&contentId={contentid}&defaultYN=Y&MobileOS=ETC&MobileApp=AppTest"


            request = ul.Request(detailIntro_url)  # 요청
            # 메세지를 보낸다.
            response = ul.urlopen(request)  # 응답 메세지를 오픈한다.
            rescode = response.getcode()  # 제대로 데이터가 수신됐는지 확인하는 코드 성공시 200

            if (rescode == 200):
                responseData2 = response.read()  # 요청받은 데이터를 읽음
                rD2 = xmltodict.parse(responseData2)  # XML형식의 데이터를 dict형식으로 변환시켜줌
                pprint.pprint(rD2)  # 정상적으로 데이터가 출력되는지 확인

                # 컨텐츠타입(contentTypeId)에 맞는 데이터 이면서, subevent 정보가 존재하는 데이터만 출력
                # if rD2["response"]["body"]["items"] is not None and rD2["response"]["body"]["items"]["item"]["subevent"]is not None:
                #     w_data2 = rD2["response"]["body"]["items"]["item"]  # item 데이터만 정제
                #     #pprint.pprint(w_data)
                #     print("제목 : " + i["title"])
                #     print("컨텐츠ID : " + i["contentid"])
                #     print("소개상세정보조회")
                #     print("장소 : " + w_data2["eventplace"])
                #     print("이벤트 날짜 및 시간 : " + w_data2["playtime"])
                #     print("전화번호 : " + w_data2["sponsor1tel"])
                #     print("설명 : " + w_data2["subevent"])
                #     #print("설명 : " + w_data["program"])


            if (numOfData >= int(totalCount)):
                print("데이터 수집이 완료 되었습니다!")
                sys.exit()





