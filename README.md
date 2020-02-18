# 데일리오아시스 - Server
개인의 관광 취향을 고려하여 매일 관광지를 추천해주는 서비스
(본 저장소는 데일리오아시스 API 서버 입니다.)

# 서비스 요약
1. 사용자가 선택한 '관광 취향태그'와 사용자의 주거지 위치를 고려하여 매일 3개의 관광지를 추천해줍니다. 
2. 추천된 관광지를 실제로 방문하면 GPS 기반으로 '방문완료'를 할 수 있습니다. (이를 퀘스트 수행이라고 합니다.)
3. 사용자는 퀘스트 수행을 완료함으로써 경험치, 칭호등의 보상을 받아 사용자의 케릭터를 육성 시킬 수 있습니다. 
4. 데일리 오아시스에서 제공하는 관광 정보는 모두 한국광관공사 Tour api로 부터 제공받아 양질의 관광지에 대한 선별을 거쳤습니다.
5. 사용자는 지도에 표시되는 관광지에 대한 상세정보(운영시간, 상세설명, 리뷰)를 얻을 수 있습니다.
6. 관광지 리뷰는 사용자가 실제로 '방문완료'를 해야 작성할 수 있기 때문에 신뢰도가 높은 리뷰 입니다. 

# 기술 스택 & 시스템 구성도
- Front-end : react
- Back-end : django rest framework
- Hosting : AWS(EC2, RDS, LB, S3, Route, ACM..)

# 데일리오아시스 API 서버 기능
데일리오아시스 서버는 서비스 구현한 API를 다음과 같이 제공합니다. 
- /signup : 회원가입(JWT 토큰인증기반)
- /login : 로그인(JWT 토큰인증기반)
- /currentUser : 현재 유저에 대한 정보 제공
- /currentQuest : 현재 유저가 추천받은 관광데이터 목록 제공
- /doneQuest : 현재 유저가 '방문완료'한 관광데이터 목록 제공
- /userTitleList : 유저의 칭호 목록 제공
- /updateUserAddress : 유저의 주거지 주소 수정 기능
- /updateUserTitle : 유저의 대표 칭호 수정 기능
- /updateUserPreference : 유저의 취향태그 수정 기능
- /updateUserNickname : 유저의 닉네임 수정 기능
- /activityList : 모든 관광 데이터 제공
- /activityListByPreference : '관광 취향태그'별 관광 데이터 제공
- /characterList : 케릭터 데이터 제공
- /titleList : 칭호 데이터 제공
- /writeReview : 리뷰 작성 기능
- /finishQuest : 관광지 '방문완료' 처리
- /activityReview : 관광지와 해당 관광지의 리뷰 목록 제공



