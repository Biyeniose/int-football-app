# International Football statistics web app (1916 to 2024)

Steps to run:
`cd int-football-app`

`docker compose build`

`docker compose up`

Open app on: `http://127.0.0.1:5000/`

## Docker commands

List all containers, including stopped ones: `docker ps -a`

Stop All Running Containers: `docker stop $(docker ps -q)`

Remove All Containers: `docker stop $(docker ps -q)`

Delete All Docker Images: `docker rmi $(docker images -q)`

Remove all unused images: `docker image prune -a`

Clean up unused volumes, networks, and dangling images, use: `docker system prune -a --volumes -f`
