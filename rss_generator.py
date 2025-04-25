from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz # To handle timezone awareness

def generate_rss_feed(papers_list, feed_filepath):
    """Generates an RSS feed from the list of papers and saves it to a file.

    Args:
        papers_list (list): A list of paper dictionaries from the parser.
        feed_filepath (str): The path to save the generated RSS feed file.
    """
    fg = FeedGenerator()
    fg.title('Hugging Face Daily Papers')
    fg.link(href='https://huggingface.co/papers', rel='alternate') # Link to the source page
    # Use the link of the first paper as the feed ID, assuming papers are sorted by date
    fg.id(papers_list[0]['link'] if papers_list else 'tag:huggingface.co,2024:papers/daily')
    fg.description('Daily research papers curated by the Hugging Face community.')
    fg.language('en')

    # Sort papers by published_at date, newest first
    # Handle potential None values in published_at
    papers_list.sort(key=lambda p: p.get('published_at') or '1970-01-01T00:00:00.000Z', reverse=True)


    for paper in papers_list:
        fe = fg.add_entry()
        fe.title(paper['title'])
        fe.link(href=paper['link'])
        fe.id(paper['link']) # Use the ArXiv link as the unique identifier

        # Build the description with thumbnail, authors, upvotes, and summary
        description = ""
        if paper.get('thumbnail'):
            description += f'<p><img src="{paper["thumbnail"]}" alt="Paper thumbnail" style="max-width: 300px; height: auto;" /></p>'

        description += f"<p><b>Authors:</b> {paper.get('authors', 'N/A')}</p>"
        description += f"<p><b>Upvotes:</b> {paper.get('upvotes', 0)}</p>" # Added Upvotes
        description += f"<p><b>Summary:</b> {paper.get('summary', 'N/A')}</p>"

        fe.description(description)

        # Parse and set the publication date
        pub_date_str = paper.get('published_at')
        if pub_date_str:
            try:
                # Parse the ISO 8601 format string
                pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                # Ensure it's timezone-aware (UTC)
                fe.pubDate(pub_date.astimezone(pytz.utc))
            except ValueError:
                print(f"Warning: Could not parse date '{pub_date_str}' for paper ID {paper.get('id')}")
                # Optionally set a default date or leave it out
                # fe.pubDate(datetime.now(pytz.utc)) # Example: set to now

        # Add authors
        fe.author(name=paper.get('authors', 'N/A'))

    # Generate the RSS feed as a string
    rss_feed = fg.rss_str(pretty=True)

    # Save the feed to the specified file
    try:
        with open(feed_filepath, 'wb') as f: # Write in binary mode for UTF-8
            f.write(rss_feed)
        print(f"RSS feed successfully generated and saved to {feed_filepath}")
    except IOError as e:
        print(f"Error writing RSS feed to {feed_filepath}: {e}")