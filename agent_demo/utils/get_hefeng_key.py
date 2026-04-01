import time
import jwt
import requests
import os
from cryptography.hazmat.primitives import serialization
# ===================== 配置（自动定位密钥，彻底解决路径问题） =====================
KID = "C8B7K8EHXG"
SUB = "26E5FT2NVK"
# 自动获取当前脚本所在目录，拼接密钥路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_PATH = os.path.join(SCRIPT_DIR, "ed25519-private.pem")
# ==============================================================================
def load_private_key(path):
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        raise FileNotFoundError(f"私钥文件不存在，请检查路径：{path}")
    except Exception as e:
        raise ValueError(f"私钥加载失败：{str(e)}")
def generate_jwt():
    private_key = load_private_key(PRIVATE_KEY_PATH)
    now = int(time.time())
    payload = {"sub": SUB, "iat": now - 30, "exp": now + 3600}
    headers = {"alg": "EdDSA", "kid": KID}
    return jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)