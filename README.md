# API Library service

API  service for library written on Django Rest Framework

## Features:

- Admin panel /admin/
- JWT authenticated
- Privacy with .env files
- Testing more than half functionality
- Different permissions to authorized / non-authorized users
- Documentation is located via /api/doc/swagger/
- Managing of borrowing and book return
- Telegram notifications about borrowings
- CRUD functionality with book, borrowings
- Filtering borrowings by user ID and status
- Docker app start

## Installing:
```angular2html
git clone https://github.com/Oleksiy-Liubchenko/DRF_Library.git
cd DRF_Library
python -m venv venv
source venv/bin/activate #for iOS or Linux
venv/Scripts/activate #for Windows
pip install -r requirements.txt
python3 manage.py loaddata fixtures_file.json 
```
".env_sample" file change name to ".env"  and fill your data
```
python manage.py migrate
python manage.py runserver
```

## Run with Docker:
```angular2html
docker-compose build
docker-compose up
```

## Getting access

- Create user via /api/user/register/ (or py.manage.py createsuperuser in terminal)
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR
- Install ModHeader extension to your browser and create Request header with value Bearer <Your access tokekn>

## Endpoints:
### Books urls:
- [GET] /api/books/books/
- [POST] /api/books/books/
- [GET] /api/books/books/{id}/
- [PUT] /api/books/books/{id}/
- [PATCH] /api/books/books/{id}/
- [DELETE] /api/books/books/{id}/


### Borrowing urls:
- [GET] /api/borrowings/borrowings/
- [POST] /api/borrowings/borrowings/
- [GET] /api/borrowings/borrowings/{id}/
- [PUT] /api/borrowings/borrowings/{id}/
- [PATCH] /api/borrowings/borrowings/{id}/
- [DELETE] /api/borrowings/borrowings/{id}/
- [POST] /api/borrowings/borrowings/{id}/return/
- [POST] /api/borrowings/borrowings/{id}/return_book/

### User urls:
- [GET] /api/user/all_users/
- [GET] /api/user/me/
- [PUT] /api/user/me/
- [PATCH] /api/user/me/
- [POST] /api/user/register/
- [POST] /api/user/token/
- [POST] /api/user/token/refresh/


## Get Telegram notifications:
- Create new bot by BotFather and get token as TELEGRAM_BOT_TOKEN
- Get your CHAT_ID with https://api.telegram.org/bot<YourBOTToken>/getUpdates command in your browser