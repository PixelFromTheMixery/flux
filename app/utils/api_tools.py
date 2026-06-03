# region Docs
"""
API tool for interacting with an anytype instance.

Performs the actual API calls if API key and url is supplied, optional data

Variables:
    # Call-based
    RETRIES (int): Number of request retries
    DELAY (int): Number of seconds between between retries
    TIMEOUT (int): How long to wait for a hang

    RESPONSE_MAP (dict): lambda map of API request types


Methods:
    method: Description of a module-level method.

"""
# endregion

import random
import time
from typing import Optional

import requests
from pydantic import BaseModel

from .logger import logger


class APIRequest(BaseModel):
    target: str
    category: str
    url: str
    info: str
    auth_token: str
    payload: Optional[dict | str] = None


RETRIES: int = 3
DELAY: int = 2
TIMEOUT: int = 3

RESPONSE_MAP = {
    "delete": lambda u, h: requests.delete(u, headers=h, timeout=TIMEOUT),
    "get": lambda u, h: requests.get(u, headers=h, timeout=TIMEOUT),
    "patch": lambda u, h, p: requests.patch(
        u,
        headers=h,
        timeout=TIMEOUT,
        **({"json": p} if isinstance(p, dict) else {"data": p}),
    ),
    "post": lambda u, h, p: requests.post(
        u,
        headers=h,
        timeout=TIMEOUT,
        **({"json": p} if isinstance(p, dict) else {"data": p}),
    ),
    "put": lambda u, h, p: requests.put(
        u,
        headers=h,
        timeout=TIMEOUT,
        json=p if isinstance(p, dict) else None,
        **({"json": p} if isinstance(p, dict) else {"data": p}),
    ),
}


def exception_handler(e, result, attempt):
    # region Docs
    """
    Records the Exception Message for troubleshooting

    Args:
        e (RequestException): Exception raised by call
        result (Response): Message may contain solution
        attempt (int): number of tries

    Returns:
        type: Description of return value.
    Raises:
        Exception: Conditions.
    """
    # endregion

    print(f"RequestException on attempt {attempt}: {e}")
    message = result.get("message") if result else None
    if message:
        print(f"json response: {message}")
    return RETRIES + 1


def build_header(target, auth_token, content_type: str = "application/json") -> dict:
    base_header = {"Content-Type": content_type}
    if target == "traggo":
        base_header["X-Api-Token"] = auth_token
    else:
        base_header["Authorization"] = "Bearer " + auth_token
    return base_header


def make_call(api_request: APIRequest):
    # region Docs
    """
    Makes a call based on method, url, and info

    Args:
        category (str): REST method
        url (str): url to make call to
        info (str): string for logging to explain what the call is doing
        data (dict): mapping of call values

    Returns:
        dict: json value of api response.

    Raises:
        ConnectionError/Timeout: Infinite attempts until able to contact instance.
        HTTPError(429): Too many calls, gives some time to wait until next delay
        Other: Any other issue, possibly from Anytype
    """
    # endregion

    headers = build_header(api_request.target, api_request.auth_token)
    category = api_request.category

    attempt = 0
    while True:
        try:
            logger.info(
                "Attempt to %s from %s: %s of %s",
                api_request.info,
                api_request.target,
                attempt,
                RETRIES,
            )

            response = (
                RESPONSE_MAP[category](api_request.url, headers, api_request.payload)
                if category in ["patch", "post", "put"]
                else RESPONSE_MAP[category](api_request.url, headers)
            )

            response.raise_for_status()
            return response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait_time = 60 + random.uniform(0, 5)
            logger.warning(
                "Network issue (%s). Retrying infinitely... Next try in %.1f",
                e,
                wait_time,
            )
            time.sleep(wait_time)
            continue  # Restarts the 'while True' loop immediately

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429 and attempt <= RETRIES - 1:
                attempt += 1
                logger.warning(
                    "429 limit hit. Retry %s/%s in %s...", attempt, RETRIES, DELAY
                )
                time.sleep(DELAY)
                continue

            # If it's not a 429, or we ran out of 429 retries, handle normally
            attempt = exception_handler(e, response, attempt)
            if attempt > RETRIES:
                raise
