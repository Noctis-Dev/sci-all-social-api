from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from transformers import pipeline

from gemini.gemini import get_access_token
from service import gemini_service
from service import layoutlm_service
from broker.rabbit_broker import message_producer
from persistance.database import engine, metadata, database
from web import publication_controller, metadata_controller, comment_controller

metadata.create_all(engine)


app = FastAPI()
app.include_router(publication_controller.router, prefix="/api/v1/publications")
app.include_router(metadata_controller.router, prefix="/api/v1/metadata")
app.include_router(comment_controller.router, prefix="/api/v1/comments")


@app.get("/health")
async def health():
    return "OK"


@app.on_event("startup")
async def startup():
    await database.connect()
    gemini_service.access_token = get_access_token()
    layoutlm_service.model = pipeline(
        'question-answering',
        model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        tokenizer=('mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es')
    )


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    message_producer.close_connection()

