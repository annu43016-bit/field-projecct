# ThyroVision AI — Real Thyroid Dataset Project

## Dataset provenance
This project uses the UCI Machine Learning Repository **New-Thyroid** dataset (215 records, 5 continuous test attributes, 3 classes). The data file is fetched when the Flask app starts from a public GitHub mirror of the UCI `new-thyroid.data` file:
https://raw.githubusercontent.com/mikeizbicki/datasets/master/csv/uci/new-thyroid.data

Dataset documentation and attribute/class descriptions:
https://archive.ics.uci.edu/dataset/102/thyroid+disease
https://github.com/mikeizbicki/datasets/blob/master/csv/uci/new-thyroid.names

The labels are documented as: 1 = normal, 2 = hyperthyroid, 3 = hypothyroid. The source documentation says the class diagnosis was based on a complete medical record, not only the five measurements.

## Run on Windows
1. Extract the ZIP.
2. Open the folder in VS Code or Command Prompt.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open: `http://127.0.0.1:5000`

Internet is required on first startup because the raw public dataset is downloaded at runtime. If it cannot be reached, the app deliberately disables predictions instead of inventing data.

## What the app does
- Loads the real public dataset (no synthetic rows are generated).
- Splits the dataset into 75% training and 25% held-out test data, stratified by class.
- Trains a Random Forest classifier on the training portion.
- Displays held-out test accuracy and returns a class prediction plus model score breakdown.
- The UI accepts the five original dataset measurements: T3-resin uptake, total serum thyroxin, total serum triiodothyronine, basal TSH, and maximum TSH difference after TRH.

## Important limitations
This is a small historical dataset (215 rows), not a modern clinical dataset. It is not representative of every population or laboratory, has not been clinically validated for deployment, and is not a medical device. Its output is for academic demonstration only and must not be used to diagnose or treat anyone. Do not present its accuracy as real-world clinical accuracy. The measurement names/units are retained from the source and should not be substituted with modern lab test units without validation.

## Project files
- `app.py`: dataset download, preprocessing, training, evaluation, prediction API
- `templates/index.html`: website
- `static/style.css`: design
- `static/app.js`: prediction form interaction
- `requirements.txt`: dependencies

## Deploying on Render (Free)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Select the `thyrovision_real` folder as the repository root only if using a monorepo; otherwise upload the contents of this folder to the repository root.

Educational project only. This model is not clinically validated and must not be used for diagnosis or treatment decisions.
