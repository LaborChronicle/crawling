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

def parse_latimes_page(html, url, csv_writer):
    """Parse the LA Times page to extract the article's title, author names, article text, and URL."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the body tag with the class 'page-body'
    body = soup.find('body', class_='page-body')
    if not body:
        print("No valid page body found.")
        return

    # Find the div with class 'page-content paywall'
    page_content = body.find('div', class_='page-content paywall')
    if not page_content:
        print("No page content found.")
        return

    # Extract the title from h1 with class 'headline'
    title_element = page_content.find('h1', class_='headline')
    title_text = title_element.get_text(strip=True) if title_element else "No Title Found"

    # Find the div with class 'page-wrapper'
    page_wrapper = page_content.find('div', class_='page-wrapper')
    if not page_wrapper:
        print("No page wrapper found.")
        return

    # Find the main tag and then the article tag inside it
    main_tag = page_wrapper.find('main')
    article_tag = main_tag.find('article') if main_tag else None
    if not article_tag:
        print("No article found.")
        return

    # Extract authors from div with class 'byline'
    byline_div = article_tag.find('div', class_='byline')
    author_texts = []
    if byline_div:
        author_links = byline_div.find_all('a')
        author_texts = [a.get_text(strip=True) for a in author_links]
    author_text = ', '.join(author_texts) if author_texts else "No Author Found"

    # Extract article text from div with data-element='story-body'
    story_body_div = article_tag.find('div', attrs={'data-element': 'story-body'})
    article_texts = []
    if story_body_div:
        paragraphs = story_body_div.find_all('p')
        article_texts = [p.get_text(strip=True) for p in paragraphs]
    full_text = ' '.join(article_texts) if article_texts else "No Text Found"

    # Write to CSV
    csv_writer.writerow([title_text, author_text, full_text, url])

def parse_teamsters_page(html, url, csv_writer):
    """Parse the Teamster.org page to extract the article's title, author name, article text, and URL."""
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the article tag
    article_tag = soup.find('article')
    if not article_tag:
        print("No article tag found.")
        return

    # Extract the title from the header tag
    header_tag = article_tag.find('header')
    title_element = header_tag.find(class_='single__hed--title') if header_tag else None
    title_text = title_element.get_text(strip=True) if title_element else "No Title Found"

    # Locate the div with class 'single__entry'
    entry_div = article_tag.find('div', class_='single__entry')
    if not entry_div:
        print("No entry div found.")
        return

    # Extract the author from the div with class 'single__press'
    press_div = entry_div.find('div', class_='single__press')
    author_text = "No Author Found"
    if press_div:
        strong_tag = press_div.find('strong')
        if strong_tag:
            # Extract author name by removing "Press Contact:" prefix
            press_text = strong_tag.get_text(strip=True)
            if press_text.startswith("Press Contact:"):
                author_text = press_text.replace("Press Contact:", "").strip()

    # Extract article text from p tags in the 'single__entry' div,
    # excluding the p tag within the 'single__press' div
    article_texts = []
    for paragraph in entry_div.find_all('p'):
        # Check if the paragraph is inside the 'single__press' div
        if press_div and press_div.find('p') == paragraph:
            continue
        article_texts.append(paragraph.get_text(strip=True))
    full_text = ' '.join(article_texts) if article_texts else "No Text Found"

    # Write to CSV
    csv_writer.writerow([title_text, author_text, full_text, url])

def parse_router(html, url, csv_writer):
    """Route to the appropriate parser based on the URL."""
    if "latimes.com" in url:
        parse_latimes_page(html, url, csv_writer)
    elif "teamster.org" in url:
        parse_teamsters_page(html, url, csv_writer)
    else:
        print(f"No parser implemented for {url}")

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
                parse_router(html_content, url, csv_writer)

if __name__ == "__main__":
    main()
