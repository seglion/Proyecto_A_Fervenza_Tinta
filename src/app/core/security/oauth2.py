from fastapi.security import OAuth2PasswordBearer

# tokenUrl should point to the endpoint that issues the token
# In our case, it's /users/auth/token (relative to the root of the API)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth/token")
