# server.py
import numpy as np
import pandas as pd
from shiny import reactive, render, ui
from globals import quote_data, NUMERIC_FIELDS, FIELD_CHOICES

def server(input, output, session):

    # ----- Helper: build a filter widget for a field ----------------------
    def make_filter_widget(field_name: str, widget_id: str):
        # No field selected -> nothing to show
        if not field_name:
            return ui.p("No field selected.")

        # Numeric field -> range slider
        if field_name in NUMERIC_FIELDS:
            col = quote_data[field_name].dropna()
            if col.empty:
                return ui.p("No data available for this field.")

            # Check if this numeric field is actually integer-valued
            is_int = pd.api.types.is_integer_dtype(col)

            if is_int:
                min_val = int(col.min())
                max_val = int(col.max())
                return ui.input_slider(
                    widget_id,
                    f"Range for {field_name}",
                    min=min_val,
                    max=max_val,
                    value=(min_val, max_val),
                    step=1,          # <-- integer steps
                )
            else:
                min_val = float(col.min())
                max_val = float(col.max())
                return ui.input_slider(
                    widget_id,
                    f"Range for {field_name}",
                    min=min_val,
                    max=max_val,
                    value=(min_val, max_val),
                    # step left as default for continuous
                )

        # Categorical-like field -> multi-select (unchanged)
        col = quote_data[field_name].dropna().astype(str)
        unique_vals = sorted(col.unique().tolist())

        return ui.input_selectize(
            widget_id,
            f"Values for {field_name}",
            choices=unique_vals,
            selected=None,
            multiple=True,
        )

    # ----- Dynamic filter widgets -----------------------------------------
    @output
    @render.ui
    def filterWidget1():
        return make_filter_widget(input.filterField1(), "filterValue1")

    @output
    @render.ui
    def filterWidget2():
        return make_filter_widget(input.filterField2(), "filterValue2")

    @output
    @render.ui
    def filterWidget3():
        return make_filter_widget(input.filterField3(), "filterValue3")

    @output
    @render.ui
    def filterWidget4():
        return make_filter_widget(input.filterField4(), "filterValue4")

    # ----- Helper: apply one filter to a DataFrame ------------------------
    def apply_filter(df: pd.DataFrame, field: str, value_input_name: str, include_input_name: str) -> pd.DataFrame:
        if not field:
            return df

        include = getattr(input, include_input_name)()

        # Numeric filter
        if field in NUMERIC_FIELDS:
            rng = getattr(input, value_input_name)()
            if rng is None:
                return df
            lo, hi = rng[0], rng[1]
            mask = df[field].between(lo, hi)

        # Categorical filter
        else:
            vals = getattr(input, value_input_name)()
            if not vals:
                # If nothing selected, treat as "no filter"
                return df
            vals = [str(v) for v in vals]
            mask = df[field].astype(str).isin(vals)

        # Include vs exclude
        if not include:
            mask = ~mask

        return df[mask]

    # ----- Main reactive: filtered + grouped data -------------------------
    @reactive.Calc
    def selected_data() -> pd.DataFrame:
        df = quote_data

        # 1) Apply filters (if any) -------------------------------------------
        df = apply_filter(df, input.filterField1(), "filterValue1", "filterInclude1")
        df = apply_filter(df, input.filterField2(), "filterValue2", "filterInclude2")
        df = apply_filter(df, input.filterField3(), "filterValue3", "filterInclude3")
        df = apply_filter(df, input.filterField4(), "filterValue4", "filterInclude4")

        # 2) Group by selected fields -----------------------------------------
        f1 = input.selectField1()
        f2 = input.selectField2()
        f3 = input.selectField3()
        f4 = input.selectField4()

        group_fields = [f for f in [f1, f2, f3, f4] if f]

        # If no fields: fall back to quote_id-level detail
        if len(group_fields) == 0:
            group_fields = ["quote_id"]

        def sale_count_func(ids: pd.Series) -> int:
            # ids is the quote_id column for this group
            issued_mask = df.loc[ids.index, "issued"] == "Y"
            return ids[issued_mask].nunique()

        grouped = (
            df.groupby(group_fields, dropna=False)
            .agg(
                quote_count=("quote_id", "nunique"),
                sale_count=("quote_id", sale_count_func),
            )
            .reset_index()
        )

        grouped["close_rate"] = np.where(
            grouped["quote_count"] == 0,
            0.0,
            grouped["sale_count"] / grouped["quote_count"],
        )

        # 3) Rename grouping columns to display labels ------------------------
        display_name_map = {
            field: FIELD_CHOICES.get(field, field)
            for field in group_fields
        }
        grouped = grouped.rename(columns=display_name_map)

        # 4) Create nicely formatted summary columns --------------------------
        # Quote Count and Sale Count as integers with commas
        grouped["Quote Count"] = grouped["quote_count"].map(
            lambda x: f"{int(x):,}" if pd.notna(x) else ""
        )
        grouped["Sale Count"] = grouped["sale_count"].map(
            lambda x: f"{int(x):,}" if pd.notna(x) else ""
        )

        # Close Rate as percentage with 1 decimal place
        grouped["Close Rate"] = grouped["close_rate"].map(
            lambda x: f"{round(float(x) * 100, 1):,.1f}%" if pd.notna(x) else ""
        )

        # 5) Drop the raw numeric columns (optional – keeps the table clean) ---
        grouped = grouped.drop(columns=["quote_count", "sale_count", "close_rate"])

        return grouped

    # ----- Exhibit table --------------------------------------------------
    @output
    @render.data_frame
    def exhibit_table():
        return render.DataTable(
            selected_data(),
            summary=True,
            filters=False,
            height="500px",
            width="fit-content",
        )
