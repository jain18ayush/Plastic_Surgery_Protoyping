import sys 
from bs4 import BeautifulSoup
import os
import csv

def toCSV(source, rows):
    csv_filename = f'{source}.csv'

    # Determine if the CSV file already exists
    file_exists = os.path.isfile(csv_filename)

    # Write to CSV file
    with open(csv_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Data has been written to {csv_filename}")

def extractData(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    if table is None:
        return

    # Extract table rows
    rows = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        rows.append(row_data)
    
    return rows



def extract_aero(html_directory, finished_file):
    """
    Extracts domains from HTML files in a directory and processes only those not in the finished file.

    Args:
    html_directory (str): The directory containing HTML files.
    finished_file (str): Path to the file containing already processed domains.

    Returns:
    list: List of domains that have been processed.
    """
    #create finished file if it does not exist
    if not os.path.exists(finished_file):
        with open(finished_file, 'w') as file:
            pass  # Just create an empty file

    # Read finished domains from the file
    with open(finished_file, 'r') as file:
        finished_domains = set(line.strip() for line in file)

    for filename in os.listdir(html_directory):
        if filename.endswith('.html'):
            # Extract domain from filename (removing the .html extension)
            domain = filename[:-5]
            
            # Process only if domain is not in finished list
            if domain not in finished_domains:
                # Open and read the HTML file
                with open(os.path.join(html_directory, filename), 'r') as file:
                    content = file.read()
                    # Extract data from the content
                    data = extractData(content)
                    
                    if data is not None:
                        toCSV('aeroleads', data)
                    
                    # Add domain to processed domains
                    with open('finished.txt', 'a') as file:
                      file.write(domain + '\n')

def run_process():
  extract_aero('./HTML/aeroleads', './finished.txt')

if __name__ == "__main__":
  run_process()