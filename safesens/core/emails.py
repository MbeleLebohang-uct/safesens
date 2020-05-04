from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sites.models import Site
from django.templatetags.static import static

from .utils import build_absolute_uri


def get_email_context():
    site = Site.objects.get_current()
    logo_url = build_absolute_uri(static("images/logo-light.svg"))
    send_email_kwargs = {"from_email": settings.DEFAULT_FROM_EMAIL}
    email_template_context = {
        "domain": site.domain,
        "logo_url": logo_url,
        "site_name": site.name,
    }
    return send_email_kwargs, email_template_context


def prepare_url(params: str, redirect_url: str) -> str:
    """Add params to redirect url."""
    split_url = urlsplit(redirect_url)
    split_url = split_url._replace(query=params)
    return split_url.geturl()