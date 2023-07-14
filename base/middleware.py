# from functools import wraps
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import jwt
def admin_required(request):
    # @wraps(function)
    # def wrap(request, *args, **kwargs):
    #     print(request.user)
    #     if request.user.is_staff:
    #         return function(request, *args, **kwargs)
    #     else:
    #         return HttpResponse('Unauthorized', status=401)
    token = request.META['HTTP_AUTHORIZATION']
    if token:
        # Bearer <token>
        token = token.split(' ')[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
            if payload['is_staff']:
                request.payload = payload
                return True
            else:
                return False
        except:
            return False
    return False

    #             return request
    #         else:
    #             return HttpResponse('Unauthorized', status=401)
    #     except jwt.ExpiredSignatureError:
    #         return HttpResponse('Unauthorized', status=401)
    #     except jwt.InvalidTokenError:
    #         return HttpResponse('Unauthorized', status=401)
    # return request

# def admin_required2(request):
#     # @wraps(function)
#     # def wrap(request, *args, **kwargs):
#     #     print(request.user)
#     #     if request.user.is_staff:
#     #         return function(request, *args, **kwargs)
#     #     else:
#     #         return HttpResponse('Unauthorized', status=401)
#     token = request.META['HTTP_AUTHORIZATION']
#     if token:
#         # Bearer <token>
#         token = token.split(' ')[1]
#         try:
#             payload = jwt.decode(token, 'secret', algorithm='HS256')
#             if payload['is_staff']:
#                 request.payload = payload
#                 return True
#             else:
#                 return False
#         except:
#             return False
#     return False

def student_required(function):
    # @wraps(function)
    # def wrap(request, *args, **kwargs):
    #     if not request.user.is_staff:
    #         return function(request, *args, **kwargs)
    #     else:
    #         return HttpResponse('Unauthorized', status=401)
    # return wrap
    token = request.META['HTTP_AUTHORIZATION']
    if token:
        token = token.split(' ')[1]
        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
            if not payload['is_staff']:
                request.payload = payload
                return True
            else:
                return False
        except:
            return False
    return False

# def admin_or_student_required(function):
#     # @wraps(function)
#     # def wrap(request, *args, **kwargs):
#     #     if request.user.is_staff or not request.user.is_staff:
#     #         return function(request, *args, **kwargs)
#     #     else:
#     #         return HttpResponse('Unauthorized', status=401)
#     # return wrap
#     token = request.META['HTTP_AUTHORIZATION']
#     if token:
#         token = token.split(' ')[1]
#         try:
#             payload = jwt.decode(token, 'secret', algorithm='HS256')
#             request.payload = payload
#             return True
#         except:
#             return False
#     return False

def admin_or_student_required(function):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.split(' ')[1]
            try:
                payload = jwt.decode(token, 'secret', algorithm='HS256')
                request.payload = payload
                return function(request, *args, **kwargs)
            except:
                return Response({'message': 'Invalid token'}, status=401)
        return Response({'message': 'Unauthorized'}, status=401)
    return wrap