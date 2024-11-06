import shutil

import os
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import yaml

from curadoria_coletiva.collect_materials import collect_materials

materials_path = "curadoria_coletiva/materials"
# Path to the local YAML file
yaml_file_path = "curadoria_coletiva/all_materials.yml"

collect_materials(materials_path, yaml_file_path)

app = dash.Dash(__name__)
app.title = "Curadoria Coletiva"

# Load data from the YAML file
def _load_yaml_data(file_path):
    """Loads data from the specified YAML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Create a DataFrame from the loaded data
def _create_dataframe(data):
    """Converts YAML data into a Pandas DataFrame."""
    return pd.DataFrame(data)

# Layout structure of the application
def _create_layout(df):
    """Creates the layout for the Dash app."""
    return html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
        _create_logo_section(),
        html.H1("Curadoria Coletiva", style={'color': '#8B008B', 'text-align': 'center', 'margin-bottom': '30px'}),
        _create_search_box(),
        _create_filter_dropdowns(df),
        html.Div(id='results', style={'margin-top': '30px'})
    ])

def _create_logo_section():
    """Generates the logo section with dark and light theme support."""
    return html.Div(
        style={'text-align': 'center'},
        children=[
            html.Picture(
                children=[
                    html.Source(
                        media="(prefers-color-scheme: dark)",
                        srcSet="https://github.com/cumbucadev/design/raw/main/images/logo-dark-transparent.png"
                    ),
                    html.Img(
                        alt="Cumbuca Dev Logo",
                        src="https://github.com/cumbucadev/design/raw/main/images/logo-light-transparent.png",
                        style={'width': '15%'}
                    ),
                ]
            ),
        ]
    )

def _create_search_box():
    """Creates the search input box."""
    return html.Div([
        dcc.Input(id='search-box', type='text', placeholder="Digite para buscar...",
                  style={'width': '100%', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
    ], style={'margin-bottom': '20px'})

def _create_filter_dropdowns(df):
    """Creates the dropdowns for category and sorting filters."""
    return html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['assuntos'].explode().unique().tolist())],
            placeholder="Assunto",
            style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'middle'}
        ),
        dcc.Dropdown(
            id='sort-dropdown',
            options=[{'label': col.replace('_', ' ').capitalize(), 'value': col} for col in df.columns],
            placeholder="Ordenar por",
            style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'middle', 'margin-left': '4%'}
        ),
    ], style={'margin-bottom': '20px'})

# Generate the layout of results with additional styling
def generate_result_layout(filtered_df):
    """Generates the result layout for filtered DataFrame."""
    result_layout = []
    for _, row in filtered_df.iterrows():
        result_layout.extend(_generate_result_for_row(row))
    return result_layout

def _generate_result_for_row(row):
    """Generates individual result row layout."""
    result_row = []

    # Title
    result_row.append(html.H3(row['titulo'], style={'color': '#2C3E50', 'border-bottom': '2px solid #E1BEE7', 'padding-bottom': '5px'}))

    # Display fields and clickable links
    for col in df.columns:
        if col != 'comentarios':
            result_row.extend(_generate_field_content(row, col))

    # Recommendation and comment links
    github_edit_link = f"https://github.com/cumbucadev/curadoria-coletiva/edit/main/curadoria_coletiva/{row['file_path']}"
    result_row.append(html.Div([
        html.A("Recommend", href=github_edit_link, target='_blank', style={'color': '#6A1B9A', 'margin-right': '10px', 'font-weight': 'bold'}),
        html.A("Comment", href=github_edit_link, target='_blank', style={'color': '#6A1B9A', 'font-weight': 'bold'})
    ], style={'margin-bottom': '15px'}))

    # Collapsible comments section
    result_row.append(_generate_collapsible_comments(row))

    return result_row

def _generate_field_content(row, col):
    """Generates content for each field in the result row."""
    field_content = []
    if col == 'url':
        field_content.append(html.P([
            html.Strong(f"{col.replace('_', ' ').capitalize()}: "),
            html.A(row[col], href=row[col], target='_blank', style={'color': '#3949AB', 'text-decoration': 'underline'})
        ]))
    elif col == 'recomendado_por' and row[col]:
        recomendado_usuario = str(row[col]).strip("[]'\"")  # Clean the 'recommended_by' string
        field_content.append(html.P([
            html.Strong("Recomendado por: "),
            html.A(f"@{recomendado_usuario}", href=f"https://github.com/{recomendado_usuario}", target='_blank', style={'color': '#8e44ad'})
        ]))
    else:
        field_content.append(html.P(f"{col.replace('_', ' ').capitalize()}: {row[col] or 'Not available'}"))
    return field_content

def _generate_collapsible_comments(row):
    """Generates the collapsible comments section."""
    comments_text = "".join([
        f"<p><b><a href='https://github.com/{comment['usuario']}' target='_blank' style='color: #8e44ad;'>@{comment['usuario']}</a>:</b> {comment['texto']}</p>"
        for comment in row['comentarios']
    ])
    return html.Details([
        html.Summary(f"Comments ({len(row['comentarios'])})", style={'cursor': 'pointer', 'font-weight': 'bold'}),
        dcc.Markdown(comments_text, dangerously_allow_html=True, style={
            'padding': '10px', 'background-color': '#F3E5F5', 'border-radius': '5px', 'white-space': 'pre-wrap'
        })
    ], style={'margin-bottom': '20px'})

# Callback to update the table based on filters
def _register_callbacks(app, df):
    """Registers the callback functions to handle updates on the app."""
    @app.callback(
        Output('results', 'children'),
        Input('search-box', 'value'),
        Input('category-dropdown', 'value'),
        Input('sort-dropdown', 'value')
    )
    def update_table(search_term, selected_category, sort_column):
        """Updates the table layout based on search, category, and sorting filters."""
        filtered_df = df

        # Apply search filter
        if search_term:
            filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        # Apply category filter
        if selected_category:
            filtered_df = filtered_df[filtered_df['assuntos'].apply(lambda x: selected_category in x)]

        # Apply sorting
        if sort_column:
            filtered_df = filtered_df.sort_values(by=sort_column)

        # Generate and return result layout
        return generate_result_layout(filtered_df)

# Load data and create DataFrame
data = _load_yaml_data(yaml_file_path)
df = _create_dataframe(data)

# Initialize and set up the app
app.layout = _create_layout(df)

# Expondo o servidor Flask subjacente para Gunicorn
server = app.server

# Register callbacks
_register_callbacks(app, df)

# Main entry point to start the Dash app
if __name__ == '__main__':
    # Run the server
    app.run_server()
