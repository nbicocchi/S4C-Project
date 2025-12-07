import requests
import time


def call_mobility_api(url, payload, retries=3, delay=2, timeout=5):
    """
    Call the mobility API with retries and timeout.

    Args:
        url (str): Full URL of the endpoint.
        payload (dict): JSON payload to send.
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.
        timeout (int): Request timeout in seconds.

    Returns:
        dict: {"success": bool, "data": dict} or {"success": False, "error": str}
    """
    for attempt in range(1, retries + 1):
        try:
            res = requests.post(url, json=payload, timeout=timeout)
            if res.status_code == 200:
                return {"success": True, "data": res.json()}

            # HTTP error
            return {
                "success": False,
                "error": f"Mobility API responded with HTTP {res.status_code}",
                "details": res.text
            }

        except requests.exceptions.RequestException as e:
            if attempt == retries:
                return {"success": False, "error": str(e)}
            time.sleep(delay)

    return {"success": False, "error": "Unknown error calling mobility_api"}
