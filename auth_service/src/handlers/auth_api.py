from __future__ import annotations

import json
import uuid
from uuid import UUID
from typing import List, Optional
import aiohttp

from fastapi import FastAPI, Depends, HTTPException, UploadFile, Body
from fastapi.security.http import HTTPAuthorizationCredentials


app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.get("/login")
async def login():
    pass


@app.get("/register")
async def register():
    pass


@app.get("/get_id_by_token")
async def get_id_by_token(token: HTTPAuthorizationCredentials):
    pass
