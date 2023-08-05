from importlib import resources
from typing import List, Tuple
import json

from py3js.infra import Chart


class WordCloud(Chart):
    def __init__(self,
                 words: List[Tuple[str, int]],
                 width: int = 800, height: int = 600):
        self._words = words
        Chart.__init__(self, width, height)
        self._html = resources.read_text("py3js", "wordcloud.html")
        self._html = (self
                      ._html
                      .replace("$width", str(width))
                      .replace("$height", str(height)))

    def _render_data(self):
        data = [{
            "text": x[0],
            "value": x[1]
        } for x in self._words]

        data_json = json.dumps(data)

        r = (self._html
             .replace("$data", data_json))

        return r
