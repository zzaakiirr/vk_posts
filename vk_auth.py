import os

import vk


def fetch_vk_api():
    vk_app_id = os.environ.get('VK_APP_ID')
    vk_login = os.environ.get('VK_LOGIN')
    vk_password = os.environ.get('VK_PASSWORD')

    session = vk.AuthSession(
        app_id=vk_app_id,
        user_login=vk_login,
        user_password=vk_password,
        scope="wall",
    )
    api = vk.API(session, v=5.85, lang='en')

    return api
