from configs.env import RESEND_API_KEY
from schemes.user.user_scheme import User
import resend

resend.api_key = RESEND_API_KEY


def matching_mailing(users: list[User]):
    for i in range(len(users)):
        recipient_index = (i + 1) % len(users)
        r = resend.Emails.send({
            "from": "dating@redbread.tech",
            "to": f"{users[i].e_mail}",
            "subject": "Somebody liked your profile",
            "html": f"{users[recipient_index].name} liked you. Participant's email address: {users[recipient_index].e_mail}"
        })
