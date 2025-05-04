import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class PerformanceAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_metrics(self, returns: pd.Series, risk_free_rate: float = 0.02) -> Dict:
        """Calculate various performance metrics."""
        metrics = {}
        
        # Total Return
        metrics['total_return'] = (1 + returns).prod() - 1
        
        # Annualized Return
        metrics['annualized_return'] = (1 + metrics['total_return']) ** (252 / len(returns)) - 1
        
        # Volatility
        metrics['volatility'] = returns.std() * np.sqrt(252)
        
        # Sharpe Ratio
        metrics['sharpe_ratio'] = (metrics['annualized_return'] - risk_free_rate) / metrics['volatility']
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns / rolling_max - 1
        metrics['max_drawdown'] = drawdowns.min()
        
        # Win Rate
        metrics['win_rate'] = (returns > 0).mean()
        
        # Average Win/Loss
        wins = returns[returns > 0]
        losses = returns[returns < 0]
        metrics['avg_win'] = wins.mean() if len(wins) > 0 else 0
        metrics['avg_loss'] = losses.mean() if len(losses) > 0 else 0
        
        # Profit Factor
        total_wins = (1 + wins).prod() - 1
        total_losses = abs((1 + losses).prod() - 1)
        metrics['profit_factor'] = total_wins / total_losses if total_losses != 0 else float('inf')
        
        return metrics

    def analyze_trades(self, portfolio: pd.DataFrame, signals: pd.DataFrame) -> Dict:
        """Analyze individual trades."""
        trades = []
        position = 0
        entry_price = 0
        entry_date = None
        
        for i in range(1, len(portfolio)):
            current_date = portfolio.index[i]
            current_price = portfolio['holdings'].iloc[i] / position if position != 0 else 0
            
            if signals['signal'].iloc[i] == 1 and position <= 0:  # Buy
                position = portfolio['holdings'].iloc[i] / current_price if current_price != 0 else 0
                entry_price = current_price
                entry_date = current_date
            elif signals['signal'].iloc[i] == -1 and position > 0:  # Sell
                exit_price = current_price
                exit_date = current_date
                pnl = (exit_price - entry_price) * position
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'position': position,
                    'pnl': pnl,
                    'return': pnl / (entry_price * position) if entry_price * position != 0 else 0
                })
                position = 0
        
        return {
            'trades': trades,
            'total_trades': len(trades),
            'winning_trades': len([t for t in trades if t['pnl'] > 0]),
            'losing_trades': len([t for t in trades if t['pnl'] <= 0])
        }

    def generate_report(self, portfolio: pd.DataFrame, signals: pd.DataFrame) -> Dict:
        """Generate a comprehensive performance report."""
        returns = portfolio['total'].pct_change()
        
        metrics = self.calculate_metrics(returns)
        trade_analysis = self.analyze_trades(portfolio, signals)
        
        return {
            'performance_metrics': metrics,
            'trade_analysis': trade_analysis,
            'equity_curve': portfolio['total'],
            'drawdowns': self._calculate_drawdowns(portfolio['total'])
        }

    def _calculate_drawdowns(self, equity_curve: pd.Series) -> pd.Series:
        """Calculate drawdown series."""
        rolling_max = equity_curve.expanding().max()
        drawdowns = equity_curve / rolling_max - 1
        return drawdowns 