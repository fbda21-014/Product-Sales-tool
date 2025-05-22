import dash
import dash_auth
import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import numpy as np
import re
 
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
    'padding': '14px 16px',
    'border': '1px solid #ced4da',
    'borderRadius': '8px',
    'backgroundColor': '#f1f3f5',
    'color': TEXT_COLOR,
    'fontSize': '1rem',
    'marginBottom': '1.2rem',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.06)',
    'transition': 'all 0.25s ease',
    'outline': 'none',
    'cursor': 'pointer'
}

graph_container_style = {
    'backgroundColor': '#e0e0e0',  # Darker grey
    'borderRadius': '16px',
    'boxShadow': '0 8px 16px rgba(0, 0, 0, 0.08)',
    'padding': '2rem',
    'marginBottom': '2rem',
    'border': '1px solid #dee2e6',
    'transition': 'all 0.3s ease-in-out'
}

tab_selected_style = {
    'backgroundColor': PRIMARY_COLOR,
    'color': '#ffffff',
    'border': 'none',
    'borderBottom': '4px solid ' + ACCENT_COLOR,
    'fontWeight': '700',
    'fontSize': '1.1rem',
    'padding': '16px 24px',
    'borderRadius': '16px 16px 0 0',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'marginRight': '10px',
    'letterSpacing': '0.5px',
    'transition': 'all 0.3s ease'
}

tab_style = {
    'backgroundColor': '#f8f9fa',
    'color': TEXT_COLOR,
    'fontSize': '1.05rem',
    'padding': '16px 24px',
    'cursor': 'pointer',
    'border': 'none',
    'borderRadius': '16px 16px 0 0',
    'marginRight': '10px',
    'transition': 'all 0.3s ease-in-out',
    'fontWeight': '500',
    'letterSpacing': '0.3px',
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.04)'
}

header = html.Div(
    children=[
        html.H1("📊 Dashboard for Product Sales Analysis", style={
            'color': '#ffffff',
            'fontSize': '2.8rem',
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
        'background': 'linear-gradient(135deg, #3f51b5, #5a55ae)',  # You can use PRIMARY_COLOR if defined
        'padding': '2rem',
        'borderRadius': '16px',
        'boxShadow': '0 6px 12px rgba(0, 0, 0, 0.1)',
        'marginBottom': '2rem'
    }
)
 
app_analysis = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app_analysis.server
 
USERS = {"admin": "Ouna321", "user": "Ouna123"}
auth = dash_auth.BasicAuth(app_analysis, USERS)
 
tabs = dcc.Tabs(
    id="main-tabs",
    value="geographical",
    children=[
    # Geographical Distribution
        dcc.Tab(
            label="🌎 Requests by Geographical Location",
            value="geographical",
            selected_style=tab_selected_style,
            style=tab_style,
            children=[
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Label("Continent", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id="geo-continent-filter",
                            options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                            value=None,
                            clearable=True,
                            placeholder="Select Continent",
                            style=dropdown_style
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Country", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id="geo-country-filter",
                            options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                            value=None,
                            clearable=True,
                            placeholder="Select Country",
                            style=dropdown_style
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Platform", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id="geo-platform-filter",
                            options=[{"label": p, "value": p} for p in sorted(df[PLATFORM].dropna().unique())],
                            value=None,
                            clearable=True,
                            placeholder="Select Platform",
                            style=dropdown_style
                        ),
                    ], md=4),
                ], className="g-2", style={'marginBottom': '1.2rem'}),
                dcc.Graph(id="geo-distribution-graph", style=graph_container_style),
            ], style={'maxWidth': '900px', 'margin': 'auto'})
            ]
        ),

    # Gender Distribution
    dcc.Tab(
        label="👫 Requests by Gender",
        value="gender_distribution",
        selected_style=tab_selected_style,
        style=tab_style,
        children=[
            html.Div([
                dbc.Row([
                    dbc.Col([
                            html.Label("Continent", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="gender-continent-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Continent",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Country", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="gender-country-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Country",
                                style=dropdown_style
                            ),
                        ], md=4),
                    dbc.Col([
                        html.Label("Request Type", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id="request-type-gender-filter",
                            options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                            value=None,
                            clearable=True,
                            placeholder="Select Request Type",
                            style=dropdown_style
                        ),
                    ], md=4),
                ], className="g-2", style={'marginBottom': '1.2rem'}),
                dcc.Graph(id="gender-distribution-graph", style=graph_container_style)
            ], style={'maxWidth': '900px', 'margin': 'auto'})
        ]
    ),

            # Time Period Distribution
        dcc.Tab(
            label="📅 Requests over Time Period",
            value="time_period",
            selected_style=tab_selected_style,
            style=tab_style,
            children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Continent", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="time-continent-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Continent",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Country", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="time-country-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Country",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Time Granularity", style={'fontWeight': 'bold'}),
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
                          ], md=4),
                    ], className="g-2", style={'marginBottom': '1.2rem'}),
                    dcc.Graph(id="time-period-graph", style=graph_container_style),
                ], style={'maxWidth': '900px', 'margin': 'auto'})    
            ]
        ),

            # Product Interest Tab (using Platform as Product)
        dcc.Tab(
            label="🛒 Product Interest by Platform",
            value="product",
            selected_style=tab_selected_style,
            style=tab_style,
            children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Continent", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="product-continent-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Continent",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Country", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="product-country-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Country",
                                style=dropdown_style
                            ),
                        ], md=4),
                    ], className="g-2", style={'marginBottom': '1.2rem'}),
                    dcc.Graph(id="product-interest-map", style=graph_container_style),
                ], style={'maxWidth': '900px', 'margin': 'auto'})
            ]
        ),

    # Age Distribution
    dcc.Tab(
        label="👴 Requests by Age",
        value="age_distribution",
        selected_style=tab_selected_style,
        style=tab_style,
        children=[
            html.Div([
                dbc.Row([
                        dbc.Col([
                            html.Label("Continent", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="age-continent-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[CONTINENT].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Continent",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Country", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="age-country-filter",
                                options=[{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Country",
                                style=dropdown_style
                            ),
                        ], md=4),
                        dbc.Col([
                            html.Label("Request Type", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="request-type-age-filter",
                                options=[{"label": rt, "value": rt} for rt in sorted(df[REQUEST_TYPE].dropna().unique())],
                                value=None,
                                clearable=True,
                                placeholder="Select Request Type",
                                style=dropdown_style
                            ),
                        ], md=4),
                    ], className="g-2", style={'marginBottom': '1.2rem'}),
                    dcc.Graph(id="age-distribution-graph", style=graph_container_style),
                ], style={'maxWidth': '900px', 'margin': 'auto'})
            ]
        ),
        # Statistical Analysis Tab
        dcc.Tab(
            label="📊 Statistical Analysis",
            value="statistical_analysis",
            selected_style=tab_selected_style,
            style=tab_style,
            children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Metric", style={'fontWeight': 'bold'}),
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
                        ], md=4),
                        dbc.Col([
                            html.Label("Column", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id="statistical-column",
                                options=[
                                    {"label": "Age (approx)", "value": "Age (approx)"},
                                    {"label": INQUIRY_TIME, "value": INQUIRY_TIME},
                                    {"label": DATE, "value": DATE}
                                ] + [
                                    {"label": col, "value": col} for col in numeric_columns if col not in ["Age (approx)"]
                                ],
                                value="Age (approx)",
                                clearable=False,
                                style=dropdown_style
                            ),
                        ], md=4),
                    ], className="g-2", style={'marginBottom': '1.2rem'}),
                    html.Div(id="statistical-analysis-output", style=graph_container_style),
                ], style={'maxWidth': '900px', 'margin': 'auto'})
            ]
        ),
    ]
)
 
app_analysis.layout = html.Div([
    header,
    tabs
], style = {
    'backgroundColor': '#d1f2eb',  # Soft teal background
    'minHeight': '100vh',
    'padding': '20px',
    'color': TEXT_COLOR  # Maintain your consistent text color
}
)

# Geographical tab callbacks
# Geographical tab callbacks
@app_analysis.callback(
    Output("geo-distribution-graph", "figure"),
    [Input("geo-continent-filter", "value"),
     Input("geo-country-filter", "value"),
     Input("geo-platform-filter", "value")]
)
def update_geo_distribution_graph(selected_continent, selected_country, selected_platform):
    # Start with full data
    filtered_df = df.copy()
    
    # Apply filters
    if selected_continent:
        filtered_df = filtered_df[filtered_df[CONTINENT] == selected_continent]
    if selected_country:
        filtered_df = filtered_df[filtered_df[COUNTRY] == selected_country]
    if selected_platform:
        filtered_df = filtered_df[filtered_df[PLATFORM] == selected_platform]
    
    # Group by country for choropleth map
    geo_df = filtered_df.groupby(COUNTRY).size().reset_index(name="Number of Requests")
    
    fig = px.choropleth(
        geo_df, locations=COUNTRY, locationmode="country names", color="Number of Requests",
        color_continuous_scale=px.colors.sequential.Plasma, 
        title="Geographical Distribution of Requests"
    )
    
    fig.update_layout(
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
        )
    )
    
    return fig

# Add dependency for geo-country-filter on geo-continent-filter
@app_analysis.callback(
    Output("geo-country-filter", "options"),
    [Input("geo-continent-filter", "value")]
)
def update_geo_country_options(selected_continent):
    if selected_continent:
        filtered_countries = df[df[CONTINENT] == selected_continent][COUNTRY].dropna().unique()
        return [{"label": c, "value": c} for c in sorted(filtered_countries)]
    else:
        return [{"label": c, "value": c} for c in sorted(df[COUNTRY].dropna().unique())]
 
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
    [Input("time-granularity-filter", "value"),
     Input("time-continent-filter", "value"),
     Input("time-country-filter", "value")]
)
def update_time_graph(granularity, selected_continent, selected_country):
    # Filter the data first
    filtered_df = df.copy()
    if selected_continent:
        filtered_df = filtered_df[filtered_df[CONTINENT] == selected_continent]
    if selected_country:
        filtered_df = filtered_df[filtered_df[COUNTRY] == selected_country]
    
    # Resample request data by selected time unit (day, month, etc.)
    data = filtered_df.set_index(DATE).resample(granularity)[REQUEST_TYPE].count().reset_index()
    data.rename(columns={REQUEST_TYPE: 'Number of Requests'}, inplace=True)

    # Create a purple line chart
    fig = px.line(
        data,
        x=DATE,
        y="Number of Requests",
        title="Requests Over Time",
        markers=True
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
    [Input("statistical-metric", "value"),
     Input("statistical-column", "value")]
)
def update_statistical_analysis(selected_metric, selected_column):
    if not selected_metric or not selected_column:
        return "Select a metric and a column for analysis."

    series = df[selected_column].dropna()

    # Try converting to numeric if possible
    try:
        series_numeric = pd.to_numeric(series, errors='coerce').dropna()
    except:
        series_numeric = pd.Series(dtype=float)

    result = "No valid data found."

    # For numeric data
    if not series_numeric.empty:
        if selected_metric == "mean":
            result = f"The mean of {selected_column} is: {series_numeric.mean():.2f}"
        elif selected_metric == "median":
            result = f"The median of {selected_column} is: {series_numeric.median():.2f}"
        elif selected_metric == "std":
            result = f"The standard deviation of {selected_column} is: {series_numeric.std():.2f}"
        elif selected_metric == "mode":
            mode_val = series_numeric.mode()
            result = f"The mode of {selected_column} is: {mode_val[0]:.2f}" if not mode_val.empty else "No mode found."
        return result

    # For datetime columns
    if pd.api.types.is_datetime64_any_dtype(series):
        if selected_metric == "mean":
            result = f"The mean date of {selected_column} is: {series.mean().date()}"
        elif selected_metric == "median":
            result = f"The median date of {selected_column} is: {series.median().date()}"
        elif selected_metric == "std":
            result = f"The standard deviation is: {series.std()}"
        elif selected_metric == "mode":
            mode_val = series.mode()
            result = f"The mode of {selected_column} is: {mode_val[0].date()}" if not mode_val.empty else "No mode found."
        return result

    # For string/categorical data (like Inquiry Time)
    if selected_metric == "mode":
        mode_val = series.mode()
        result = f"The mode of {selected_column} is: {mode_val[0]}" if not mode_val.empty else "No mode found."
        return result

    return f"{selected_metric.title()} is not applicable to {selected_column}."
 
import os

if __name__ == '__main__':
    app_analysis.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )

