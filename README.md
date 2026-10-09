## Setup

**Requirements:** Python 3.10+ (developed on 3.12) and a free Kaggle account.

### Without `make`

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

3. Install the project and its dependencies:
```bash
   pip install -e ".[dev]"
```

4. Set up your Kaggle credentials:
   - Create an API token in your Kaggle account: *Settings → API*.
   - Copy the template and fill it in:
```bash
     cp .env.example .env        # on Windows PowerShell: copy .env.example .env
```
   - Edit `.env` and paste your token. This file is git-ignored and never committed.

5. Download the data (optional, since the notebooks do it automatically if it's missing):
```bash
   python src/retrieve_data.py
```
   The dataset is saved in `data/` and is git-ignored.

6. Open the desired notebook in `notebooks/` and run it top to bottom.

### Shortcuts with `make`

If you have `make` installed, just use `make setup`. Further 
instructions (linting, formatting, tests, docs) can be seen wth `make help`.