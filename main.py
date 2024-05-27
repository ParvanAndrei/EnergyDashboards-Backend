from fastapi import FastAPI, Header, Depends, Request, Response
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from datetime import date



# from routes import todos
# from fastapi_keycloak_middleware import KeycloakConfiguration, KeycloakMiddleware

origins = [
    "*",
    "http://localhost:3000"
]

app = FastAPI()
# app.include_router(todos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/accestoken")
def read_headers(request: Request):
    return dict(request.headers)

# @app.get("/accestoken")
# # def protected_route(token: str = Depends(get_access_token)):
# def protected_route(request: Request):
#     # print("TOKEN HERE ", token)
#     username = request.headers.get("OIDC_preferred_username")
#     given_name = request.headers.get("X-User-Given-Name")
#     family_name = request.headers.get("X-User-Family-Name")
#     # return {"token": token}
#     return {"username": username,
#             "given_name" : given_name,
#             "familit_name" : family_name
#             }

# @app.get("/accestoken")
# def get_access_token(request: Request):
#     access_token = request.headers.get("OIDC_preferred_username")
#     print(request.headers)
#     # family_name = request.headers.get("X-User-Family-Name")
#     # given_name = request.headers.get("X-User-Given-Name")
#     # username = request.headers.get("X-User-Username")
#     # print("THIS IS GIVEN NAME FROM HEADER", given_name)
#     # print("THIS IS FAMILY NAME FROM HEADER", family_name)
#     return {
#         "access_token": access_token
#         # "family_name": family_name,
#         # "given_name": given_name,
#         # "username": username
#     }

@app.get("/energy-consumption-per-minute")
def root(start_date, end_date):
    endpoint = f"https://api-electrify.promptyapi.com/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_MINUTE"
    header = {'accept': 'application/json'}
    # r = requests.get(url="https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date=2024-03-01&end_date=2024-04-01&granularity=ONE_DAY", headers=header)
    response = requests.get(url=endpoint, headers=header)
    if response.status_code == 200:
        try:
            raw_data = response.json()
            processed_data = [{"value": item["value"], "timestamp": item["timestamp"]} for item in raw_data]
            return processed_data
        except Exception as e:
            return {"error": f"Failed to parse JSON: {e}"}
    else:
        return {"error": f"Status code {response.status_code} received"} 
    
@app.get("/energy-consumption-per-hour")
def root(start_date, end_date):
    endpoint = f"https://api-electrify.promptyapi.com/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_HOUR"
    header = {'accept': 'application/json'}
    # r = requests.get(url="https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date=2024-03-01&end_date=2024-04-01&granularity=ONE_DAY", headers=header)
    r = requests.get(url=endpoint, headers=header)
    if r.status_code == 200:
        try:
            data = r.json()
            return data
        except Exception as e:
            return {"error": f"Failed to parse JSON: {e}"}
    else:
        return {"error": f"Status code {r.status_code} received"} 

@app.get("/energy-consumption-per-day")
def root(start_date, end_date):
    endpoint = f"https://api-electrify.promptyapi.com/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_DAY"
    header = {'accept': 'application/json'}
    response = requests.get(url=endpoint, headers=header)
    if response.status_code == 200:
        try:
            raw_data = response.json()
            processed_data = [{"value": item["value"], "timestamp": item["timestamp"]} for item in raw_data]
            return processed_data
        except Exception as e:
            return {"error": f"Failed to parse JSON: {e}"}
    else:
        return {"error": f"Status code {response.status_code} received"} 

@app.get("/energy-consumption-per-month")
def root():
    today = date.today()
    firstMonthOfTheYear = today.replace(month=1, day=1)
    endpoint = f"https://api-electrify.promptyapi.com/api/v1/energy/energy_monitoring_total?start_date={firstMonthOfTheYear}&end_date={today}&granularity=ONE_MONTH"
    header = {'accept': 'application/json'}
    response = requests.get(url= endpoint, headers=header)
    if response.status_code == 200:
        try:
            raw_data = response.json()
            processed_data = [{"value": item["value"], "timestamp": item["timestamp"]} for item in raw_data]
            return processed_data
        except Exception as e:
            return {"error": f"Failed to parse JSON: {e}"}
    else:
        return {"error": f"Status code {response.status_code} received"} 
    
