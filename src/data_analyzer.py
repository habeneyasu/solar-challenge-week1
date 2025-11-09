"""
Object-Oriented Data Analysis Module
Implements OO patterns for solar data analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from scipy.stats import zscore


class SolarDataAnalyzer:
    """
    Main class for solar data analysis using OO patterns.
    Implements Strategy and Template Method patterns.
    """
    
    def __init__(self, data_path: Path, country_name: str):
        """
        Initialize the analyzer with dataset path and country name.
        
        Parameters:
        -----------
        data_path : Path
            Path to the CSV file
        country_name : str
            Name of the country being analyzed
        """
        self.data_path = data_path
        self.country_name = country_name
        self.raw_data: Optional[pd.DataFrame] = None
        self.cleaned_data: Optional[pd.DataFrame] = None
        self.analysis_results: Dict = {}
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
        --------
        pd.DataFrame: Loaded dataframe
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.raw_data = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.raw_data):,} records for {self.country_name}")
        return self.raw_data
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Generate summary statistics using df.describe().
        
        Returns:
        --------
        pd.DataFrame: Summary statistics
        """
        if self.raw_data is None:
            raise ValueError("Data must be loaded first. Call load_data()")
        
        numeric_cols = self.raw_data.select_dtypes(include=[np.number]).columns
        summary = self.raw_data[numeric_cols].describe()
        
        self.analysis_results['summary_statistics'] = summary
        return summary
    
    def analyze_missing_values(self, threshold: float = 5.0) -> Dict:
        """
        Analyze missing values using df.isna().sum().
        Flags columns with >threshold% missing values.
        
        Parameters:
        -----------
        threshold : float
            Percentage threshold for flagging (default: 5.0)
        
        Returns:
        --------
        dict: Missing value analysis results
        """
        if self.raw_data is None:
            raise ValueError("Data must be loaded first. Call load_data()")
        
        missing_count = self.raw_data.isna().sum()
        missing_percent = (missing_count / len(self.raw_data)) * 100
        
        critical_columns = missing_percent[missing_percent > threshold].index.tolist()
        overall_completeness = 100 - (missing_count.sum() / (len(self.raw_data) * len(self.raw_data.columns))) * 100
        
        result = {
            'missing_count': missing_count,
            'missing_percent': missing_percent,
            'critical_columns': critical_columns,
            'overall_completeness': overall_completeness,
            'threshold': threshold
        }
        
        self.analysis_results['missing_values'] = result
        return result
    
    def detect_outliers(self, columns: List[str], z_threshold: float = 3.0) -> pd.Series:
        """
        Detect outliers using Z-score method.
        
        Parameters:
        -----------
        columns : List[str]
            Columns to analyze for outliers
        z_threshold : float
            Z-score threshold (default: 3.0)
        
        Returns:
        --------
        pd.Series: Boolean series indicating outlier rows
        """
        if self.raw_data is None:
            raise ValueError("Data must be loaded first. Call load_data()")
        
        available_cols = [col for col in columns if col in self.raw_data.columns]
        
        if not available_cols:
            raise ValueError(f"None of the specified columns found: {columns}")
        
        z_scores = np.abs(zscore(self.raw_data[available_cols], nan_policy='omit'))
        outlier_mask = (z_scores > z_threshold).any(axis=1)
        
        self.analysis_results['outliers'] = {
            'mask': outlier_mask,
            'count': outlier_mask.sum(),
            'percentage': (outlier_mask.sum() / len(self.raw_data)) * 100
        }
        
        return outlier_mask
    
    def clean_data(self, outlier_mask: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Clean data: impute missing values and correct negative values.
        
        Parameters:
        -----------
        outlier_mask : pd.Series, optional
            Mask for outliers (if None, will detect)
        
        Returns:
        --------
        pd.DataFrame: Cleaned dataframe
        """
        if self.raw_data is None:
            raise ValueError("Data must be loaded first. Call load_data()")
        
        self.cleaned_data = self.raw_data.copy()
        
        # Impute missing values with median
        key_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 
                      'Tamb', 'RH', 'BP', 'TModA', 'TModB']
        available_key_cols = [col for col in key_columns if col in self.cleaned_data.columns]
        
        for col in available_key_cols:
            if self.cleaned_data[col].isna().sum() > 0:
                median_value = self.cleaned_data[col].median()
                self.cleaned_data[col].fillna(median_value, inplace=True)
        
        # Correct negative values
        non_negative_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust', 'Precipitation']
        for col in non_negative_cols:
            if col in self.cleaned_data.columns:
                self.cleaned_data.loc[self.cleaned_data[col] < 0, col] = 0
        
        # Add cleaning flag
        self.cleaned_data['Cleaning'] = 'Post-Clean'
        
        print(f"✓ Data cleaned: {len(self.cleaned_data):,} records")
        return self.cleaned_data
    
    def export_cleaned_data(self, output_path: Path) -> None:
        """
        Export cleaned data to CSV.
        
        Parameters:
        -----------
        output_path : Path
            Path to save cleaned data
        """
        if self.cleaned_data is None:
            raise ValueError("Data must be cleaned first. Call clean_data()")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.cleaned_data.to_csv(output_path, index=False)
        print(f"✓ Cleaned data exported to: {output_path}")
    
    def get_analysis_summary(self) -> Dict:
        """
        Get comprehensive analysis summary.
        
        Returns:
        --------
        dict: Complete analysis summary
        """
        return {
            'country': self.country_name,
            'raw_data_shape': self.raw_data.shape if self.raw_data is not None else None,
            'cleaned_data_shape': self.cleaned_data.shape if self.cleaned_data is not None else None,
            'analysis_results': self.analysis_results
        }


class DataQualityAssessor:
    """
    Assesses data quality using OO pattern.
    Implements Strategy pattern for different quality metrics.
    """
    
    def __init__(self, analyzer: SolarDataAnalyzer):
        """
        Initialize with a SolarDataAnalyzer instance.
        
        Parameters:
        -----------
        analyzer : SolarDataAnalyzer
            Analyzer instance to assess
        """
        self.analyzer = analyzer
    
    def assess_completeness(self) -> float:
        """Assess data completeness percentage."""
        if 'missing_values' in self.analyzer.analysis_results:
            return self.analyzer.analysis_results['missing_values']['overall_completeness']
        return 0.0
    
    def assess_outlier_rate(self) -> float:
        """Assess outlier percentage."""
        if 'outliers' in self.analyzer.analysis_results:
            return self.analyzer.analysis_results['outliers']['percentage']
        return 0.0
    
    def get_quality_score(self) -> Dict[str, float]:
        """
        Get overall quality score.
        
        Returns:
        --------
        dict: Quality metrics
        """
        completeness = self.assess_completeness()
        outlier_rate = self.assess_outlier_rate()
        
        # Quality score: weighted average
        quality_score = (completeness * 0.7) + ((100 - outlier_rate) * 0.3)
        
        return {
            'completeness': completeness,
            'outlier_rate': outlier_rate,
            'quality_score': quality_score
        }


class CorrelationAnalyzer:
    """
    Analyzes correlations between variables.
    Implements Strategy pattern for different correlation methods.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with dataframe.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Data to analyze
        """
        self.data = data
    
    def analyze_correlations(self, columns: List[str]) -> pd.DataFrame:
        """
        Calculate correlation matrix.
        
        Parameters:
        -----------
        columns : List[str]
            Columns to analyze
        
        Returns:
        --------
        pd.DataFrame: Correlation matrix
        """
        available_cols = [col for col in columns if col in self.data.columns]
        if len(available_cols) < 2:
            raise ValueError("Need at least 2 columns for correlation analysis")
        
        return self.data[available_cols].corr()
    
    def get_strong_correlations(self, threshold: float = 0.5) -> List[Tuple[str, str, float]]:
        """
        Get pairs with strong correlations.
        
        Parameters:
        -----------
        threshold : float
            Correlation threshold (default: 0.5)
        
        Returns:
        --------
        List[Tuple]: List of (var1, var2, correlation) tuples
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        corr_matrix = self.data[numeric_cols].corr()
        
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > threshold:
                    strong_corrs.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_val
                    ))
        
        return strong_corrs

