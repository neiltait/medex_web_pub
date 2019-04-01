
def get_user_presenter(user):
    if user:
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_address': user.email_address
        }
    else:
        return {
            'first_name': '',
            'last_name': '',
            'email_address': ''
        }
