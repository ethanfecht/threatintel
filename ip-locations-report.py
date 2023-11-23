import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_coordinates(text):
    # Find the position of the opening and closing parentheses
    start = text.find('(')
    end = text.find(')')

    # Extract and return the text between the parentheses
    if start != -1 and end != -1:
        return text[start + 1:end].strip()
    else:
        return None

# Function to create Google Maps URL
def google_maps_link(coords):
    base_url = "https://www.google.com/maps/place/" + str(coords)
    return f'<a href="{base_url}" target="_blank">Location of City</a>'

# List of IPs to process


#Pick one of these options, and comment the other out

#option1 - accept IP input from the user (comma separated)
user_input = input('Send me your IPs!')
ips = user_input.split(',')
print(ips)
print("Please wait...")


#option2 - input them directly in the script - line break separated
# ips = """
#""".split('\n')



# Initialize a list to store the data
data = []

# Loop through each IP address
for ip in ips:
    ip = ip.strip().replace('[', '').replace(']', '') #re-fang any defanged IPs

    # Make a request to the URL
    response = requests.get(f'https://www.iplocationtools.com/{ip}')

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize data variables
    city = None
    country = None
    isp = None
    domain = None
    coordinates = None

    # Find all table rows
    table_rows = soup.find_all('tr')

    if '0°0' in table_rows:
        continue

    # Iterate over each row to find the city information
    for row in table_rows:
        if 'City' in row.get_text():
            city_cells = row.find_all('td')
            if city_cells:
                city_full_text = city_cells[-1].get_text(strip=True)
                # Split the text by 'Report Incorrect Location' and take the first part
                city = city_full_text.split('Report Incorrect Location')[0].strip()
                # Further split to remove the word "City" if it is present
                if city.startswith('City'):
                    city = city[4:].strip()
            break  # Exit the loop once the city is found


    # Iterate over each row to find the country information
    for row in table_rows:
        if 'Country' in row.get_text():
            country_cells = row.find_all('td')
            if country_cells:
                country_full_text = country_cells[0].get_text(strip=True)
                # Split the text by 'Report Incorrect Location' and take the first part
                country = country_full_text.split('Report Incorrect Location')[0].strip()
                # Further split to remove the word "Country" if it is present
                if country.startswith('Country'):
                    country = country[7:].strip()
            break  # Exit the loop once the country is found


    # Iterate over each row to find the ISP information
    for row in table_rows:
        if 'ISP' in row.get_text():
            isp_cells = row.find_all('td')
            if isp_cells:
                isp_full_text = isp_cells[0].get_text(strip=True)
                # Split the text by 'Report Incorrect Location' and take the first part
                isp = isp_full_text.split('Report Incorrect Location')[0].strip()
                # Further split to remove the word "ISP" if it is present
                if isp.startswith('ISP'):
                    isp = isp[3:].strip()
            break  # Exit the loop once the country is found


    # Iterate over each row to find the domain information
    for row in table_rows:
        if 'Domain Name' in row.get_text():
            domain_cells = row.find_all('td')
            if domain_cells:
                domain_full_text = domain_cells[0].get_text(strip=True)
                # Split the text by 'Report Incorrect Location' and take the first part
                domain = domain_full_text.split('Report Incorrect Location')[0].strip()
                # Further split to remove the words "Domain Name" if it is present
                if domain.startswith('Domain Name'):
                    domain = domain[11:].strip()
            break  # Exit the loop once the country is found


    # Iterate over each row to find the city coordinates information
    for row in table_rows:
        if 'Coordinates of City' in row.get_text():
            coord_cells = row.find_all('td')
            if coord_cells:
                coordinates = coord_cells[-1].get_text(strip=True).split('\n')[-1].strip()
                coordinates = coordinates.replace(' ','')
                coordinates = extract_coordinates(coordinates)


    # Append the data
    data.append({'IP': ip, 'City': city, 'Country': country, 'ISP': isp, 'Domain Name': domain, 'Coordinates of City': coordinates})


# Creating a DataFrame
df = pd.DataFrame(data)
# Apply the function to the 'Coordinates of City' column
df['Google Maps Link'] = df['Coordinates of City'].apply(google_maps_link)

#Sort dataframe by country
df = df.sort_values(by='Country')

print(df)


# Export DataFrame to HTML
html_file = 'ip_data.html'
df.to_html(html_file, escape=False, index=False)
print(f"DataFrame exported as HTML to {html_file}")

# Export DataFrame to CSV
csv_file = 'ip_data.csv'
df.to_csv(csv_file, index=False)
print(f"DataFrame exported as CSV to {csv_file}")
