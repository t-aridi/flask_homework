from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # Load the coffee export data from CSV
    df = pd.read_csv("coffee_exports.csv")

    # Get the selected chart type from the form (default is "box")
    chart_type = request.form.get("chart_type", "box")

    # Choose a chart based on user selection
    if chart_type == "bar":
        fig = px.bar(
            df,
            x="Country",
            y="Export_Value_USD",
            color="Region",
            title="Coffee Export Value by Country (USD)"
        )
    elif chart_type == "scatter":
        fig = px.scatter(
            df,
            x="Export_Tons",
            y="Export_Value_USD",
            color="Region",
            size="Export_Tons",
            hover_name="Country",
            title="Coffee Export Tons vs Value (USD)"
        )
    else:
        fig = px.box(
            df,
            x="Region",
            y="Export_Value_USD",
            color="Region",
            title="Coffee Export Value Distribution by Region"
        )

    # Apply a dark layout to the plot
    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')

    # Convert the Plotly figure to JSON for rendering in the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)


if __name__ == "__main__":
    app.run(debug=True)
