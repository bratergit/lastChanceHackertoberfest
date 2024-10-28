import pandas as pd
import numpy as np
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_financial_data(df):
    try:
        # Define expected columns
        expected_columns = ['Date', 'Open', 'Close', 'Volume']

        # Remove extra columns
        df = df[expected_columns]
        logging.info("Extra columns removed.")

        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        logging.info("Date column converted to datetime.")

        # Drop rows with invalid dates
        df = df.dropna(subset=['Date'])
        logging.info("Rows with invalid dates dropped.")

        # Remove duplicate rows
        df = df.drop_duplicates()
        logging.info("Duplicate rows removed.")

        # Convert numeric columns to numeric types and handle non-numeric values
        for col in ['Open', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        logging.info("Non-numeric values in 'Open', 'Close', and 'Volume' columns handled.")

        # Drop rows with NaN values in numeric columns
        df = df.dropna(subset=['Open', 'Close', 'Volume'])
        logging.info("Rows with NaN values in numeric columns dropped.")

        # Handle missing values by forward filling
        # df = df.fillna(method='ffill')
        df = df.ffill()
        logging.info("Missing values handled by forward filling.")

        # Remove outliers using Z-score method
        z_scores = np.abs(
            (df.select_dtypes(include=[np.number]) - df.select_dtypes(include=[np.number]).mean()) / df.select_dtypes(
                include=[np.number]).std())
        df = df[(z_scores < 3).all(axis=1)]
        logging.info("Outliers removed using Z-score method.")

        return df

    except Exception as exc:
        logging.error(f"An error occurred during data cleaning: {exc}")
        return None


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Clean financial data.')
    parser.add_argument('input_file', type=str, help='Path to the raw financial data file')
    args = parser.parse_args()

    try:
        # Load raw data
        raw_data = pd.read_csv(args.input_file, on_bad_lines='skip')
        logging.info("Raw financial data loaded.")
    except FileNotFoundError:
        logging.error(f"File not found: {args.input_file}")
    except pd.errors.EmptyDataError:
        logging.error(f"File is empty: {args.input_file}")
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
    else:
        # Clean data
        cleaned_data = clean_financial_data(raw_data)
        if cleaned_data is not None:
            cleaned_data.to_csv('cleaned_financial_data.csv', index=False)
            logging.info("Cleaned financial data saved to 'cleaned_financial_data.csv'.")
