# Pokémon Generator Bot

## About

This project has been made entirely by [David Gómez](https://www.linkedin.com/in/david-g-89a22825b/).

## How to run

First of all, rename .env_example to .env and replace token value with the token of your Discord Developer Portal application, if you do not have one, create it.

### Docker (Recommended)

> Note: For this method you will need [Docker](https://docs.docker.com/engine/install/)

Go to the folder of the project using `cd` command and then build and run the image for the project:

```shell
docker build --file docker/Dockerfile -t <my_image>:<version> .
```

```shell
docker run <my_image>:<version> --name <container_name>
```

Then you will have your container with your bot running.

### As a python script

If you do not want to use Docker, you can install the dependencies in your machine manually and run your script.

> Note: This project is developed to support python 3.11, for the moment, it has not been tested in future or past versions of python

If you have Python 3.11 already installed, you can install the requirements by using:

```shell
pip install -r requirements.txt
```

Then, you will be able to run the script.

```shell
python main.py
```

And then your bot will be running.

## Bot Commands

All commands start with '-' followed by the command itself.

The main command is '-pokemon' which is the command which generates the Pokémon with its data.

If you want to run another command or if you want to add one by yourself, go to main.py and you will see how I implemented the command I mentioned before so you can take it as a base to implement yours.

## How does this bot work?

What the bot does when you execute '-pokemon' is to make a request to [PokéAPI](https://github.com/PokeAPI/pokeapi) and retrieves data from the response. It also randomizes the color of the Pokémon (if it is shiny or not)
and gets the image from [PokémonDB](https://pokemondb.net/sprites).
