import dash
import dash_auth
import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import numpy as np
import re
import os
 
# Load your data
# Define correct column names manually
columns = ["Country", "Continent", "Age Group", "Gender", "Platform", "Request Type", "Job Type", "Referral Source", "Inquiry Time", "Date"]

# Load the CSV by skipping the faulty header
df = pd.read_csv("Ona.csv", sep=",", names=columns, skiprows=1)

# Convert 'Date' column to datetime
df["Date"] = pd.to_datetime(df["Date"])

COUNTRY = "Country"
CONTINENT = "Continent"
AGE_GROUP = "Age Group"
GENDER = "Gender"
PLATFORM = "Platform"
REQUEST_TYPE = "Request Type"
JOB_TYPE = "Job Type"
REFERRAL = "Referral Source"
INQUIRY_TIME = "Inquiry Time"
DATE = "Date"
 
# Extract average from age group string
def age_group_to_number(s):
    if pd.isnull(s): return np.nan
    match = re.match(r"(\d+)[^\d]+(\d+)", str(s))
    if match:
        return (int(match.group(1)) + int(match.group(2))) / 2
    try:
        return float(s)
    except:
        return np.nan
 
df["Age (approx)"] = df[AGE_GROUP].apply(age_group_to_number)
numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
 
# New color palette and styling
BACKGROUND_COLOR = '#f9f9f9'
PRIMARY_COLOR = '#636EFA'
SECONDARY_COLOR = '#EF553B'
TEXT_COLOR = '#1f2c56'
ACCENT_COLOR = '#00cc96'
GRAPH_COLORS = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, '#ab63fa', '#FFA15A']
 
dropdown_style = {
    'width': '100%',
    'padding': '12px 14px',
    'border': '1px solid #ced4da',
    'borderRadius': '8px',
    'backgroundColor': '#ffffff',
    'color': TEXT_COLOR,
    'fontSize': '0.95rem',
    'marginBottom': '1rem',
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
    'transition': 'all 0.25s ease',
    'outline': 'none',
    'cursor': 'pointer'
}

graph_container_style = {
    'backgroundColor': '#ffffff',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
    'padding': '1.5rem',
    'marginBottom': '1rem',
    'border': '1px solid #e9ecef',
    'height': '600px'
}

sidebar_style = {
    'backgroundColor': '#ffffff',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
    'padding': '1.5rem',
    'marginBottom': '1rem',
    'border': '1px solid #e9ecef',
    'height': 'fit-content',
    'position': 'sticky',
    'top': '20px'
}

tab_selected_style = {
    'backgroundColor': PRIMARY_COLOR,
    'color': '#ffffff',
    'border': 'none',
    'borderBottom': '4px solid ' + ACCENT_COLOR,
    'fontWeight': '700',
    'fontSize': '1rem',
    'padding': '12px 20px',
    'borderRadius': '12px 12px 0 0',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'marginRight': '8px',
    'letterSpacing': '0.5px',
    'transition': 'all 0.3s ease'
}

tab_style = {
    'backgroundColor': '#f8f9fa',
    'color': TEXT_COLOR,
    'fontSize': '0.95rem',
    'padding': '12px 20px',
    'cursor': 'pointer',
    'border': 'none',
    'borderRadius': '12px 12px 0 0',
    'marginRight': '8px',
    'transition': 'all 0.3s ease-in-out',
    'fontWeight': '500',
    'letterSpacing': '0.3px',
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.04)'
}

header = html.Div(
    children=[
        html.H1("📊 Dashboard for Product Sales Analysis", style={
            'color': '#ffffff',
            'fontSize': '2.5rem',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'marginBottom': '0.2rem',
            'textShadow': '1px 1px 3px rgba(0,0,0,0.3)'
        }),
        html.H4("Insights by Geography, Time, and Demographics", style={
            'color': '#f8f9fa',
            'textAlign': 'center',
            'fontWeight': 'normal',
            'marginTop': '0',
            'textShadow': '0.5px 0.5px 2px rgba(0,0,0,0.2)'
        })
    ],
    style={
        'background': 'linear-gradient(135deg, #3f51b5, #5a55ae)',
        'padding': '1.5rem',
        'borderRadius': '16px',
        'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.1)',
        'marginBottom': '2rem'
    }
)
 
app_analysis = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app_analysis.server

USERS = {"admin": "Ouna321", "user": "Ouna123"}
auth = dash_auth.BasicAuth(app_analysis, USERS)

# Sidebar filters component
sidebar_filters = html.Div(
    id="sidebar-filters",
    style=sidebar_style,
    children=[
        html.H4("Filters", style={'color': TEXT_COLOR, 'marginBottom': '1.5rem', 'fontWeight': 'bold'}),
        html.Div(id="dynamic-filters")
    ]
)

# Main tabs
tabs = dcc.Tabs(
    id="main-tabs",
    value="geographical",
    children=[
        dcc.Tab(
            label="🌎 Geography",
            value="geographical",
            selected_style=tab_selected_style,
            style=tab_style
        ),
        dcc.Tab(
            label="👫 Gender",
            value="gender_distribution",
            selected_style=tab_selected_style,
            style=tab_style
        ),
        dcc.Tab(
            label="📅 Time Period",
            value="time_period",
            selected_style=tab_selected_style,
            style=tab_style
        ),
        dcc.Tab(
            label="🛒 Product Interest",
            value="product",
            selected_style=tab_selected_style,
            style=tab_style
        ),
        dcc.Tab(
            label="👴 Age",
            value="age_distribution",
            selected_style=tab_selected_style,
            style=tab_style
        ),
        dcc.Tab(
            label="📊 Statistics",
            value="statistical_analysis",
            selected_style=tab_selected_style,
            style=tab_style
        )
    ]
)

# Main content area
main_content = html.Div(id="main-content", style=graph_container_style)
 
app_analysis.layout = html.Div([
    header,
    tabs,
    dbc.Row([
        dbc.Col([sidebar_filters], md=3, style={'paddingRight': '1rem'}),
        dbc.Col([main_content], md=9, style={'paddingLeft': '1rem'})
    ], style={'marginTop': '1rem'})
], style={
    'backgroundColor': '#f8f9fc',
    'minHeight': '100vh',
    'padding': '20px',
    'color': TEXT_COLOR
})

# Callback to update sidebar filters based on selected tab
@app_analysis.callback(
    Output("dynamic-filters", "children"),
    [Input("main-tabs", "value")]
)
def update_sidebar_filters(selected_tab):
    if selected_tab == "geographical":
        return [
            html.Label("Continent", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="geo-continent-filter",
                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Continent",
                style=dropdown_style
            ),
            html.Label("Country", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="geo-country-filter",
                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Country",
                style=dropdown_style
            ),
            html.Label("Request Type", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="geo-request-type-filter",
                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Request Type",
                style=dropdown_style
            ),
        ]
    
    elif selected_tab == "gender_distribution":
        return [
            html.Label("Continent", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="gender-continent-filter",
                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Continent",
                style=dropdown_style
            ),
            html.Label("Country", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="gender-country-filter",
                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Country",
                style=dropdown_style
            ),
            html.Label("Request Type", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="request-type-gender-filter",
                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Request Type",
                style=dropdown_style
            ),
        ]
    
    elif selected_tab == "time_period":
        return [
            html.Label("Continent", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="time-continent-filter",
                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Continent",
                style=dropdown_style
            ),
            html.Label("Country", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="time-country-filter",
                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Country",
                style=dropdown_style
            ),
            html.Label("Time Granularity", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="time-granularity-filter",
                options=[
                    {"label": "Day", "value": "D"},
                    {"label": "Week", "value": "W"},
                    {"label": "Month", "value": "MS"},
                    {"label": "Year", "value": "Y"}
                ],
                value="MS",
                clearable=False,
                style=dropdown_style
            ),
            html.Label("Request Type", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="time-request-type-filter",
                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Request Type",
                style=dropdown_style
            ),
        ]
    
    elif selected_tab == "product":
        return [
            html.Label("Continent", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="product-continent-filter",
                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Continent",
                style=dropdown_style
            ),
            html.Label("Country", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="product-country-filter",
                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Country",
                style=dropdown_style
            ),
        ]
    
    elif selected_tab == "age_distribution":
        return [
            html.Label("Continent", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="age-continent-filter",
                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Continent",
                style=dropdown_style
            ),
            html.Label("Country", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="age-country-filter",
                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Country",
                style=dropdown_style
            ),
            html.Label("Request Type", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="request-type-age-filter",
                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Request Type",
                style=dropdown_style
            ),
        ]
    
    elif selected_tab == "statistical_analysis":
        return [
            html.Label("Metric", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="statistical-metric",
                options=[
                    {"label": "Mean", "value": "mean"},
                    {"label": "Median", "value": "median"},
                    {"label": "Mode", "value": "mode"},
                    {"label": "Standard Deviation", "value": "std"}
                ],
                value="mean",
                clearable=False,
                style=dropdown_style
            ),
            html.Label("Request Type", style={'fontWeight': 'bold', 'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id="statistical-request-filter",
                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                value=None,
                clearable=True,
                placeholder="Select Request Type",
                style=dropdown_style
            ),
        ]
    
    return []

# Callback to update main content based on selected tab
@app_analysis.callback(
    Output("main-content", "children"),
    [Input("main-tabs", "value")]
)
def update_main_content(selected_tab):
    if selected_tab == "geographical":
        return dcc.Graph(id="geo-distribution-graph", style={'height': '100%'})
    elif selected_tab == "gender_distribution":
        return dcc.Graph(id="gender-distribution-graph", style={'height': '100%'})
    elif selected_tab == "time_period":
        return dcc.Graph(id="time-period-graph", style={'height': '100%'})
    elif selected_tab == "product":
        return dcc.Graph(id="product-interest-map", style={'height': '100%'})
    elif selected_tab == "age_distribution":
        return dcc.Graph(id="age-distribution-graph", style={'height': '100%'})
    elif selected_tab == "statistical_analysis":
        return html.Div(id="statistical-analysis-output", style={
            'padding': '2rem',
            'fontSize': '1.2rem',
            'textAlign': 'center',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '8px',
            'margin': '2rem',
            'minHeight': '200px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        })
    
    return html.Div("Select a tab to view content")

# All your existing callbacks remain the same
@app_analysis.callback(
    Output("geo-distribution-graph", "figure"),
    [
        Input("geo-continent-filter", "value"),
        Input("geo-country-filter", "value"),
        Input("geo-request-type-filter", "value")
    ]
)
def update_geo_distribution_graph(selected_continent, selected_country, selected_request):
    filtered_df = df.copy()

    if selected_continent:
        filtered_df = filtered_df[filtered_df[CONTINENT] == selected_continent]
    if selected_country:
        filtered_df = filtered_df[filtered_df[COUNTRY] == selected_country]
    if selected_request:
        filtered_df = filtered_df[filtered_df[REQUEST_TYPE] == selected_request]

    geo_df = filtered_df.groupby(COUNTRY).size().reset_index(name="Number of Requests")

    fig = px.choropleth(
        geo_df,
        locations=COUNTRY,
        locationmode="country names",
        color="Number of Requests",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Geographical Distribution of Requests"
    )

    fig.update_layout(
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True
        )
    )

    return fig

# Product Interest Graph (using Platform as Product)
@app_analysis.callback(
    Output("product-interest-map", "figure"),
    [Input("product-continent-filter", "value"),
     Input("product-country-filter", "value")]
)
def update_product_interest_donut(selected_continent, selected_country):
    # Filter the dataset
    product_df = df.copy()
    if selected_continent:
        product_df = product_df[product_df[CONTINENT] == selected_continent]
    if selected_country:
        product_df = product_df[product_df[COUNTRY] == selected_country]

    # Prepare data
    product_counts = product_df[PLATFORM].value_counts().reset_index()
    product_counts.columns = ['Product', 'Number of Requests']

    # Define custom color sequence
    custom_colors = ['#1f77b4', '#9467bd', '#ff7f0e']  # blue, purple, orange

    # Create Donut Chart
    fig = px.pie(
        product_counts,
        names='Product',
        values='Number of Requests',
        hole=0.4,
        color_discrete_sequence=custom_colors,
        title='Product Interest by Platform (Donut View)'
    )
    fig.update_layout(title_x=0.5)
    return fig
    
# Country dropdown depends on continent (Product Interest)
@app_analysis.callback(
    Output("product-country-filter", "options"),
    [Input("product-continent-filter", "value")]
)
def update_product_country_options(selected_continent):
    if selected_continent:
        filtered_countries = df[df[CONTINENT] == selected_continent][COUNTRY].dropna().unique()
        return [{"label": c, "value": c} for c in sorted(filtered_countries)]
    else:
        return [{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())]

# Time period tab - country dropdown depends on continent
@app_analysis.callback(
    Output("time-country-filter", "options"),
    [Input("time-continent-filter", "value")]
)
def update_time_country_options(selected_continent):
    if selected_continent:
        filtered_countries = df[df[CONTINENT] == selected_continent][COUNTRY].dropna().unique()
        return [{"label": c, "value": c} for c in sorted(filtered_countries)]
    else:
        return [{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())]

# Gender tab - country dropdown depends on continent
@app_analysis.callback(
    Output("gender-country-filter", "options"),
    [Input("gender-continent-filter", "value")]
)
def update_gender_country_options(selected_continent):
    if selected_continent:
        filtered_countries = df[df[CONTINENT] == selected_continent][COUNTRY].dropna().unique()
        return [{"label": c, "value": c} for c in sorted(filtered_countries)]
    else:
        return [{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())]

# Age tab - country dropdown depends on continent
@app_analysis.callback(
    Output("age-country-filter", "options"),
    [Input("age-continent-filter", "value")]
)
def update_age_country_options(selected_continent):
    if selected_continent:
        filtered_countries = df[df[CONTINENT] == selected_continent][COUNTRY].dropna().unique()
        return [{"label": c, "value": c} for c in sorted(filtered_countries)]
    else:
        return [{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())]
 
# Updated Time Period Graph with Continent and Country filters
@app_analysis.callback(
    Output("time-period-graph", "figure"),
    [
        Input("time-granularity-filter", "value"),
        Input("time-continent-filter", "value"),
        Input("time-country-filter", "value"),
        Input("time-request-type-filter", "value")
    ]
)
def update_time_graph(granularity, selected_continent, selected_country, selected_request):
    filtered_df = df.copy()
    if selected_continent:
        filtered_df = filtered_df[filtered_df[CONTINENT] == selected_continent]
    if selected_country:
        filtered_df = filtered_df[filtered_df[COUNTRY] == selected_country]
    if selected_request:
        filtered_df = filtered_df[filtered_df[REQUEST_TYPE] == selected_request]

    data = filtered_df.set_index(DATE).resample(granularity)[REQUEST_TYPE].count().reset_index()
    data.rename(columns={REQUEST_TYPE: 'Number of Requests'}, inplace=True)

    fig = px.line(
        data, x=DATE, y="Number of Requests", title="Requests Over Time", markers=True
    )
    fig.update_traces(line=dict(color="purple"))
    fig.update_layout(title_x=0.5)
    return fig

# Updated Gender distribution with continent and country filters
@app_analysis.callback(
    Output("gender-distribution-graph", "figure"),
    [
        Input("gender-continent-filter", "value"),
        Input("gender-country-filter", "value"),
        Input("request-type-gender-filter", "value")
    ]
)
def update_gender_graph(selected_continent, selected_country, selected_request):
    # Start with full data
    df_filtered = df.copy()

    # Apply continent filter first
    if selected_continent:
        df_filtered = df_filtered[df_filtered[CONTINENT] == selected_continent]

    # Then apply country filter (if selected and if it's in the filtered continent)
    if selected_country:
        df_filtered = df_filtered[df_filtered[COUNTRY] == selected_country]

    # Then apply request type
    if selected_request:
        df_filtered = df_filtered[df_filtered[REQUEST_TYPE] == selected_request]

    # Restrict to Male and Female only
    df_filtered = df_filtered[df_filtered[GENDER].isin(["Male", "Female"])]

    # Group by gender
    gender_data = df_filtered[GENDER].value_counts().reset_index()
    gender_data.columns = ['Gender', 'Requests']

    # Color scheme: green for Male, orange for Female
    gender_colors = ['#28a745', '#fd7e14']

    # Create bar chart
    fig = px.bar(
        gender_data,
        y='Gender',
        x='Requests',
        orientation='h',
        color='Gender',
        color_discrete_sequence=gender_colors,
        category_orders={'Gender': ['Male', 'Female']}
    )

    fig.update_layout(
        title="Requests by Gender",
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#343a40'),
        margin=dict(l=40, r=20, t=60, b=40)
    )

    return fig
 
# Updated Age distribution with continent and country filters
@app_analysis.callback(
    Output("age-distribution-graph", "figure"),
    [Input("age-continent-filter", "value"),
     Input("age-country-filter", "value"),
     Input("request-type-age-filter", "value")]
)
def update_age_graph(selected_continent, selected_country, selected_request):
    # Start with full data
    df_filtered = df.copy()
    
    # Apply continent filter
    if selected_continent:
        df_filtered = df_filtered[df_filtered[CONTINENT] == selected_continent]
    
    # Apply country filter
    if selected_country:
        df_filtered = df_filtered[df_filtered[COUNTRY] == selected_country]
    
    # Apply request type filter
    if selected_request:
        df_filtered = df_filtered[df_filtered[REQUEST_TYPE] == selected_request]

    # Define the correct age group order
    age_order = ["18-25", "26-35", "36-45", "46-55", "56+"]

    # Make Age Group a categorical column with order
    df_filtered[AGE_GROUP] = pd.Categorical(df_filtered[AGE_GROUP], categories=age_order, ordered=True)

    # Group and count
    age_data = df_filtered[AGE_GROUP].value_counts().sort_index().reset_index()
    age_data.columns = ['Age Group', 'Requests']

    # Custom color palette: pink, green, blue, orange, purple
    custom_colors = ['#ff69b4', '#28a745', '#007bff', '#fd7e14', '#6f42c1']

    # Plot bar chart
    fig = px.bar(
        age_data,
        x='Age Group',
        y='Requests',
        color='Age Group',
        category_orders={'Age Group': age_order},
        color_discrete_sequence=custom_colors
    )

    fig.update_layout(
        title="Ordered Age Distribution",
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#343a40'),
        margin=dict(l=40, r=20, t=60, b=40)
    )

    return fig
 
# Statistical Analysis
@app_analysis.callback(
    Output("statistical-analysis-output", "children"),
    [
        Input("statistical-metric", "value"),
        Input("statistical-request-filter", "value")
    ]
)
def update_statistical_analysis(selected_metric, selected_request):
    if not selected_metric or not selected_request:
        return "Please select both a metric and a request type."

    # Filter dataset to selected request type
    filtered_df = df[df[REQUEST_TYPE] == selected_request]

    # Group by Job Type (assuming it represents sales roles)
    job_counts = filtered_df[JOB_TYPE].value_counts()

    if job_counts.empty:
        return f"No job data available for '{selected_request}'."

    if selected_metric == "mean":
        value = job_counts.mean()
        return f"🔍 Mean requests per job type for '{selected_request}': {value:.2f}"
    elif selected_metric == "median":
        value = job_counts.median()
        return f"📊 Median requests per job type for '{selected_request}': {value:.2f}"
    elif selected_metric == "mode":
        mode_val = job_counts.mode()
        value = mode_val[0] if not mode_val.empty else "N/A"
        return f"📌 Mode of requests per job type for '{selected_request}': {value}"
    elif selected_metric == "std":
        value = job_counts.std()
        return f"📈 Standard deviation of requests for '{selected_request}': {value:.2f}"
    elif selected_metric == "count":
        value = job_counts.sum()
        return f"📦 Total requests made for '{selected_request}': {value}"
    else:
        return "⚠️ Invalid metric selected."

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app_analysis.run(host='0.0.0.0', port=port, debug=False)


