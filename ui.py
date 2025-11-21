# ui.py
from pathlib import Path
from shiny import ui
from globals import FIELD_CHOICES

glossary_md = Path("glossary.md").read_text(encoding="utf-8")
faq_md = Path("faq.md").read_text(encoding="utf-8")

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Quote/Close Dashboard"),

        ui.input_radio_buttons(
            "page",
            "Navigation",
            choices={
                "selectFields": "Select Field(s)",
                "selectFilters": "Select Filter(s)",
                "exhibit": "Exhibit",
                "glossary": "Glossary",
                "faq": "FAQ",
            },
            selected="selectFields",
        ),
    ),
    ui.panel_title("Quote/Close Dashboard"),

    # --- Select Fields tab -------------------------------------------------
    ui.panel_conditional(
        "input.page === 'selectFields'",
        ui.card(
            ui.card_header("Select 1 or More Field(s)"),
            ui.input_select(
                "selectField1",
                "Select Field 1",
                choices=FIELD_CHOICES,
                selected="",
            ),
            ui.input_select(
                "selectField2",
                "Select Field 2",
                choices=FIELD_CHOICES,
                selected="",
            ),
            ui.input_select(
                "selectField3",
                "Select Field 3",
                choices=FIELD_CHOICES,
                selected="",
            ),
            ui.input_select(
                "selectField4",
                "Select Field 4",
                choices=FIELD_CHOICES,
                selected="",
            ),
        ),
    ),

    # --- Select Filters tab -----------------------------------------------
    ui.panel_conditional(
        "input.page === 'selectFilters'",
        ui.card(
            ui.card_header("Select Filter(s)"),

            ui.layout_column_wrap(
                2,
                # Filter 1
                ui.card(
                    ui.card_header("Filter 1"),
                    ui.input_select(
                        "filterField1",
                        "Field",
                        choices=FIELD_CHOICES,
                        selected="",
                    ),
                    ui.output_ui("filterWidget1"),
                    ui.input_checkbox(
                        "filterInclude1",
                        "Include matching rows (uncheck to exclude)",
                        value=True,
                    ),
                ),
                # Filter 2
                ui.card(
                    ui.card_header("Filter 2"),
                    ui.input_select(
                        "filterField2",
                        "Field",
                        choices=FIELD_CHOICES,
                        selected="",
                    ),
                    ui.output_ui("filterWidget2"),
                    ui.input_checkbox(
                        "filterInclude2",
                        "Include matching rows (uncheck to exclude)",
                        value=True,
                    ),
                ),
                # Filter 3
                ui.card(
                    ui.card_header("Filter 3"),
                    ui.input_select(
                        "filterField3",
                        "Field",
                        choices=FIELD_CHOICES,
                        selected="",
                    ),
                    ui.output_ui("filterWidget3"),
                    ui.input_checkbox(
                        "filterInclude3",
                        "Include matching rows (uncheck to exclude)",
                        value=True,
                    ),
                ),
                # Filter 4
                ui.card(
                    ui.card_header("Filter 4"),
                    ui.input_select(
                        "filterField4",
                        "Field",
                        choices=FIELD_CHOICES,
                        selected="",
                    ),
                    ui.output_ui("filterWidget4"),
                    ui.input_checkbox(
                        "filterInclude4",
                        "Include matching rows (uncheck to exclude)",
                        value=True,
                    ),
                ),
            ),
        ),
    ),

    # --- Exhibit tab -------------------------------------------------------
    ui.panel_conditional(
        "input.page === 'exhibit'",
        ui.card(
            ui.card_header("Exhibit"),
            ui.output_data_frame("exhibit_table"),
        ),
    ),

    # --- Glossary tab ------------------------------------------------------
    ui.panel_conditional(
        "input.page === 'glossary'",
        ui.card(
            ui.card_header("Glossary"),
            ui.markdown(glossary_md),
        ),
    ),

    # --- FAQ tab -----------------------------------------------------------
    ui.panel_conditional(
        "input.page === 'faq'",
        ui.card(
            ui.card_header("FAQ"),
            ui.markdown(faq_md),
        ),
    ),

    # --- Simple CSS "theme" tweaks ----------------------------------------
    ui.tags.style(
        """
        /* Overall body background */
        body {
            background-color: #ecf0f5;
        }

        /* Fake header bar (the blue strip with title) */
        .bslib-page-title {
            background-color: #3c8dbc;
            color: #fff;
            padding: 10px 15px;
            margin: 0 0 15px 0;
        }

        .bslib-page-title h1, 
        .bslib-page-title h2, 
        .bslib-page-title h3 {
            color: #fff;
            margin: 0;
            font-size: 20px;
            font-weight: 600;
        }

        /* Sidebar background & text (dashboards-style dark) */
        .bslib-page-sidebar .sidebar {
            background-color: #222d32;
            color: #b8c7ce;
        }

        .bslib-page-sidebar .sidebar h3 {
            color: #fff;
            font-weight: 600;
            margin-bottom: 15px;
        }

        /* Remove default card-like spacing in sidebar */
        .bslib-page-sidebar .sidebar .shiny-input-container {
            margin-bottom: 0;
        }

        /* Make radio buttons look like menu items */
        #page .form-check {
            margin: 0;
        }

        #page .form-check-input {
            display: none;             /* hide the radio circle */
        }

        #page .form-check-label {
            display: block;
            padding: 8px 15px;
            cursor: pointer;
            color: #b8c7ce;
            border-radius: 0;
        }

        #page .form-check-label:hover {
            background-color: #1e282c;
            color: #fff;
        }

        /* "Selected" menu item */
        #page .form-check-input:checked + .form-check-label {
            background-color: #1e282c;
            border-left: 3px solid #3c8dbc;
            color: #fff;
        }

        /* Main content cards closer to shinydashboard boxes */
        .card {
            border-radius: 0;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            border: 1px solid #d2d6de;
        }

        .card-header {
            background-color: #3c8dbc;
            color: #fff;
            font-weight: 600;
            padding: 8px 15px;
        }
        """
    ),
)
