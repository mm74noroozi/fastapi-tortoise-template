from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import (OAuth2PasswordBearer,
                              OAuth2PasswordRequestForm,
                              SecurityScopes)
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from models import ProductPydantic, ProductInPydantic, Product
from jose import jwt, JWTError
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from config import Config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


register_tortoise(app, db_url=Config.DB_URL, modules={'models': ['models']},
                  generate_schemas=True, add_exception_handlers=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth(scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
    except JWTError:
        # log it
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    print(scopes)
    # check token expiration ...
    # check the scope ...
    return payload


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # check the login and get the user
    # user = ...
    user = {"username": form_data.username, "email": "example@gmail.com"}
    token = jwt.encode(user, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/create-product", response_model=ProductPydantic)
async def create_product(productIn: ProductInPydantic, _=Security(get_auth,
                                                                  scopes=["Product:Create"])):
    product = await Product.create(**productIn.model_dump(exclude_unset=True))
    return product


@app.get("/products", response_model=list[ProductPydantic])
async def get_products(_=Security(get_auth, scopes=["Product:List"])):
    # should be Paginate using fastapi Pagination
    products = await Product.all()
    return products

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
