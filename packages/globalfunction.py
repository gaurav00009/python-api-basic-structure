import hashlib
import random
import re
import time
from os.path import splitext
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext as _

import requests


def generateapikey():
    return hashlib.sha224(str(random.getrandbits(256)).encode("utf-8")).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


"""
    Check Authentication Function
"""


def decode(coded_string):
    import base64

    return base64.b64decode(coded_string)


def encode(coded_string):
    import base64

    coded_string = coded_string.replace(" ", "")
    convert = base64.b64encode(coded_string)
    convert = convert.replace("+", "-")
    convert = convert.replace("/", "_")
    convert = convert.rstrip("=")
    return convert.upper()


"""
  check username
"""


# add number in username
def get_number(s):
    s = s.lower()
    r = re.compile("([a-zA-Z-]+)([0-9]+)")
    m = r.match(s)
    try:
        first = m.group(1)
        last = int(m.group(2)) + 1
        return first + str(last)
    except Exception:
        return s + str("1")


def getError(msg):
    try:
        from django.core.mail import send_mail

        send_mail(
            "Error ",
            "",
            "zeta1.clavax@gmail.com",
            ["zeta1.clavax@gmail.com"],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=msg,
        )
    except Exception as e:
        print(e)
        pass


def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ".jpg" if ext == "" else ext  # or ext[1:] if you don't want the leading '.'


def save_image_from_url(model, url):

    r = requests.get(url)
    extension = get_ext(url)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()
    name = "image" + str(int(time.time())) + str(extension)
    model.save(name, File(img_temp), save=True)
    return name


def verifyuser(apikey):
    """
    veryfy the user by there api key
    is valid api key return userID
    check is blocked
    check is deleted
    """
    resp = {}
    if not (apikey is None):
        try:
            User = get_user_model()
            # get user details by there apikey
            udata = User.objects.get(api_key=apikey)
            # check user block or deleted.
            try:

                # check whether the user is blocked
                if udata.is_active == "0":
                    resp["error"] = True
                    resp["msg"] = _(
                        "You are not active user, Please contact to administrator."
                    )

                if len(resp) == 0:
                    resp["error"] = False
                    resp["data"] = udata
            except Exception as e:
                print(e)
                resp["error"] = True
                resp["msg"] = _("Network error, please try again.")
        except Exception as e:
            print(e)
            resp["error"] = True
            resp["msg"] = "User secret key is invalid."
    else:
        resp["error"] = True
        resp["msg"] = _("User secret key is required")
    return resp
