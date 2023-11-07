from firebase_admin import auth
from django.http import JsonResponse

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        exempt_views = ['/accounts/register/', '/accounts/login/']

        if request.path in exempt_views:
            response = self.get_response(request)
        else:
            auth_header = request.META.get('HTTP_AUTHORIZATION')

            if auth_header and auth_header.startswith('Bearer '):
                custom_token = auth_header.split('Bearer ')[1]
                try:
                    user = auth.verify_id_token(custom_token)
                    user_id = user['uid']
                    email = user['email']
                    request.firebase_user = {'uid': user_id, 'email': email}
                except auth.InvalidIdTokenError as e:
                    return JsonResponse({'error': str(e)}, status=401)
            else:
                return JsonResponse({'error': 'Invalid or missing custom token'}, status=401)

            response = self.get_response(request)
            
        return response
