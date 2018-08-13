# Powerline
Telegram chat hub for customer support and community building.


# Deploying
In the project root, log in to heroku and heroku container registry. Then run
`heroku container:push --recursive`
`heroku container:release web`

See [Heroku:Docker Deploys](https://devcenter.heroku.com/articles/container-registry-and-runtime) for details.

# Developing
## Running locally
1. rename `env.sample` files to `.env` and fill in contents.
2. `docker-compose up --build`

## Tunneling data
Using ngrok `./ngrok http 8433` and put the domain in `.env` files where required.

## Running tests
Ensure in that you have activated the virtual environment and installed the packages. Then within a subfolder (eg. `worker/`) run `pytest`.
