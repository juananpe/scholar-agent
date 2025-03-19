import asyncio
import os
from dotenv import load_dotenv

from scholar_search import get_scholarly_articles

# Load environment variables
load_dotenv()

async def test_scholar_search():
    # Check for API key
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("Error: SERPER_API_KEY not found in environment variables")
        return
    
    # Get scholarly articles with a simple query
    print("Searching for 'project based learning in software engineering' articles...")
    results = await get_scholarly_articles("project based learning in software engineering", limit=5)
    
    # Print the results
    print("\nResults:")
    print(results)

if __name__ == "__main__":
    asyncio.run(test_scholar_search()) 