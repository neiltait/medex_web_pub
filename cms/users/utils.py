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


def get_medical_team_member_presenter(team_member):
    if team_member:
        return {
            'full_name': team_member.full_name
        }
    else:
        return {
            'full_name': ''
        }
