import json
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError
from pydantic import BaseModel

from src.keycloak_client import keycloak_client

app = FastAPI()

idp = KeycloakOpenID(
    server_url="http://localhost:9080/auth/",
    realm_name="platform",
    client_id="test",
    client_secret_key="",
)


class Credentials(BaseModel):
    username: str = "manhpt"
    password: str = "1"


class RefreshCredentials(BaseModel):
    refresh_token: str


@app.post("/token", tags=["public-endpoint"])
async def get_token(credentials: Credentials):
    try:
        token = idp.token(
            username=credentials.username,
            password=credentials.password,
        )
        return token
    except KeycloakError as error:
        raise HTTPException(
            status_code=error.response_code, detail=json.loads(error.error_message)
        )


@app.post("/refresh_token", tags=["secured-endpoint"])
async def refresh_token(credentials: RefreshCredentials):
    try:
        token = idp.refresh_token(credentials.refresh_token)
        return token
    except KeycloakError as error:
        raise HTTPException(
            status_code=error.response_code, detail=json.loads(error.error_message)
        )


@app.get("/me", tags=["secured-endpoint"])
async def get_me(
    token: Optional[str] = Depends(APIKeyHeader(name="token", auto_error=False))
):
    try:
        return idp.userinfo(token)
    except KeycloakError as error:
        raise HTTPException(
            status_code=error.response_code, detail=json.loads(error.error_message)
        )


@app.get("/rpt", tags=["secured-endpoint"])
async def get_uma(
    token: Optional[str] = Depends(APIKeyHeader(name="token", auto_error=False))
):
    response = await keycloak_client.post(
        "/auth/realms/vinbase/protocol/openid-connect/token",
        headers={
            "Authorization": f"Bearer {token}",
        },
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": "test",
        },
    )
    return response.json()
