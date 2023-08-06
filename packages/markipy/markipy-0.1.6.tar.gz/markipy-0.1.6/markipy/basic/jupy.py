from IPython.display import display, HTML

from .atom import  Atom


class Jupy(Atom):
    def __init__(self):
        Atom.__init__(self, "Jupy", "0.1")

    @staticmethod
    def create_tag(tag, content):
        return f"<{tag}>{content}</{tag}>"

    @staticmethod
    def html_list(data):
        for x in data:
            if x is not None:
                display(HTML(Jupy.create_tag("b", x)))

    @staticmethod
    def enlarge_jupyter_Notebook(width_percentage: int):
        display(HTML(f"<style>.container {{ width:{width_percentage}% !important; }}</style>"))
