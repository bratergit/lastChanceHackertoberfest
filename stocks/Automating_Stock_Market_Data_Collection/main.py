import yfinance as yf
import logging
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


if __name__ == "__main__":
    # Example usage
    ticker = input("Enter stock ticker: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    data = fetch_stock_data(ticker, start_date, end_date)
    if data is not None:
        print(data)
