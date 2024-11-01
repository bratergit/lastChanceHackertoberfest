import yfinance as yf
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_stock_data(ticker, start_date, end_date):
    try:
        # Validate date format
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Fetch data from Yahoo Finance
        logging.info(f"Fetching data for ticker: {ticker} from {start_date} to {end_date}")
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            logging.error(f"No data found for ticker: {ticker} in the given date range or ticker is invalid.")
            return None

        logging.info(f"Data fetched successfully for ticker: {ticker}")
        return df[['Open', 'Close', 'Volume']]

    except ValueError as ve:
        logging.error(f"Date format error: {ve}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def save_to_csv(data, ticker, start_date, end_date, directory):
    try:
        # Ensure directory exists
        os.makedirs(directory, exist_ok=True)

        # Construct full file path
        filename = f"{ticker}_{start_date}_{end_date}.csv"
        filepath = os.path.join(directory, filename)

        # Save DataFrame to CSV
        data.to_csv(filepath)
        logging.info(f"Data saved to {filepath} successfully.")
    except Exception as e:
        logging.error(f"An error occurred while saving to CSV: {e}")

if __name__ == "__main__":
    # Example usage
    ticker = input("Enter stock ticker: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    

    data = fetch_stock_data(ticker, start_date, end_date)
    if data is not None:
        print(data)
        save_choice = input("Do you want to save this data to a CSV file? (yes/no): ").strip().lower()
        if save_choice == "yes":
            # Ask for optional save directory
            save_directory = input("Enter directory to save data (leave empty for default 'stocks_data/'): ") or "stocks_data/"
            save_to_csv(data, ticker, start_date, end_date, save_directory)
        else:
            logging.info("Data was not saved to a CSV file.")
