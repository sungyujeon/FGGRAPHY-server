# final-project-server



## 0. 프로젝트 시작하기

1. 팀 구성 : 황상필(팀장), 전선규(팀원)
2. 역할 분담
   - 백앤드 : 전선규
   - 프론트앤드 : 황상필
     - 프론트앤드 기능구현 중 홈페이지 로딩화면 / Recommendation / 별점 / 예고편은 선규형이 작성
3. 프로젝트 협업 환경
   - 원활한 프로젝트 진행을 위해 5/15(토) 첫 미팅 + 5/20(목)~5/27(목) 총 9일간 모두 직접 만나서 진행(온라인진행X)
   - API서버에서 데이터를 정제하여 url정보를 README에 저장하여 보내주면 이를 활용하여 데이터를 받아오고 Vue를 이용하여 화면 구성
   - 잠자는 시간 제외하고 모든 시간을 함께 코딩하면서 서로 모르는부분은 알려주고 끊임없는 소통을 통해 원하는 기능구현을 모두 할 수 있도록 최선을 다했다.



## 1. 목표 서비스 구현 및 실제 구현 정도

1. 목표 서비스 구현 목록
   - 회원가입 / 로그인 / 로그아웃 기능
   - 홈페이지 carousel구성 및 랭킹 차트 보여주기
   - 랭킹 탭 개설 및 장르별 랭킹 페이지 구성(홈페이지와 동일한 구조)
   - 검색 기능
   - 최상위 평점 기준 추천 영화목록 보여주기
   - 개별 영화 상세정보 및 리뷰 / 코맨트(작성, 수정, 삭제) / 좋아요 / 예고편
   - 유저별 프로필페이지 구현(티어, 최근리뷰남긴 영화목록, 높은 평점을 준 영화목록, 팔로우)
   - 컬렉션, 랭킹1등 특전혜택(랭킹 페이지 포스터 변경 권한 부여)
2. 실제 구현 정도
   - 컬렉션을 제외한 모든 목표 서비스 구현 성공



## 2. 데이터베이스 모델링(ERD)



## 3. 필수 기능에 대한 설명

1. 랭킹을 기준으로 모든 페이지가 구성되었다고 해도 틀린말이 아닐정도로 랭킹이 중요하다.
   - 전체랭킹 3등이내 / 각 장르별 랭킹 3등이내라면 내가 높은 평점을 준 영화 10개가 페이지에 노출되는 영광을 누릴 수 있다.(랭킹은 열심히 활동하게되면 포인트를 기준으로 하루 한 번 정산하는 시스템)
   - 각 장르별 랭킹 1등이 되면 각 장르의 대표 영화 포스터를 수정할 수 있는 권한을 부여
   - 랭킹에 따라 %로 티어가 부여되고 해당 티어는 내 아이디옆에 색과함께 구분되어 나타남
2. 리뷰 작성, 좋아요, 팔로우, 댓글 작성 등의 기능은 유저 편의성을 위해 비동기식 처리를 활용하였음
   - 세부적으로 리뷰는 오로지 한 영화에 대해 한 번만 남기도록 처리하였고, 모든 수정/삭제 권한은 내가 쓴 글에 대해서만 가능하도록 로직을 구현하였다.
3. 검색 기능의 경우 검색어가 들어간 모든 영화를 검색하도록 로직을 구현하였다.
4. 추천영화 및 예고편은 3D기술을 접목시킨 기능구현으로 보는이로 하여금 신비로움과 재미를 모두 잡을 수 있도록 신경써서 구현하였다.



## 4. 배포 서버 URL



## 5. 기타(느낀점)



## INSERT DATA

- `$ python manage.py makemigrations`

- `$ python manage.py migrate`

- http://127.0.0.1:8000/api/v1/movies/insert-data/

  `에러 발생 시 movies/modules.py.InsertData.my_exec >> self.get_seed_users() 주석 처리`



## TEST

##### Amdin

- genre ranker 모델 init http://127.0.0.1:8000/api/v1/movies/init-genre-ranker/

- 전체 랭킹 갱신 http://127.0.0.1:8000/accounts/calc-ranking/

- 장르별 랭킹 갱신 http://127.0.0.1:8000/api/v1/movies/calc-genre-ranking/

  



##### Account

- User별 최근 리뷰 n개 조회 http://127.0.0.1:8000/api/v1/movies/reviews/{username}/latest/?review_num={review_num}

  <small>>> parameter 넣지 않으면 10개로 설정</small>

- User 정보 조회 http://127.0.0.1:8000/accounts/profile/{username}/

- User 정보 삭제 http://127.0.0.1:8000/accounts/profile/{username}/ `method:DELETE`

- follow http://127.0.0.1:8000/accounts/profile/{username}/follow/ `method: POST` 



##### Ranking

- 전체 상위 랭커 n명 정보 http://127.0.0.1:8000/accounts/top-ranked/?user_num={user_num}

- 전체 상위 랭커 n명의 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/top-ranked/?ranker_num={ranker_num}&movie_num={movie_num}

  <small>>> parameter 넣지 않으면 5명, 10개로 설정</small>

- 전체 장르별 랭커 n명의 추천영화 n개 출력 http://127.0.0.1:8000/api/v1/movies/genres/top-ranked/?ranker_nums={ranker_nums}&movie_num={movie_num}

  `type: json`, `key(genre_id): value(rankers object list)`

  key는 genre_id, value는 랭킹 n등 안에 드는 사람들의 genre_user 객체 리스트

- 특정 장르별 랭커 n명의 추천 영화 n개 출력 http://127.0.0.1:8000/api/v1/movies/genres/{genre_id}/top-ranked/?ranker_nums={ranker_nums}&movie_num={movie_num} `위와 동일(genre_id) 추가`

- 장르별 랭킹 페이지 전체 정보(각 장르별 랭킹 1등이 등록한 영화, default=가장 평점 높게 준 영화, 리뷰 많은 장르 순으로 정렬) http://127.0.0.1:8000/api/v1/movies/genres/rankings/

- 장르별 랭킹 페이지에서 유저 1등의 영화 정보 수정 http://127.0.0.1:8000/api/v1/movies/genres/rankings/{genre_id}/ `method: PUT / data: movie: {movie_id}`



##### Movie

- search http://127.0.0.1:8000/api/v1/movies/search/{search_input}/

- 모든 영화 정보 http://127.0.0.1:8000/api/v1/movies/
- 단일 영화 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/
- 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/top-rated/?movie_count={movie_count}
- 유저별 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/users/{username}/top-rated/?movie_count={movie_count}
- 유저 장르별 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/users/{username}/genres/{genre_id}/top-rated/?movie_count={movie_count}



##### Genre(장르별 영화)

- 모든 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/
- 개별 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/10751/datas
- 개별 장르의 모든 영화 정보 http://127.0.0.1:8000/api/v1/movies/genres/10751/
- review 많은 순 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/top-reviewed/

- 전체 장르별 랭커 n명 출력 http://127.0.0.1:8000/api/v1/movies/genres/top-ranked/?ranker_nums={ranker_nums}

  `type: json`, `key(genre_id): value(rankers object list)`

  key는 genre_id, value는 랭킹 n등 안에 드는 사람들의 genre_user 객체 리스트


##### Movie Detail 내(1개 영화)

- Review
  - 모든 리뷰 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/
  - 리뷰 작성 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/ `method: POST / data: content`
  - 단일 리뷰 정보 http://127.0.0.1:8000/api/v1/movies/reviews/{review_pk}/
  - 리뷰 수정 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_pk}/ `method: PUT / data: content`
  - 리뷰 삭제 http://127.0.0.1:8000/api/v1/movies/reviews/{review_pk}/ `method: DELETE`
  - 리뷰 좋아요 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_pk}/like/ `method: POST`
  - movie에 user가 review를 작성했는지 여부 조회 http://127.0.0.1:8000/api/v1/movies/{movie_pk}/is-review/ 
- Comment

  - 모든 댓글 정보 http://127.0.0.1:8000/api/v1/movies/reviews/{review_pk}/comments/
  - 댓글 작성 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/ `method: POST / data: content`
  - 단일 댓글 정보 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/
  - 댓글 수정 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/ `method: PUT / data: content`
  - 댓글 삭제 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/ `method: DELETE`
- Rating
  - 평점 가져오기 http://127.0.0.1:8000/api/v1/movies/{movie_id}/rating/
  - 평점 남기기 / 수정하기 / 삭제하기 http://127.0.0.1:8000/api/v1/movies/{movie_id}/rating/ `method: POST / data: rating`




##### Collection

- 모든 컬렉션 정보 http://127.0.0.1:8000/api/v1/movies/collections/
- 한 유저의 컬렉션 전체 조회 http://127.0.0.1:8000/api/v1/movies/users/{username}/collections/
- 컬렉션 생성 http://127.0.0.1:8000/api/v1/movies/collections/ `method: POST / data: title`
- 단일 컬렉션 정보 조회http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/
- 컬렉션 수정 http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/ `method: PUT / data: title`
- 컬렉션 삭제 http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/ `method: DELETE`
- 컬렉션 내 영화 추가 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/{movie_pk}/ `method: POST`
- 컬렉션 내 영화 삭제 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/{movie_pk}/ `method: DELETE`
- 컬렉션 좋아요 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/like/ `method: POST`



##### Infinite Scroll

- 리뷰 http://127.0.0.1:8000/api/v1/movies/infinite-scroll/reviews/?page_num={page_num}





## sass with vue