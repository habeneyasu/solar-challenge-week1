"""
Solar Farm Data Analysis Dashboard
Analysis of solar energy potential across Benin, Sierra Leone, and Togo
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Solar Farm Data Analysis",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #004E89;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">☀️ Solar Farm Data Analysis</h1>', unsafe_allow_html=True)
st.markdown("### Cross-Country Comparison: Benin, Sierra Leone, and Togo")

# Sidebar
st.sidebar.header("📊 Dashboard Controls")
st.sidebar.markdown("---")

# Data loading section
st.sidebar.subheader("📁 Data Loading")
data_path = st.sidebar.text_input(
    "Data Directory Path",
    value="data",
    help="Path to directory containing CSV files"
)

# Check if data directory exists
data_dir = Path(data_path)
if not data_dir.exists():
    st.sidebar.warning(f"⚠️ Data directory '{data_path}' not found. Please create it and add your CSV files.")
    st.info("""
    **📋 Instructions:**
    1. Create a `data/` directory in the project root
    2. Add your CSV files for solar farm data
    3. The app will automatically detect and load CSV files
    """)
else:
    # Get CSV files
    csv_files = list(data_dir.glob("*.csv"))
    
    if csv_files:
        st.sidebar.success(f"✅ Found {len(csv_files)} CSV file(s)")
        selected_file = st.sidebar.selectbox(
            "Select a file to analyze",
            options=[f.name for f in csv_files],
            index=0
        )
        
        # Load data
        try:
            df = pd.read_csv(data_dir / selected_file)
            
            # Main content
            st.markdown("---")
            
            # Data Overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            with col4:
                st.metric("Data Size", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            st.markdown("---")
            
            # Tabs for different analyses
            tab1, tab2, tab3, tab4 = st.tabs([
                "📋 Data Preview",
                "📊 Exploratory Data Analysis",
                "🌍 Cross-Country Comparison",
                "📈 Visualizations"
            ])
            
            with tab1:
                st.subheader("Data Preview")
                st.dataframe(df.head(100), use_container_width=True)
                
                st.subheader("Data Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Column Names:**")
                    st.write(list(df.columns))
                with col2:
                    st.write("**Data Types:**")
                    st.write(df.dtypes)
                
                st.subheader("Missing Values")
                missing_data = df.isnull().sum()
                missing_data = missing_data[missing_data > 0]
                if len(missing_data) > 0:
                    st.bar_chart(missing_data)
                else:
                    st.success("✅ No missing values found!")
            
            with tab2:
                st.subheader("Statistical Summary")
                st.dataframe(df.describe(), use_container_width=True)
                
                st.subheader("Correlation Matrix")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 1:
                    corr = df[numeric_cols].corr()
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
                    st.pyplot(fig)
                else:
                    st.info("Need at least 2 numeric columns for correlation analysis")
            
            with tab3:
                st.subheader("Cross-Country Analysis")
                
                # Check for country column
                country_cols = [col for col in df.columns if 'country' in col.lower() or 'nation' in col.lower()]
                
                if country_cols:
                    country_col = country_cols[0]
                    st.write(f"**Using column: {country_col}**")
                    
                    # Country distribution
                    country_counts = df[country_col].value_counts()
                    st.bar_chart(country_counts)
                    
                    # Country comparison
                    selected_metric = st.selectbox(
                        "Select metric for comparison",
                        options=numeric_cols if len(numeric_cols) > 0 else [],
                        index=0 if len(numeric_cols) > 0 else None
                    )
                    
                    if selected_metric:
                        country_stats = df.groupby(country_col)[selected_metric].agg(['mean', 'std', 'min', 'max'])
                        st.dataframe(country_stats, use_container_width=True)
                        
                        # Visualization
                        fig, ax = plt.subplots(figsize=(10, 6))
                        df.boxplot(column=selected_metric, by=country_col, ax=ax)
                        plt.title(f"{selected_metric} by Country")
                        plt.suptitle("")
                        plt.xlabel("Country")
                        plt.ylabel(selected_metric)
                        st.pyplot(fig)
                else:
                    st.info("No country column detected. Please ensure your data has a column with country information.")
            
            with tab4:
                st.subheader("Data Visualizations")
                
                # Select columns for visualization
                if len(numeric_cols) > 0:
                    x_col = st.selectbox("X-axis", options=numeric_cols, index=0)
                    y_col = st.selectbox("Y-axis", options=numeric_cols, index=min(1, len(numeric_cols)-1)) if len(numeric_cols) > 1 else None
                    
                    if y_col:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.scatter(df[x_col], df[y_col], alpha=0.5)
                        ax.set_xlabel(x_col)
                        ax.set_ylabel(y_col)
                        ax.set_title(f"{y_col} vs {x_col}")
                        st.pyplot(fig)
                    
                    # Distribution plot
                    selected_dist = st.selectbox("Select column for distribution", options=numeric_cols, index=0)
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.hist(df[selected_dist].dropna(), bins=30, edgecolor='black')
                    ax.set_xlabel(selected_dist)
                    ax.set_ylabel("Frequency")
                    ax.set_title(f"Distribution of {selected_dist}")
                    st.pyplot(fig)
                else:
                    st.info("No numeric columns available for visualization")
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.exception(e)
    else:
        st.sidebar.warning("⚠️ No CSV files found in the data directory")
        st.info("""
        **📋 No data files found:**
        - Please add CSV files to the `data/` directory
        - The app will automatically detect and load them
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Solar Farm Data Analysis Dashboard | Part of 10 Academy Training Challenge</p>
</div>
""", unsafe_allow_html=True)

