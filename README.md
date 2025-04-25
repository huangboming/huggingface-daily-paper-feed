# Hugging Face Papers RSS Feed Generator

This project automatically generates RSS feeds for the daily, weekly, and monthly curated papers listed on the Hugging Face website.
Since Hugging Face doesn't provide official RSS feeds for these pages, this project bridges that gap.

## Features

*   Fetches paper data (title, link, authors, summary, publication date, thumbnail, upvotes) directly from Hugging Face.
*   Generates standard RSS 2.0 feeds.
*   Automated updates using GitHub Actions.
*   Provides separate feeds for daily, weekly, and monthly papers.

## Generated Feeds

The following feed files are automatically generated and updated in this repository:

*   **Daily:** [`feed.xml`](./feed.xml)
    *   Updates daily around midnight UTC.
    *   Sources from: `https://huggingface.co/papers`
*   **Weekly:** [`feed_weekly.xml`](./feed_weekly.xml)
    *   Updates every Monday around midnight UTC.
    *   Sources from: `https://huggingface.co/papers/week/YYYY-Www` (dynamic URL)
*   **Monthly:** [`feed_monthly.xml`](./feed_monthly.xml)
    *   Updates on the 1st of every month around midnight UTC.
    *   Sources from: `https://huggingface.co/papers/month/YYYY-MM` (dynamic URL)

You can subscribe to these feeds using your favorite RSS reader by using the raw file URL (e.g., `https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPOSITORY/main/feed.xml`).

## How it Works

1.  **Parsing:** A Python script (`parser.py`) fetches the HTML content of the relevant Hugging Face papers page.
2.  **Data Extraction:** It uses BeautifulSoup and JSON parsing to extract the paper details embedded within the page's HTML.
3.  **RSS Generation:** Another Python script (`rss_generator.py`) uses the `feedgen` library to construct the RSS feed from the extracted data.
4.  **Automation:** GitHub Actions workflows (`.github/workflows/`) are scheduled to run automatically:
    *   The daily workflow runs `parser.py` targeting the main papers page.
    *   The weekly/monthly workflows calculate the correct URL for the current week/month and then run `parser.py`.
    *   If the generated feed file has changed, the workflow commits and pushes the update to the repository.

## Local Execution Tutorial

You can also run the script locally to generate the feeds manually.

**Prerequisites:**

*   Python 3.7+
*   pip (Python package installer)
*   Git

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
    cd YOUR_REPOSITORY
    ```
    (Replace `YOUR_USERNAME/YOUR_REPOSITORY` with the actual path to this repo).

2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the parser:**
    The `parser.py` script handles both fetching/parsing and calling the RSS generator.

    *   **Generate Daily Feed (Default):** Fetches from the main `/papers` URL.
        ```bash
        python parser.py
        ```
        This will create/update `feed.xml`.

    *   **Generate Weekly Feed:** You need to provide the specific weekly URL.
        ```bash
        # Replace YYYY-Www with the desired week, e.g., 2025-W17
        python parser.py --source https://huggingface.co/papers/week/YYYY-Www --output feed_weekly.xml
        ```

    *   **Generate Monthly Feed:** Provide the specific monthly URL.
        ```bash
        # Replace YYYY-MM with the desired month, e.g., 2025-04
        python parser.py --source https://huggingface.co/papers/month/YYYY-MM --output feed_monthly.xml
        ```

    *   **Use a local HTML file (for testing):**
        ```bash
        # Make sure 'local_papers.html' exists
        python parser.py --source local_papers.html --output test_feed.xml
        ```

5.  **Find the output:** The generated RSS feed file (`feed.xml`, `feed_weekly.xml`, etc.) will be created in the project's root directory.

## Contributing

Feel free to open issues or pull requests if you find bugs or have suggestions for improvement.