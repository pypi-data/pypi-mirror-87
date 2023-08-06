from holehe.core import *
from holehe.localuseragent import *


async def lastfm(email, client, out, pbar):
    name = "lastfm"
    try:
        req = await client.get("https://www.last.fm/join")
        token = req.cookies["csrftoken"]
    except BaseException:
        pbar.update(1);out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {"csrfmiddlewaretoken": token, "userName": "", "email": email}
    headers = {
        "Accept": "*/*",
        "Referer": "https://www.last.fm/join",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "csrftoken=" + str(token),
    }
    try:

        check = await client.post("https://www.last.fm/join/partial/validate", headers=headers, data=data)
    except BaseException:
        pbar.update(1);out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    if check.json()["email"]["valid"]:
        pbar.update(1);out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        pbar.update(1);out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
