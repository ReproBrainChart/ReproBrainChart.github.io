"""Create a dashboard showing clone statistics over time."""

import os

import pandas as pd
from bokeh.layouts import Spacer, column, row
from bokeh.models import ColumnDataSource, CustomJS, DatetimeTickFormatter, Select
from bokeh.plotting import curdoc, figure, output_file, show


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    stats_dir = os.path.join(script_dir, "../../_data/clone-tracking")

    out_file = os.path.abspath(os.path.join(script_dir, "../../assets/dashboard.html"))
    output_file(out_file)

    df = pd.read_csv(
        os.path.abspath(
            os.path.join(
                script_dir,
                "../../_data/clone-tracking/cumulative/all_repos_cumulative.csv",
            ),
        ),
    )
    df["date"] = pd.to_datetime(df["date"])
    repos = [col for col in df.columns if col != "date"]

    # dropdown menu
    select = Select(title="Repository", value="Overall", options=repos)

    def get_data(source_data, repo):
        df = source_data[["date", repo]]
        df.rename(columns={repo: "stats"}, inplace=True)
        return df

    render_cds = ColumnDataSource({"date": df["date"], "stats": df["Overall"]})
    cds = ColumnDataSource(df)

    curdoc().theme = "light_minimal"

    # plot
    p = figure(width=600, height=500, x_axis_type="datetime", toolbar_location="above")
    p.circle(
        x="date",
        y="stats",
        source=render_cds,
        size=3,
        line_width=2,
        line_color="#2c79de",
        fill_color="#2c79de",
    )
    line = p.line(x="date", y="stats", source=render_cds, color="#2c79de")
    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d %Y")
    p.title.text = "Cumulative downloads"

    # callbacks
    callback = CustomJS(
        args=dict(render_cds=render_cds, cds=cds, select=select),
        code="""
        render_cds.data["stats"] = cds.data[select.value];
        render_cds.change.emit();
    """,
    )

    select.js_on_change("value", callback)

    show(row(p, Spacer(width=15), column(Spacer(height=200), select)))
