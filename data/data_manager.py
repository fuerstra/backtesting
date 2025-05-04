import pandas as pd
import yfinance as yf
from typing import Union, Optional
import os
import logging

class DataManager:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.logger = logging.getLogger(__name__)

    def load_data(self, 
                 source: str,
                 symbol: str,
                 start_date: str,
                 end_date: str,
                 interval: str = "1d") -> pd.DataFrame:
        """
        Load market data from various sources.
        
        Args:
            source: Data source ('yfinance' or 'csv')
            symbol: Asset symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval: Data interval (1d, 1h, etc.)
            
        Returns:
            DataFrame with OHLCV data
        """
        cache_file = os.path.join(self.cache_dir, f"{symbol}_{start_date}_{end_date}_{interval}.csv")
        
        if os.path.exists(cache_file):
            self.logger.info(f"Loading cached data from {cache_file}")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        
        if source.lower() == 'yfinance':
            data = self._load_yfinance(symbol, start_date, end_date, interval)
        elif source.lower() == 'csv':
            data = self._load_csv(symbol)
        else:
            raise ValueError(f"Unsupported data source: {source}")
        
        # Cache the data
        data.to_csv(cache_file)
        return data

    def _load_yfinance(self, symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
        """Load data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            return data
        except Exception as e:
            self.logger.error(f"Error loading data from Yahoo Finance: {e}")
            raise

    def _load_csv(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV file."""
        try:
            return pd.read_csv(file_path, index_col=0, parse_dates=True)
        except Exception as e:
            self.logger.error(f"Error loading data from CSV: {e}")
            raise

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize the data."""
        # Remove any rows with NaN values
        cleaned_data = data.dropna()
        
        # Ensure all numeric columns are float type
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = cleaned_data[col].astype(float)
        
        return cleaned_data 