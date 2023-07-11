# user_login Service

## Description
- github address : [https://github.com/robert-min/user_login](https://github.com/robert-min/user_login)
- API docs : [user_login/docs](http://15.165.197.195:8000/doc)
- Test : 
  - unit test / api test(integration test) : [user_login/backend/src/README.md](https://github.com/robert-min/user_login/tree/main/backend/src)
  - performance load test : [성능테스트](https://github.com/robert-min/user_login/issues/11)

<br>

#### 서비스 실행 방법 1 (현재 배포된 서비스 접속 후 확인)

- [링크](http://15.165.197.195)
  
<br>

#### 서비스 실행 방법 2 (Docker-compose)
- `docker`, `docker-compose`가 설치되어 있어야 합니다.
- `docker-compose.yaml` 파일이 있는 경로에서 아래 명령어 실행이 필요합니다.
- 실행 후 웹브라우저에서 `http://localhost` 경로로 접속 후 실행할 수 있습니다.
```sh
# docker-compose.yaml 경로
sudo docker-compose up -d
```

<br>


#### 서비스 실행 방법 3(Local 개별 실행)
- python 3.9, node.js 13버전, vue-cli가 필요합니다.
- Local 실행의 경우 개발 환경에 따라 실행오류가 있을 수 있습니다.
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