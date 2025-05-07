import json
import plotly.express as px

def build_charts(groq_output):
    charts = []

    try:
        chart_data = json.loads(groq_output)
    except json.JSONDecodeError:
        return ["<p><b>Error:</b> Groq returned invalid JSON. Please try again.</p>"]

    for i, chart in enumerate(chart_data):
        try:
            chart_type = chart.get("type", "").lower()
            title = chart.get("title", f"Chart {i+1}")
            x = chart.get("x", [])
            y = chart.get("y", [])

            if chart_type == "bar":
                fig = px.bar(x=x, y=y, title=title)
            elif chart_type == "line":
                fig = px.line(x=x, y=y, title=title)
            elif chart_type == "pie":
                fig = px.pie(names=x, values=y, title=title)
            else:
                charts.append(f"<p><b>Unsupported chart type:</b> {chart_type}</p>")
                continue

            charts.append(fig.to_html(full_html=False))

        except Exception as e:
            charts.append(f"<p><b>Chart rendering error:</b> {str(e)}</p>")

    if not charts:
        charts.append("<p><b>No valid charts generated.</b></p>")

    return charts
