# This is the Repo for "Registration Recognition API"


| Test Branch: master | Test Branch: dev | Azure Deployment | Azure Status | Python SDK Pre |
| -- | -- | -- | -- | -- |
| [![Build:Master](https://github.com/maxleimkuehler/fahrzeugschein-api/workflows/Build/badge.svg?branch=master)](https://github.com/maxleimkuehler/fahrzeugschein-api/actions?query=workflow%3ABuild) | [![Build:Dev](https://github.com/maxleimkuehler/fahrzeugschein-api/workflows/Build/badge.svg?branch=dev)](https://github.com/maxleimkuehler/fahrzeugschein-api/actions?query=workflow%3ABuild)  | [![Deployment](https://github.com/maxleimkuehler/fahrzeugschein-api/workflows/Release/badge.svg)](https://github.com/maxleimkuehler/fahrzeugschein-api/actions?query=workflow%3ARelease) | [![Status](https://github.com/maxleimkuehler/fahrzeugschein-api/workflows/Test/badge.svg)](https://github.com/maxleimkuehler/fahrzeugschein-api/actions?query=workflow%3ATest) | [![Pre-Release Python SDK Package](https://github.com/maxleimkuehler/fahrzeugschein-api/workflows/Pre-Release%20Python%20SDK%20Package/badge.svg)](https://github.com/maxleimkuehler/fahrzeugschein-api/actions?query=workflow%3A%22Pre-Release+Python+SDK+Package%22) |


## Monitoring

[fahrzeugschein-api](https://portal.azure.com/#@markwarneke.me/dashboard/arm/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourcegroups/dashboards/providers/microsoft.portal/dashboards/8dac3b6e-26e9-499e-9fb6-b4c58899814a)

## Services

- [Group](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/overview)
- [ACI](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.ContainerInstance/containerGroups/fahrzeugschein-api/overview)
- [Storage](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.Storage/storageAccounts/fahrzeugschein/overview)
- [Vault](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/overview)
- [ACR](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/mmmintelligence/providers/Microsoft.ContainerRegistry/registries/mmmintelligence/overview)

## Development Setup

Set up a virtual environment and install requirements:

```bash
python3 -m venv env
source env/bin/activate
make init

# Login to Azure
az login
az account set -s markwarneke130

# Fetch needed secrets into hack/.env
make secrets
source hack/.env

#manually add Env local env in hack/.env
&& export LOCAL_DEV=True

# Run locally - see Dockerize and deploy
make serve
```

## Api Documentation

Open http://localhost:8000/docs in your browser.

## Docker

Create a `.docker.env` file for the docker.
Get secrets from [KeyVault:fahrzeugschein/env-file-docker](https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/secrets) via `make secrets` -> remove `export` and `&&`, one variable on a new line. 

```bash
# Make sure .docker.env is present
make build

# Run docker
make run

# Run as deamon
make run.d
make logs

# Open http://localhost:80/docs in your browser.
```

## Tests

```bash
# Set environment variables
sessionId=""
apiKey=""

./hack/test/health.sh

./hack/test/getFahrzeugschein.sh

./hack/test/getStatus.sh

./hack/test/submitFahrzeugschein.sh
```

CI needs the following variables configured

```bash
# For build & release
AZURE_CREDENTIALS=https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/secrets
ACR_PASSWORD=https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/secrets

# For ze tests
AZURE_STORAGE_ACCOUNT_KEY=https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/secrets
AZURE_STORAGE_ACCOUNT_NAME=https://portal.azure.com/#@markwarneke.me/resource/subscriptions/bff72fc9-ba07-4b56-bd6a-15d551fb3edb/resourceGroups/fahrzeugschein/providers/Microsoft.KeyVault/vaults/fahrzeugschein/secrets
```

## Python SDK PyPi Package

See [mmmint-registration-recognition](https://pypi.org/project/mmmint-registration-recognition/)

## Deployment Scripts

See [hack](./hack/README.md)
