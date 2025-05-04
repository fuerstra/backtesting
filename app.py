from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from data.data_manager import DataManager
from strategy.strategy_engine import StrategyEngine
from analysis.performance_analyzer import PerformanceAnalyzer
import json
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def replace_nan_with_none(obj):
    if isinstance(obj, (float, np.float64)) and np.isnan(obj):
        return None
    elif isinstance(obj, dict):
        return {k: replace_nan_with_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none(item) for item in obj]
    return obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_backtest', methods=['POST'])
def run_backtest():
    try:
        # Get parameters from request
        data = request.json
        symbol = data.get('symbol', 'AAPL')
        start_date = data.get('start_date', '2020-01-01')
        end_date = data.get('end_date', '2023-01-01')
        initial_capital = float(data.get('initial_capital', 10000))
        
        # Initialize components
        data_manager = DataManager()
        strategy_engine = StrategyEngine()
        performance_analyzer = PerformanceAnalyzer()

        # Load data
        logger.info("Loading data...")
        market_data = data_manager.load_data(
            source='yfinance',
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval='1d'
        )
        market_data = data_manager.clean_data(market_data)

        # Configure strategy
        logger.info("Configuring strategy...")
        strategy_engine.add_indicator('sma_short', 'sma', close=market_data['Close'], window=20)
        strategy_engine.add_indicator('sma_long', 'sma', close=market_data['Close'], window=50)
        strategy_engine.add_indicator('rsi', 'rsi', close=market_data['Close'], window=14)

        # Run backtest
        logger.info("Running backtest...")
        backtest_results = strategy_engine.backtest(market_data, initial_capital=initial_capital)

        # Analyze performance
        logger.info("Analyzing performance...")
        performance_report = performance_analyzer.generate_report(
            backtest_results['portfolio'],
            backtest_results['signals']
        )

        # Prepare data for visualization
        portfolio_data = {
            'dates': backtest_results['portfolio'].index.astype(str).tolist(),
            'total': backtest_results['portfolio']['total'].fillna(0).tolist(),
            'holdings': backtest_results['portfolio']['holdings'].fillna(0).tolist(),
            'cash': backtest_results['portfolio']['cash'].fillna(0).tolist()
        }

        price_data = {
            'dates': market_data.index.astype(str).tolist(),
            'close': market_data['Close'].fillna(0).tolist()
        }

        signals_data = {
            'dates': backtest_results['signals'].index.astype(str).tolist(),
            'signals': backtest_results['signals']['signal'].fillna(0).tolist()
        }

        indicators_data = {
            'sma_short': market_data['sma_short_sma'].fillna(0).tolist(),
            'sma_long': market_data['sma_long_sma'].fillna(0).tolist(),
            'rsi': market_data['rsi_rsi'].fillna(0).tolist()
        }

        # Prepare performance metrics
        metrics = performance_report['performance_metrics']
        trade_analysis = performance_report['trade_analysis']

        response = {
            'success': True,
            'portfolio_data': portfolio_data,
            'price_data': price_data,
            'signals_data': signals_data,
            'indicators_data': indicators_data,
            'metrics': replace_nan_with_none(metrics),
            'trade_analysis': replace_nan_with_none(trade_analysis)
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in backtest: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 