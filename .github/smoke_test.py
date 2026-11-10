"""Check that the game runs in a browser and that the keys work."""
import sys
import time

from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/prong.html"


def hold(page, key, seconds=0.5):
    """Hold a key down, as the game only moves a player while a key is held."""
    page.keyboard.down(key)
    time.sleep(seconds)
    page.keyboard.up(key)


with sync_playwright() as p:
    browser = p.chromium.launch()
    # About the size of the iframe on the website
    page = browser.new_page(viewport={"width": 600, "height": 600})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    time.sleep(3)
    page.mouse.click(300, 300)
    before = page.screenshot()
    time.sleep(0.5)
    after_wait = page.screenshot()
    hold(page, "s")
    hold(page, "ArrowRight")
    time.sleep(1)
    after_keys = page.screenshot()
    browser.close()

if errors:
    sys.exit(f"Page errors: {errors}")
if before == after_wait:
    sys.exit("The game is not running: the page did not change")
if after_wait == after_keys:
    sys.exit("Pressing keys did not change the page")
print("OK")
