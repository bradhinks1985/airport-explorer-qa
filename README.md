# Airport Explorer — QA Automation Portfolio Project

A Flask-based airport and city information web application developed as a personal
QA automation portfolio project.

The project demonstrates software testing across multiple levels, including
API, database, integration, UI, and end-to-end testing using Python, pytest,
and Playwright.


## Project Overview

The featured Airport Explorer app page is the Airport Info page. It allows users to view information about the selected airport.
The application integrates several data sources and services, including:

- SQLite airport database
- Wikipedia API
- OpenAI API
- Aviation Weather API
- Airport route, airlines, and destinations data
- External map and search links

The primary focus of this project is demonstrating an automated testing strategy for a web application.


## QA & Test Automation

The automated test suite covers multiple testing levels:

Test Level - Purpose: 
- API: Validate internal and external API behavior 
- Database: Validate airport data stored in SQLite 
- Integration: Verify communication between application components 
- UI: Validate individual user interface functionality 
- E2E: Validate complete user workflows 
- Exploratory: Manual testing of scenarios that are difficult to automate 


### Testing Techniques

Positive testing
Negative testing
Equivalence partitioning
State transition testing
Exploratory testing


## Test Automation Tools

Python 
pytest 
Playwright
Flask test client 
SQLite 


## Test Structure

tests/

api/
    test_airports_api.py
    test_wikipedia_api.py

database/
    test_airport_database.py

e2e/
    test_airport_info_e2e.py

integration/
    test_airport_ai_summary.py
    test_airport_info_database.py
    
ui/
    test_airlines_destinations.py
    test_airport_ai_summary.py
    test_airport_filters.py
    test_airport_information.py
    test_airport_on_map.py
    test_domestic_routes.py
    test_international_routes.py


## Test Documentation

Additional QA documentation is located in the docs/ directory.

docs/
    test-plan.md
    test-cases.md


## Running the Application
1. Clone the repository
git clone https://bradhinks1985/airport-explorer-qa.git
cd airport-explorer-qa

2. Create a virtual environment
Windows:
python -m venv venv
Activate it:
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Create a .env file in the project root and add the required API
configuration.
Do not commit .env or API keys to GitHub.

5. Start the Flask application
python app.py
The application will be available locally at:
http://127.0.0.1:5000


## Running the Tests

Run the complete automated test suite:
python -m pytest -v

Run a specific test directory:
python -m pytest -v tests/api/

Run a specific test file:
python -m pytest -v tests/ui/test_airport_information.py

Run an individual test:
python -m pytest -v tests/ui/test_airport_information.py::test_valid_airport
Test Environment
Python 3.14
Windows
Flask
SQLite
pytest
Playwright
Chromium

The application and automated tests are designed to run locally.


## External Dependencies

The application uses external services including:

Wikipedia API
OpenAI API


## Project Goals

This project was created to demonstrate practical QA automation skills,
including:

Test planning
Test case design
Automated testing
API testing
Database testing
Integration testing
End-to-end testing
Negative testing
Page Object Model design


## Author

Brad Hinks
QA / Business Analyst transitioning toward QA Automation.
This project represents a personal portfolio project demonstrating practical
software testing and test automation skills.
