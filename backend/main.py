from pathlib import Path

import uvicorn

from common.log import log
from core.register import register_app

app = register_app()


@app.get("/")
def read_root():
    log.info("testing logging info")
    log.error("testing logging with error2")
    a = 2 + 30
    return {"Hello": f"World123 {a}"}


if __name__ == '__main__':
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', reload=True, port=5001)
    except Exception as e:
        raise e
