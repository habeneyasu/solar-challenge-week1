"""
Object-Oriented Visualization Module
Implements OO patterns for data visualization
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Optional, Tuple
import pandas as pd


class BaseVisualizer:
    """
    Base class for visualizations.
    Implements Template Method pattern.
    """
    
    def __init__(self, data: pd.DataFrame, country_name: str):
        """
        Initialize visualizer.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Data to visualize
        country_name : str
            Country name for titles
        """
        self.data = data
        self.country_name = country_name
        self.fig = None
        self.ax = None
    
    def create_figure(self, figsize: Tuple[int, int] = (12, 6)) -> None:
        """Create matplotlib figure."""
        self.fig, self.ax = plt.subplots(figsize=figsize)
    
    def set_title(self, title: str) -> None:
        """Set plot title."""
        if self.ax:
            self.ax.set_title(title, fontweight='bold')
    
    def show(self) -> None:
        """Display the plot."""
        if self.fig:
            plt.tight_layout()
            plt.show()
    
    def save(self, filepath: str) -> None:
        """Save the plot."""
        if self.fig:
            self.fig.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to: {filepath}")


class TimeSeriesVisualizer(BaseVisualizer):
    """
    Visualizes time series data.
    Implements Strategy pattern.
    """
    
    def plot_timeseries(self, columns: List[str], timestamp_col: str = 'Timestamp') -> None:
        """
        Plot time series for specified columns.
        
        Parameters:
        -----------
        columns : List[str]
            Columns to plot
        timestamp_col : str
            Timestamp column name
        """
        if timestamp_col not in self.data.columns:
            raise ValueError(f"Timestamp column '{timestamp_col}' not found")
        
        self.create_figure(figsize=(15, 4*len(columns)))
        
        if len(columns) == 1:
            axes = [self.ax]
        else:
            self.fig, axes = plt.subplots(len(columns), 1, figsize=(15, 4*len(columns)))
        
        for idx, col in enumerate(columns):
            if col in self.data.columns:
                axes[idx].plot(self.data[timestamp_col], self.data[col], alpha=0.6, linewidth=0.8)
                axes[idx].set_title(f'{col} Over Time - {self.country_name}', fontweight='bold')
                axes[idx].set_xlabel('Timestamp')
                axes[idx].set_ylabel(col)
                axes[idx].grid(True, alpha=0.3)
        
        plt.tight_layout()


class CorrelationVisualizer(BaseVisualizer):
    """
    Visualizes correlation matrices.
    """
    
    def plot_heatmap(self, columns: List[str]) -> None:
        """
        Plot correlation heatmap.
        
        Parameters:
        -----------
        columns : List[str]
            Columns to include in heatmap
        """
        available_cols = [col for col in columns if col in self.data.columns]
        
        if len(available_cols) < 2:
            raise ValueError("Need at least 2 columns for correlation heatmap")
        
        corr_matrix = self.data[available_cols].corr()
        
        self.create_figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, square=True, 
                   linewidths=1, cbar_kws={"shrink": 0.8}, ax=self.ax)
        
        self.set_title(f'Correlation Heatmap - {self.country_name}')


class DistributionVisualizer(BaseVisualizer):
    """
    Visualizes data distributions.
    """
    
    def plot_histogram(self, column: str, bins: int = 50, fit_distribution: Optional[str] = None) -> None:
        """
        Plot histogram with optional distribution fit.
        
        Parameters:
        -----------
        column : str
            Column to plot
        bins : int
            Number of bins
        fit_distribution : str, optional
            Distribution to fit ('normal', 'weibull')
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        
        self.create_figure()
        
        data = self.data[column].dropna()
        self.ax.hist(data, bins=bins, alpha=0.7, edgecolor='black')
        
        # Add distribution fit if requested
        if fit_distribution == 'normal':
            from scipy.stats import norm
            mu, sigma = norm.fit(data)
            x = np.linspace(data.min(), data.max(), 100)
            self.ax.plot(x, norm.pdf(x, mu, sigma) * len(data) * (data.max() - data.min()) / bins,
                        'r-', linewidth=2, label=f'Normal fit (μ={mu:.2f}, σ={sigma:.2f})')
            self.ax.legend()
        
        self.set_title(f'Distribution of {column} - {self.country_name}')
        self.ax.set_xlabel(column)
        self.ax.set_ylabel('Frequency')
        self.ax.grid(True, alpha=0.3, axis='y')

