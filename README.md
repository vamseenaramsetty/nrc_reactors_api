
# NRC Reactors Data API

The NRC Reactors Data API is a Python-based API that provides access to information about nuclear reactors in the United States. It ingests data from the United States Nuclear Regulatory Commission (NRC) and makes it accessible through a set of API endpoints.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Retrieve all reactors](#1-retrieve-all-reactors)
  - [Retrieve reactor details](#2-retrieve-reactor-details)
  - [List reactors on outage](#3-list-reactors-on-outage)
  - [Get the last outage date](#4-get-the-last-outage-date)
- [Usage Examples](#usage-examples)
- [Testing with Swagger](#testing-with-swagger)
- [Code Documentation](#code-documentation)

## Getting Started

### Prerequisites

To run the NRC Reactors Data API, ensure you have the following prerequisites installed:

- Python 3
- SQLite
- Flask
- BeautifulSoup (for web scraping)
- Requests (for HTTP requests)
- flask_swagger_ui

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vamseenaramsetty/nrc_reactors_api.git
   cd nrc_reactors_api
   ```

   
## Setting Up the Environment

To run the NRC Reactors Data API, follow these steps:

1. **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

2. **Change to the project directory:**

    ```bash
    cd nrc_reactors_api
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask application:**

    ```bash
    python app.py
    ```

    The API will be accessible at [http://localhost:5000](http://localhost:5000).



## API Endpoints
   
The API provides the following endpoints:

Retrieve all reactors with an optional filter by state.
```
GET /reactors/
GET /reactors?state=<state>
```

Retrieve reactor details by plant name.
```
GET /reactors/plant_name/<plant_name>
```
List all reactors that are on outage for a given date range.

```
GET /reactors/on-outage/<start_date_end_date>
```
Get the last known outage date of a specific reactor by its unit.
```
GET /reactors/last-outage-date/<unit>
```


**Usage Examples**

Example 1: Retrieve all reactors

```
curl http://localhost:5000/reactors
```
Example 2: Retrieve reactors in the state of California
```
curl http://localhost:5000/reactors?state=CA
```
Example 3: Retrieve details about the reactor with the plant name "Callaway"
```
curl http://localhost:5000/reactors/plant_name/Callaway
```
Example 4: List reactors on outage between `January 1, 2023`, and `January 31, 2023`
```
curl http://localhost:5000/reactors/on-outage/01-01-2023_01-31-2023
```

Example 5: List the details of all endpoints available
```
curl http://localhost:5000/
```

Example 6: Test the API using swagger
```
curl http://127.0.0.1:5000/swagger/
```

### Testing with Swagger
The URL http://127.0.0.1:5000/swagger/ can be used to test the different end points. Select the endpoint which is to be tested, then click on 'Try It Out' and
give the necessary parameters. Click on 'Execute'. The result will be loaded on the screen.


### Code Documentation

**Functions**:

1. `create_table()`
   - Description: Creates the SQLite database table named "reactors" with columns for various reactor details.
   - Usage: Initializes the database structure.
   
2. `get_reactor_status_data()`
   - Description: Fetches reactor status data from a specified URL.
   - Usage: Retrieves the data source for reactor status.

3. `create_reactor_status_table()`
   - Description: Creates the SQLite database table named "reactor_status_data" to store reactor status data.
   - Usage: Initializes the database structure for reactor status data storage.

4. `scrape_and_load()`
   - Description: Scrapes data from a specified URL and loads it into the "reactors" database table.
   - Usage: Populates the database with reactor information from a web page.

5. `convert_to_iso8601(date_str)`
   - Description: Converts date strings to ISO 8601 format.
   - Usage: Converts date formats for data consistency.

### API Endpoints:

1. `/`
   - Description: Home endpoint providing details of available API endpoints.
   - Usage: Accessing the root of the API returns a list of available endpoints.

2. `/reactors/on-outage/<start_date_end_date>`
   - Description: Lists all reactors that are on outage for a given date range.
   - Usage: Provides a list of reactors and their outage status within the specified date range.

3. `/reactors/last-outage-date/<unit>`
   - Description: Gets the last known outage date of a specific reactor by its unit.
   - Usage: Retrieves the last outage date for a specified reactor unit.

4. `/reactors/`
   - Description: Retrieves all reactors with an optional filter by state.
   - Usage: Retrieves a list of all reactors or filters them by state if a state parameter is provided.

5. `/reactors/plant_name/<plant_name>`
   - Description: Retrieves details about a specific reactor by its plant name.
   - Usage: Retrieves detailed information about a reactor based on its unique plant name.

### Note:
- The code also includes Swagger documentation for API endpoints, allowing users to interact with the API and view the available endpoints with descriptions.
- The code initializes the database structure, fetches reactor status data, scrapes reactor information from a web page, and provides endpoints for querying and retrieving reactor data.
