# Solar Challenge Week 0
## Solar Farm Data Analysis - West Africa

Comprehensive Exploratory Data Analysis (EDA) of solar energy datasets from three West African countries: Benin, Sierra Leone, and Togo. This project includes data profiling, cleaning, visualization, and cross-country comparison for solar energy potential assessment.

**Part of**: 10 Academy KAIM Training Program - Week 0 Challenge  
**Project Code**: B8W0  
**Author**: Haben Eyasu

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Data Description](#data-description)
- [Notebooks](#notebooks)
- [Usage](#usage)
- [Project Deliverables](#project-deliverables)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project performs end-to-end Exploratory Data Analysis on solar irradiance datasets from three West African countries to:

- Profile, clean, and explore each country's solar dataset
- Prepare data for cross-country comparison and region-ranking
- Identify patterns, anomalies, and relationships in solar irradiance data
- Generate actionable insights for solar energy planning

### Datasets Analyzed

1. **Benin - Malanville**: `benin-malanville.csv`
2. **Sierra Leone - Bumbuna**: `sierraleone-bumbuna.csv`
3. **Togo - Dapaong**: `togo-dapaong_qc.csv`

---

## Project Structure

```
solar-challenge-week1/
├── README.md                    # Project documentation (this file)
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── LICENSE                     # Project license
│
├── data/                       # Data directory (gitignored)
│   ├── benin-malanville.csv    # Original Benin dataset
│   ├── benin_clean.csv         # Cleaned Benin dataset
│   ├── sierraleone-bumbuna.csv # Original Sierra Leone dataset
│   ├── sierraleone_clean.csv   # Cleaned Sierra Leone dataset
│   ├── togo-dapaong_qc.csv     # Original Togo dataset
│   └── togo_clean.csv          # Cleaned Togo dataset
│
├── notebooks/                  # Jupyter notebooks
│   ├── __init__.py
│   ├── README.md              # Notebooks documentation
│   ├── benin_eda.ipynb        # Benin EDA analysis
│   ├── sierraleone_eda.ipynb # Sierra Leone EDA analysis
│   └── togo_eda.ipynb         # Togo EDA analysis
│
├── app/                       # Application code
│   ├── __init__.py
│   └── app.py                 # Streamlit dashboard (future)
│
├── scripts/                   # Utility scripts
│   ├── __init__.py
│   └── README.md
│
├── src/                       # Source code modules
│   └── __init__.py
│
├── tests/                     # Test files
│   └── __init__.py
│
├── .github/                   # GitHub workflows
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
│
├── .vscode/                   # VS Code settings
│   └── settings.json
│
├── venv/                      # Virtual environment (gitignored)
│
├── REPORT_TEMPLATE.md         # Project report template
├── TIME_MANAGEMENT_LOG.md     # Time management log
├── REPORT_GUIDE.md            # Report preparation guide
└── SUBMISSION_MAPPING.md      # Submission mapping guide
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/habeneyasu/solar-challenge-week1.git
   cd solar-challenge-week1
   ```

2. **Update system packages (Linux):**
   ```bash
   sudo apt update
   sudo apt install python3.12-venv
   ```

3. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Verify Installation

```bash
python --version
pip list
```

---

## Data Description

Each dataset contains time-series measurements with the following variables:

| Variable | Description | Unit |
|----------|-------------|------|
| `Timestamp` | Date and time of observation | yyyy-mm-dd hh:mm |
| `GHI` | Global Horizontal Irradiance | W/m² |
| `DNI` | Direct Normal Irradiance | W/m² |
| `DHI` | Diffuse Horizontal Irradiance | W/m² |
| `ModA` | Module A measurement | W/m² |
| `ModB` | Module B measurement | W/m² |
| `Tamb` | Ambient Temperature | °C |
| `RH` | Relative Humidity | % |
| `WS` | Wind Speed | m/s |
| `WSgust` | Wind Gust Speed | m/s |
| `WD` | Wind Direction | °N (to east) |
| `BP` | Barometric Pressure | hPa |
| `TModA` | Temperature of Module A | °C |
| `TModB` | Temperature of Module B | °C |
| `Cleaning` | Cleaning flag | 1 or 0 |
| `Precipitation` | Precipitation rate | mm/min |

---

## Notebooks

### EDA Notebooks

Each country has a comprehensive EDA notebook following industry best practices:

1. **`notebooks/benin_eda.ipynb`**
   - Complete EDA for Benin - Malanville dataset
   - All required analysis sections implemented
   - Executive summary and documentation

2. **`notebooks/sierraleone_eda.ipynb`**
   - Complete EDA for Sierra Leone - Bumbuna dataset
   - Professional structure and analysis

3. **`notebooks/togo_eda.ipynb`**
   - Complete EDA for Togo - Dapaong dataset
   - Comprehensive analysis and insights

### Notebook Structure

Each notebook includes:
- **Section 1**: Setup and Data Loading
- **Section 2**: Summary Statistics & Missing-Value Report
- **Section 3**: Outlier Detection & Basic Cleaning
- **Section 4**: Time Series Analysis
- **Section 5**: Cleaning Impact Analysis
- **Section 6**: Correlation & Relationship Analysis
- **Section 7**: Wind & Distribution Analysis
- **Section 8**: Temperature Analysis
- **Section 9**: Bubble Chart Analysis
- **Section 10**: Executive Summary & Key Findings
- **Section 11**: Documentation

### Running Notebooks

```bash
# Activate virtual environment
source venv/bin/activate

# Launch Jupyter Notebook
jupyter notebook notebooks/

# Or launch JupyterLab
jupyter lab notebooks/
```

---

## Usage

### Running EDA Analysis

1. **Open a notebook:**
   ```bash
   jupyter notebook notebooks/benin_eda.ipynb
   ```

2. **Run all cells:**
   - Use `Cell > Run All` from the menu
   - Or press `Shift + Enter` to run cells sequentially

3. **View cleaned data:**
   - Cleaned datasets are automatically saved to `data/` directory
   - Files: `benin_clean.csv`, `sierraleone_clean.csv`, `togo_clean.csv`

### Accessing Cleaned Data

```python
import pandas as pd
from pathlib import Path

# Load cleaned dataset
df_clean = pd.read_csv('data/benin_clean.csv')
print(df_clean.head())
```


## CI/CD

The project includes a GitHub Actions CI/CD pipeline (`.github/workflows/ci.yml`) that:

- Runs on pushes to `main` and `setup-task` branches
- Tests Python installation
- Verifies dependencies installation
- Ensures code quality

### View CI Status

Check the "Actions" tab in the GitHub repository to view CI pipeline runs.

---

## Git Workflow

### Branch Structure

- `main`: Main development branch
- `setup-task`: Initial project setup
- `eda-benin`: Benin EDA development
- `eda-sierraleone`: Sierra Leone EDA development
- `eda-sogo`: Togo EDA development

### Common Commands

```bash
# Check current branch
git branch

# Create and switch to new branch
git checkout -b feature-branch

# Stage changes
git add .

# Commit changes
git commit -m "feat: description of changes"

# Push to remote
git push origin branch-name
```

---

## Dependencies

### Core Libraries

- **pandas** (≥1.5.0): Data manipulation and analysis
- **numpy** (≥1.21.0): Numerical computing
- **matplotlib** (≥3.5.0): Plotting and visualization
- **seaborn** (≥0.11.0): Statistical data visualization
- **scipy** (≥1.9.0): Scientific computing
- **scikit-learn** (≥1.2.0): Machine learning utilities

### Development Tools

- **jupyter** (≥1.0.0): Interactive notebook environment
- **streamlit** (≥1.28.0): Dashboard development
- **windrose** (≥1.8.0): Wind rose plots

See `requirements.txt` for complete list.

---

## Contributing

This is a training project for the 10 Academy KAIM program. For questions or issues:

1. Check existing documentation
2. Review notebook documentation sections
3. Refer to `REPORT_GUIDE.md` for detailed instructions

---

## License

See `LICENSE` file for details.

---

## References

- IEC 61724-1:2017 - Photovoltaic system performance monitoring
- ISO 9060:2018 - Solar energy instrumentation standards
- Industry-standard EDA practices for renewable energy data analysis

---

## Contact

**Author**: Haben Eyasu  
**Repository**: https://github.com/habeneyasu/solar-challenge-week1  
**Program**: 10 Academy KAIM Training - Week 0

---

**Last Updated**: November 2025  
**Status**: ✅ Complete
