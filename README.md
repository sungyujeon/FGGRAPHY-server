# final-project-server



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

- User 정보 조회 http://127.0.0.1:8000/accounts/{username}/

- User 정보 삭제 http://127.0.0.1:8000/accounts/{username}/ `method:DELETE`

- follow http://127.0.0.1:8000/accounts/{username}/follow/ `method: POST` 



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
- 컬렉션 생성 http://127.0.0.1:8000/api/v1/movies/collections/ `method: POST / data: title`

- 단일 컬렉션 정보 http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/
- 컬렉션 수정 http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/ `method: PUT / data: title`

- 컬렉션 삭제 http://127.0.0.1:8000/api/v1/movies/collections/{collection_pk}/ `method: DELETE`

- 컬렉션 내 영화 추가 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/{movie_pk}/ `method: POST`
- 컬렉션 내 영화 삭제 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/{movie_pk}/ `method: DELETE`
- 컬렉션 좋아요 http://127.0.0.1:8000/api/v1/movies/user-collections/{collection_pk}/like/ `method: POST`



##### Infinite Scroll

- 리뷰 http://127.0.0.1:8000/api/v1/movies/infinite-scroll/reviews/?page_num={page_num}





## sass with vue
