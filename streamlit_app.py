import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_csv_data(file_path, date_column):
    df = pd.read_csv(file_path)
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    return df

data1 = load_csv_data("Data1.csv", "date")
data2 = load_csv_data("Data2.csv", "timepoint")
data3a = load_csv_data("Data3a.csv", "Date")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main Page", "Project Information", "Additional Questions", "Dataset Description"])  # Added the new page here

if page == "Main Page":
    st.title("Flight Data Analysis")
    st.write("Created by XYZ123")
    st.write("This webapp provides various visualizations related to flight data, weather conditions, and reasons for flight delays or cancellations. You can use the sidebar to select a date range and explore different datasets.")

    st.sidebar.header("Date Range Selector")
    start_date = data3a["Date"].min()
    end_date = data3a["Date"].max()
    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        [start_date, end_date],
        min_value=start_date,
        max_value=end_date,
    )
    
    if len(selected_dates) == 2:
        start_date = pd.Timestamp(selected_dates[0])
        end_date = pd.Timestamp(selected_dates[1])

        filtered_data1 = data1[
            (data1["date"] >= start_date) & (data1["date"] <= end_date)
        ]
        filtered_data2 = data2[
            (data2["timepoint"] >= start_date) & (data2["timepoint"] <= end_date)
        ]
        filtered_data3a = data3a[
            (data3a["Date"] >= start_date) & (data3a["Date"] <= end_date)
        ]
    else:
        st.warning("Please select a valid date range.")

    st.header("Arrivals and Departures Over Time")
    if not filtered_data1.empty:
        st.line_chart(
            filtered_data1[["date", "arrivals", "departures"]].set_index("date")
        )
    else:
        st.warning("No data available for the selected date range.")

    st.header("Weather Conditions Over Time")
    if not filtered_data2.empty:
        st.bar_chart(filtered_data2[["timepoint", "temp2m"]].set_index("timepoint"))
    else:
        st.warning("No weather data available for the selected date range.")

    st.header("Cancelled Flights Over DayOfWeek")
    if 'DayOfWeek' in filtered_data3a.columns and 'Cancelled' in filtered_data3a.columns:
        cancelled_count = filtered_data3a.groupby("DayOfWeek")["Cancelled"].count()
        st.bar_chart(cancelled_count)
    else:
        st.warning("No data for cancelled flights.")

    st.header("Diverted Flights Over DayOfWeek")
    if 'DayOfWeek' in filtered_data3a.columns and 'Diverted' in filtered_data3a.columns:
        diverted_count = filtered_data3a.groupby("DayOfWeek")["Diverted"].count()
        st.bar_chart(diverted_count)
    else:
        st.warning("No data for diverted flights.")

    st.header("Security Delays Over DayOfWeek")
    if 'DayOfWeek' in filtered_data3a.columns and 'SecurityDelay' in filtered_data3a.columns:
        security_delay_count = filtered_data3a.groupby("DayOfWeek")["SecurityDelay"].count()
        st.bar_chart(security_delay_count)
    else:
        st.warning("No data for security delays.")

    delay_counts = {
        "Cancelled": filtered_data3a["Cancelled"].sum(),
        "Diverted": filtered_data3a["Diverted"].sum(),
        "SecurityDelay": filtered_data3a["SecurityDelay"].sum(),
    }

    delay_df = pd.DataFrame(list(delay_counts.items()), columns=["Reason", "Count"])

    st.header("Distribution of Reasons for Delay")
    st.bar_chart(delay_df.set_index("Reason"))

elif page == "Project Information":
    st.title("Project Information")
    st.write(
        "Through this project, I explored the relationship between flight delays, weather conditions, "
        "and other factors. I learned how to preprocess data, create various visualizations, and draw insights "
        "from them. The experience highlighted the importance of cleaning data and handling errors properly. "
        "I also discovered the challenges in drawing conclusions from incomplete or noisy data. Overall, "
        "the project helped me understand how different data sources can interact to reveal meaningful patterns."
    )
    st.write(
        "There are some limitations with CSV data storage and built-in visualization tools, but the flexibility of Streamlit "
        "allowed me to create an interactive web app for data exploration."
    )

elif page == "Additional Questions":
    st.title("Additional Questions")
    st.write("Q1: What did you set out to study?")
    st.write("I set out to study the relationship between flight data, weather conditions, and reasons for delays or cancellations. The goal was to understand if specific factors had a notable impact on flight operations.")

    st.write("Q2: What did you discover/what were your conclusions?")
    st.write("I discovered that weather conditions and other external factors could impact flight delays or cancellations. The data showed trends over time that aligned with known weather patterns and disruptions.")

    st.write("Q3: What difficulties did you have in completing the project?")
    st.write(
        "I faced challenges with data consistency and handling missing or erroneous data. Additionally, limited "
        "visualization options without external libraries made certain representations more challenging."
    )

    st.write("Q4: What skills did you wish you had while you were doing the project?")
    st.write(
        "I wished I had more advanced skills in data cleaning and handling complex data operations in pandas. "
        "Also, deeper knowledge of data visualization techniques would have been helpful."
    )

    st.write("Q5: What would you do next to expand or augment the project?")
    st.write(
        "To expand the project, I would integrate additional data sources for weather, flight schedules, and airport information. "
        "This would allow for a more comprehensive analysis of factors affecting flight operations. I would also improve the "
        "user interface and interactivity to provide a more seamless experience."
    )
    
elif page == "Dataset Description":
    st.title("Dataset Description")
    st.header("Data Source 1")
    st.write(
        "FlightAware offers flight tracking and aviation data services. Users can access real-time flight statuses, airport information, and historical flight data spanning from 2019 to 2024."
    )

    st.header("Data Source 2")
    st.write(
        "7timer.info provides astronomical data through its API. Users can access information like sunrise, sunset, and moon phase. Gathering historical data from 2019 to 2024 for RUH requires repeated API requests."
    )

    st.header("Data Source 3")
    st.write(
        "Kaggle's dataset provides comprehensive information about flight delays at Riyadh Airport, including reasons for delays, cancellations, and diversions."
    )
