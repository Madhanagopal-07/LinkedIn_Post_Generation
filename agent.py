import getpass
import os

from langchain.chat_models import init_chat_model
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

from typing import TypedDict,List
from dotenv import load_dotenv

_ = load_dotenv()

model = init_chat_model("gemini-2.5-flash", 
                        model_provider="google_genai"
                       )

tavily_search_tool = TavilySearch(
                        max_results=5,
                        topic="general",
                        include_images=True
                    )

class SearchResponse(TypedDict):
    urls: List[str]
    images: List[str]
    content: str
    tags: List[str]


def search_agent(input):
    template = '''  Please search for this {topic}.
                    Generate a LinkedIn post about {topic}. No preamble.
                    Keep the tone professional, engaging, and concise. 
                    Present the key points in a point-wise format using the symbol 🔹.
                    End with an insight or call-to-action that encourages discussion.
                    Also, suggest 3 to 5 relevant LinkedIn hashtags for the post.'''
    
    agent = create_react_agent(
                                model=model,
                                tools=[tavily_search_tool],
                                prompt = template,
                                response_format=SearchResponse
                            )
    response = agent.invoke(
                            {"messages": [{"role": "user", "content": input}]}
                            )
    return response['structured_response']

#if __name__ =="__main__":
    #print(search_agent("Artificial intelligence")['content'])