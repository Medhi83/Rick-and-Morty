# API - Rick & Morty
REST API that allows a user to comment on characters and episodes in the Rick &amp; Morty universe.


## Prerequisites
- python3.9
- docker-compose


## Quick start

Run the app and mariadb
```shell
make run
```

Create the database
```shell
make create_database
```

Import data from :
- scripts/json_data/rick_morty-chracters_v1.json
- scripts/json_data/rick_morty-episodes_v1.json

```shell
make import_data
```

## API Documentation

http://localhost:8080/api/swagger

Some examples :
- Get list of characters : http://localhost:8080/characters
- Get list of episodes : http://localhost:8080/episodes
- Get list of comments : http://localhost:8080/comments

- Export comments: http://localhost:8080/comments/export


## Set up for development

Create virtual environment from python3.9 and install requirements

```shell
make install_env
```

Running the tests locally
```shell
make test
```