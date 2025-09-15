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


### Easy install in VSCode

[vscode:mcp link](vscode:mcp/install?%7B%22name%22%3A%22scholar_search%22%2C%22command%22%3A%22uv%22%2C%22args%22%3A%5B%22--directory%22%2C%22%2Fopt%2Fscholar-agent%22%2C%22run%22%2C%22scholar_search.py%22%5D%7D)

### Prompt suggestions

- get 5 articles about AI Agents in Software Engineering
- for each article, use playwright tools to extract its abstract and write them in abstracts.md
- generate a .bib file using the references that we have obtained
- generate an intro.tex about AI Agents in Software Engineering, referencing the 5 articles