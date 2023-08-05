from getpass import getuser
from os import uname
from typing import Optional
from uuid import uuid4

import analytics

from ..version import __version__
from .config import Config


def _context():
    u = uname()
    return {
        "app": {"name": "sym-cli", "version": __version__},
        "os": {"name": u.sysname, "version": u.release},
    }


def _user_id():
    return f"{Config.get_org()}:{Config.get_email()}"


def _identity_kwargs():
    try:
        return {"user_id": _user_id(), "context": _context()}
    except KeyError:
        return {"anonymous_id": str(uuid4()), "context": _context()}


def _skip(global_options: Optional["GlobalOptions"]):
    if not Config.is_logged_in():
        return True
    if global_options:
        return global_options.disable_analytics

    return False


def identify(global_options: Optional["GlobalOptions"] = None):
    if _skip(global_options):
        return

    traits = {"username": getuser()}

    for attr in ("org", "email"):
        try:
            traits[attr] = Config.instance()[attr]
        except KeyError:
            pass

    kwargs = _identity_kwargs()
    analytics.identify(traits=traits, **kwargs)
    if "user_id" in kwargs:
        analytics.group(group_id=Config.get_org(), **kwargs)


def track(event, global_options: Optional["GlobalOptions"] = None, **properties):
    if _skip(global_options):
        return

    analytics.track(event=event, properties=properties, **_identity_kwargs())
