## Setting up EVN

```sh
python -m venv venv
```

```sh
pip install pipreqs uvicorn aiosqlite python-jose passlib python-multipart "python-jose[cryptography]" "passlib[bcrypt]" pydantic[email]
```

```sh
pipreqs C:\Users\vieng\Documents\Workspaces\ChatGPT\ChatGPT-HR --force
```

```sh
pip freeze > requirements01.txt
```

```sh
pip install -r requirements.txt
```

```sh
pip install pydantic[dotenv]

```

```sh
pip install uvicorn
```

```sh
pip uninstall
```

```sh
openssl rand -hex 32
```

## Run App

```sh
uvicorn app.main:app --reload
```
