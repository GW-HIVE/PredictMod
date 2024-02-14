import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

import logging

logger = logging.getLogger()

def get_csrf(request):
    response = JsonResponse({
        'detail': 'CSRF cookie set',
        'X-CSRFToken': get_token(request),
        })
    # Frustratingly, headers are not available on the JS side...
    # response['X-CSRFToken'] = get_token(request)
    return response

def log_info(request, user):
    logger.debug(f"---> User after authentication: {user}")
    logger.debug(f"---> User type is {type(user)}")

    has_user = hasattr(request, 'user')
    has_session = hasattr(request, 'session')

    logger.debug(f"---> Request user? {has_user}")
    logger.debug(f"---> Request session? {has_session}")
    
    session_keys = {
    "_auth_user_id": "SESSION_KEY",
    "_auth_user_backend": "BACKEND_SESSION_KEY",
    "_auth_user_hash": "HASH_SESSION_KEY",
    }
    for k, v in session_keys.items():
        if k in request.session.keys():
            logger.debug(f"---> Session info - {k}:\n{request.session[k]} (session 'key' {v})")
        else:
            logger.debug(f"---> Key {k} not in session info!! <---")
    logger.debug(f"---> Computed user info: {user._meta.pk.value_to_string(user)}")

    has_session_auth_hash = hasattr(user, "get_session_auth_hash")
    has_backend = hasattr(user, "backend")

    logger.debug(f"---> Has SESSION AUTH HASH? {has_session_auth_hash}")
    logger.debug(f"---> Has BACKEND? {has_backend} --- {user.backend}")

# @require_POST
# @ensure_csrf_cookie
@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({'detail': 'False'}, status=599)
    data = json.loads(request.body)
    logger.debug(f"---> Caught request! Data?: {data}")
    username = data.get('email')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    log_info(request, user)

    logger.debug('='*80)
    session_keys = {
    "_auth_user_id": "SESSION_KEY",
    "_auth_user_backend": "BACKEND_SESSION_KEY",
    "_auth_user_hash": "HASH_SESSION_KEY",
    }
    for k, v in session_keys.items():
        if k in request.session.keys():
            logger.debug(f"---> Session info - {k}:\n{request.session[k]} (session 'key' {v})")
        else:
            logger.debug(f"---> Key {k} not in session info!! <---")
    logger.debug(f"---> Computed user info: {user._meta.pk.value_to_string(user)}")
    logger.debug('='*80)

    login(request, user)

    logger.debug(f"===> User is logged in? {user.is_authenticated}")

    logger.debug('='*80)
    logger.debug(user.__dict__)
    logger.debug('='*80)

    return JsonResponse({'user': user.get_username()})

@csrf_exempt
def create_user_view(request):
    logger.debug(f"---> Got user creation request")
    body = json.loads(request.body)
    logger.debug("===== BODY =====")
    logger.debug(body)
    logger.debug("================")
    first_name = body.get('first_name', None)
    last_name = body.get('last_name', None)
    userPass = body.get('password', None)
    userMail = body.get('email', None)
    logger.debug(f"---> Got `create user` request with Name {first_name} {last_name} Password {userPass} Email {userMail}")

    


def logout_view(request):
    logger.debug(f"---> Caught request! Body: {request.body}")
    logger.debug(f"---> User info? {request.user}")    
    users = User.objects.all()
    for u in users:
        logger.debug(f"User {u}: Authenticated? {u.is_authenticated}")

    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)

    logger.debug(f"="*80)
    logger.debug(f"---> NEW USER INFO <---")
    users = User.objects.all()
    for u in users:
        logger.debug(f"User {u}: Authenticated? {u.is_authenticated}")
    logger.debug(f"="*80)

    return JsonResponse({'detail': 'Successfully logged out.'})


@ensure_csrf_cookie
def session_view(request):
    logger.debug(f"---> Caught request! Body: {request.body}")
    logger.debug(f"---> User info? {request.user}")    
    users = User.objects.all()
    for u in users:
        logger.debug(f"User {u}: Authenticated? {u.is_authenticated}")

    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})


def whoami_view(request):
    logger.debug(f"---> Caught request! Body: {request.body}")
    logger.debug(f"---> User info? {request.user}")
    users = User.objects.all()
    for u in users:
        logger.debug(f"User {u}: Authenticated? {u.is_authenticated}")
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'username': request.user.username})