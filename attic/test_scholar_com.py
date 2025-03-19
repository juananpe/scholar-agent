import asyncio
from dotenv import load_dotenv
import os
import json
import sys

# Import the search_google_scholar function from scholar.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scholar_serper_com import search_google_scholar

async def test_search():
    """Test the Google Scholar search functionality."""
    # Load environment variables
    load_dotenv()
    
    # Check if the API key is set
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("Error: SERPER_API_KEY is not set in the environment variables.")
        print("Please set it in your .env file.")
        return
    
    # Test queries
    test_queries = [
        "project based learning in software engineering",
        "climate change impact on agriculture",
        "quantum computing algorithms"
    ]
    
    # Run tests for each query
    for query in test_queries:
        print(f"\nSearching for: {query}")
        try:
            results = await search_google_scholar(query)
            
            if isinstance(results, str) and results == "No results found":
                print(f"No results found for query: {query}")
            else:
                print(f"Found {len(results)} results")
                
                # Print first result details
                if results:
                    first_result = results[0]
                    print(f"\nTop result:")
                    print(f"Title: {first_result.get('title')}")
                    print(f"Publication: {first_result.get('publication_info')}")
                    if 'cited_by' in first_result:
                        print(f"Cited by: {first_result.get('cited_by')} papers")
                    print(f"Link: {first_result.get('link')}")
        except Exception as e:
            print(f"Error searching for {query}: {str(e)}")
    
if __name__ == "__main__":
    asyncio.run(test_search()) 