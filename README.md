The Binance Futures Testnet Bot is a lightweight Python project that enables users to experiment with algorithmic trading strategies on the Binance USDT-M Futures Testnet. Built with simplicity and learning in mind, the bot provides both a command-line interface (CLI) and a menu-driven interactive UI, making it accessible for beginners while still flexible enough for advanced users.

At its core, the bot supports the placement of Market, Limit, and Stop-Limit orders, allowing users to simulate real-world trading scenarios without financial risk. As a bonus feature, it implements the TWAP (Time-Weighted Average Price) strategy, which automatically splits a large trade into smaller slices executed at fixed time intervals. This is particularly useful for demonstrating how algorithmic execution can minimize slippage and reduce exposure to sudden price changes.

The bot connects securely to Binance’s Futures Testnet via REST API. Users manage their API Key and Secret through a .env file, ensuring credentials remain private. Each request and response is logged to logs/bot.log for transparency, debugging, and post-trade analysis. The project also automatically validates quantities and prices against Binance’s symbol filters, rounding values when necessary to avoid errors.

Key features include:
	•	Testnet integration with fake USDT balances, ensuring a safe environment for practice.
	•	Order management tools, including order status checks and cancellation of open orders.
	•	Interactive UI (python ui.py) with simple menu options for common trading actions.
	•	Extensible architecture with modular components, making it easy to add new strategies such as Grid trading or risk-management rules.

In summary, this project is an excellent starting point for anyone interested in learning about crypto trading bots, Futures trading mechanics, and algorithmic strategies, all within a safe sandbox environment. It balances clarity, security, and extensibility, making it a valuable educational and experimental tool for developers and traders alike.
