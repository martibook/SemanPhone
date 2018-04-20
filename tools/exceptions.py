class NoResults(Exception):
    render_page = "no_results.html"
    def __init__(self):
        Exception.__init__(self)
        pass

