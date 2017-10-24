# BinanceClient

BinanceClient is a lightweight Python client for interacting with the Binance (www.binance.com) REST API. This is a third-party package and is not affiliated in any way with Binance.

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

### Get latest price of all tickers
```
bc.all_prices()
```

### Place market buy order (5 shares at price of 100)
```
bc.order('TICKER', 'BUY', 'MARKET', 5, 100)
```

### Get order status
```
bc.order_status('TICKER', orig_client_order_id='my_order_1234')
```

### Cancel open order
```
bc.cancel_order('TICKER')
```

### Get current portfolio positions
```
bc.current_positions()
```
