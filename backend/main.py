from pathlib import Path

import uvicorn

from core.register import register_app

app = register_app()

if __name__ == '__main__':
    try:
        uvicorn.run(app=f'{Path(__file__).stem}:app', reload=True, port=5001)
    except Exception as e:
        raise e
