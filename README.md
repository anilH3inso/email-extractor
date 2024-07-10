# email-extractor
 This Python script automates the process of extracting email addresses from websites. It utilizes the Requests library for fetching web pages and BeautifulSoup (bs4) for parsing HTML content. Designed for flexibility and efficiency.

# Web Scraper for Email Extraction

This Python script crawls a website recursively, extracts email addresses, and saves them to a text file.

## Installation

1. **Clone the repository:**

git clone https://github.com/your-username/your-repository.git



2. **Navigate to the project directory:**

cd your-repository



3. **Install dependencies:**

pip install -r requirements.txt



- Ensure you have Python 3.x installed.

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library (bs4)

## Usage

1. **Run the script:**

python main.py



2. **Follow the prompts:**

- Enter the website URL to scrape.
- Specify the maximum number of URLs to scan (enter `0` for unlimited).
- Provide an output file name (e.g., `emails.txt`) to save extracted email addresses.

3. **Output:**

- The script will crawl the provided website, extract email addresses from each page, and save them to the specified output file.

## Example

```bash
$ python main.py
$ Enter website URL: https://example.com
$ Enter the maximum number of URLs to scan (enter 0 for unlimited): 10
$ Enter output file name (e.g., emails.txt): extracted_emails.txt
shell
Copy code
$ Scanning directory: https://example.com
$ Total URLs scanned: 10
$ Total emails collected: 22
$ Elapsed time: 25.50 seconds
$ Emails extracted and saved to extracted_emails.txt
