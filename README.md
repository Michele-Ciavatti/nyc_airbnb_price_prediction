## Setup

**Requirements:** Python 3.10+ (developed on 3.12) and a free Kaggle account.

1. Clone the repository and enter the project folder:

```bash
   git clone https://github.com/Michele-Ciavatti/nyc_airbnb_price_prediction.git
   cd nyc_airbnb_price_prediction
```

2. Create and activate an environment (conda or venv):

```bash
   conda create -n nyc-airbnb python=3.12
   conda activate nyc-airbnb
```

3. Set up your Kaggle credentials:
   - Create an API token in your Kaggle account: *Settings → API*.
   - Copy the template and fill it in:

   ```bash
      # Linux / macOS / Git Bash
      cp .env.example .env

      # Windows (cmd or PowerShell)
      copy .env.example .env
   ```

   - Edit `.env` and paste your token. This file is git-ignored and never committed.

4. Install the project and its dependencies:

```bash
   # If you have invoke installed (run invoke --list to see all commands)
   invoke setup

   # Otherwise
   pip install -e ".[dev]"
   pre-commit install
```

5. Open the desired notebook in `notebooks/` and run it top to bottom.

## Project structure

```text
nyc_airbnb_price_prediction/
├── data/  
    ├── external
    ├── interim
    ├── processed
    ├── raw  
├── docs/                    # MkDocs documentation sources
│   ├── api.md  
│   └── index.md  
├── notebooks/               # Analysis notebooks, run in order
│   ├── 01_eda.ipynb         # Exploratory data analysis
│   └── 02_modeling.ipynb    # Model training and evaluation
├── src/                     # Reusable project code, imported by the notebooks
│   ├── __init__.py
│   ├── dataset.py           # Dataset download (kagglehub) and loading
│   └── plots.py             # Plotting helpers
├── .env.example             # Template for Kaggle credentials (copy to .env, never commit .env)
├── .gitattributes  
├── .gitignore  
├── .pre-commit-config.yaml  # Pre-commit hooks (ruff, detect-secrets, nbstripout, ...)
├── .secrets.baseline        # detect-secrets baseline of known/accepted findings
├── LICENSE  
├── README.md  
├── mkdocs.yml               # MkDocs configuration
├── pyproject.toml           # Package metadata, dependencies and tool configuration
└── tasks.py                 # Invoke tasks (setup, lint, test, docs, ...); see `invoke --list`
```
