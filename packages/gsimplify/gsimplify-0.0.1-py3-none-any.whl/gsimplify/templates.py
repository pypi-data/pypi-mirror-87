from jinja2 import Environment, FileSystemLoader, Template, select_autoescape


class Templates:
    def __init__(self, templates_dir=""):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def get(self, template: str) -> Template:
        return self.env.get_template(template)
