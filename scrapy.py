import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.nrc.gov/reactors/operating/list-power-reactor-units.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Finding the table containing the data
table = soup.find('table', {'summary': 'List of Power Reactor Units'})

# Extracting headers (optional)
headers = [header.text for header in table.find_all('th')]

# Extracting rows
rows = table.find_all('tr')[1:]  # [1:] to skip header row
data = []
for row in rows:
    columns = row.find_all('td')
    columns = [column.text.strip() for column in columns]
    data.append(columns)

# Saving to CSV
with open('reactor_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Plant Name', 'Docket Number', 'License Number', 'Reactor Type', 'Location', 'Owner/Operator', 'NRC Region'])  # Writing headers
    for row in data:
        plant_name, docket_number = row[0].split('\n')
        license_number = row[1]
        reactor_type = row[2]
        location = row[3]
        owner_operator = row[4]
        nrc_region = row[5]
        writer.writerow([plant_name, docket_number, license_number, reactor_type, location, owner_operator, nrc_region])
