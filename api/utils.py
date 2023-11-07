from firebase_admin import auth

def get_user_by_name(username):
    users = auth.list_users()
    for u in users.users:
        if u.display_name == username:
            return u