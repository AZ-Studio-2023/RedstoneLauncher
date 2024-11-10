import hashlib
import os.path
import uuid

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from Helpers.getValue import CLIENT_ID, REDIRECT_URL, DATA_PATH, CACHE_PATH
from Helpers.outputHelper import logger


def get_offline_player_uuid(player_name):
    input_str = "OfflinePlayer:" + player_name
    hash_bytes = hashlib.md5(input_str.encode('utf-8')).digest()
    most_sig_bits = 0
    least_sig_bits = 0
    for i in range(8):
        most_sig_bits = (most_sig_bits << 8) | (hash_bytes[i] & 0xff)
    return uuid.UUID(int=(most_sig_bits << 64) | least_sig_bits)

class WorkerSignals(QObject):
    progress = pyqtSignal(dict)


class MicrosoftLogin(QRunnable):
    def __init__(self):
        super(MicrosoftLogin, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            # 获取授权码
            auth_url = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_url={REDIRECT_URL}&response_mode=query&scope=XboxLive.signin%20offline_access"
            webbrowser.open(auth_url)
            auth_code = None

            class AuthHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    nonlocal auth_code
                    query = urlparse(self.path).query
                    query_components = parse_qs(query)
                    auth_code = query_components["code"][0]

                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    html_content = """
                    <html>
                    <head>
                        <meta charset='UTF-8'>
                        <title>Redstone Launcher</title>
                    </head>
                    <body>
                        <h1>&#30331;&#24405;&#25104;&#21151;&#65281;&#24744;&#21487;&#20197;&#20851;&#38381;&#27492;&#31383;&#21475;&#20102;</h1>
                    </body>
                    </html>
                    """
                    self.wfile.write(html_content.encode('ascii'))

            httpd = HTTPServer(('localhost', 60000), AuthHandler)
            httpd.handle_request()

            self.signals.progress.emit({"code": 100})
            # 使用授权码获取访问令牌
            token_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
            token_data = {
                "client_id": CLIENT_ID,
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_url": REDIRECT_URL,
                "scope": "XboxLive.signin offline_access"
            }
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_data = token_response.json()
            access_token = token_data["access_token"]
            refresh_token = token_data["refresh_token"]

            # Xbox Live身份验证
            xbox_auth_url = "https://user.auth.xboxlive.com/user/authenticate"
            xbox_auth_data = {
                "Properties": {
                    "AuthMethod": "RPS",
                    "SiteName": "user.auth.xboxlive.com",
                    "RpsTicket": f"d={access_token}"
                },
                "RelyingParty": "http://auth.xboxlive.com",
                "TokenType": "JWT"
            }
            xbox_auth_response = requests.post(xbox_auth_url, json=xbox_auth_data)
            xbox_auth_response.raise_for_status()
            xbl_token = xbox_auth_response.json()["Token"]
            user_hash = xbox_auth_response.json()["DisplayClaims"]["xui"][0]["uhs"]

            # 获取XSTS令牌
            xsts_auth_url = "https://xsts.auth.xboxlive.com/xsts/authorize"
            xsts_auth_data = {
                "Properties": {
                    "SandboxId": "RETAIL",
                    "UserTokens": [xbl_token]
                },
                "RelyingParty": "rp://api.minecraftservices.com/",
                "TokenType": "JWT"
            }
            xsts_auth_response = requests.post(xsts_auth_url, json=xsts_auth_data)
            xsts_auth_response.raise_for_status()
            xsts_token = xsts_auth_response.json()["Token"]

            # 获取Minecraft访问令牌
            minecraft_auth_url = "https://api.minecraftservices.com/authentication/login_with_xbox"
            minecraft_auth_data = {
                "identityToken": f"XBL3.0 x={user_hash};{xsts_token}"
            }
            minecraft_auth_response = requests.post(minecraft_auth_url, json=minecraft_auth_data)
            minecraft_auth_response.raise_for_status()
            minecraft_access_token = minecraft_auth_response.json()["access_token"]

            # 检查是否拥有游戏
            ownership_url = "https://api.minecraftservices.com/entitlements/mcstore"
            headers = {"Authorization": f"Bearer {minecraft_access_token}"}
            ownership_response = requests.get(ownership_url, headers=headers)
            ownership_response.raise_for_status()

            if len(ownership_response.json()["items"]) > 0:
                profile_url = "https://api.minecraftservices.com/minecraft/profile"
                profile_response = requests.get(profile_url, headers=headers)
                profile_response.raise_for_status()
                profile_data = profile_response.json()
                response = requests.get(f"https://minotar.net/avatar/{profile_data['name']}")
                if response.status_code == 200:
                    with open(os.path.join(CACHE_PATH, f"{profile_data['name']}.png"), 'wb') as file:
                        file.write(response.content)
                else:
                    logger.debug("下载玩家头像失败")
                logger.info(f"登录成功！玩家名：{profile_data['name']}")
                self.signals.progress.emit( {
                    "access_token": minecraft_access_token,
                    "username": profile_data["name"],
                    "uuid": profile_data["id"],
                    "refresh_token": refresh_token,
                    "code": 200
                })

            else:
                logger.error("该账号未拥有Minecraft")
                self.signals.progress.emit({"code": 403, "error": "该账号未拥有Minecraft"})
        except requests.RequestException as e:
            logger.error(f"网络请求错误: {str(e)}")
            self.signals.progress.emit({"code": 500, "error": f"网络请求错误: {str(e)}"})
        except KeyError as e:
            logger.error(f"响应数据缺少关键字段: {str(e)}")
            self.signals.progress.emit({"code": 500, "error": f"响应数据缺少关键字段: {str(e)}"})
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            self.signals.progress.emit({"code": 500, "error": f"未知错误: {str(e)}"})
