from fastapi.security import OAuth2PasswordBearer

# tokenUrl should point to the endpoint that issues the token
# In our case, it's /api/v1/users/auth/token (relative to the root of the API)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth/token")
