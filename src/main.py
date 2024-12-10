from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_page(url):
    """Use Selenium to fetch the HTML content after JavaScript execution."""
    try:
        # Setup Selenium WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load the content
        html_content = driver.page_source
        driver.quit()  # Close the browser
        return html_content
    except Exception as e:
        print(f"Error fetching {url} with Selenium: {e}")
        return None

def parse_bbc_page(html, url, csv_writer):
    """Parse the HTML page to extract the article's title, author names from nested spans in the 'byline-block', and article text, then include the URL."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the main article tag
    article = soup.find('article')
    if not article:
        print("No article found on this page.")
        return

    # Extract the title from the 'headline-block'
    title = article.find('div', attrs={"data-component": "headline-block"})
    title_text = title.get_text(strip=True) if title else "No Title Found"

    # Find the first span that appears to contain an author name
    byline = article.find('div', attrs={"data-component": "byline-block"})
    author_text = "No Author Found"  # Default text if no valid span is found
    if byline:
        spans = byline.find_all('span')
        for span in spans:
            text = span.get_text(strip=True)
            words = text.split()
            # Check if the span text contains at least two words and both start with an uppercase letter
            if len(words) >= 2 and all(word[0].isupper() for word in words[:2]):
                author_text = text
                break  # Stop after the first span with name-like text is found

    # Extract article text from 'text-block'
    article_text = []
    content_blocks = article.find_all('div', attrs={"data-component": ["text-block"]})
    for block in content_blocks:
        text = block.get_text(strip=True)
        article_text.append(text)
    full_text = ' '.join(article_text)  # Combine all text blocks into one string

    # Write to CSV including the URL, author, and text
    csv_writer.writerow([title_text, author_text, full_text, url])

def read_urls(filename):
    """Read URLs from a file, each URL on a new line."""
    with open(filename, 'r') as file:
        urls = file.readlines()
        return [url.strip() for url in urls]

def main():
    urls = read_urls('/Users/caleblitalien/labor_chronicle/crawling/src/targets.txt')

    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Title', 'Author', 'Text', 'URL'])  # Write the header row
        
        for url in urls:
            print(f"Processing {url}")
            html_content = fetch_page(url)
            if html_content:
                parse_bbc_page(html_content, url, csv_writer)

if __name__ == "__main__":
    main()
