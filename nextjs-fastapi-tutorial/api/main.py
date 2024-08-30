from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https:localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],

)

@app.get('/')
def health_check():
    return 'Health check complete'