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
