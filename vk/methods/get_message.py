"""Get msg."""

import requests
from loguru import logger

from .consts import V


def get_message(access_token: str, pts: int) -> tuple[list, list, str]:
    """Get msg."""
    body = {
        "extended": 1,
        "pts": pts,
        "fields":"id,first_name,last_name",
        "access_token": access_token,
    }

    query = {
        "v": V,
    }

    req = requests.post(
        "https://api.vk.me/method/messages.getLongPollHistory",
        data=body,
        params=query,
        timeout=20,
    ).json()
    logger.debug(f"[VK API] get_message response: {req}")
    if req.get("error"):
        return {"error": True, "text": "access token has expired"}

    peer_type = req["response"]["conversations"][-1]["peer"]["type"]

    title = None
    
    if peer_type == "user":
        title = "Direct message"
    elif peer_type == "chat":
        title = req["response"]["conversations"][-1]["chat_settings"]["title"]

    return {
        "items": req["response"]["messages"]["items"],
        "profiles": req["response"]["profiles"],
        "title": title,
        }
