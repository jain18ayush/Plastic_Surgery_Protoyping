import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import tldextract

#returns a list that is all the values in list2 not present in list1
def dedup(domains_from_file, domains):
  unique_domains = [domain for domain in domains if domain not in domains_from_file]
  return unique_domains

def normalize_domain(domain):
  extracted = tldextract.extract(domain)
  normalized_domain = f"{extracted.domain}.{extracted.suffix}".lower()
  return normalized_domain

def save_html(source, domain, html_content):
  folder_path = f'./HTML/{source}'
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  file_path = folder_path + f'/{domain}.html'
  print(file_path)
  with open(file_path, 'w') as file:
    file.write(html_content)

# Function to read domains from a file
def read_domains(file_path):
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]
    return domains

def get_finished_HTML_domains(directory='./HTML/aeroleads'):
    # creates the directory if it does not exist already 
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Initialize an empty list to store filenames
    domains_from_file = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the file ends with .html
        if filename.endswith('.html'):
            # Remove the .html extension and add to the list
            domains_from_file.append(os.path.splitext(filename)[0])
    
    return domains_from_file

def get_domains(filepath):
  with open(filepath, 'r') as file:
    domains = set(line.strip() for line in file)
  return domains

def download_aero(domains):
  
  #need to remove the domain if it already has an html file. 
  HTML_domains = get_finished_HTML_domains('./HTML/aeroleads')
  domain_list = dedup(HTML_domains, domains)

  print(len(domain_list))
  #initial stuff 
  # Set up the WebDriver (this example uses Chrome)
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")

  driver = webdriver.Chrome(options=chrome_options)

  # Replace with the URL of the page containing the input field
  url = "https://aeroleads.com/email-finder"

  driver.get(url)

  ##clicks button to change to the proper email
  button = driver.find_element(By.XPATH, '//*[@id="kt_app_content_container"]/ul/li[2]/a')

  # Click the button
  button.click()

  time.sleep(5)

  for domain_name in domain_list:
    # Locate the input field by its ID
    input_field = driver.find_element(By.ID, "domain_input")
    #clear the input before writing to it again
    input_field.clear()
    # Fill in the input field with a value
    input_field.send_keys(domain_name)

    # Optionally, submit the form if necessary (this example presses Enter)
    input_field.send_keys(Keys.RETURN)

    # Close the WebDriver after a short wait to see the result (optional)
    time.sleep(2)

    #now need to get the 
    html_content = driver.page_source
    #save html
    save_html('aeroleads', domain=domain_name, html_content=html_content)

  driver.quit()

def run_download(filepath):
  domain_list = get_domains(filepath) #normalize domains
  domains = [normalize_domain(domain) for domain in domain_list]

  download_aero(domains)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python step1.py <file_path>")
    else:
        file_path = sys.argv[1]
        run_download(file_path)