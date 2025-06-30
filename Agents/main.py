from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool,save_to_txt

load_dotenv()

# Set up LLM
llm = ChatOpenAI(model='gpt-3.5-turbo')

# Define output schema
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
("system",
"""
You are a research assistant that helps generate a research paper.
You MUST use the tool 'save_text_to_file' to save your final summary to disk.

Wrap your final output as a valid JSON object in the format below:

{format_instructions}

⚠️ DO NOT include extra explanation or natural language. Only return the JSON object with actual values.
For example:

{{
  "topic": "Satellites",
  "summary": "Satellites are devices used for communication...",
  "source": ["https://en.wikipedia.org/wiki/Satellite"],
  "tools": ["wikipedia", "save_text_to_file"]
}}
"""),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

# Tools list
tools = [search_tool, wiki_tool, save_tool]

# Create the agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Main loop
while True:
    query = input('\nWhat can I help you research? (type "exit" to quit)\n> ')
    if query.lower() in ["exit", "quit"]:
        print("Goodbye! It was nice chatting with you")
        break

    try:
        raw_response = agent_executor.invoke({'query': query})
        parsed = parser.parse(raw_response.get('output'))

        print("\n--------------- SUMMARY ---------------")
        print(parsed.summary)

        # Save manually (optional fallback)
        save_to_txt(parsed.summary)

    except Exception as e:
        print("\n⚠️ Error parsing agent output:")
        print(e)
