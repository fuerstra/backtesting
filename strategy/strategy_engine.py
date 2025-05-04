import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

class StrategyEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.indicators = {}
        self.signals = pd.DataFrame()

    def add_indicator(self, name: str, indicator_type: str, **params) -> None:
        """Add a technical indicator to the strategy."""
        if indicator_type.lower() == 'sma':
            self.indicators[name] = SMAIndicator(**params)
        elif indicator_type.lower() == 'ema':
            self.indicators[name] = EMAIndicator(**params)
        elif indicator_type.lower() == 'rsi':
            self.indicators[name] = RSIIndicator(**params)
        elif indicator_type.lower() == 'bollinger':
            self.indicators[name] = BollingerBands(**params)
        else:
            raise ValueError(f"Unsupported indicator type: {indicator_type}")

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all indicators for the given data."""
        for name, indicator in self.indicators.items():
            if isinstance(indicator, SMAIndicator):
                data[f'{name}_sma'] = indicator.sma_indicator()
            elif isinstance(indicator, EMAIndicator):
                data[f'{name}_ema'] = indicator.ema_indicator()
            elif isinstance(indicator, RSIIndicator):
                data[f'{name}_rsi'] = indicator.rsi()
            elif isinstance(indicator, BollingerBands):
                data[f'{name}_bb_high'] = indicator.bollinger_hband()
                data[f'{name}_bb_low'] = indicator.bollinger_lband()
                data[f'{name}_bb_mid'] = indicator.bollinger_mavg()
        
        return data

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on the indicators."""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0  # 0: hold, 1: buy, -1: sell

        # Example: Simple moving average crossover strategy
        if 'sma_short' in self.indicators and 'sma_long' in self.indicators:
            short_sma = data['sma_short_sma']
            long_sma = data['sma_long_sma']
            
            # Generate signals
            signals.loc[short_sma > long_sma, 'signal'] = 1
            signals.loc[short_sma < long_sma, 'signal'] = -1

        return signals

    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000.0) -> Dict:
        """Run a backtest with the current strategy."""
        # Calculate indicators
        data = self.calculate_indicators(data)
        
        # Generate signals
        signals = self.generate_signals(data)
        
        # Initialize portfolio
        portfolio = pd.DataFrame(index=data.index)
        portfolio['holdings'] = 0.0
        portfolio['cash'] = initial_capital
        portfolio['total'] = initial_capital
        
        position = 0
        for i in range(1, len(data)):
            current_date = data.index[i]
            current_price = data['Close'].iloc[i]
            
            if signals['signal'].iloc[i] == 1 and position <= 0:  # Buy signal
                position = portfolio['cash'].iloc[i-1] / current_price
                portfolio.loc[current_date, 'holdings'] = position * current_price
                portfolio.loc[current_date, 'cash'] = 0
            elif signals['signal'].iloc[i] == -1 and position > 0:  # Sell signal
                portfolio.loc[current_date, 'cash'] = position * current_price
                portfolio.loc[current_date, 'holdings'] = 0
                position = 0
            else:  # Hold
                portfolio.loc[current_date, 'holdings'] = position * current_price
                portfolio.loc[current_date, 'cash'] = portfolio['cash'].iloc[i-1]
            
            portfolio.loc[current_date, 'total'] = portfolio.loc[current_date, 'holdings'] + portfolio.loc[current_date, 'cash']
        
        return {
            'portfolio': portfolio,
            'returns': portfolio['total'].pct_change(),
            'signals': signals
        } 