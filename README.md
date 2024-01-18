# ChallengeFligoo
REST API For a hiring challenge 

## Running 
It can be runned either locally or on a docker container.

### For a local run
You must run the following steps:
* Run ```pip install -r requirements.txt```
* Create a file named .env  with the following settings:

```SECRET_KEY="django-insecure-0o$7%ki&h_ry-j!bc#2#j3j+&+=kb$bbflc*a2mnf_g3hzh1_i"```

This is the Default django secret key

### To run it inside a docker container 
You must do the follwoing steps:
* Create a file named ```docker.env``` inside the main proyect folder with the following settings: 
``` 
SECRET_KEY = "django-insecure-0o$7%ki&h_ry-j!bc#2#j3j+&+=kb$bbflc*a2mnf_g3hzh1_i"
DB = "POSTGRES"
POSTGRES_DB = mydb
POSTGRES_USER = postgresuser
POSTGRES_PASSWORD = postgrespassword
```
* After that you need to run the following commands:
```
docker compose build
docker compose up
```

This will build and run the containers as well as run the db migrations 

## API Details
This API has the following endpoints:

### GET /api/players/
Show all players 


### POST /api/player
Creates a player, it recieves the following data
```
{
    name:str
}
```

### GET /api/player/{id}
Shows the player with the matching id if it exists. 

### DELETE /api/player/{id}
Deletes the player with the matching id if it exists.

### GET /api/games/
Lists all available games

### POST /api/games/
Creates a game, it receives the following data
```
{
    starting_token:str,
    players:[int]
}
```
The starting token is either 'X' or 'O'. And the players must be a list of player ids (This is currently bugged, it should only receive up to 2 players but is receiving any amount)

### GET /api/games/{id}
Shows the full information of a given game, like the board status, turn number and which is the current players. 

### DELETE /api/games/{id}
Deletes the game with matching _id_ if it exists

## POST /api/games/{id}/play

Makes a move the board by the given player on the given position, it recieves the following arguments
```
{
    player:int,
    row:int,
    column
}
```