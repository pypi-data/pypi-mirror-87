from html.parser import HTMLParser


class FormException(Exception):
    pass


class FormParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def error(self, message):
        raise Exception(message)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                raise FormException("Second form on page")
            if self.in_form:
                raise FormException("Already in form")
            self.in_form = True
        if not self.in_form:
            return
        attrs = {name.lower(): value for name, value in attrs}
        if tag == "form":
            if "action" in attrs:
                self.url = attrs["action"]
            if "method" in attrs:
                self.method = attrs["method"]
        elif tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise FormException("Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True
