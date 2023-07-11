## user_login Test Code

<br>

#### unit test

```sh
 
# db_connect.py unit test
python -m unittest test/unit_test/db_connect_test.py

# encrypt.py unit test
python -m unittest test/unit_test/encrypt_test.py

# utils.py unit test
python -m unittest test/unit_test/utils_test.py

```

<br>

#### api test
```sh
 
# api(integration) test
python -m pytest test/api_test/user_auth_test.py

```

<br>
