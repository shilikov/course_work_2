from dotenvs import load_env_values
import os

if load_env_values():
    api_token = os.getenv('group_token')
    api_version = os.getenv('VK_api_V')
    vk_login = os.getenv('user_token')
    vk_password = os.getenv('group_id')
