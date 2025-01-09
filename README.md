# Search Web Tool
This is a Naptha tool module for searching web using the Serper API. The tool returns the title, webpage url for a given query. Tool modules can be run independently or used by agents.

## Usage

Make sure `SERPER_API_KEY` is not empty in the .env file

**Available parametes**
```bash
tool_name - search_web_tool for web search and search_news_tool for articles
query - Search query
location (optional) - Short hand of country name (United Kingdom - uk)
date (optional) -   h (past hour)
                    d (past day)
                    w (past week)
                    m (past month)
                    y (past year)
```

### Run the Tool

**Search web for news articles**
```bash
naptha run tool:search_news_tool -p "tool_name=search_web_tool query=NapthaAI"
```

**Search web for given query**
```bash
naptha run tool:search_web_tool -p "tool_name=search_web_tool query=NapthaAI"
```