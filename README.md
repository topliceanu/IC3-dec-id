# Legacy-Derived Anonymous Credentials Hackathon Project

Project reference doc - https://docs.google.com/document/d/1kJV-C8LyCIMLo675jSzb8v6Kbe5CBpV0Ib4EsVhiA4U/edit#heading=h.k1wppfx6wur1

Built at IC3'23

## Install

- Install python dependencies

```bash
python3.10 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

- Install circom and snarkjs

Follow the [installation guides](https://docs.circom.io/getting-started/installation/).

## Running the issuer

```bash
flask --app issuer run -p 8000
```

## Getting the user token

```bash
python query_discord.py authorization_token
```
