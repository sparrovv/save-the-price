# house prices scrapper

## Goal

Collect house listings every day, save them in google sheets and google storage for later analysis.

## Running locally

Prerequisites:
- google account
- gsheet id
- google storage
- secrets
- otodom search criteria

ENV VARS:

- GCS_PROJECT  
- GCS_BUCKET
- GCS_SA_KEY 

```
otodomsearchcriteriaurl='https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search[filter_float_price:to]=1600000&search[filter_float_m:from]=70&search[filter_float_m:to]=120&search[filter_enum_rooms_num][0]=4&search[filter_enum_rooms_num][1]=5+&search[filter_enum_market][0]=secondary&search[filter_float_build_year:from]=1995&search[filter_float_build_year:to]=2019&search[city_id]=38&zoom=15&lat=50.064663716138&lon=19.889994965510223'

dotenv python3 scrape.py [options] $otodomsearchcriteriaurl
```

## Roadmap

Phase 1:

- [x] - collect data from otodom given a predefined search criteria
- [x] - append to google sheets and save a detailed file in google storage
- [x] - automate through google actions

Phase 2:

- [] - write scripts to analyse the change


## GitHub Actions

### Service Account

A service account with appropriate permissions on the Cloud Storage bucket is required for GitHub Actions to deploy the site - See [Creating and managing service accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

### Secrets

The GitHub Actions workflow depends on the following secrets, which must be configured for the repo - See [Creating and storing encrypted secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets):

| Secret Name | Description |
| :---------- | :---------- |
| GCS_PROJECT | The name of the CGP project containing the Cloud Storage Bucket |
| GCS_BUCKET | The name of the Cloud Storage bucket to deploy the site |
| GCS_SA_KEY | The base64 encoded authentication key for the service account with privileges to deploy the site - See [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) |

### Testing

The GitHub Actions workflow can be tested locally using [act](https://github.com/nektos/act).

To supply secret values for testing you must export them as environment variables - The required variables are shown (as secrets) in `.actrc`.

