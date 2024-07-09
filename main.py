import uvicorn
from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.log.logger import logger


app = FastAPI(debug=True)

app.include_router(auth_router)


@app.get('/')
async def root():
    return {'message': 'This is root directory'}

if __name__ == '__main__':
    logger.info('Starting server...')
    uvicorn.run(app, host='127.0.0.1',
                port=8080)
