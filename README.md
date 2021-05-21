# final-project-server



## INSERT DATA

- $ python manage.py makemigrations
- $ python manage.py migrate
- http://127.0.0.1:8000/api/v1/movies/TMDB/  insert TMDB movie datas
- http://127.0.0.1:8000/accounts/seed-user/ insert users
- http://127.0.0.1:8000/api/v1/movies/seed-review/ insert reviews
- http://127.0.0.1:8000/api/v1/movies/count-reviews/ count genre reviews
- http://127.0.0.1:8000/api/v1/movies/seed-comment/ insert comments
- http://127.0.0.1:8000/api/v1/movies/seed-rating/ insert ratings in Movie_User_Rating Model
- http://127.0.0.1:8000/api/v1/movies/count-ratings/ count ratings and insert avg, count fields in Movie Model
- http://127.0.0.1:8000/accounts/calc-ranking/ ranking



## TEST

##### Movie

- 모든 영화 정보 http://127.0.0.1:8000/api/v1/movies/
- 단일 영화 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/
- 평점 상위 n개 영화 정보 http://127.0.0.1:8000/api/v1/movies/top-rated/{n}/



##### Genre(장르별 영화)

- 모든 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/
- 개별 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/10751/datas
- 개별 장르의 모든 영화 정보 http://127.0.0.1:8000/api/v1/movies/genres/10751/
- review 많은 순 장르 정보 http://127.0.0.1:8000/api/v1/movies/genres/top-reviewed/



##### Movie Detail 내(1개 영화)

- Review
  - 모든 리뷰 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/

  - 리뷰 작성 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/

    postman: data(content) / POST

  - 단일 리뷰 정보 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_pk}/

  - 리뷰 수정 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_pk}/

    postman: data(content) / PUT

  - 리뷰 삭제 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/{review_pk}/

    postman: DELETE

- Comment

  - 모든 댓글 정보 http://127.0.0.1:8000/api/v1/movies/reviews/{review_pk}/

  - 댓글 작성 http://127.0.0.1:8000/api/v1/movies/{movie_id}/reviews/

    postman: data(content) / POST

  - 단일 댓글 정보 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/

  - 댓글 수정 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/

    postman: data(content) / PUT

  - 댓글 삭제 http://127.0.0.1:8000/api/v1/movies/comments/{comment_pk}/

    postman: DELETE



##### Account

- 전체 랭킹 갱신(admin) http://127.0.0.1:8000/accounts/calc-ranking/
- 전체 상위 랭커 n명 정보 http://127.0.0.1:8000/accounts/top-ranked/{n}/

  



##### Infinite Scroll

- 리뷰 http://127.0.0.1:8000/api/v1/movies/infinite-scroll/reviews/?page_num={page_num}
