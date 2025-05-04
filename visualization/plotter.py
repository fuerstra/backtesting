import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class Plotter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Use a built-in style instead of seaborn
        plt.style.use('ggplot')

    def plot_equity_curve(self, portfolio: pd.DataFrame, title: str = "Equity Curve") -> None:
        """Plot the equity curve."""
        plt.figure(figsize=(12, 6))
        plt.plot(portfolio.index, portfolio['total'], label='Portfolio Value', linewidth=2)
        plt.title(title, fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Portfolio Value ($)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_drawdowns(self, drawdowns: pd.Series, title: str = "Drawdowns") -> None:
        """Plot the drawdown curve."""
        plt.figure(figsize=(12, 6))
        plt.fill_between(drawdowns.index, drawdowns.values, 0, color='red', alpha=0.3)
        plt.plot(drawdowns.index, drawdowns.values, color='red', linewidth=2)
        plt.title(title, fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Drawdown (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_trades(self, data: pd.DataFrame, signals: pd.DataFrame, title: str = "Trades") -> None:
        """Plot the price chart with buy/sell signals."""
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label='Price', alpha=0.7, linewidth=2)
        
        # Plot buy signals
        buy_signals = signals[signals['signal'] == 1]
        plt.scatter(buy_signals.index, data.loc[buy_signals.index, 'Close'], 
                   marker='^', color='green', label='Buy', s=100)
        
        # Plot sell signals
        sell_signals = signals[signals['signal'] == -1]
        plt.scatter(sell_signals.index, data.loc[sell_signals.index, 'Close'], 
                   marker='v', color='red', label='Sell', s=100)
        
        plt.title(title, fontsize=14, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_indicators(self, data: pd.DataFrame, indicators: List[str], title: str = "Technical Indicators") -> None:
        """Plot technical indicators."""
        fig, axes = plt.subplots(len(indicators) + 1, 1, figsize=(12, 6 * (len(indicators) + 1)))
        
        # Plot price
        axes[0].plot(data.index, data['Close'], label='Price', linewidth=2)
        axes[0].set_title('Price', fontsize=12)
        axes[0].grid(True, alpha=0.3)
        axes[0].legend(fontsize=10)
        
        # Plot indicators
        for i, indicator in enumerate(indicators, 1):
            if indicator.endswith('_sma'):
                axes[i].plot(data.index, data[indicator], label=indicator, linewidth=2)
            elif indicator.endswith('_rsi'):
                axes[i].plot(data.index, data[indicator], label=indicator, linewidth=2)
                axes[i].axhline(y=70, color='r', linestyle='--', alpha=0.5)
                axes[i].axhline(y=30, color='g', linestyle='--', alpha=0.5)
            elif indicator.endswith('_bb_high'):
                axes[i].plot(data.index, data[indicator], label='Upper Band', linewidth=2)
                axes[i].plot(data.index, data[indicator.replace('_high', '_low')], label='Lower Band', linewidth=2)
                axes[i].plot(data.index, data[indicator.replace('_high', '_mid')], label='Middle Band', linewidth=2)
            
            axes[i].set_title(indicator, fontsize=12)
            axes[i].grid(True, alpha=0.3)
            axes[i].legend(fontsize=10)
        
        plt.suptitle(title, fontsize=14, y=1.02)
        plt.tight_layout()
        plt.show()

    def plot_performance_metrics(self, metrics: Dict, title: str = "Performance Metrics") -> None:
        """Plot key performance metrics."""
        plt.figure(figsize=(10, 6))
        
        # Select metrics to plot
        metric_names = ['total_return', 'annualized_return', 'sharpe_ratio', 'max_drawdown']
        values = [metrics[name] for name in metric_names]
        
        # Format metric names for display
        display_names = ['Total Return', 'Annualized Return', 'Sharpe Ratio', 'Max Drawdown']
        
        bars = plt.bar(display_names, values)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2%}' if height < 1 else f'{height:.2f}',
                    ha='center', va='bottom')
        
        plt.title(title, fontsize=14, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show() 