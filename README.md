# Powerline
Telegram chat hub for customer support and community building.

## High level architecture
```
Telegram --> webhook --> redis queue --> worker(s) --> Telegram
                                            ^
                                            |
                                            v
                                        Postgresql
```


# Reading material
https://core.telegram.org/bots  
https://www.michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference https://github.com/pytransitions/transitions  
https://github.com/python-telegram-bot/python-telegram-bot  
http://python-rq.org/docs/


# Deploying
In the project root, log in to heroku and heroku container registry. Then run
`heroku container:push --recursive`
`heroku container:release web`

See [Heroku:Docker Deploys](https://devcenter.heroku.com/articles/container-registry-and-runtime) for details.

# Developing
Make sure you have docker installed. You do *not* need to create an account, just go [here](https://download.docker.com/mac/edge/Docker.dmg)

Create your own bot on Telegram using botfather. Make sure to name it something like 1235-testbot so that people don't easily find it on random.

## Running locally
1. rename `env.sample` files to `.env` and fill in contents with bot tokens.
2. Using ngrok `./ngrok http 8433` and put the bot tokens and ngrok domain in `docker-compose.yml`.
4. `docker-compose up --build`


# Testing
Tests use [pytest](https://docs.pytest.org/en/latest/contents.html).

## Running tests
1. Get pipenv with `pip install --user pipenv`.
2. `cd worker/`
3. `pipenv install --dev`
4. `pipenv shell` to activate virtual environment
5. within virtual environment, run `pytest`

# Database
Postgresql + sqlalchemy.

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

# Todo
- [ ] Move to a single conf and .env file
- [ ] Clarify/clean logging
- [ ] Detect user language
- [ ] Clarify/clean imports
- [ ] Separate/dummy enums for tests
- [ ] Clarify/clean tests
- [ ] Separate bot testing to core and functional tests
- [ ] Design + implement: User settings + Account deletion
- [ ] Design + implement: Admin authentication
- [ ] Design + implement: Sending broadcasts to users via telegram / bot
- [ ] Handler for images. Detecting hashtags
- [ ] Design + implement: Live wall of user-tagged images
- [ ] Design + implement: User management
- [ ] Documentation
