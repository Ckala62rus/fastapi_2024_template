from pathlib import Path

import uvicorn

from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', reload=True)
    except Exception as e:
        raise e
