# BinanceClient

BinanceClient is a Python client for interacting with the Binance (www.binance.com) REST API. This is a third-party package and is not affiliated in any way with Binance.

## Installation
```
git clone https://github.com/radarthreat/BinanceClient
```

## Usage
### Instantiate client object
```
bc = BinanceClient(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')
```

### Test connection
```
bc.test_connection()
```

### Get latest price of ticker
```
bc.latest_price('TICKER')
```
