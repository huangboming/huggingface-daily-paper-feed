import json
import requests
from bs4 import BeautifulSoup
from rss_generator import generate_rss_feed
import argparse

def fetch_html(url):
    """Fetches HTML content from a given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_daily_papers(source):
    """Parses the Hugging Face Daily Papers HTML to extract paper data.

    Args:
        source (str): URL of the daily papers page or path to a local HTML file.

    Returns:
        list: A list of dictionaries, where each dictionary contains
              information about a paper.
              Returns an empty list if the data cannot be found or parsed.
    """
    html_content = None
    if source.startswith('http://') or source.startswith('https://'):
        print(f"Fetching HTML from URL: {source}")
        html_content = fetch_html(source)
    else:
        print(f"Reading HTML from file: {source}")
        try:
            with open(source, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {source}")
            return []

    if not html_content:
        print("Error: Could not get HTML content.")
        return []

    try:
        soup = BeautifulSoup(html_content, 'lxml')

        # Find the div containing the paper data
        papers_div = soup.find('div', attrs={'data-target': 'DailyPapers'})
        if not papers_div:
            print("Error: Could not find the 'DailyPapers' div.")
            return []

        # Extract the JSON data from the 'data-props' attribute
        data_props_json = papers_div.get('data-props')
        if not data_props_json:
            print("Error: Could not find 'data-props' attribute.")
            return []

        # Parse the JSON data
        data = json.loads(data_props_json)

        # Extract paper information
        papers_list = []
        if 'dailyPapers' in data and isinstance(data['dailyPapers'], list):
            for item in data['dailyPapers']:
                paper_info = item.get('paper')
                if paper_info and isinstance(paper_info, dict):
                    paper_id = paper_info.get('id')
                    title = paper_info.get('title', 'N/A').replace('\n', ' ').strip()
                    summary = paper_info.get('summary', 'N/A').replace('\n', ' ').strip()
                    published_at = paper_info.get('publishedAt') # Keep as string for now
                    link = f"https://arxiv.org/abs/{paper_id}" if paper_id else 'N/A'

                    authors_list = paper_info.get('authors', [])
                    author_names = [author.get('name', 'Unknown') for author in authors_list if isinstance(author, dict)]
                    authors_str = ", ".join(author_names)

                    # Extract thumbnail and upvotes from the parent 'item' dictionary
                    thumbnail = item.get('thumbnail', None)
                    upvotes = paper_info.get('upvotes', 0) # Upvotes seem to be inside paper_info

                    papers_list.append({
                        'id': paper_id,
                        'title': title,
                        'link': link,
                        'authors': authors_str,
                        'summary': summary,
                        'published_at': published_at,
                        'thumbnail': thumbnail,
                        'upvotes': upvotes
                    })
        else:
            print("Error: 'dailyPapers' key not found or not a list in JSON data.")
            return []

        return papers_list

    except json.JSONDecodeError:
        print("Error: Could not decode JSON from data.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        return []

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Parse Hugging Face Daily Papers and generate RSS feed.')
    parser.add_argument(
        '--source',
        type=str,
        default='https://huggingface.co/papers',
        help='URL of the Hugging Face papers page or path to a local HTML file.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='feed.xml',
        help='Path to save the generated RSS feed file.'
    )
    args = parser.parse_args()

    html_source = args.source
    rss_file = args.output

    extracted_papers = parse_daily_papers(html_source)

    if extracted_papers:
        print(f"Successfully extracted {len(extracted_papers)} papers from {html_source}.")

        # Print details of the first paper as a sample, including new fields
        if extracted_papers:
            print("\n--- Sample Paper --- ")
            for key, value in extracted_papers[0].items():
                print(f"{key.capitalize()}: {value}")
            print("-------------------")

        # Generate and save the RSS feed
        generate_rss_feed(extracted_papers, rss_file)
    else:
        print(f"Failed to extract papers from {html_source}.")