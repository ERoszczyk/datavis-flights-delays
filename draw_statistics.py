import calendar

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from streamlit_plotly_events import plotly_events

month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
         6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
month_name_to_number = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

month_abbr_to_full_name = {
    'Jan': 'January',
    'Feb': 'February',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December'
}

dayOfWeek = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday',
             6: 'Saturday', 7: 'Sunday'}


def draw_avg_flight_delay_by_delay_type(df, selected_airport, start_date, end_date, start_time, end_time):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    df = df[df['ARRIVAL_DELAY'] > 0]
    if selected_airport:
        df = df[df['AIRPORT_x'].str.contains(selected_airport)]
    # Calculate average delay by delay type
    average_delay_by_type = df[
        ['ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
         'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']].mean().round(2)
    # Create a bar chart
    title = 'Average Flight Delay By Delay Type'
    fig = px.bar(x=['ARRIVAL DELAY', 'DEPARTURE DELAY', 'AIR SYSTEM DELAY', 'SECURITY DELAY', 'AIRLINE DELAY',
                    'LATE AIRCRAFT DELAY', 'WEATHER DELAY'],
                 y=average_delay_by_type.values,
                 labels={'x': 'Delay Type', 'y': 'Average Delay Time (minutes)'},
                 title=title, width=500)

    # Show the plot
    st.plotly_chart(fig)


def draw_monthly_avg_flight_delay_by_month(df, selected_airport, start_date, end_date, start_time, end_time):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    df = df[df['ARRIVAL_DELAY'] > 0]
    if selected_airport:
        df = df[df['AIRPORT_x'].str.contains(selected_airport)]

    delay_columns = ['MONTH', 'ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
                     'LATE_AIRCRAFT_DELAY',
                     'WEATHER_DELAY']
    df_delays = df[delay_columns]

    # Calculate monthly average delays
    monthly_avg_delays = df_delays.groupby('MONTH').mean().reset_index()

    # Convert month numbers to month names
    monthly_avg_delays['MONTH'] = monthly_avg_delays['MONTH'].apply(lambda x: calendar.month_abbr[x])

    # Specify the order of months
    months_order = list(calendar.month_abbr)[1:]  # Starts from January

    # Convert 'MONTH' column to categorical with specified order
    monthly_avg_delays['MONTH'] = pd.Categorical(monthly_avg_delays['MONTH'], categories=months_order, ordered=True)

    # Sort the DataFrame by the categorical 'MONTH' column
    monthly_avg_delays = monthly_avg_delays.sort_values(by='MONTH')

    # Melt the DataFrame for easier plotting
    melted_df = pd.melt(monthly_avg_delays, id_vars=['MONTH'], var_name='Delay Type',
                        value_name='Average Delay (minutes)')

    # Plot using Plotly Express
    title = 'Monthly Average Flight Delays by Delay Type'

    fig = px.line(melted_df, x='MONTH', y='Average Delay (minutes)', color='Delay Type',
                  title=title,
                  labels={'Average Delay (minutes)': 'Average Delay (minutes)', 'MONTH': 'Month'},
                  category_orders={
                      "Delay Type": ['ARRIVAL DELAY', 'DEPARTURE DELAY', 'AIR SYSTEM DELAY', 'SECURITY DELAY',
                                     'AIRLINE DELAY', 'LATE AIRCRAFT DELAY', 'WEATHER DELAY']},
                  markers='MONTH',
                  height=450, width=600, color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig)


def draw_avg_flight_delay_by_delay_type_routes(df, dep_airport, arr_airport, start_date, end_date, start_time,
                                               end_time):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    if dep_airport and arr_airport:
        df = df[(df['AIRPORT_x'].str.contains(dep_airport)) & (df['AIRPORT_y'].str.contains(arr_airport))]
    # Calculate average delay by delay type
    average_delay_by_type = df[
        ['ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
         'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']].mean().round(2)
    # Create a bar chart
    title = 'Average Flight Delay By Delay Type'

    fig = px.bar(x=['ARRIVAL DELAY', 'DEPARTURE DELAY', 'AIR SYSTEM DELAY', 'SECURITY DELAY', 'AIRLINE DELAY',
                    'LATE AIRCRAFT DELAY', 'WEATHER DELAY'],
                 y=average_delay_by_type.values,
                 labels={'x': 'Delay Type', 'y': 'Average Delay Time (minutes)'},
                 title=title, width=500)

    # Show the plot
    st.plotly_chart(fig)


def draw_monthly_avg_flight_delay_by_month_routes(df, dep_airport, arr_airport, start_date, end_date, start_time,
                                                  end_time):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    if dep_airport and arr_airport:
        df = df[(df['AIRPORT_x'].str.contains(dep_airport)) & (df['AIRPORT_y'].str.contains(arr_airport))]

    delay_columns = ['MONTH', 'ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
                     'LATE_AIRCRAFT_DELAY',
                     'WEATHER_DELAY']
    df_delays = df[delay_columns]

    # Calculate monthly average delays
    monthly_avg_delays = df_delays.groupby('MONTH').mean().reset_index()

    # Convert month numbers to month names
    monthly_avg_delays['MONTH'] = monthly_avg_delays['MONTH'].apply(lambda x: calendar.month_abbr[x])

    # Specify the order of months
    months_order = list(calendar.month_abbr)[1:]  # Starts from January

    # Convert 'MONTH' column to categorical with specified order
    monthly_avg_delays['MONTH'] = pd.Categorical(monthly_avg_delays['MONTH'], categories=months_order, ordered=True)

    # Sort the DataFrame by the categorical 'MONTH' column
    monthly_avg_delays = monthly_avg_delays.sort_values(by='MONTH')

    # Melt the DataFrame for easier plotting
    melted_df = pd.melt(monthly_avg_delays, id_vars=['MONTH'], var_name='Delay Type',
                        value_name='Average Delay (minutes)')

    # Plot using Plotly Express
    title = 'Monthly Average Flight Delays by Delay Type'

    fig = px.line(melted_df, x='MONTH', y='Average Delay (minutes)', color='Delay Type',
                  title=title,
                  labels={'Average Delay (minutes)': 'Average Delay (minutes)', 'MONTH': 'Month'},
                  category_orders={
                      "Delay Type": ['ARRIVAL DELAY', 'DEPARTURE DELAY', 'AIR SYSTEM DELAY', 'SECURITY DELAY',
                                     'AIRLINE DELAY', 'LATE AIRCRAFT DELAY', 'WEATHER DELAY']},
                  markers='MONTH',
                  height=450, width=600, color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig)


def draw_no_flights_by_month(df, airline, start_time, end_time, type):
    # Number of flights by month
    if airline != 'All':
        df = df[df['AIRLINE'].str.contains(airline)]
    df = df[(pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]
    if type == 'On Time':
        df = df[df['ARRIVAL_DELAY'] <= 0]
    elif type == 'Delayed':
        df = df[df['ARRIVAL_DELAY'] > 0]
    elif type == 'Cancelled':
        df = df[df['CANCELLED'] == 1]

    dff = df.MONTH.value_counts().to_frame().reset_index().sort_values(by='MONTH')
    dff.columns = ['month', 'flight_num']
    month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
             6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    dff.month = dff.month.map(month)

    trace = go.Bar(
        x=dff.month,
        y=dff.flight_num,
        marker=dict(
            color=dff.flight_num,
            colorscale='Reds',
            showscale=True)
    )

    data = [trace]
    layout = go.Layout(
        title='Number of Flights By Month',
        yaxis=dict(title='Number of Flights'
                   )
    )

    fig = go.Figure(data=data, layout=layout)
    sel_month = plotly_events(fig)
    if (sel_month):
        month_name = month_abbr_to_full_name[sel_month[0]['x']]
        st.session_state.month_selected = month_name


def draw_flight_no(df, selected_month, airline, start_time, end_time, type):
    df = df[df['MONTH'] == month_name_to_number[selected_month]]

    if airline != 'All':
        df = df[df['AIRLINE'].str.contains(airline)]

    df = df[(pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]

    if type == 'On Time':
        df = df[df['ARRIVAL_DELAY'] <= 0]
    elif type == 'Delayed':
        df = df[df['ARRIVAL_DELAY'] > 0]
    elif type == 'Cancelled':
        df = df[df['CANCELLED'] == 1]

    # Group by day and get the count of flights
    flight_counts = df.groupby('DAY')['FLIGHT_NUMBER'].count().reset_index()

    # Plot the data using Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=flight_counts['DAY'],
        y=flight_counts['FLIGHT_NUMBER'],
        mode='lines+markers',
        name='',
        line=dict(shape='linear', dash='dot'),
        connectgaps=True,  # This attribute connects gaps in the data with a line
        # text=flight_counts['FLIGHT_NUMBER'],
        text=[f'Flights number: {count}' for count in flight_counts['FLIGHT_NUMBER']],
        textposition='top center',
        hovertemplate='%{text}',
        hoverinfo='text',
    ))

    # Update layout
    fig.update_layout(
        title=f"Number of Flights in {selected_month}",
        xaxis_title='Day of the Month',
        yaxis_title='Number of Flights',
        showlegend=False,
        yaxis=dict(range=[0, flight_counts['FLIGHT_NUMBER'].max() + 1])
    )

    # Display the plot
    plotly_events(fig)


def number_of_flights_by_day_of_week(df, selected_month, airline, start_time, end_time, type):
    if selected_month != 'All':
        df = df[df['MONTH'] == month_name_to_number[selected_month]]
    if airline != 'All':
        df = df[df['AIRLINE'].str.contains(airline)]
    df = df[(pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]

    if type == 'On Time':
        df = df[df['ARRIVAL_DELAY'] <= 0]
    elif type == 'Delayed':
        df = df[df['ARRIVAL_DELAY'] > 0]
    elif type == 'Cancelled':
        df = df[df['CANCELLED'] == 1]
    flight_counts = df.groupby('DAY_OF_WEEK')['FLIGHT_NUMBER'].count().reset_index()

    flight_counts['DAY_OF_WEEK'] = flight_counts['DAY_OF_WEEK'].map(dayOfWeek)

    trace1 = go.Bar(
        x=flight_counts['DAY_OF_WEEK'],
        y=flight_counts['FLIGHT_NUMBER'],
        name='Weather',
        marker=dict(
            color=flight_counts['FLIGHT_NUMBER'],
            colorscale=px.colors.sequential.YlOrRd,
            showscale=True
        )
    )

    data = [trace1]
    layout = go.Layout(
        title='Number of Flights By Day of Week',
        yaxis=dict(title='Number of Flights')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly_events(fig)


def mean_arr_dep_by_airlines(df, start_date, end_date, start_time, end_time, airlines):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (
            pd.to_datetime(df['ARRIVAL_TIME']).dt.time >= start_time) & (
                    pd.to_datetime(df['ARRIVAL_TIME']).dt.time <= end_time)]

    if len(airlines) > 0:
        df = df[df['AIRLINE'].isin(airlines)]

    dff = df.groupby('AIRLINE').DEPARTURE_DELAY.mean().to_frame().sort_values(by='DEPARTURE_DELAY',
                                                                              ascending=False).round(2)
    trace1 = go.Bar(
        x=dff.index,
        y=dff.DEPARTURE_DELAY,
        name='Departure Delay',
        marker=dict(
            color='navy'
        )
    )

    dff = df.groupby('AIRLINE').ARRIVAL_DELAY.mean().to_frame().sort_values(by='ARRIVAL_DELAY',
                                                                            ascending=False).round(2)
    trace2 = go.Bar(
        x=dff.index,
        y=dff.ARRIVAL_DELAY,
        name='Arrival Delay',
        marker=dict(
            color='red'
        )
    )

    data = [trace1, trace2]
    layout = go.Layout(xaxis=dict(tickangle=15), title='Mean Arrival & Departure Delay by Airlines',
                       yaxis=dict(title='Delay (minutes)'),
                       barmode='stack', autosize=True)

    fig = go.Figure(data=data, layout=layout)
    plotly_events(fig)


def cancellation_rate_by_airlines(df, start_date, end_date, airlines):
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]
    if len(airlines) > 0:
        df = df[df['AIRLINE'].isin(airlines)]

    dff = df.groupby('AIRLINE')[['CANCELLED']].mean().sort_values(by='CANCELLED',
                                                                  ascending=False).round(3)

    trace1 = go.Scatter(
        x=dff.index,
        y=dff.CANCELLED,
        mode='markers',
        marker=dict(
            symbol='star-square',
            sizemode='diameter',
            sizeref=1,
            size=20,
            color=dff.CANCELLED,
            colorscale=px.colors.sequential.Plotly3,
            showscale=True
        )
    )

    data = [trace1]
    layout = go.Layout(xaxis=dict(tickangle=20),
                       title='Cancellation Rate by Airlines', yaxis=dict(title='Cancellation Rate'
                                                                         )
                       )

    fig = go.Figure(data=data, layout=layout)
    plotly_events(fig)
