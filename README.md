# final-project-server



## INSERT DATA

- `$ python manage.py makemigrations`
- `$ python manage.py migrate`
- `http://127.0.0.1:8000/api/v1/movies/TMDB/`  insert TMDB movie datas
- `http://127.0.0.1:8000/accounts/seed-user/` insert users
- `http://127.0.0.1:8000/api/v1/movies/seed-rating/` insert ratings in Movie_User Model
- `http://127.0.0.1:8000/api/v1/movies/count-ratings/` count ratings and insert avg, count fields in Movie Model

