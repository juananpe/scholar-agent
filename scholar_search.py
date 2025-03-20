from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
import datetime
from parsel import Selector
from playwright.async_api import async_playwright
from typing import Optional, Dict, Any, List

load_dotenv()

mcp = FastMCP("scholar")

SCHOLAR_URL = "https://google.serper.dev/scholar"
LOG_FILE = "scholar_log.json"


async def log_to_file(log_entry: Dict[str, Any]):
    """
    Log an entry to the JSON log file.
    
    Args:
        log_entry (Dict[str, Any]): The log entry to append to the log file
    """
    # Load existing log if it exists
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, start with an empty list
            logs = []
    
    # Append new log entry
    logs.append(log_entry)
    
    # Write updated logs back to file
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)


async def log_abstract_request(url: str, publisher: str, abstract: Optional[str]):
    """
    Log the abstract request details to the log file.
    
    Args:
        url (str): The URL of the paper
        publisher (str): The publisher name
        abstract (Optional[str]): The fetched abstract or None if not found
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "abstract",
        "url": url,
        "publisher": publisher,
        "success": abstract is not None,
        "abstract_length": len(abstract) if abstract else 0,
        "abstract": abstract
    }
    
    await log_to_file(log_entry)


async def log_search_request(query: str, articles: List[Dict[str, Any]]):
    """
    Log the search query and results to the log file.
    
    Args:
        query (str): The search query
        articles (List[Dict[str, Any]]): The articles found
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "search",
        "query": query,
        "results_count": len(articles) if isinstance(articles, list) else 0,
        "results": articles if isinstance(articles, list) else []
    }
    
    await log_to_file(log_entry)


async def fetch_abstract(url: str, publisher: str) -> Optional[str]:
    """
    Fetch the abstract from a research paper URL.

    Args:
        url (str): The URL of the research paper
        publisher (str): The publisher of the paper ('acm', 'ieee', 'researchgate', 'springer', or 'sciencedirect')

    Returns:
        Optional[str]: The abstract text if found, None otherwise
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=50)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        try:
            await page.goto(url)
            content = await page.content()
            selector = Selector(text=content)

            # Define selectors for each publisher
            selectors = {
                'acm': [
                    'section#abstract[property="abstract"] div[role="paragraph"]::text',
                    '.issue-item__abstract p::text',
                    '.abstractSection p::text',
                    'div[property="description"] p::text'
                ],
                'ieee': [
                    'meta[property="twitter:description"]::attr(content)'
                ],
                'researchgate': [
                    '.research-detail-middle-section__abstract::text'
                ],
                'springer': [
                    '#Abs1-section::text'
                ],
                'sciencedirect': [
                    '.abstract.author::text'
                ]
            }

            # Get the appropriate selectors for the publisher
            publisher_selectors = selectors.get(publisher.lower())
            if not publisher_selectors:
                raise ValueError(f"Unsupported publisher: {publisher}")

            # Try each selector until we find the abstract
            abstract = None
            for selector_pattern in publisher_selectors:
                abstract = selector.css(selector_pattern).get()
                if abstract:
                    break
                    
            # Log the request regardless of success
            await log_abstract_request(url, publisher, abstract)
            
            return abstract

        finally:
            await browser.close()


async def search_scholar(query: str) -> dict | None:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError(
            "SERPER_API_KEY is not set in the environment variables.")

    payload = json.dumps({"q": query})

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SCHOLAR_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}


@mcp.tool()
async def get_scholarly_articles(query: str, limit: int = 10):
    """
    Search Google Scholar for scholarly articles on a given query.

    Args:
        query: The search query (e.g. "machine learning")
        limit: Maximum number of articles to return (default: 10)

    Returns:
        List of scholarly articles with title, authors, publication, and link
    """
    results = await search_scholar(query)

    if not results or "organic" not in results or len(results["organic"]) == 0:
        await log_search_request(query, [])
        return "No scholarly articles found"

    articles = []

    for i, result in enumerate(results["organic"]):
        if i >= limit:
            break

        article = {
            "title": result.get("title", "No title"),
            "authors": result.get("publicationInfo", "Unknown authors"),
            "publication": result.get("publicationInfo", "Unknown publication"),
            "year": result.get("year", "Unknown year"),
            "link": result.get("link", "No link available"),
            "snippet": result.get("snippet", "No snippet available"),
            "citedBy": result.get("citedBy", 0)
        }

        articles.append(article)
    
    # Log the search request and results
    await log_search_request(query, articles)

    return json.dumps(articles, indent=2)


@mcp.tool()
async def get_paper_abstract(url: str, publisher: str) -> str:
    """
    Fetch the abstract from a research paper URL.

    Args:
        url (str): The URL of the research paper
        publisher (str): The publisher of the paper ('acm', 'ieee', 'researchgate', 'springer', or 'sciencedirect')

    Returns:
        str: The abstract text if found, or an error message if not found
    """
    try:
        abstract = await fetch_abstract(url, publisher)
        if abstract:
            return abstract
        return "Could not find abstract for the given paper"
    except Exception as e:
        return f"Error fetching abstract: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
