# fastapi-auth
Standard authorization method from fastapi documentation

## Dependencies
- python-multipart
- pydantic
- python-jose
- passlib
- bcrypt

### Requirements
You must have a class with a config in the system, which will be located in the app.core.config path.

This architecture is based on the analogy with the project
https://github.com/tiangolo/full-stack-fastapi-postgresql

app.core.config
```sh
import secrets
from pydantic import BaseSettings

class Settings(BaseSettings)
    API_URL: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)  # Return a random URL-safe text string, in Base64 encoding
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8   # 60 minutes * 24 hours * 8 days = 8 days
```

### Using
#### Creating access token
Token for auth headers
```sh
from fastapi_auth.schemas import Token
from fastapi_auth.security import create_access_token

test_subject_id = 1
return Token(
        access_token=create_access_token(test_subject_id),
        token_type="bearer"
    )
```
Token for auth-cookie with httpOnly
```sh
from fastapi_auth.schemas import Token
from fastapi_auth.security import create_access_token, create_cookie

access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
token = create_access_token(user['id'], expires_delta=access_token_expires)
return create_cookie(token) or create_cookie_with_redirect(path, token)
```

#### Get current sub_id
Get sub in token
https://fastapi.tiangolo.com/tutorial/security/first-steps/
```sh
from fastapi_auth.deps import get_subject_from_token

@router.get("/login/test-token")
def test_token(current_subject_id: int = Depends(get_subject_from_token))
```
Get sub in auth-cookie with httpOnly
```sh
from fastapi_auth.deps import get_subject_from_cookie

@router.get("/login/test-cookie")
async def test_cookie(current_subject_id: int = Depends(get_subject_from_cookie)):
```
