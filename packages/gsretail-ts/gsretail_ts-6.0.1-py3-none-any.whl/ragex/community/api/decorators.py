from functools import wraps
from inspect import isawaitable
from typing import Text, Callable, Optional, Union, Tuple

import sanic_jwt.utils as sanic_jwt_utils
from jsonschema import validate, ValidationError
from sanic import Blueprint
from sanic_jwt import exceptions
from sanic_jwt.decorators import instant_config
from sanic_jwt.validators import validate_scopes

from ragex.community import config
from ragex.community.api import json_schema
from ragex.community.constants import REQUEST_DB_SESSION_KEY
from ragex.community.services.role_service import normalise_permissions
from ragex.community.services.user_service import UserService
from ragex.community.utils import default_arg, error


def inject_rasa_x_user(
    initialized_on=None, allow_api_token=False, extract_user_from_jwt=False, **kw
):
    """Adapted from sanic_jwt.decorators.inject_user"""

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if initialized_on and isinstance(initialized_on, Blueprint):
                instance = initialized_on
            else:
                instance = request.app

            with instant_config(instance, request=request, **kw):
                if allow_api_token:
                    try:
                        payload = instance.auth.extract_payload(request, verify=False)
                    except Exception as _:
                        payload = None
                else:
                    payload = instance.auth.extract_payload(request, verify=False)

                user = await instance.auth.retrieve_user(
                    request, payload, allow_api_token, extract_user_from_jwt
                )

                response = f(request, user=user, *args, **kwargs)
                return await response

        return decorated_function

    return decorator


def rasa_x_scoped(
    scopes: Optional[Union[Tuple[Text], Text]] = None,
    require_all: bool = False,
    require_all_actions: bool = True,
    initialized_on: Blueprint = None,
    allow_api_token: bool = False,
    allow_rasa_x_token: bool = False,
    **kw,
) -> Callable:
    """Adapted from sanic_jwt.decorators.scoped"""

    if isinstance(scopes, str):
        scopes = [scopes]

    scopes = normalise_permissions(scopes)

    async def authorise_user(
        request_args, request_kwargs, instance, reasons, request, status, user_scopes
    ):
        print(f"user_scopes:{user_scopes}")
        # Retrieve the scopes from the payload if not provided
        if not user_scopes:
            user_scopes = instance.auth.extract_scopes(request)

        if user_scopes is None:
            # If there are no defined scopes in the payload,
            # deny access
            is_authorized = False
            status = 403
            reasons = "Invalid scope user scope None"
        else:
            override = instance.auth.override_scope_validator
            destructure = instance.auth.destructure_scopes
            is_authorized = await validate_scopes(
                request,
                scopes,
                user_scopes,
                require_all=require_all,
                require_all_actions=require_all_actions,
                override=override,
                destructure=destructure,
                request_args=request_args,
                request_kwargs=request_kwargs,
            )
            if not is_authorized:

                status = 403
                reasons = "Invalid scope is Autherized False"

        return is_authorized, reasons, status

    def decorator(f):
        async def await_and_return_response(args, kwargs, request):
            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response
            return response

        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            user_service = UserService(request[REQUEST_DB_SESSION_KEY])

            if initialized_on and isinstance(initialized_on, Blueprint):
                instance = initialized_on
            else:
                instance = request.app

            with instant_config(instance, request=request, **kw):
                if request.method == "OPTIONS":
                    return await sanic_jwt_utils.call(f, request, *args, **kwargs)

                is_authenticated = False
                user_scopes = None
                reasons = None
                status = None

                if allow_rasa_x_token:
                    rasa_x_token = default_arg(request, "token", None)
                    if rasa_x_token == config.rasa_x_token:
                        return await await_and_return_response(args, kwargs, request)

                if allow_api_token:
                    # if decorator allows api_tokens for authentication
                    # skip the usual JWT authentication
                    api_token = default_arg(request, "api_token")
                    if api_token:
                        user = user_service.api_token_auth(api_token)
                        is_authenticated = True
                        status = 200
                        permissions = user["permissions"]
                        user_scopes = normalise_permissions(permissions)

                if not is_authenticated:
                    try:
                        (
                            is_authenticated,
                            status,
                            reasons,
                        ) = instance.auth._check_authentication(
                            request, request_args=args, request_kwargs=kwargs
                        )
                    except AttributeError:
                        raise exceptions.SanicJWTException(
                            "Authentication instance not found. Perhaps you "
                            "used @scoped without passing in a blueprint? "
                            "Try @scoped(..., initialized_on=blueprint)",
                            status_code=500,
                        )
                    except exceptions.SanicJWTException as e:
                        status = e.status_code
                        reasons = e.args[0]

                if is_authenticated:
                    is_authorized, reasons, status = await authorise_user(
                        args, kwargs, instance, reasons, request, status, user_scopes
                    )
                else:
                    is_authorized = False

                if is_authorized:
                    # the user is authorized.
                    # run the handler method and return the response
                    # NOTE: it's possible to use return await.utils(f, ...) in
                    # here, but inside the @protected decorator it wont work,
                    # so this is left as is for now
                    return await await_and_return_response(args, kwargs, request)

                else:
                    raise exceptions.Unauthorized(reasons, status_code=status)

        return decorated_function

    return decorator


def validate_schema(schema: Text):
    """Decorator which checks whether a json request body is compliant to a schema."""

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            json_to_validate = request.json
            try:
                validate(json_to_validate, json_schema[schema])

                return await f(request, *args, **kwargs)
            except ValidationError as e:
                return error(
                    400,
                    "WrongSchema",
                    "The payload schema is invalid."
                    # "Please check the API specification at "
                    # "https://rasa.com/docs/rasa-x/api/rasa-x-http-api/ for the correct schema."
                    ,
                    details=e,
                )

        return decorated_function

    return decorator
