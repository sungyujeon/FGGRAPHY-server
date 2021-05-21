# final-project-server



## INSERT DATA

- `$ python manage.py makemigrations`
- `$ python manage.py migrate`
- `http://127.0.0.1:8000/api/v1/movies/TMDB/`  insert TMDB movie datas
- `http://127.0.0.1:8000/accounts/seed-user/` insert users
- `http://127.0.0.1:8000/api/v1/movies/seed-rating/` insert ratings in Movie_User Model
- `http://127.0.0.1:8000/api/v1/movies/count-ratings/` count ratings and insert avg, count fields in Movie Model
- `http://127.0.0.1:8000/accounts/calc-ranking/` ranking



## TEST

##### Movie

- 모든 영화 정보 http://127.0.0.1:8000/api/v1/movies/
- 단일 영화 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/
- 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/top-rated/{n}/



##### Movie Detail 내(1개 영화)

- 모든 리뷰 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/

  postman : data(content)



- 모든 댓글 정보(하는중)

  http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_id}/comments/

- 

##### Account

- 전체 랭킹 갱신(admin) http://127.0.0.1:8000/accounts/calc-ranking/
- 전체 상위 랭커 n명 정보 http://127.0.0.1:8000/accounts/top-ranked/{n}/
- 
