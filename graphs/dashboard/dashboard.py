import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load CSV data
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Load CSV file
st.title("Real-time Data Dashboard")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load the data from CSV
    data = load_data(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data)

    # Select columns for plotting
    st.sidebar.header("Filter Data for Visualization")
    columns = data.columns.tolist()

    x_axis = st.sidebar.selectbox("Select X-axis", columns)
    y_axis = st.sidebar.selectbox("Select Y-axis", columns)
    chart_type = st.sidebar.selectbox("Select Chart Type", ['Line', 'Bar', 'Scatter'])

    st.write(f"Displaying {chart_type} chart for {y_axis} over {x_axis}")

    # Plotting the selected chart
    fig, ax = plt.subplots()
    if chart_type == 'Line':
        ax.plot(data[x_axis], data[y_axis], marker='o')
    elif chart_type == 'Bar':
        ax.bar(data[x_axis], data[y_axis])
    elif chart_type == 'Scatter':
        ax.scatter(data[x_axis], data[y_axis])

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{chart_type} Chart")

    st.pyplot(fig)

