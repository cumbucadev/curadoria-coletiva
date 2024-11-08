import dash
from dash import dcc, html, Input, Output
import pandas as pd
import yaml

from curadoria_coletiva.collect_materials import collect_materials

materials_path = "curadoria_coletiva/materials"
yaml_file_path = "curadoria_coletiva/all_materials.yml"

collect_materials(materials_path, yaml_file_path)

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    ],
)
app.title = "Curadoria Coletiva"


def _load_yaml_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def _create_dataframe(data):
    return pd.DataFrame(data)


def _create_layout(df):
    """Creates the layout for the Dash app."""
    return html.Div(
        style={
            "font-family": "Arial, sans-serif",
            "padding": "20px",
        },
        children=[
            _create_logo_section(),
            html.H1(
                "Curadoria Coletiva",
                style={
                    "color": "#8B008B",
                    "text-align": "center",
                    "margin-bottom": "30px",
                },
            ),
            _create_search_box(),
            _create_filter_dropdowns(df),
            html.Div(id="results", style={"margin-top": "30px"}),
        ],
    )


def _create_logo_section():
    return html.Div(
        style={"text-align": "center"},
        children=[
            html.Picture(
                children=[
                    html.Source(
                        media="(prefers-color-scheme: dark)",
                        srcSet="https://github.com/cumbucadev/design/raw/main/images/logo-dark-transparent.png",
                    ),
                    html.Img(
                        alt="Cumbuca Dev Logo",
                        src="https://github.com/cumbucadev/design/raw/main/images/logo-light-transparent.png",
                        style={
                            "width": "15vw",  # O logo será 15% da largura da tela
                            "max-width": "200px",  # Tamanho máximo
                        },
                    ),
                ]
            ),
        ],
    )


def _create_search_box():
    return html.Div(
        [
            dcc.Input(
                id="search-box",
                type="text",
                placeholder="Digite para buscar...",
                style={
                    "width": "100%",
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "border-radius": "5px",
                },
            ),
        ],
        style={"margin-bottom": "20px"},
    )


def _create_filter_dropdowns(df):
    """Creates the dropdowns for subject, format, and sorting filters."""
    return html.Div(
        style={
            "display": "flex",
            "flex-wrap": "wrap",
            "gap": "10px",
            "margin-bottom": "20px",
        },
        children=[
            dcc.Dropdown(
                id="subject-dropdown",
                options=[
                    {"label": i, "value": i}
                    for i in sorted(df["assuntos"].explode().unique().tolist())
                ],
                placeholder="Assunto",
                style={"width": "100%"},
                multi=True,
            ),
            dcc.Dropdown(
                id="format-dropdown",
                options=[
                    {"label": i, "value": i} for i in sorted(df["formato"].unique())
                ],
                placeholder="Formato",
                style={"width": "100%"},
                multi=True,
            ),
            dcc.Dropdown(
                id="learning-style-dropdown",
                options=[
                    {"label": i, "value": i} for i in sorted(df["estilo_aprendizagem"].unique())
                ],
                multi=True,
                placeholder="Estilo de aprendizagem",
                style={"width": "100%"},
            ),
            dcc.Dropdown(
                id="language-dropdown",
                options=[
                    {"label": i, "value": i} for i in sorted(df["idioma"].unique())
                ],
                multi=True,
                placeholder="Idioma",
                style={"width": "100%"},
            ),
            dcc.Dropdown(
                id="sort-dropdown",
                options=[
                    {"label": col.replace("_", " ").capitalize(), "value": col}
                    for col in df.columns
                    if col not in ["file_path", "url"]
                ],
                placeholder="Ordenar por",
                style={"width": "100%"},
            ),
        ],
    )


def generate_result_layout(filtered_df):
    result_layout = []
    for _, row in filtered_df.iterrows():
        result_layout.extend(_generate_result_for_row(row))
    return result_layout


def _generate_result_for_row(row):
    result_row = []

    result_row.append(
        html.H3(
            row["titulo"],
            style={
                "color": "#2C3E50",
                "border-bottom": "2px solid #E1BEE7",
                "padding-bottom": "5px",
            },
        )
    )

    for col in df.columns:
        if col != "comentarios" and col != "file_path":
            result_row.extend(_generate_field_content(row, col))

    github_edit_link = f"https://github.com/cumbucadev/curadoria-coletiva/edit/main/curadoria-coletiva/{row['file_path']}"
    result_row.append(
        html.Div(
            [
                html.A(
                    "Recommend",
                    href=github_edit_link,
                    target="_blank",
                    style={
                        "color": "#6A1B9A",
                        "margin-right": "10px",
                        "font-weight": "bold",
                    },
                ),
                html.A(
                    "Comment",
                    href=github_edit_link,
                    target="_blank",
                    style={"color": "#6A1B9A", "font-weight": "bold"},
                ),
            ],
            style={"margin-bottom": "15px"},
        )
    )

    result_row.append(_generate_collapsible_comments(row))

    return result_row


def _generate_field_content(row, col):
    field_content = []
    if col == "url":
        field_content.append(
            html.P(
                [
                    html.Strong(f"{col.replace('_', ' ').capitalize()}: "),
                    html.A(
                        row[col],
                        href=row[col],
                        target="_blank",
                        style={"color": "#3949AB", "text-decoration": "underline"},
                    ),
                ]
            )
        )
    elif col == "recomendado_por" and row[col]:
        recomendado_usuario = str(row[col]).strip("[]'\"")
        field_content.append(
            html.P(
                [
                    html.Strong("Recomendado por: "),
                    html.A(
                        f"@{recomendado_usuario}",
                        href=f"https://github.com/{recomendado_usuario}",
                        target="_blank",
                        style={"color": "#8e44ad"},
                    ),
                ]
            )
        )
    else:
        field_content.append(
            html.P(
                f"{col.replace('_', ' ').capitalize()}: {row[col] or 'Not available'}"
            )
        )
    return field_content


def _generate_collapsible_comments(row):
    comments_text = "".join(
        [
            f"<p><b><a href='https://github.com/{comment['usuario']}' target='_blank' style='color: #8e44ad;'>@{comment['usuario']}</a>:</b> {comment['texto']}</p>"
            for comment in row["comentarios"]
        ]
    )
    return html.Details(
        [
            html.Summary(
                f"Comments ({len(row['comentarios'])})",
                style={"cursor": "pointer", "font-weight": "bold"},
            ),
            dcc.Markdown(
                comments_text,
                dangerously_allow_html=True,
                style={
                    "padding": "10px",
                    "background-color": "#F3E5F5",
                    "border-radius": "5px",
                    "white-space": "pre-wrap",
                },
            ),
        ],
        style={"margin-bottom": "20px"},
    )


def _register_callbacks(app, df):
    @app.callback(
        Output("results", "children"),
        Input("search-box", "value"),
        Input("subject-dropdown", "value"),
        Input("format-dropdown", "value"),
        Input("learning-style-dropdown", "value"),
        Input("language-dropdown", "value"),
        Input("sort-dropdown", "value"),
    )
    def update_table(
        search_term,
        selected_subject,
        selected_format,
        selected_learning_style,
        selected_language,
        sort_column,
    ):
        """Atualiza a tabela com base nos filtros de busca, assunto, formato, estilo de aprendizagem e ordenação."""
        filtered_df = df

        if search_term:
            filtered_df = filtered_df[
                filtered_df.apply(
                    lambda row: row.astype(str)
                    .str.contains(search_term, case=False)
                    .any(),
                    axis=1,
                )
            ]

        if selected_subject:
            filtered_df = filtered_df[
                filtered_df["assuntos"].apply(
                    lambda x: all(cat in x for cat in selected_subject)
                )
            ]

        if selected_format:
            filtered_df = filtered_df[filtered_df["formato"].isin(selected_format)]

        if selected_learning_style:
            filtered_df = filtered_df[
                filtered_df["estilo_aprendizagem"].isin(selected_learning_style)
            ]

        if selected_language:
            filtered_df = filtered_df[
                filtered_df["idioma"].isin(selected_language)
            ]

        if sort_column:
            filtered_df = filtered_df.sort_values(by=sort_column)

        if not filtered_df.empty:
            return generate_result_layout(filtered_df)
        else:
            return html.Div(
                "Nenhum resultado encontrado.",
                style={"color": "red", "text-align": "center", "margin-top": "20px"},
            )


data = _load_yaml_data(yaml_file_path)
df = _create_dataframe(data)

app.layout = _create_layout(df)
server = app.server
_register_callbacks(app, df)

if __name__ == "__main__":
    app.run_server(debug=True)
