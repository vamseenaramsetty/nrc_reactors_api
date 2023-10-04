# nrc_reactors_api
SESCO Technical Assessment to produce APIs using Python


```markdown
# NRC Reactors Data API

The NRC Reactors Data API is a Python-based API that provides access to information about nuclear reactors in the United States. It ingests data from the United States Nuclear Regulatory Commission (NRC) and makes it accessible through a set of API endpoints.

## Table of Contents

- [Getting Started]
  - [Prerequisites]
  - [Installation]
- [API Endpoints]
  - [1. Retrieve all reactors](#1-retrieve-all-reactors)
  - [2. Retrieve reactor details](#2-retrieve-reactor-details)
  - [3. List reactors on outage](#3-list-reactors-on-outage)
  - [4. Get last outage date](#4-get-last-outage-date)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3
- SQLite
- Flask
- BeautifulSoup (for web scraping)
- Requests (for HTTP requests)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vamseenaramsetty/nrc_reactors_api.git
   ```

2. Change to the project directory:

   ```bash
   cd nrc_reactors_api
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```


4. Run the Flask application:

   ```bash
   python app.py
   ```

The API will be accessible at `http://localhost:5000`.

## API Endpoints

The API provides the following endpoints:

### 1. Retrieve all reactors with an optional filter by state.

- `GET /reactors/`
- `GET /reactors/<state>`

### 2. Retrieve reactor details by plant name.

- `GET /reactors/plant_name/<plant_name>`

### 3. List all reactors that are on outage for a given date range.

- `GET /reactors/on-outage/<start_date_end_date>`

### 4. Get the last known outage date of a specific reactor by its unit.

- `GET /reactors/last-outage-date/<unit>`

## Usage Examples

Example 1: Retrieve all reactors
```bash
curl http://localhost:5000/reactors/
```

Example 2: Retrieve reactors in the state of California
```bash
curl http://localhost:5000/reactors/CA
```

Example 3: Retrieve details about the reactor with the plant name "Callaway"
```bash
curl http://localhost:5000/reactors/plant_name/Callaway
```

Example 4: List reactors on outage between January 1, 2023, and January 31, 2023
```bash
curl http://localhost:5000/reactors/on-outage/01-01-2023_01-31-2023
```


