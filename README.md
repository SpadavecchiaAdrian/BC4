# BC4 - Soccer league ranking

This is a code challenge.

## Requirements

Important: you need python 3.11.4 on system to run local

This project use Poetry as dependency administrator -> https://python-poetry.org/

It is recommended to install poetry if you expect to modify the code, run locally or run test (only localy for the moment).

Install poetry -> https://python-poetry.org/docs/#installation

To create the environment and install dependencies 
```bash
poetry shell
poetry install
```

Also, for the simplicity of the daily work, it is recommended docker, compose and GNU Make -> as an incursion to https://3musketeers.io/.

For GNU make instalation please search acording your SO.

## Using Make

The Makefile has auto-documentation, so if in your console enter:

```bash
make
```

All the commands available are shown as for example

```bash
(bc4-py3.11) adri@Desktop:~/Desktop/BC4$ make
docker-down                    Stop and clean compose
docker-run                     Run compose locally
docker-stop                    Stop compose
local-run                      Run FastAPI locally
local-test                     run test locally
```

For example, if you need to run locally:
```bash
make local-run
```
Or, run test:
```bash
make local-test
```

## OpenAPI documentation

FastAPI auto documentation is availible on '/docs'.
If you are runing locally with 'make local-run', you can find it in your explorer on 'http://localhost:8000/docs'

## Running with Doker Compose
To run the app with docker compose you can use make as mentioned above 'make docker-run'.

If you don't have make and just want to try:

```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
```

When the api run over Docker it takes the port 8080, so the main endpoint is 'http://localhost:8080/rankings' and the OpenAPI documentation is 'http://localhost:8080/docs'