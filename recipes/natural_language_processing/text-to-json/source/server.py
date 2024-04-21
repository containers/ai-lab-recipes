from fastapi import FastAPI
from langserve import add_routes

from __main__ import no_download_json_chain


app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

add_routes(app, no_download_json_chain())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)