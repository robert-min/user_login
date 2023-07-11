# user_login Service

<br>

### Description
- Service address : [링크](http://15.165.197.195)
- github address : [https://github.com/robert-min/user_login](https://github.com/robert-min/user_login)
- API docs : [user_login/docs](http://15.165.197.195:8000/doc)
- Test : 
  - unit test / api test(integration test) : [user_login/backend/src/README.md](https://github.com/robert-min/user_login/tree/main/backend/src)
  - performance load test : [성능테스트](https://github.com/robert-min/user_login/issues/11)

<br>

### Backend File Tree

```
 
./backend
├── Dockerfile                                              -  backend Dockerfile
├── app.py                                                  -  run server file
├── conf/                               
│   └── conf.json                                           - sql conf file
├── entrypoint.sh
├── requirements.txt                                        - backend package
└── src/
    ├── README.md                                           - Test code README file
    ├── __init__.py
    ├── api/
    │   ├── __init__.py                                     - api init file
    │   ├── auth.py                                         - auth api file
    │   └── user.py                                         - user api file
    ├── lib/
    │   ├── __init__.py                                     - lib init file
    │   ├── db_connect.py                                   - db connection module file
    │   ├── encrypt.py                                      - password encryption module file
    │   ├── model.py                                        - db ORM model file
    │   ├── utils.py                                        - utils module file
    │   └── validator.py                                    - API validation module file
    └── test/
        ├── __init__.py
        ├── api_test/                                       
        │   ├── __init__.py
        │   └── user_auth_test.py                           - API test code file
        └── unit_test/
            ├── __init__.py
            ├── db_connect_test.py                          - db connection test code file
            ├── encrypt_test.py                             - encryption test code file
            └── utils_test.py                               - utils test code file

```

<br>

### 서비스 실행 방법

#### 방법 1 (현재 배포된 서비스 접속 후 확인)

- [링크](http://15.165.197.195)
  
<br>

#### 방법 2 (Docker-compose)
- `docker`, `docker-compose`가 설치되어 있어야 합니다.
- `docker-compose.yaml` 파일이 있는 경로에서 아래 명령어 실행이 필요합니다.
- 실행 후 웹브라우저에서 `http://localhost` 경로로 접속 후 실행할 수 있습니다.
```sh
 
# docker-compose.yaml 경로
sudo docker-compose up -d
 
```

<br>


#### 방법 3 (Local 개별 실행)
- python 3.9, node.js 13버전, vue-cli가 필요합니다.
- Local 실행의 경우 개발 환경에 따라 실행오류가 있을 수 있습니다.
- 로컬 테스트의 경우 백엔드 서버와 프로느 서버 모두 실행된 상태에서 테스트 진행이 가능합니다.
```sh
 
# backend 실행(root 경로)
cd ./backend
pip install -r requirements.txt

# 개발테스트 환경
python app.py

# frontend 실행(root 경로)
cd ./frontend
npm install
npm run serve

# http://localhost:8080 접속 확인
 
```

<br>