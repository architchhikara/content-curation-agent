# Wisdom Scraper & Data Portal

A Python-based application that scrapes content (captions, metadata) from various social media platforms (YouTube, Instagram, Facebook, LinkedIn, X) and appends the data to a Google Sheet.

## Features

- **YouTube:** Fetches video title, description, author, and date using the official YouTube Data API.
There is also a Sheet which uses App Script https://docs.google.com/spreadsheets/d/1tsdQJu1JcJXQnz7txlKIEFg-NBFFhmadFToOeXVMTsc/edit?gid=0#gid=0


- **Instagram:** Uses `instaloader` to fetch post captions and metadata.
- **Facebook:** Uses Open Graph metadata for a safe, non-login approach.
- **X (Twitter):** Uses `tweepy` (Official API) to fetch tweets.
- **LinkedIn:** Uses Open Graph metadata and supports optional official API integration.
- **Safety:** Implements random delays, user-agent rotation, and circuit breakers (stops on HTTP 429).
- **Google Sheets:** Automatically appends scraped data to a specified Google Sheet.

## Setup

### 1. Prerequisites

- Python 3.8+
- A Google Cloud Project with the Google Sheets API and Google Drive API enabled.
- API Keys for YouTube and X (Twitter).

### 2. Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. **Google Sheets Setup:**
   - Create a project in Google Cloud Console.
   - Enable **Google Sheets API** and **Google Drive API**.
   - Create a Service Account and download the JSON key file.
   - Rename the JSON file to `service_account.json` and place it in the project root.
   - Share your target Google Sheet with the email address found in `service_account.json` (e.g., `content-curation-agent@...`).

2. **Environment Variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your API keys:
     - `YOUTUBE_API_KEY`: Get this from Google Cloud Console.
     - `TWITTER_...`: Get these from the X Developer Portal.
     - `GOOGLE_SHEET_NAME`: The name of the Google Sheet to write to.

### 4. Usage

1. Open `main.py` and update the `URLS_TO_SCRAPE` list with the links you want to process.
2. Run the script:
   ```bash
   python main.py
   ```

## Architecture

- **`scrapers/`**: Individual modules for each platform.
- **`utils/`**: Helper functions (random delays, user-agents) and Google Sheets handler.
- **`main.py`**: Entry point that orchestrates the scraping process.
