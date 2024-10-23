import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to check if images on the page have alt attributes
def check_image_alt(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if request was successful

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')  # Find all images

        # Check if images have alt attributes
        alt_results = []
        for img in images:
            img_src = img.get('src', 'No src found')
            img_alt = img.get('alt', 'No alt attribute')
            alt_results.append({'Image Source': img_src, 'Alt Attribute': img_alt})

        return {"URL": url, "Alt Results": alt_results}

    except requests.exceptions.RequestException as e:
        return {"URL": url, "Error": str(e)}

# Function to read URLs from a CSV file, check their image alt attributes, and write results to another CSV file
def check_urls_from_csv(input_csv, output_csv, max_workers=10):
    results = []

    # Open and read the input CSV file
    with open(input_csv, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        url_list = [row[0] for row in reader]

    # Use ThreadPoolExecutor for multi-threaded URL processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_image_alt, url): url for url in url_list}

        # Collect the results as they complete
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Write the results to a new CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Image Source', 'Alt Attribute'])

        # Write each result to the CSV file
        for result in results:
            url = result["URL"]
            if "Error" in result:
                writer.writerow([url, "Error", result["Error"]])
            else:
                for img_info in result["Alt Results"]:
                    writer.writerow([url, img_info['Image Source'], img_info['Alt Attribute']])

    print(f"Results have been saved to {output_csv}")

# Example usage
input_csv = "url_list.csv"   # Input CSV file with URLs
output_csv = "alt_check_results.csv"  # Output CSV file to store the results
max_workers = 10  # Number of threads to use

check_urls_from_csv(input_csv, output_csv, max_workers)
