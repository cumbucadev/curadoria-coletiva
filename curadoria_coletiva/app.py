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
            html.A(
                "Colabore Já! Recomende Materiais 🤓 📚",
                href="https://github.com/cumbucadev/curadoria-coletiva",
                target="_blank",
                style={
                    "display": "block",
                    "text-align": "center",
                    "color": "#6A1B9A",
                    "font-weight": "bold",
                    "margin-bottom": "30px",
                    "font-size": "18px",
                },
            ),
            html.H6(
                "Busca",
                style={
                    "margin-bottom": "20px",
                    "font-weight": "bold",
                },
            ),
            _create_search_box(),
            html.H6(
                "Filtros de Pesquisa",
                style={
                    "margin-bottom": "20px",
                    "font-weight": "bold",
                },
            ),
            _create_filter_dropdowns(df),
            html.Div(
                id="results-section",
                style={"margin-top": "30px"},
                children=[
                    html.H2(
                        id="results-section-title",
                        children="Resultados",
                        style={
                            "color": "#8B008B",
                            "margin-bottom": "20px",
                        },
                    ),
                    html.Div(id="results"),
                ]
            ),
            _create_footer()
        ],
    )


def _create_logo_section():
    return html.Div(
        style={"text-align": "center"},
        children=[
            html.A(
                href="https://cumbuca.dev",  # Link para a Cumbuca Dev
                target="_blank",  # Abre o link em uma nova aba
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
                    "display": "flex",
                    "flex-wrap": "wrap",
                    "width": "100%",
                    "gap": "10px",
                    "margin-bottom": "20px",
                    "border": "2px solid #E1BEE7",  # Cor da borda mais suave
                    "border-radius": "10px",  # Borda arredondada
                    "padding": "10px",  # Adiciona algum espaçamento interno
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Sombra suave para dar profundidade
                    "background-color": "#F9F9F9",  # Cor de fundo clara
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
            "border": "2px solid #E1BEE7",  # Cor da borda mais suave
            "border-radius": "10px",  # Borda arredondada
            "padding": "10px",  # Adiciona algum espaçamento interno
            "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Sombra suave para dar profundidade
            "background-color": "#F9F9F9",  # Cor de fundo clara
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
                id="level-dropdown",
                options=[
                    {"label": i, "value": i} for i in sorted(df["nivel_dificuldade"].unique())
                ],
                multi=True,
                placeholder="Dificuldade",
                style={"width": "100%"},
            ),
            dcc.Checklist(
                id="free-filter",
                options=[
                    {"label": " É gratuito", "value": "gratuito"}
                ],
                value=[],
                style={"width": "100%", "margin-top": "10px"},
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

def _create_footer():
    return html.Footer(
        style={
            "padding": "20px",
            "text-align": "center",
            "border-top": "1px solid #ddd",
        },
        children=[
            html.Div(
                style={"margin-bottom": "10px"},
                children=[
                    html.H4("Siga a Cumbuca Dev nas redes sociais"),
                ]
            ),
            html.Div(
                children=[
                    # GitHub
                    html.A(
                        href="https://github.com/cumbucadev",
                        target="_blank",
                        children=[
                            html.Img(
                                src="/assets/icons8-github-50.png",  # Logo do GitHub local
                                alt="GitHub",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                    # Instagram
                    html.A(
                        href="https://www.instagram.com/cumbucadev",
                        target="_blank",
                        children=[
                            html.Img(
                                src="/assets/icons8-instagram-48.png",  # Logo do Instagram local
                                alt="Instagram",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                    # Twitter
                    html.A(
                        href="https://twitter.com/cumbucadev",
                        target="_blank",
                        children=[
                            html.Img(
                                src="/assets/icons8-twitterx-48.png",  # Logo do Twitter local
                                alt="Twitter",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                    # YouTube
                    html.A(
                        href="https://www.youtube.com/cumbucadev",
                        target="_blank",
                        children=[
                            html.Img(
                                src="/assets/icons8-youtube-48.png",  # Logo do YouTube local
                                alt="YouTube",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                    # LinkedIn
                    html.A(
                        href="https://www.linkedin.com/company/cumbucadev",
                        target="_blank",
                        children=[
                            html.Img(
                                src="/assets/icons8-linkedin-48.png",  # Logo do LinkedIn local
                                alt="LinkedIn",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                    # Email
                    html.A(
                        href="mailto:cumbucadev@gmail.com",
                        children=[
                            html.Img(
                                src="/assets/icons8-email-50.png",  # Ícone de Email local
                                alt="Email",
                                style={"width": "30px", "height": "30px", "margin": "0 10px"}
                            )
                        ]
                    ),
                ],
            ),
            html.Div(
                style={"margin-top": "10px", "font-size": "12px", "color": "#777"},
                children=[
                    "© 2024 Cumbuca Dev - Todos os direitos reservados."
                ]
            ),
        ],
    )



def generate_result_layout(filtered_df):
    result_layout = []
    for _, row in filtered_df.iterrows():
        result_layout.append(
            html.Div(
                _generate_result_for_row(row),
                style={
                    "border": "2px solid #E1BEE7",  # Cor da borda
                    "border-radius": "10px",  # Borda arredondada
                    "padding": "15px",  # Espaçamento interno
                    "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)",  # Sombra para profundidade
                    "background-color": "#F9F9F9",  # Cor de fundo
                    "margin-bottom": "20px",  # Espaçamento entre os resultados
                }
            )
        )

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
                    html.Span(f"{col.replace('_', ' ').capitalize()}: "),
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
                    html.Span("Recomendado por: "),
                    html.A(
                        f"@{recomendado_usuario}",
                        href=f"https://github.com/{recomendado_usuario}",
                        target="_blank",
                        style={"color": "#8e44ad"},
                    ),
                ]
            )
        )
    elif col == "eh_gratuito":
        field_content.append(
            html.P(
                f"{col.replace('_', ' ').capitalize()}: {'sim' if row[col] else 'não'}"
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
        [Output("results", "children"), Output("results-section-title", "children")],
        Input("search-box", "value"),
        Input("subject-dropdown", "value"),
        Input("format-dropdown", "value"),
        Input("learning-style-dropdown", "value"),
        Input("language-dropdown", "value"),
        Input("level-dropdown", "value"),
        Input("free-filter", "value"),
        Input("sort-dropdown", "value"),
    )
    def update_table(
        search_term,
        selected_subject,
        selected_format,
        selected_learning_style,
        selected_language,
        selected_level,
        free_filter,
        sort_column,
    ):
        """Atualiza a tabela e o título com a contagem de resultados com base nos filtros."""
        filtered_df = df

        # Aplicar os filtros
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
            filtered_df = filtered_df[filtered_df["estilo_aprendizagem"].isin(selected_learning_style)]

        if selected_language:
            filtered_df = filtered_df[filtered_df["idioma"].isin(selected_language)]

        if selected_level:
            filtered_df = filtered_df[filtered_df["nivel_dificuldade"].isin(selected_level)]

        if free_filter:
            filtered_df = filtered_df[filtered_df["eh_gratuito"] == True]

        # Aplicar ordenação se selecionada
        if sort_column:
            filtered_df = filtered_df.sort_values(by=sort_column)

        # Contagem de resultados
        result_count = len(filtered_df)
        result_title = f"Resultados ({result_count})"

        # Layout dos resultados
        result_layout = generate_result_layout(filtered_df)

        return result_layout, result_title


data = _load_yaml_data(yaml_file_path)
df = _create_dataframe(data)

app.layout = _create_layout(df)
server = app.server
_register_callbacks(app, df)

if __name__ == "__main__":
    app.run_server(debug=True)
