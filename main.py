'''
core file for start app
'''

from fastapi import Body, FastAPI, Query, status, HTTPException, Path, UploadFile, File, Depends

app = FastAPI()

'''
╭──────────────────────────────────────────────╮
│                  Import Routers              │
╰──────────────────────────────────────────────╯
'''

from app.routers import customers