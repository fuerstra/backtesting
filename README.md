# Python Backtesting System

A comprehensive backtesting system for trading strategies, built with Python.

## Features

- Data Management
  - Historical market data loading (OHLCV)
  - Multiple data sources (Yahoo Finance, CSV)
  - Data cleaning and normalization
  - Data caching for performance

- Strategy Engine
  - Framework for defining trading strategies
  - Technical indicators library (SMA, EMA, RSI, Bollinger Bands)
  - Signal generation
  - Position management

- Backtesting Core
  - Portfolio simulation
  - Transaction cost calculation
  - Performance metrics calculation

- Performance Analysis
  - Return calculations
  - Risk metrics
  - Trade analysis
  - Performance visualization

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backtesting
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Configure your strategy in `main.py`:
```python
# Add indicators
strategy_engine.add_indicator('sma_short', 'sma', close=data['Close'], window=20)
strategy_engine.add_indicator('sma_long', 'sma', close=data['Close'], window=50)

# Run backtest
backtest_results = strategy_engine.backtest(data, initial_capital=10000.0)
```

2. Run the backtest:
```bash
python main.py
```

## Project Structure

```
backtesting/
├── data/
│   └── data_manager.py      # Data loading and management
├── strategy/
│   └── strategy_engine.py   # Strategy definition and execution
├── analysis/
│   └── performance_analyzer.py  # Performance metrics calculation
├── visualization/
│   └── plotter.py          # Results visualization
├── main.py                 # Main script
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Available Technical Indicators

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)
- Bollinger Bands

## Performance Metrics

- Total Return
- Annualized Return
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Profit Factor
- Average Win/Loss

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 