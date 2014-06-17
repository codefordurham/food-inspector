import requests


def check_image(url):
    """Checks if an image url exists, returns True if the image exists."""
    r = requests.get(url)
    if r.status_code == 200:
        return True
