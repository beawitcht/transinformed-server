# Trans Informed server

![Uptime Robot status](https://img.shields.io/uptimerobot/status/m793393353-5ef24de0db746db2e74fdfba) ![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m793393353-5ef24de0db746db2e74fdfba) [![CodeQL](https://github.com/beawitcht/transinformed-server/actions/workflows/codeql.yml/badge.svg)](https://github.com/beawitcht/transinformed-server/actions/workflows/codeql.yml) ![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade/www.transinformed.co.uk?publish) ![GitHub](https://img.shields.io/github/license/beawitcht/transinformed-server) [![Twitter Follow](https://img.shields.io/twitter/follow/beawitching_cic?style=social)](https://www.twitter.com/beawitching_cic)
***

<p align="center">
    <img src="https://raw.githubusercontent.com/beawitcht/transinformed-server/main/app/static/images/logo.svg" width="200" alt="Trans Informed logo">
</p>

## About
This is a web app to generate personalised documents for gender diverse people to use as an aid in their conversations with their GPs around accessing gender affirming care.


## Setup guide

### Installation

#### Navigate to app directory:
```bash
cd app/
```
#### Install with pip:

```bash
pip install -r requirements.txt
```
### Configure .env
#### The following environment variables are required:
```
PDF_API_KEY=<your-pdf-api-key> # api key for conversion to PDF: convertapi.com
RECAPTCHA_PUBLIC_KEY=<your-recaptcha-public-key> # google recaptcha public key
RECAPTCHA_PRIVATE_KEY=<your-recaptcha-private-key> # google recaptcha private key
IS_DEV = 1 # set to 1 to disable caching
PDF_LIMIT = 100/minute # set rate limit for pdf downloads (see flask-limiter documentation)
```
### Run with gunicorn
```bash
gunicorn -w 4 -b 127.0.0.1:8000 main:app
```
***
[![open collective](https://opencollective.com/beawitching/donate/button.png?color=blue)](https://opencollective.com/beawitching)
