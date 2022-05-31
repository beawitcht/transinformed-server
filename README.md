# Trans Informed server

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/beawitcht/transinformed-server.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/beawitcht/transinformed-server/context:python) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/beawitcht/transinformed-server) [![Twitter Follow](https://img.shields.io/twitter/follow/beawitcht?style=social)](https://www.twitter.com/beawitcht)
***
<img src="https://raw.githubusercontent.com/beawitcht/transinformed-server/main/app/static/logo.svg" width="200" alt="Trans Informed logo" style="display:block; margin-left:auto; margin-right:auto;">

## About
#### ***This service is still a very early prototype and is not suitable for use.***
This is a web app to generate contextualised documents for people to bring to their GPs to provide them with one document containing the most important information for both the GP and the patient.


## Setup guide

### Installation

#### Navigate to app directory:
```
$ cd app/
```
#### Install with pip:

```
$ pip install -r requirements.txt
```
### Configure .env
#### The following environment variables are required:
```
PDF_API_KEY=<your-pdf-api-key> # api key for conversion to PDF: convertapi.com
RECAPTCHA_PUBLIC_KEY=<your-recaptcha-public-key> # google recaptcha public key
RECAPTCHA_PRIVATE_KEY=<your-recaptcha-private-key> # google recaptcha private key
```
### Run with gunicorn
#### Install gunicorn:
```
% pip install gunicorn
```
#### Run with gunicorn:
```
$ gunicorn -w 4 -b 127.0.0.1:8000 main:app
```
***
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T7BLO3U)
