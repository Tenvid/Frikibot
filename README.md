# Pokébot

Discord bot which generates an embed with a random Pokémon

## How to run


### Docker compose
> Note: For this method you will need to have [Docker](https://docs.docker.com/engine/install/) installed

Copy this text in a docker-compose.yml next to `Dockerfile` and replace the placeholders

```yml
services:
  Pokebot:
    container_name: Pokebot
    build:
      context: ../
      dockerfile: docker/Dockerfile
    restart: unless-stopped
    environment:
      - DATABASE=pokemon.db
      - TRAINER_TABLE=entrenador
      - POKEMON_TABLE=pokemon
      - DISCORD_TOKEN={discord developer token}
    image: pokebot-image
    volumes:
      - {folder in your computer}:/app/db
```

### Docker run

> Note: For this method you will need to have [Docker](https://docs.docker.com/engine/install/) installed

Create a .env file based on .env_example


On the root folder run these commands

```shell
docker build --file docker/Dockerfile -t pokebot-image .
```

```shell
docker run pokebot-image --name Pokebot
```

### As a python script

> Note: This project is developed to support python 3.11, for the moment, it has not been tested in future or past versions of python

- Install dependencies in requirements.txt
- Create a .env file based on .env_example


```shell
pip install -r requirements.txt
```

Then, you will be able to run the script.

```shell
python __main.py__
```

And then your bot will be running.

## Bot Commands

All commands start with '-' followed by the command itself.

The main command is '-pokemon' which is the command which generates the Pokémon with its data.

If you want to run another command or if you want to add one by yourself, go to main.py and you will see the implementation.
