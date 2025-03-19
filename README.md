# Scholar Search MCP Server

A tool for searching scholarly articles using Google Scholar's search results through the Serper API.

## Features

- Search Google Scholar for scholarly articles
- Retrieve publication details including title, authors, publication info, and citation counts
- Fetch abstracts from research papers (supports ACM, IEEE, and ResearchGate)

## Setup

1. Install dependencies:

```bash
pip install -e .
# or
pip install mcp python-dotenv httpx parsel playwright
```

2. Setup Playwright (required for abstract extraction):

```bash
playwright install chromium
```

3. Create a `.env` file with your Serper API key:

```
SERPER_API_KEY=your_api_key_here
```

4. Run the MCP server:

```bash
python scholar_search.py
```

## Testing

You can test the functionality with the included test script:

```bash
python test_scholar_search.py
```

This will perform a search for example queries and display the results.

## API Reference

### `get_scholarly_articles(query: str, limit: int = 10)`

Searches Google Scholar for scholarly articles matching the query.

**Parameters:**
- `query`: Search term (e.g., "machine learning")
- `limit`: Maximum number of results to return (default: 10)

**Returns:** JSON string with article details including title, authors, publication info, and links.

### `get_paper_abstract(url: str, publisher: str)`

Extracts the abstract from a research paper's URL.

**Parameters:**
- `url`: URL of the research paper
- `publisher`: Publisher platform ('acm', 'ieee', or 'researchgate')

**Returns:** The paper's abstract if found, or an error message.
