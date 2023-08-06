from urllib.parse import urljoin

import requests
from bokeh.embed import json_item
from bokeh.models import Plot


def upload_bokeh_plot(plot: Plot, api_base: str = "https://api.plot.gallery"):
    upload = {"plot_json": json_item(plot)}
    resp = requests.post(urljoin(api_base, "v1/plots/"), json=upload)
    result = resp.json()
    return f"https://plot.gallery/plot/{result['id']}"
