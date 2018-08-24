# Powerline
Telegram chat hub for customer support and community building.

# Deploying
In the project root, log in to heroku and heroku container registry. Then run
`heroku container:push --recursive`
`heroku container:release web`

See [Heroku:Docker Deploys](https://devcenter.heroku.com/articles/container-registry-and-runtime) for details.

# Developing
Make sure you have docker installed. You do *not* need to create an account, just go [here](https://download.docker.com/mac/edge/Docker.dmg)
## Running locally
1. rename `env.sample` files to `.env` and fill in contents.
2. `docker-compose up --build`

## Tunneling data
Using ngrok `./ngrok http 8433` and put the domain in `docker-compose.yml`.

# Testing
Tests use [pytest](https://docs.pytest.org/en/latest/contents.html).

## Running tests
1. Get pipenv with `pip install --user pipenv`.
2. `cd worker/`
3. `pipenv install --dev`
4. `pipenv shell` to activate virtual environment
5. within virtual environment, run `pytest`

# Database

## Heroku
```
heroku pg:psql
SELECT * FROM USERS;
\q
```

## Local (docker)
```
psql -h localhost -p 9000 -U postgres
SELECT * FROM USERS;
\q
```
