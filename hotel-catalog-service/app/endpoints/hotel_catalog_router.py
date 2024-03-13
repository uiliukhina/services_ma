import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

import keycloak
from keycloak import KeycloakOpenID
from typing import Optional, Callable

from app.auth.keycloak_auth import KeycloakAuthenticator
from app.creds import *

from functools import wraps
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.models.hotel import Hotel, CreateHotelRequest
# from app.rabbitmq import send_booking
from app.services.hotel_catalog_service import HotelCatalogService

hotel_catalog_router = APIRouter(prefix='/hotel-catalog', tags=['HotelCatalog'])

name = 'HotelCatalog with Booking Service'

keycloak_authenticator = KeycloakAuthenticator()

access_tokens = {}

keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=keycloak_client_id,
    client_secret_key=keycloak_client_secret,
    realm_name="ilukhina",
    verify=False
)


def get_current_user(token: str):
    try:
        user_info = keycloak_openid.userinfo(token=token)
    except keycloak.exceptions.KeycloakAuthenticationError:
        raise HTTPException(status_code=403, detail={"details:": "Your access token is not valid"})

    return user_info


@hotel_catalog_router.get("/login")
def login(request: Request):
    response_content = keycloak_authenticator.login()
    return response_content

@hotel_catalog_router.get("/logout")
async def logout(request: Request):

    logout_url = keycloak_authenticator.logout()
    return RedirectResponse(logout_url)

@hotel_catalog_router.get("/callback")
async def callback(request: Request):
    access_token = await keycloak_authenticator.callback(request)
    user_info = get_current_user(access_token)

    print("user_info: " + user_info.__str__())
    access_tokens.update({access_token: user_info})

    user = get_current_user(access_token)

    print("use: " + user.__str__())

    realm_access = user.get("realm_access", [])
    print(realm_access)
    roles = realm_access.get("roles", [])

    response_message = f"""
    <html>
    <head>
    <style>
    .center {{
        text-align: center;
        margin-top: 20%;
        font-size: 36px; 
    }}
    </style>
    </head>
    <body>
    <div class="center">{access_token}</div>
    </body>
    </html>
    """

    return HTMLResponse(response_message)


def keycloak_security(required_roles: Optional[list] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
                *args,
                **kwargs):

            token = kwargs.get("token")

            if token:
                user = get_current_user(token)

                realm_access = user.get("realm_access", [])
                roles = realm_access.get("roles", [])

                if not any(role in roles for role in required_roles):
                    error_message = f"""
                                                                                   <html>
                                                                                       <head>
                                                                                           <title>Insufficient permissions</title>
                                                                                           <style>
                                                                                               body {{
                                                                                                   font-size: 27px;
                                                                                                   color: black;
                                                                                                   text-align: center;
                                                                                               }}
                                                                                           </style>
                                                                                       </head>
                                                                                       <body>
                                                                                           <p>Permission for your role denied</p>
                                                                                           <p>You may use service only with next roles: {roles}</p>
                                                                                           <a href="http://localhost:80/hotel-api/hotel-catalog/login">Login</a>
                                                                                       </body>
                                                                                   </html>
                                                                               """
                    return HTMLResponse(content=error_message, status_code=403)

            else:
                error_message = f"""
                                                               <html>
                                                                   <head>
                                                                       <title>Unauthorized Access</title>
                                                                       <style>
                                                                           body {{
                                                                               font-size: 33px;
                                                                               color: red;
                                                                               text-align: center;
                                                                           }}
                                                                       </style>
                                                                   </head>
                                                                   <body>
                                                                       <p>You're not authorized. Please login with this URL first:</p>
                                                                       <a href="http://localhost:80/hotel-api/hotel-catalog/login">Login</a>
                                                                   </body>
                                                               </html>
                                                           """
                return HTMLResponse(content=error_message, status_code=403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


@hotel_catalog_router.get('/')
@keycloak_security(["admin", "user"])
def get_hotels(hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService),
              token: str = None) -> list[Hotel]:
    return hotel_catalog_service.get_hotels()


@hotel_catalog_router.get('/{hotel_id}')
@keycloak_security(["admin", "user"])
def get_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService),
              token: str = None) -> Hotel:
    hotel = hotel_catalog_service.get_hotel_by_id(hotel_id)
    if hotel:
        return hotel.dict()
    else:
        raise HTTPException(404, f'Hotel with id={hotel_id} not found')


@hotel_catalog_router.post('/add')
@keycloak_security(["admin"])
def add_hotel(request: CreateHotelRequest,
              hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService),
              token: str = None) -> Hotel:
    new_hotel = hotel_catalog_service.add_hotel(
        name=request.name,
        city=request.city,
        image_url=request.image_url,
        description=request.description)

    user_id = uuid.uuid4()

    return new_hotel.dict()


@hotel_catalog_router.put('/update/{hotel_id}')
@keycloak_security(["admin"])
def update_hotel(hotel_id: UUID, request: CreateHotelRequest,
                 hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService),
              token: str = None) -> Hotel:
    updated_hotel = hotel_catalog_service.update_hotel(hotel_id, request.name, request.image_url, request.city,
                                                       request.description)
    return updated_hotel.dict()


@hotel_catalog_router.delete('/delete/{hotel_id}')
@keycloak_security(["admin"])
def delete_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService),
              token: str = None) -> None:
    hotel_catalog_service.delete_hotel(hotel_id)
    return {'message': 'Hotel deleted successfully'}
