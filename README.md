# Frikibot

This is an example for a Discord bot that can generate a Pokémon card with random stats.

![./images/PokemonCardExample.png](./images/PokemonCardExample.png)

## Contributing

> See [CONTRIBUTING.md](/CONTRIBUTING.md)

## How to run

> For all methods you will need to clone this repo

### Directly with python

> For this method you need a Python version higher than python 3.11
> and lower than python 3.13.

1. Install `requirements.txt` (I recommend to use a virtualenv)
2. Create a bot from an App in [Discord dev portal](https://discord.com/developers/applications)
3. Copy the token of your bot
4. Make a copy of `.env_example` called `.env` and set your token (you can let the other fields by default)
5. Run the `__main__.py`.

If you hace `python3` you should run:

```python
python3 frikibot/__main__.py
```

Or if you have `python`:

```python
python frikibot/__main__.py
```

### Running with Docker

> For this method you need [Docker](https://docs.docker.com/get-started/get-docker/)

1. Create a bot from an App in [Discord dev portal](https://discord.com/developers/applications)
2. Build

```bash
docker build -f docker/Dockerfile . -t frikibot:0.1
```

3. Run

```bash
docker run --name frikibot_test_args -e DATABASE=pokemon.db \
  -e TRAINER_TABLE=entrenador -e POKEMON_TABLE=pokemon \
  -e DISCORD_TOKEN=<YOUR-TOKEN> \
  frikibot:0.1
```

### Running with Docker compose

1. Create a bot from an App in [Discord dev portal](https://discord.com/developers/applications)
2. Copy the token of your bot
3. Make a copy of `.env_example` called `.env` and set your token (you can let the other fields by default)
4. Run

```bash
docker compose -f docker/docker-compose.yml --env-file frikibot/.env up
```

## Commands

- `-pokemon`: Generates a Pokémon card.
- `-dex`: You can navigate between your Pokémon.
