# Play Colossal Cave Adventure with ChatGPT

ChatGPT plays through the OG text adventure game. You'll have the opportunity to give it hints when it gets stuck.

<img src="demo.gif" width="960">

## Usage

```
python3 adventure/main.py
```

## Setup

You must have `adventure` installed on your system. It is included in the [bsd-games](https://archlinux.org/packages/extra/x86_64/bsd-games/) package available for most linux distributions.

### Installation:

Add a `.env` file following `.env.example` with your OpenAPI API key.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```