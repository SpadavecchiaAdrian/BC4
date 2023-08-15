# BC4 - Soccer league ranking

This is a code challenge.

## Requirements
This project use Poetry as dependency administrator -> https://python-poetry.org/

It is recommended if you expect to modify the code or run locally.

Also, for the simplicity of the daily work, it is recommended docker, compose and GNU Make -> as an incursion to https://3musketeers.io/.

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