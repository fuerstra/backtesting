import logging
from data.data_manager import DataManager
from strategy.strategy_engine import StrategyEngine
from analysis.performance_analyzer import PerformanceAnalyzer
from visualization.plotter import Plotter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize components
    data_manager = DataManager()
    strategy_engine = StrategyEngine()
    performance_analyzer = PerformanceAnalyzer()
    plotter = Plotter()

    # Load data
    logger.info("Loading data...")
    data = data_manager.load_data(
        source='yfinance',
        symbol='AAPL',
        start_date='2020-01-01',
        end_date='2023-01-01',
        interval='1d'
    )
    data = data_manager.clean_data(data)

    # Configure strategy
    logger.info("Configuring strategy...")
    strategy_engine.add_indicator('sma_short', 'sma', close=data['Close'], window=20)
    strategy_engine.add_indicator('sma_long', 'sma', close=data['Close'], window=50)
    strategy_engine.add_indicator('rsi', 'rsi', close=data['Close'], window=14)

    # Run backtest
    logger.info("Running backtest...")
    backtest_results = strategy_engine.backtest(data, initial_capital=10000.0)

    # Analyze performance
    logger.info("Analyzing performance...")
    performance_report = performance_analyzer.generate_report(
        backtest_results['portfolio'],
        backtest_results['signals']
    )

    # Print performance metrics
    logger.info("\nPerformance Metrics:")
    for metric, value in performance_report['performance_metrics'].items():
        logger.info(f"{metric}: {value:.4f}")

    # Plot results
    logger.info("Generating plots...")
    plotter.plot_equity_curve(backtest_results['portfolio'])
    plotter.plot_drawdowns(performance_report['drawdowns'])
    plotter.plot_trades(data, backtest_results['signals'])
    plotter.plot_indicators(data, ['sma_short_sma', 'sma_long_sma', 'rsi_rsi'])
    plotter.plot_performance_metrics(performance_report['performance_metrics'])

if __name__ == "__main__":
    main() 