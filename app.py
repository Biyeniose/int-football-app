from src.classes.football_app import FootballApp  # Import the FootballApp class

# App factory function
def create_app():
    return FootballApp().app


# Main entry point for the application
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
