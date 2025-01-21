from flask import Flask, render_template, request

class FootballApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.after_request(self.add_cache_control_headers)  # Add caching headers for static files
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/sql", view_func=self.sql_queries)
        self.app.add_url_rule("/trends", view_func=self.trends)

    def home(self):
        return render_template("index.html")

    def sql_queries(self):
        return render_template("sql_queries.html")

    def trends(self):
        players = ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappe"]
        return render_template("trends.html", players=players)

    def add_cache_control_headers(self, response):
        """
        Add Cache-Control headers for static files.
        """
        if request.path.startswith('/static/'):  # Apply only to static files
            response.headers['Cache-Control'] = 'public, max-age=31536000'  # Cache for 1 year
        return response


# App factory function
def create_app():
    return FootballApp().app


# Main entry point for the application
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
