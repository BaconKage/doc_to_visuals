import json

def build_charts(response_text):
    """
    Cleans and ensures the raw LLM output is a valid JSON string for chart rendering.
    """
    try:
        charts = json.loads(response_text)
        if isinstance(charts, list):
            # Optionally validate that all required fields exist
            for chart in charts:
                if not all(k in chart for k in ("type", "title", "x", "y")):
                    raise ValueError("Missing required keys in chart object.")
            return json.dumps(charts)
        else:
            raise ValueError("Response is not a list.")
    except Exception as e:
        print("Error building charts:", e)
        return json.dumps([])
