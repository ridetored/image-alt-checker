# image-alt-checker
This Python tool checks if images on a webpage have "alt" attributes, essential for SEO and accessibility. It processes multiple URLs concurrently using multi-threading, reads URLs from a CSV file, and outputs results in a new CSV file. Ideal for auditing image alt tags across large websites.

# Explanation:
# check_image_alt(url):

Fetches the webpage HTML using requests.
Uses BeautifulSoup to parse the HTML and find all images (<img> tags).
For each image, it checks if there is an alt attribute and records the result.

# check_urls_from_csv:

Reads URLs from an input CSV file.
Uses ThreadPoolExecutor to check multiple URLs concurrently (multi-threading).
The results for each image (image source and alt attribute) are written to an output CSV file.

# CSV Input and Output:

Input: The script reads a CSV file (url_list.csv) containing a list of URLs, one per line.
Output: The results are saved in alt_check_results.csv, with columns for the URL, image source (src), and the corresponding alt attribute (or "No alt attribute").

# Benefits of Multi-Core:
Faster Execution: Using ThreadPoolExecutor, the script can check multiple URLs concurrently, speeding up the process significantly when dealing with many URLs.
Scalable: The max_workers parameter allows you to control the number of threads used. Adjust this number based on the capabilities of your system for optimal performance.
