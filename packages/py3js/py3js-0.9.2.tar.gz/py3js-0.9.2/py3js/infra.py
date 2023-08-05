import base64


class Chart:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def _render_data(self):
        return f"{self._width}x{self._height}";

    def _repr_html_(self):
        data = self._render_data()
        b64data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        url = f"data:text/html;charset=utf-8;base64,{b64data}"
        return f"<iframe src=\"{url}\" width=\"{self._width}\" height=\"{self._height}\" scrolling=\"no\" style=\"border:none !important;\"></iframe>"

    def save(self, path: str):
        with open(path, "w") as writer:
            writer.write(self._render_data())
