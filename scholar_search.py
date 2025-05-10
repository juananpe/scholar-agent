from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
import datetime
from typing import Dict, Any, List

load_dotenv()

mcp = FastMCP("scholar")

SCHOLAR_URL = "https://google.serper.dev/scholar"
LOG_FILE = "/tmp/scholar_log.json"


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



if __name__ == "__main__":
    mcp.run(transport="stdio")
