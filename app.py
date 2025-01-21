from flask import Flask, render_template, request
import sqlite3
import os
import pandas as pd


class FootballApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.after_request(self.add_cache_control_headers)  # Add caching headers for static files
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/sql", view_func=self.sql_queries)
        self.app.add_url_rule("/trends", view_func=self.trends)
        self.app.add_url_rule(
            "/execute-query", view_func=self.execute_query, methods=["POST"]
        )

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
        if request.path.startswith("/static/"):  # Apply only to static files
            response.headers["Cache-Control"] = "public, max-age=31536000"  # Cache for 1 year
        return response

    def check_and_create_tables(self):
        """
        Check if tables exist in the SQLite database.
        If not, read the corresponding CSV files and create the tables.
        """
        db_path = "database.db"
        data_folder = "data"
        tables = ["goalscorers", "results", "shootouts"]

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for table in tables:
            # Check if the table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,)
            )
            table_exists = cursor.fetchone()

            if not table_exists:
                # If the table doesn't exist, look for the corresponding CSV file
                csv_file = os.path.join(data_folder, f"{table}.csv")
                if os.path.exists(csv_file):
                    # Read the CSV file and create the table
                    df = pd.read_csv(csv_file)
                    df.to_sql(table, conn, index=False, if_exists="replace")
                    print(f"Table '{table}' created from '{csv_file}'.")
                else:
                    print(f"CSV file '{csv_file}' not found. Cannot create table '{table}'.")

        conn.close()

    def execute_query(self):
        """
        Execute the SQL query submitted by the user.
        """
        # Ensure required tables exist
        self.check_and_create_tables()

        # Get the SQL query from the form
        query = request.form.get("query")

        try:
            # Connect to SQLite database
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Extract column names
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Format results as a list of dicts

            conn.close()
            return render_template("sql_queries.html", results=results)

        except Exception as e:
            # Handle query errors
            error_message = f"Error: {str(e)}"
            return render_template("sql_queries.html", error=error_message)


# App factory function
def create_app():
    return FootballApp().app


# Main entry point for the application
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
