import asyncio
import os
from dotenv import load_dotenv

from scholar_search import get_paper_abstract

# Load environment variables
load_dotenv()

async def test_abstract_grabber():
    # Check for API key
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("Error: SERPER_API_KEY not found in environment variables")
        return
    
    # Test cases for different publishers
    test_cases = [
        # ACM paper
        {"url": "https://dl.acm.org/doi/10.1145/3408877.3432461", "publisher": "acm"},
        # IEEE paper
        {"url": "https://ieeexplore.ieee.org/document/9306593", "publisher": "ieee"},
        # ResearchGate paper
        {"url": "https://www.researchgate.net/publication/341727879_Teaching_Computer_Science_at_K-12_Level_with_Project-Based_Learning_Pedagogy", "publisher": "researchgate"}
    ]
    
    # Run tests for each case
    for i, test_case in enumerate(test_cases):
        print(f"\nTest case {i+1}: {test_case['publisher'].upper()} paper")
        print(f"URL: {test_case['url']}")
        try:
            abstract = await get_paper_abstract(test_case['url'], test_case['publisher'])
            print("\nAbstract:")
            print(abstract)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_abstract_grabber()) 