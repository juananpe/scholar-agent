# MCP Server Examples

This repository contains example MCP server implementations for various APIs.

## Google Scholar Search Tool

The `scholar.py` script demonstrates how to use the SerpAPI Google Scholar API with MCP.

### Setup

1. Install dependencies:

```bash
pip install -e .
# or
pip install mcp python-dotenv google-search-results
```

2. Create a `.env` file with your SerpAPI key:

```
SERPER_API_KEY=your_api_key_here
```

3. Run the MCP server:

```bash
python scholar.py
```

### Testing

You can test the Google Scholar search functionality with the included test script:

```bash
python test_scholar.py
```

This will perform searches for several example queries and display the results.

## Documentation Search Tool

The `main.py` script provides an MCP server for searching documentation across multiple libraries.

### Setup

1. Install dependencies (if not already installed):

```bash
pip install -e .
```

2. Set up your API key in the `.env` file:

```
SERPER_API_KEY=your_api_key_here
```

3. Run the MCP server:

```bash
python main.py
```

## Using in Applications

These MCP servers can be used with any MCP-compatible client. For example, to call the Google Scholar search:

```python
from mcp.client import MCPClient

# Connect to the Scholar MCP server
client = MCPClient("scholar")

# Search for academic papers
results = await client.search_google_scholar("quantum computing algorithms")
```

See the [MCP documentation](https://mcp.ai) for more details on using MCP clients.
