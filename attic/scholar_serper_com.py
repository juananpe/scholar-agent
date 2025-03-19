from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from serpapi.google_search import GoogleSearch
import os
load_dotenv()

mcp = FastMCP("scholar")

@mcp.tool()
async def search_google_scholar(query: str):
    """
    Search Google Scholar for academic papers and references.
    
    Args:
        query: The search query (e.g. "machine learning 2023")
        
    Returns:
        A list of academic references with titles, authors, and citations
    """
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY is not set in the environment variables.")
    
    params = {
        "engine": "google_scholar",
        "q": query,
        "hl": "en",
        "num": 10,
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    print(results)
    
    if not results or "organic_results" not in results or not results["organic_results"]:
        return "No results found"
    
    formatted_results = []
    for result in results["organic_results"]:
        publication_info = result.get("publication_info", {})
        formatted_result = {
            "title": result.get("title", "No title"),
            "link": result.get("link", "No link"),
            "snippet": result.get("snippet", "No snippet"),
            "publication_info": publication_info.get("summary", "No publication info")
        }
        
        # Add citation count if available
        if "inline_links" in result and "cited_by" in result["inline_links"]:
            formatted_result["cited_by"] = result["inline_links"]["cited_by"].get("total", 0)
        
        formatted_results.append(formatted_result)
    
    return formatted_results

if __name__ == "__main__":
    mcp.run(transport="stdio") 