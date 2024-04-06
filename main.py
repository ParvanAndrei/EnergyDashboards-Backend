from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import date

# from routes import todos
# from fastapi_keycloak_middleware import KeycloakConfiguration, KeycloakMiddleware

origins = [
    "*",
]

 # Set up Keycloak
# keycloak_config = KeycloakConfiguration(
#      url="https://sso.your-keycloak.com/auth/",
#      realm="<Realm Name>",
#      client_id="<Client ID>",
#      client_secret="<Client Secret>",
#      authentication_scheme="Token"
# )

app = FastAPI()
# app.include_router(todos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.get("/energy-consumption-per-minute")
def root(start_date, end_date):
    endpoint = f"https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_MINUTE"
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
    endpoint = f"https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_HOUR"
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
    endpoint = f"https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date={start_date}&end_date={end_date}&granularity=ONE_DAY"
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
    endpoint = f"https://electrify-backend-production.up.railway.app/api/v1/energy/energy_monitoring_total?start_date={firstMonthOfTheYear}&end_date={today}&granularity=ONE_MONTH"
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
        return {"error": f"Status code {r.status_code} received"} 
    
