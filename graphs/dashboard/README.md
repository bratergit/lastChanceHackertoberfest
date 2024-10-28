# Real-time Data Dashboard

This project is a real-time data dashboard built using **Streamlit**. The dashboard allows users to upload a CSV file and visualize the data interactively through different chart types, such as line charts, bar charts, and scatter plots. The application is highly customizable and updates the visualizations in real time based on user inputs.

## Features
- **Upload CSV File**: Easily upload a structured CSV file containing the data you want to analyze.
- **Interactive Data Visualization**: Select columns for the X and Y axes from the uploaded CSV file and choose the chart type (Line, Bar, Scatter).
- **Real-time Chart Update**: The charts update dynamically based on user selections, making the visualization process fast and efficient.

## Prerequisites

Before running the dashboard, make sure you have Python installed along with the following packages:

- **Streamlit**: For building interactive dashboards.
- **Pandas**: For handling CSV data.
- **Matplotlib**: For generating the charts.

You can install the necessary packages by running the following command:

```bash
pip install streamlit pandas matplotlib

## How to Use

Clone this repository to your local machine:
	```bash
		git clone https://github.com/adalbertobrant/real-time-data-dashboard.git
		cd real-time-data-dashboard

Ensure you have the dependencies installed:
	```bash
		pip install -r requirements.txt

Run the dashboard.py script:
	```bash
	streamlit run dashboard.py

This will launch the Streamlit application in your default web browser. You can now:

Upload a CSV file using the file uploader.
Select the X-axis and Y-axis columns for your data.
Choose the type of chart to visualize (Line, Bar, or Scatter).
## CSV File Format

###The CSV file should be structured with column headers for each type of data (e.g., Date, Price, Volume). Here is an example format for a stock price data CSV:

csv

Date,Price,Volume
2024-01-01,100,5000
2024-01-02,105,4500
2024-01-03,110,6000
2024-01-04,120,7000

Once the file is uploaded, the data will be displayed, and you can choose the desired chart type and axes for visualization.


## Customization

You can extend the dashboard by adding more features such as date range filters, more advanced calculations (like moving averages), or even connecting to an API to fetch real-time data.
The code is modular, and new chart types or functionalities can be added easily.

## License

This project is licensed under the MIT License.

