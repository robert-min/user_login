# instal package
pip install -r requirements.txt

# memcached start(현재는 테스트를 위해 웹서버와 동일한 컨테이너 배포하지만 실제 프로덕션 배포시 분리된 컨테이너에서 배포)
memcached -d

# run backend server
gunicorn --bind 0.0.0.0:8000 "app:app" --timeout 15
