from django.conf import settings
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from packages.exceptions import EdflowException, UnauthorizedException
from packages.globalfunction import verifyuser
from packages.response import parsejson


def validator(*cargs, **ckwargs):
    def my_validator(func):
        def wrap(request, *args, **kwargs):
            try:

                """
                Header Token validation
                """
                meta_values = args[0].META
                if meta_values["HTTP_TOKEN"] != settings.HTTP_TOKEN:
                    raise UnauthorizedException("Unauthorized Access")

                """
                Header Source validation
                """
                if "HTTP_SOURCE" in meta_values and meta_values["HTTP_SOURCE"] != "":
                    source = meta_values["HTTP_SOURCE"]
                    if source not in ["iOS", "ANDROID", "WEB", "ADMIN"]:
                        raise UnauthorizedException("Invalid Source")
                else:
                    raise UnauthorizedException("Unauthorized Access")
                print(args[0].data)
                userdetail = []
                if ckwargs.get('api') is not False:
                    if not args[0].data["api_key"]:
                        raise UnauthorizedException(_("User secret key is required"))
                    apikey = args[0].data["api_key"]
                    userdetailObj = verifyuser(apikey)
                    if userdetailObj["error"]:
                        raise UnauthorizedException(userdetailObj["msg"])
                    else:
                        userdetail = userdetailObj["data"]

                try:
                    return func(request, *args, userdetail=userdetail, **kwargs)
                except EdflowException as e:
                    return Response(
                        parsejson(str(e), "", status=403),
                        status=status.HTTP_200_OK
                    )
            except UnauthorizedException as e:
                return Response(
                    parsejson(str(e), "", status=403),
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    parsejson("Something went wrong in request." + str(e), "", status=403),
                    status=status.HTTP_200_OK
                )

        return wrap

    return my_validator
