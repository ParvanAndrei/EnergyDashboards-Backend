from typing import Union
from fastapi import FastAPI
from fastapi_keycloak_middleware import KeycloakConfiguration, KeycloakMiddleware

 # Set up Keycloak
keycloak_config = KeycloakConfiguration(
     url="https://sso.your-keycloak.com/auth/",
     realm="<Realm Name>",
     client_id="<Client ID>",
     client_secret="<Client Secret>",
     authentication_scheme="Token"
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}