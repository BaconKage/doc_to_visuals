
import json
import plotly.express as px

def build_charts(groq_output):
    charts = []
    try:
        chart_data = json.loads(groq_output)
    except json.JSONDecodeError:
        return ["<p>Error: Groq returned invalid JSON.</p>"]

    for chart in chart_data:
        try:
            if chart['type'] == 'bar':
                fig = px.bar(x=chart['x'], y=chart['y'], title=chart['title'])
            elif chart['type'] == 'line':
                fig = px.line(x=chart['x'], y=chart['y'], title=chart['title'])
            elif chart['type'] == 'pie':
                fig = px.pie(names=chart['x'], values=chart['y'], title=chart['title'])
            else:
                continue
            charts.append(fig.to_html(full_html=False))
        except Exception as e:
            charts.append(f"<p>Chart render error: {str(e)}</p>")
    return charts
