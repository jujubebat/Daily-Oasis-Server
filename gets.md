# 프로젝트를 통해 배운 지식

* ## Django Framework
  - ### 장고의 MVC 모델
    장고는 MVT 모델을 따른다.
    + 장고의 Model = Model (데이터)
    + 장고의 View  = Control (비지니스 로직)
    + 장고의 Template = View (화면 UI 정의)
  - ### MVT 처리 과정
    + 1.클라이언트로부터 요청을 받으면, URLconf를 이용하여 URL을 분석
    + 2.URL 분석 결과를 통해 URL에 대한 처리를 담당할 View를 결정
    + 3.View는 자신의 로직을 실행, 데이터베이스 처리가 필요하면 Model을 통해 처리하고 결과를 반환 받음
    + 4.View의 로직처리가 끝나면 Template을 통해 HTML 파일을 생성하고 클라이언트에게 보냄
  - ### ORM(Object Relational Mapping)
    + 객체지향(OOP) 언어와 데이터를 다루는 RDBMS와의 상이한 시스템을 매핑하여, 데이터 관련 OOP 프로그래밍을 쉽게 하도록 도와주는 기술
    + Model Class를 통해서 객체를 만들고 이 객체를 통해서 DB에 접근한다.(Class == DB table)
  - ### QuerySet(쿼리셋)
    + 전달받은 Django Model의 객체 목록, QuerySet은 데이터베이스로부터 데이터를 읽고, 필터를 걸거나 정렬을 할 수 있다. 
    + objects - Model Manager, 데이터베이스와 Django Model 사이의 Query 인터페이스 역할을 한다.
    + objects를 사용하여 다수의 데이터를 가져오는 함수를 사용할 때 반환되는 객체가 QuerySet
* ## DRF(Django Rest Framework)
  - ### REST API 개발을 도와주는 Django 라이브러리 
  - ### Serializer(직렬화)
    + QuerySet, Model instance 등의 복잡한 데이터를 JSON, XML 등으로 변환시켜줌
  
* ## OPEN API를 활용한 데이터 크롤링
    + 한국 관광공사 Tour API
    + Python, MySQL 연동을 통한 데이터 크롤링 진행
 
* ## 작업 스케쥴러
    + [윈도우 작업 스케쥴러](https://wikidocs.net/5857)
    + [리눅스 작업 스케쥴러](https://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B0%98%EB%B3%B5_%EC%98%88%EC%95%BD%EC%9E%91%EC%97%85_cron,_crond,_crontab)
    + [django-crontab](https://pypi.org/project/django-crontab/) 라이브러리를 사용하면, 손쉽게 Linux crontab에 등록을 할 수 있음

* ## Stored procedure
    + 특정한 작업을 수행하는 일련의 SQL문들을 사전에 컴파일해서 서버에 저장해둔 것 
    + 빠른 SQL 실행시간 : SP은 만들어질 때 SQL구문이 분석되고 최적화 된다, 한 번 실행된 후에는 메모리에 캐시 됨.
    + 네트워크 부하 감소 : 클라이언트에서는 다수의 SQL 구문을 보낼 필요 없이 SP를 실행 시키는 명령문만 보내면 된다. 
    + 모듈별 프로그래밍 : 함수처럼 계속 호출하여 사용할 수 있음. 개발 언어에 상관없이 SP 수정 가능(유지보수성)
    + 보안성 향상 : SP를 통해서만 데이터에 접근할 수 있도록 하면 보안성을 얻을 수 있다.

* ## REST(Representational State Transfer)
   + REST : 자원을 이름으로 구분하여 해당 자원의 정보를 주고받는 것. HTTP URL을 통해 자원을 명시하고 HTTP Method를 통해 해당 자원에 대한 CRUD을 적용하는 것
   + REST API : REST 기반으로 서비스 API를 구현한 것
   + RESTful : REST라는 아키텍쳐를 구현하는 웹 서비스를 나타내기 위해 사용되는 용어 
   + REST 장점 : HTTP 프로토콜의 인프라를 그대로 활용할 수 있음, 서버와 클라이언트의 역할을 분리, REST API 메시지를 통해 의미를 쉽게 파악, 확장성과 재사용성이 높음, SOAP의 UDDI와 같은 중간 매개체 없이 리소스 제공자가 직접 리소스 요청자에게 데이터 제공
   + REST 단점 : HTTP Method가 제한적이다. 표준이 존재하지 않는다.
   + rest api user은 명사여야함
* ## JWT 토큰 인증
* ## 태그기반 관광지 추천 원리
 - 자카드 알고리즘
* ## CORS
* ## PANDAS
* ## AWS
 + EC2
 + RDS
 + ACM
 + Rout 53
-Race Condition
-윈도우, 리눅스상에서의 MYSQL 설정
-



