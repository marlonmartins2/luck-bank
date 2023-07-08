
<h1 align="center">🍀 Luck Bank API 🍀</h1>

<h3 align="center">
  # Luck-Bank is a cutting-edge digital banking repository designed to provide you with a seamless and convenient banking experience.
</h3>

## :memo: Release:
- [Latest](https://github.com/marlonmartins2/luck-bank/releases/latest)

## :rocket: Stack
- Docker / docker-compose
- Python 3.11 (official stable)
- FastAPI 0.95.x
- PyMongo 4.3.x
- Uvicorn 0.22.x

## :train2: Considerations - Mongo

The `docker-compose.yml` configuration is prepared to run the
project with a mongo instance through docker. Check the envs before running.

## 🏃Prepare for running

> configure git rebasing:

```shell
git config --global pull.rebase true
```

> cloning repository:

```shell
git git@github.com:marlonmartins2/luck-bank.git

or com htts

git clone https://github.com/marlonmartins2/luck-bank.git
```

> cd into project folder:

```shell
cd luck-bank
```

> create virtualenv:

```shell
python3 -m venv .venv
```

> Environment variable settings:

Environment variables must be added to the project inside the **/luck-bank** folder. Create the `.env` file based on the example present in `.env.sample`

## :train2: Run Project

> Use docker-compose to create the mongo container:

```bash
docker-compose down && docker-compose up --build
```

> Run the project:

```bash
source .venv/bin/activate && cd app && uvicorn app.main:app --reload --use-colors
```

> Check the Endpoint:
[APIDOC](http://localhost:8000/docs)
[APIREDOC](http://localhost:8000/redoc)

## :evergreen_tree: Branchs

The project contains the following protected _branches_:

- [_master_](https://github.com/marlonmartins2/luck-bank/tree/master) : contains the latest version of Production.
