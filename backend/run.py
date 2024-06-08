from app import create_app
import logging

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # Run the Flask application
    app.run(debug=False, host='0.0.0.0', port=5000)
