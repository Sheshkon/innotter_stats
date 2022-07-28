from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

import jwt

from app.config import settings


class AuthorizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in ['/docs', 'openapi.json']:
            return await call_next(request)
        if request.method == 'OPTIONS':
            return await call_next(request)

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    'detail': 'Is not authenticated. Not found Authorization header.'
                }
            )
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail': 'Access_token expired.'}
            )
        except IndexError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail': 'Token prefix missing.'}
            )

        request.state.user_id = payload.get('user_id')
        return await call_next(request)
