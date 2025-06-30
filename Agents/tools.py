from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = 'research.txt'):
    timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    formatted_text = f"\n---------------------- RESEARCH OUTPUT ----------------------\nTIMESTAMP: {timestamp}\n\n{data}\n\n"
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(formatted_text)
    print(f"✅ Successfully saved to {filename}")

save_tool = Tool(
    name='save_text_to_file',
    func=save_to_txt,
    description="Use this tool to save the final research summary to a text file."
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name='search',
    func=search.run,
    description="Search the web for information."
)

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
