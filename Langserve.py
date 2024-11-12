from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="gemma2-9b-it",api_key=groq_api_key)


# instead of the above method we can use prompt templates
from langchain_core.prompts import ChatPromptTemplate
generic = "Translate the following into {language}"

prompt = ChatPromptTemplate([
    ("system", generic), ("user","{text}")
])


parser = StrOutputParser()
chain = prompt|model|parser

#App Definition

app = FastAPI(title="Langchain Server",
              version="1.0",
              description= "A simple API server using Langchain runnable interfaces")

# adding chain routes
add_routes(
    app,chain,path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host = "127.0.0.1",port=8000)


