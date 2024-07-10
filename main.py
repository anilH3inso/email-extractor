import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

def get_banner_text():
    banner_text = '''

    $$$$$$$$$\                         $$\ $$\                                                 
    $$  _____|                        \__|$$ |                                                
    $$ |      $$$$$$\$$$$\   $$$$$$\  $$\ $$ |                                                
    $$$$$\    $$  _$$  _$$\  \____$$\ $$ |$$ |                                                
    $$  __|   $$ / $$ / $$ | $$$$$$$ |$$ |$$ |                                                
    $$ |      $$ | $$ | $$ |$$  __$$ |$$ |$$ |                                                
    $$$$$$$$$\ $$ | $$ | $$ |\$$$$$$$ |$$ |$$ |                                                
    \________|\__| \__| \__| \_______|\__|\__|                                                
    $$$$$$$$$\             $$\                                     $$\                         
    $$  _____|            $$ |                                    $$ |                        
    $$ |      $$\   $$\ $$$$$$\    $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
    $$$$$\    \$$\ $$  |\_$$  _|  $$  __$$\  \____$$\ $$  _____|\_$$  _|  $$  __$$\ $$  __$$\ 
    $$  __|    \$$$$  /   $$ |    $$ |  \__| $$$$$$$ |$$ /        $$ |    $$ /  $$ |$$ |  \__|
    $$ |       $$  $$<    $$ |$$\ $$ |      $$  __$$ |$$ |        $$ |$$\ $$ |  $$ |$$ |      
    $$$$$$$$$\ $$  /\$$\   \$$$$  |$$ |      \$$$$$$$ |\$$$$$$$\   \$$$$  |\$$$$$$  |$$ |      
    \________|\__/  \__|   \____/ \__|       \_______| \_______|   \____/  \______/ \__|      
                                                                                              
                                                                                              
                                                                                     -By insoHacker
                                                                                     
    '''
    return banner_text

def extract_emails(text):
    # Regular expression to find email addresses
    email_regex = r'[\w\.-]+@[\w\.-]+'
    emails = re.findall(email_regex, text)
    return emails

def crawl_website(url, max_urls=None):
    # Get base URL
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

    # List to store found emails
    found_emails = set()

    # List to keep track of visited URLs
    visited_urls = set()

    # Counter for scanned URLs and collected emails
    scanned_count = 0
    collected_emails_count = 0

    # Start time for estimation
    start_time = time.time()

    # Function to recursively crawl URLs
    def crawl(url):
        nonlocal scanned_count, collected_emails_count

        try:
            if url in visited_urls:
                return
            visited_urls.add(url)

            # Fetch URL content
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad status codes

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract emails from current page
            emails_on_page = extract_emails(response.text)
            found_emails.update(emails_on_page)
            collected_emails_count += len(emails_on_page)

            # Print the directory being scanned
            print(f"Scanning directory: {url}")

            # Increment scanned count
            nonlocal scanned_count
            scanned_count += 1

            # Find all links on the page
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(base_url, link['href'])
                if absolute_url.startswith(base_url) and absolute_url not in visited_urls:
                    if max_urls is None or scanned_count < max_urls:
                        crawl(absolute_url)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Start crawling from the given URL
    crawl(url)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print summary
    print(f"\nTotal URLs scanned: {scanned_count}")
    print(f"Total emails collected: {collected_emails_count}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return found_emails

def prompt_for_url():
    while True:
        url = input("Enter website URL: ").strip()
        if not url.startswith(('http://', 'https://')):
            print("Invalid URL. Please include 'http://' or 'https://' in the beginning.")
            continue
        return url

def prompt_for_max_urls():
    while True:
        try:
            max_urls = int(input("Enter the maximum number of URLs to scan (enter 0 for unlimited): ").strip())
            if max_urls < 0:
                print("Maximum URLs cannot be negative. Please enter a non-negative number.")
                continue
            return max_urls
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def prompt_for_output_file():
    while True:
        output_file = input("Enter output file name (e.g., emails.txt): ").strip()
        if not output_file.endswith('.txt'):
            print("Invalid file name. Please include the extension '.txt' in the file name.")
            continue
        return output_file

if __name__ == "__main__":
    # Display banner
    banner = get_banner_text()
    print(banner)

    while True:
        try:
            url = prompt_for_url()
            max_urls = prompt_for_max_urls()
            output_file = prompt_for_output_file()

            # Crawl the website and extract emails
            emails = crawl_website(url, max_urls=max_urls)

            # Save emails to file
            with open(output_file, 'w') as file:
                for email in emails:
                    file.write(email + '\n')

            print(f"\nEmails extracted and saved to {output_file}")
            break

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}. Please enter a valid URL.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

