# import sqlite3
# from flask import Flask, jsonify, request
# from bs4 import BeautifulSoup
# import requests
# from datetime import datetime

# app = Flask(__name__)

# def create_table():
#     conn = sqlite3.connect('reactors.db')
#     c = conn.cursor()
#     c.execute('DROP TABLE IF EXISTS reactors;')
#     c.execute('''
#         CREATE TABLE reactors (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             plant_name TEXT,
#             docket_number TEXT,
#             license_number TEXT,
#             reactor_type TEXT,
#             location TEXT,
#             owner_operator TEXT,
#             nrc_region TEXT,
#             state TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def get_reactor_status_data():
#     # Define the URL of the data source
#     url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/powerreactorstatusforlast365days.txt"

#     # Fetch data from the URL
#     response = requests.get(url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.text
#         # Split the data into lines
#         return data
#         # lines = data.strip().split('\n')
#         # return lines
#     else:
#         raise Exception(f"Failed to retrieve data from the URL. Status code: {response.status_code}")


# def create_reactor_status_table():
#     conn = sqlite3.connect('reactors.db')
#     c = conn.cursor()
#     c.execute('DROP TABLE IF EXISTS reactor_status_data;')
#     try:
#         # Create an SQLite table with the DATETIME datatype for the ReportDt column
#         c.execute('''
#             CREATE TABLE IF NOT EXISTS reactor_status_data (
#                 ReportDt DATETIME,
#                 Unit TEXT,
#                 Power INTEGER
#             )
#         ''')
#         n=0
#         # Iterate through the lines and insert data into the SQLite table
#         data = get_reactor_status_data()
#         lines = data.strip().split('\n')
#         # print(lines)
#         for line in lines:
#             columns = line.strip().split('|')
#             # (columns[0].split(' '))[0]
#             # break
#             # print(columns)
#             if len(columns) == 3 and n>1:
#                 # Convert the date to ISO 8601 format before inserting
#                 # columns[0] = convert_to_iso8601((columns[0].split(' '))[0])
#                 columns[0]=(columns[0].split(' '))[0]
#                 # print('date:',columns[0])
#                 # print(type(columns[0]))
#                 columns[0] = datetime.strptime(columns[0], '%m/%d/%Y').strftime('%Y-%m-%d')
#                 #print(columns[0])
#                 # print(parsed_date)
#                 c.execute('INSERT INTO reactor_status_data (ReportDt, Unit, Power) VALUES (?, ?, ?)', columns)
#             n+=1

#         # Commit the changes and close the connection
#         conn.commit()
#         conn.close()
#         print("Data fetched and stored in the SQLite table.")
#     except sqlite3.Error as e:
#         print("SQLite error:", e)
#     finally:
#         conn.close()


# def scrape_and_load():
#     url = 'https://www.nrc.gov/reactors/operating/list-power-reactor-units.html'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find('table')

#     # Connect to the database
#     conn = sqlite3.connect('reactors.db')
#     c = conn.cursor()

#     # Go through each row in the table
#     for row in table.find_all('tr')[1:]:
#         columns = row.find_all('td')

#         try:
#             plant_info = columns[0].text.strip()
#             plant_info_parts = plant_info.split('\n')
#             plant_name = plant_info_parts[0].strip()
#             docket_number = plant_info_parts[1].strip()
#             license_number = columns[1].text.strip() 
#             reactor_type = columns[2].text.strip()
#             entire_address = columns[3].text.strip()
#             if ',\u00a0\u00a0' in entire_address:
#                 address = entire_address.split(',\u00a0\u00a0')
#             else:
#                 address = entire_address.rsplit(',',1)
            
#             location = address[0]
#             owner_operator = columns[4].text.strip()
#             nrc_region = columns[5].text.strip()
#             state = address[1].strip() #location.split(',')[-1].strip()
            
#             # Construct the query
#             query = '''
#                 INSERT INTO reactors (plant_name, docket_number, license_number, reactor_type, location, owner_operator, nrc_region, state)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?);
#             '''
#             data = (plant_name, docket_number, license_number, reactor_type, location, owner_operator, nrc_region, state)

#             # Execute the query
#             c.execute(query, data)

#         except IndexError as e:
#             print(f"Row with insufficient data: {columns}")

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()


# # Function to convert date strings to ISO 8601 format
# def convert_to_iso8601(date_str):
#     return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y-%m-%d')

# # Define the API endpoint for listing reactors on outage for a date range
# # @app.route('/reactors/on-outage/<string:start_date>/<string:end_date>', methods=['GET'])
# # def list_reactors_on_outage(start_date,end_date):
# #     # start_date_str = request.args.get('start_date')
# #     # end_date_str = request.args.get('end_date')
# #     print(start_date,end_date)

# #     if not start_date or not end_date:
# #         return jsonify({'error': 'Both start_date and end_date parameters are required'}), 400

# #     try:
# #         start_date_iso = convert_to_iso8601(start_date)
# #         end_date_iso = convert_to_iso8601(end_date)

# #         # Connect to the SQLite database
# #         conn = sqlite3.connect('reactors.db')
# #         c = conn.cursor()

# #         # Execute a SELECT query to retrieve reactors on outage for the date range
# #         c.execute("""
# #             select distinct ReportDt, Unit from reactor_status_data where power=0 and ReportDt between ? and ?;""", (start_date_iso, end_date_iso,))

# #         # Fetch and format the results
# #         reactors_on_outage = [{'Unit': row[1], 'ReportDt': row[0]} for row in c.fetchall()]

# #         # Close the database connection
# #         conn.close()

# #         return jsonify({'reactors_on_outage': reactors_on_outage})

# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# @app.route('/reactors/on-outage/<string:date_range>', methods=['GET'])
# def list_reactors_on_outage(date_range):
#     # Split the date_range parameter into start_date and end_date using the underscore (_) separator
#     date_range_parts = date_range.split('_')
#     if len(date_range_parts) != 2:
#         return jsonify({'error': 'Invalid date_range format. Use "start_date_end_date" with an underscore.'}), 400

#     start_date_str, end_date_str = date_range_parts

#     try:
#         # Convert start_date and end_date to ISO 8601 format
#         start_date_iso = convert_to_iso8601(start_date_str)
#         end_date_iso = convert_to_iso8601(end_date_str)

#         # Connect to the SQLite database
#         conn = sqlite3.connect('reactors.db')
#         c = conn.cursor()

#         # Execute a SELECT query to retrieve reactors on outage for the date range
#         c.execute("""
#             SELECT DISTINCT ReportDt, Unit
#             FROM reactor_status_data
#             WHERE Power = 0 AND ReportDt BETWEEN ? AND ?;
#         """, (start_date_iso, end_date_iso))

#         # Fetch and format the results
#         reactors_on_outage = [{'Unit': row[1], 'ReportDt': row[0]} for row in c.fetchall()]

#         # Close the database connection
#         conn.close()

#         return jsonify({'reactors_on_outage': reactors_on_outage})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

    
# # Define the API endpoint to get the last known outage date of a reactor by unit
# @app.route('/reactors/last-outage-date/<string:unit>', methods=['GET'])
# def get_last_outage_date(unit):
#     # unit = request.args.get('unit')
#     print(unit)

#     if not unit:
#         return jsonify({'error': 'The unit parameter is required'}), 400

#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect('reactors.db')
#         c = conn.cursor()

#         # Execute a SELECT query to get the last known outage date for the specified unit
#         c.execute("""
#             SELECT ReportDt, unit
#             FROM reactor_status_data
#             WHERE Unit = ? AND Power = 0
#             ORDER BY ReportDt DESC
#             LIMIT 1;
#         """, (unit,))

#         # Fetch the result
#         row = c.fetchone()
#         print(row)

#         # Close the database connection
#         conn.close()

#         if row:
#             return jsonify({'last_outage_date': row[0]})
#         else:
#             return jsonify({'last_outage_date': 'No outage records found for the specified unit'})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # @app.route('/reactors/', methods=['GET'])
# # def get_all_reactors():
# #     conn = sqlite3.connect('reactors.db')
# #     c = conn.cursor()
# #     c.execute('SELECT * FROM reactors')
# #     reactors = c.fetchall()
    
# #     reactor_list = [{
# #         'id': reactor[0],
# #         'plant_name': reactor[1],
# #         'docket_number': reactor[2],
# #         'license_number': reactor[3],
# #         'reactor_type': reactor[4],
# #         'location': reactor[5],
# #         'owner_operator': reactor[6],
# #         'nrc_region': reactor[7],
# #         'state': reactor[8]
# #     } for reactor in reactors]

# #     return jsonify(reactor_list)


# # @app.route('/reactors/<string:state>', methods=['GET'])
# # def get_state_reactors(state):
# #     state = state.upper()
# #     # print(state)
# #     conn = sqlite3.connect('reactors.db')
# #     c = conn.cursor()
# #     c.execute('SELECT * FROM reactors WHERE state = ?', (state,))


# #     reactors = c.fetchall()
# #     reactor_list = [{
# #         'id': reactor[0],
# #         'plant_name': reactor[1],
# #         'docket_number': reactor[2],
# #         'license_number': reactor[3],
# #         'reactor_type': reactor[4],
# #         'location': reactor[5],
# #         'owner_operator': reactor[6],
# #         'nrc_region': reactor[7],
# #         'state': reactor[8]
# #     } for reactor in reactors]

# #     return jsonify(reactor_list)

# @app.route('/reactors/<string:state>', methods=['GET'])
# @app.route('/reactors/', methods=['GET'])
# def get_reactors_by_state(state=None):
#     conn = sqlite3.connect('reactors.db')
#     c = conn.cursor()

#     if state:
#         # If a 'state' parameter is provided, filter by state
#         state = state.upper()
#         c.execute('SELECT * FROM reactors WHERE state = ?', (state,))
#     else:
#         # If no 'state' parameter is provided, fetch all reactors
#         c.execute('SELECT * FROM reactors')

#     reactors = c.fetchall()
#     reactor_list = [{
#         'id': reactor[0],
#         'plant_name': reactor[1],
#         'docket_number': reactor[2],
#         'license_number': reactor[3],
#         'reactor_type': reactor[4],
#         'location': reactor[5],
#         'owner_operator': reactor[6],
#         'nrc_region': reactor[7],
#         'state': reactor[8]
#     } for reactor in reactors]

#     return jsonify(reactor_list)



# @app.route('/reactors/plant_name/<string:plant_name>', methods=['GET'])
# def get_reactor(plant_name):
#     print(plant_name)
#     conn = sqlite3.connect('reactors.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM reactors WHERE plant_name = ?', (plant_name,))
#     reactor = c.fetchone()
#     print(reactor)
#     conn.close()

#     if reactor is None:
#         return jsonify({'error': 'Reactor not found'}), 404

#     reactor_dict = {
#         'id': reactor[0],
#         'plant_name': reactor[1],
#         'docket_number': reactor[2],
#         'license_number': reactor[3],
#         'reactor_type': reactor[4],
#         'location': reactor[5],
#         'owner_operator': reactor[6],
#         'nrc_region': reactor[7],
#         'state': reactor[8]
#     }

#     return jsonify(reactor_dict)


# if __name__ == '__main__':
#     create_table()
#     create_reactor_status_table()  
#     scrape_and_load()
#     get_reactor_status_data()
#     app.run(debug=True)





import sqlite3
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
import json
app = Flask(__name__)

SWAGGER_URL='/swagger'
API_URL='http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': ' NRC REACTOR DATA '
    }
)

app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json','r') as f:
        return jsonify(json.load(f))

def create_table():
    try:
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS reactors;')
        c.execute('''
            CREATE TABLE reactors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_name TEXT,
                docket_number TEXT,
                license_number TEXT,
                reactor_type TEXT,
                location TEXT,
                owner_operator TEXT,
                nrc_region TEXT,
                state TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Table 'reactors' created successfully.")
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def get_reactor_status_data():
    # URL of the data source
    url = "https://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/powerreactorstatusforlast365days.txt"

    try:
        # Fetch data from the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.text
            return data
        else:
            raise Exception(f"Failed to retrieve data from the URL. Status code: {response.status_code}")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_reactor_status_table():
    try:
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS reactor_status_data;')
        
        # Create an SQLite table with the DATETIME datatype for the ReportDt column
        c.execute('''
            CREATE TABLE IF NOT EXISTS reactor_status_data (
                ReportDt DATETIME,
                Unit TEXT,
                Power INTEGER
            )
        ''')
        n=0
        # Iterate through the lines and insert data into the SQLite table
        data = get_reactor_status_data()
        lines = data.strip().split('\n')
        
        for line in lines:
            columns = line.strip().split('|')
            if len(columns) == 3 and n>1:
                columns[0]=(columns[0].split(' '))[0]
                columns[0] = datetime.strptime(columns[0], '%m/%d/%Y').strftime('%Y-%m-%d')
                c.execute('INSERT INTO reactor_status_data (ReportDt, Unit, Power) VALUES (?, ?, ?)', columns)
            n+=1

        conn.commit()
        conn.close()
        print("Data fetched and stored in the SQLite table 'reactor_status_data'.")
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def scrape_and_load():
    try:
        url = 'https://www.nrc.gov/reactors/operating/list-power-reactor-units.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')

        # Connect to the database
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()

        # Go through each row in the table
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')

            try:
                plant_info = columns[0].text.strip()
                plant_info_parts = plant_info.split('\n')
                plant_name = plant_info_parts[0].strip()
                docket_number = plant_info_parts[1].strip()
                license_number = columns[1].text.strip() 
                reactor_type = columns[2].text.strip()
                entire_address = columns[3].text.strip()
                # Eliminate unwanted characters in address
                if ',\u00a0\u00a0' in entire_address:
                    address = entire_address.split(',\u00a0\u00a0')
                else:
                    address = entire_address.rsplit(',',1)
                
                location = address[0]
                owner_operator = columns[4].text.strip()
                nrc_region = columns[5].text.strip()
                state = address[1].strip()
                
                # Insert data into reactors table
                query = '''
                    INSERT INTO reactors (plant_name, docket_number, license_number, reactor_type, location, owner_operator, nrc_region, state)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                '''
                data = (plant_name, docket_number, license_number, reactor_type, location, owner_operator, nrc_region, state)

                
                c.execute(query, data)

            except IndexError as e:
                print(f"Row with insufficient data: {columns}")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Data scraped and loaded into the SQLite table 'reactors'.")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to convert date strings to ISO 8601 format
def convert_to_iso8601(date_str):
    return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y-%m-%d')

@app.route('/', methods=['GET'])
def home():
    # Define the data structure for API endpoint details
    api_endpoints = {
        "endpoints": [
            {
                "url": "/reactors/",
                "description": "Retrieve all reactors with an optional filter by state."
            },
            {
                "url": "/reactors?state=<state>",
                "description": "Retrieve reactor details by plant name."
            },
            {
                "url": "/reactors/on-outage/<start_date_end_date>",
                "description": "List all reactors that are on outage for a given date range."
            },
            {
                "url": "/reactors/last-outage-date/<unit>",
                "description": "Get the last known outage date of a specific reactor by its unit."
            },
            {
                "url": "/reactors/plant_name/<plant_name>",
                "description": "Retrieve details about a specific reactor by plant name."
            }
        ]
    }

    return jsonify(api_endpoints)

# API endpoint to list all reactors that are on outage for a given date range
@app.route('/reactors/on-outage/<string:date_range>', methods=['GET'])
def list_reactors_on_outage(date_range):
    try:
        # Split the date_range parameter into start_date and end_date using the underscore (_) separator
        date_range_parts = date_range.split('_')
        if len(date_range_parts) != 2:
            return jsonify({'error': 'Invalid date_range format. Use "start_date_end_date" with an underscore.'}), 400

        start_date_str, end_date_str = date_range_parts

        # Convert start_date and end_date to ISO 8601 format
        start_date_iso = convert_to_iso8601(start_date_str)
        end_date_iso = convert_to_iso8601(end_date_str)

        # Connect to the SQLite database
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()

        # Execute a SELECT query to retrieve reactors on outage for the date range
        c.execute("""
            SELECT DISTINCT ReportDt, Unit
            FROM reactor_status_data
            WHERE Power = 0 AND ReportDt BETWEEN ? AND ?;
        """, (start_date_iso, end_date_iso))

        # Fetch and format the results
        reactors_on_outage = [{'Unit': row[1], 'ReportDt': row[0]} for row in c.fetchall()]

        # Close the database connection
        conn.close()

        return jsonify({'reactors_on_outage': reactors_on_outage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint  to get the last known outage date of a reactor
@app.route('/reactors/last-outage-date/<string:unit>', methods=['GET'])
def get_last_outage_date(unit):
    try:
        if not unit:
            return jsonify({'error': 'The unit parameter is required'}), 400

        # Connect to the SQLite database
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()

        # Execute a SELECT query to get the last known outage date for the specified unit
        c.execute("""
            SELECT ReportDt, unit
            FROM reactor_status_data
            WHERE Unit = ? AND Power = 0
            ORDER BY ReportDt DESC
            LIMIT 1;
        """, (unit,))

        # Fetch the result
        row = c.fetchone()

        # Close the database connection
        conn.close()

        if row:
            return jsonify({'last_outage_date': row[0]})
        else:
            return jsonify({'last_outage_date': 'No outage records found for the specified unit'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to Retrieve all reactors with an optional filter by state.
# @app.route('/reactors/<string:state>', methods=['GET'])
@app.route('/reactors/', methods=['GET'])
def get_reactors_by_state():
    state = request.args
    if state:
        state=state.getlist('state')[0]
    try:
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()

        if state:
            # If a 'state' parameter is provided, filter by state
            state = state.upper()
            c.execute('SELECT * FROM reactors WHERE state = ?', (state,))
        else:
            # If no 'state' parameter is provided, fetch all reactors
            c.execute('SELECT * FROM reactors')

        reactors = c.fetchall()
        reactor_list = [{
            'id': reactor[0],
            'plant_name': reactor[1],
            'docket_number': reactor[2],
            'license_number': reactor[3],
            'reactor_type': reactor[4],
            'location': reactor[5],
            'owner_operator': reactor[6],
            'nrc_region': reactor[7],
            'state': reactor[8]
        } for reactor in reactors]

        return jsonify(reactor_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpotint to retrieve the details about around a specific reactor
@app.route('/reactors/plant_name/<string:plant_name>', methods=['GET'])
def get_reactor(plant_name):
    try:
        conn = sqlite3.connect('reactors.db')
        c = conn.cursor()
        c.execute('SELECT * FROM reactors WHERE plant_name = ?', (plant_name,))
        reactor = c.fetchone()
        conn.close()

        if reactor is None:
            return jsonify({'error': 'Reactor not found'}), 404

        reactor_dict = {
            'id': reactor[0],
            'plant_name': reactor[1],
            'docket_number': reactor[2],
            'license_number': reactor[3],
            'reactor_type': reactor[4],
            'location': reactor[5],
            'owner_operator': reactor[6],
            'nrc_region': reactor[7],
            'state': reactor[8]
        }

        return jsonify(reactor_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    create_table()
    create_reactor_status_table()  
    scrape_and_load()
    app.run(debug=True)
