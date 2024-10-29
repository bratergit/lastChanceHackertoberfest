# Financial Data Cleaning Script

This script automates the cleaning and transformation of raw financial data into a format suitable for analysis. It handles missing values, outliers, and date formatting issues.

## Requirements

- Python 3.x
- pandas 2.2.3
- numpy 2.1.2

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/bratergit/lastChanceHackertoberfest.git
    cd lastChanceHackertoberfest/analytics/data_cleaning
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your raw financial data in a CSV file named `raw_financial_data.csv` in the same directory as the script.

2. Run the script:
    ```sh
    python main.py raw_financial_data.csv
    ```

3. The cleaned data will be saved to a file named `cleaned_financial_data.csv` in the same directory.

## File Structure

- `main.py`: The script to clean and transform raw financial data.
- `requirements.txt`: The file listing the required Python packages.
- `raw_test_data.csv`: Example raw financial data file containing different errors.

## License

This project is licensed under the MIT License.