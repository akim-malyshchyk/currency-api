# Currency API
![Github CI](https://github.com/akim-malyshchyk/currency-api/actions/workflows/ci.yml/badge.svg)

RESTful API that is deploy-able through `gunicorn` server as well as runnable as python module.
The application is able to get info about selected crypto currency.
The application is connected to PostgreSQL database and is able to write/read statistical data based on the values returned from the API. For API docs, see docs folder of this repo.

### Tech Stack
* aiohttp
* asyncio
* ccxt
* SQLAlchemy

### Database architecture
One table named `currencies` with PK named `id`, currency as `currency`, timestamp as `date_`, price as `price`.

## How to run
### Docker compose way
1. Rename `.env.template` to `.env`
2. Paste your KuCoin `API_KEY` and `SECRET_KEY` there
2. Run the following command:
```bash
docker-compose up --build
```
### Local way
Alternatively, you may want to run a server without PostgreSQL and nginx. In this case, you can use the commands below:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```
Last command may be replaced by gunicorn command:
```bash
gunicorn app:factory --bind 127.0.0.1:8000 --worker-class aiohttp.GunicornWebWorker --reload
```
You'll also have to apply database migrations manually in this case (`alembic upgrade head` from `src` directory), and adjust database environment variables inside `.env` file.
