from urllib.parse import urlencode
from django.contrib.auth.tokens import default_token_generator

from ..core.emails import get_email_context, prepare_url
from templated_email import send_templated_mail


def send_account_confirmation_email(user, redirect_url):
    """Trigger sending an account confirmation email for the given user."""
    token = default_token_generator.make_token(user)
    _send_account_confirmation_email(user.email, token, redirect_url)

# @app.task
def _send_account_confirmation_email(email, token, redirect_url):
    params = urlencode({"email": email, "token": token})
    confirm_url = prepare_url(params, redirect_url)
    send_kwargs, ctx = get_email_context()
    ctx["confirm_url"] = confirm_url
    send_templated_mail(
        template_name="account/confirm",
        recipient_list=[email],
        context=ctx,
        **send_kwargs,
    )