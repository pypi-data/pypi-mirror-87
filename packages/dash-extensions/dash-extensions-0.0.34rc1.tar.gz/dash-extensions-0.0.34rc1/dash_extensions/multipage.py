import dash_html_components as html

from dash.exceptions import PreventUpdate
from .enrich import Output, Input
from .Burger import Burger

URL_ID = "url"
CONTENT_ID = "content"


class Page:
    def __init__(self, id, label, module=None):
        self.id = id
        self.label = label
        self.module = module


class PageCollection:
    def __init__(self, pages, default_page=None, is_authorized=None, unauthorized=None):
        self.pages = pages
        self.is_authorized = is_authorized
        self.unauthorized = html.Div("Unauthorized.") if unauthorized is None else unauthorized
        self.default_page = default_page if default_page is not None else pages[0]

    def navigate_to(self, path):
        if path is None:
            raise PreventUpdate
        # Locate the page. Maybe make this more advanced later, for now just snap the id.
        page_ids = [page.id for page in self.pages]
        next_page = self.default_page
        if path is not None:
            page_id = path[1:]
            if page_id in page_ids:
                next_page = page_id
        # Check that the user is authorized.
        if self.is_authorized is not None:
            if not self.is_authorized(next_page):
                return self.unauthorized
        # At this point, the user is authorized, so the page can safely be rendered.
        return self.pages[page_ids.index(next_page)].module.layout()

    def register_navigation(self, app, content_id=CONTENT_ID, url_id=URL_ID):
        @app.callback(Output(content_id, "children"), [Input(url_id, "pathname")])
        def navigate_to(path):
            return self.navigate_to(path)

    def register_modules(self, app):
        for page in self.pages:
            if page.module is None:
                continue
            page.module.register(app)


def make_burger(pages, before_pages=None, after_pages=None, href=None, **kwargs):
    children = []
    for i, page in enumerate(pages):
        children.append(html.A(children=page.label, href=href(page) if href is not None else "/{}".format(page.id)))
        if i < (len(pages) - 1):
            children.append(html.Br())
    children = before_pages + children if before_pages is not None else children
    children = children + after_pages if after_pages is not None else children
    return Burger(children=children, **kwargs)
