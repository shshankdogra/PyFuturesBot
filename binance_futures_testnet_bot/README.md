# Binance Futures Testnet Bot v2.1
- REST
- MARKET/LIMIT/STOP-LIMIT/TWAP
- UI: `python ui.py`
- .env auto-load from `config/.env`
Setup:
`pip install -r requirements.txt`
Commands:
`python main.py order --symbol BTCUSDT --side BUY --type MARKET --qty 0.001`
`python main.py twap --symbol BTCUSDT --side BUY --total-qty 0.003 --slices 3 --interval 5`
