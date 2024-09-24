import re
from scraper.utils.textstyle import TextStyle
from bs4 import BeautifulSoup
import requests


class WrongLinkException(BaseException):
    """Empty Exception for URL validation later on. No real use besides custom error name."""
    pass


class Validator:

    def __init__(self):
        pass

    @staticmethod
    def try_catch_link_exception(url: str) -> requests.Response:
        data = requests.get(url)
        if data.status_code != 200:
            raise WrongLinkException(f"Failed to reach {url}. ({data.status_code})")

        soup = BeautifulSoup(data.text, "html.parser")
        error = soup.body.find(text=re.compile('Page not found'))  # Tries to find "Page not found" in link page
        if error:
            raise WrongLinkException
        else:
            return data

    @staticmethod
    def validate_game_name(game_name) -> str:
        game_name: str = game_name.lower().replace(" ", "-")
        return game_name

    @staticmethod
    def check_link_with_gamename(game_name) -> str:
        # Links to check for game in store
        links: list[str] = [
            f'https://www.allkeyshop.com/blog/buy-{game_name}-cd-key-compare-prices/',
            f'https://www.allkeyshop.com/blog/buy-{game_name}-compare-prices/',
            f'https://www.allkeyshop.com/blog/compare-and-buy-cd-key-for-digital-download-{game_name}/',
            f'https://www.allkeyshop.com/blog/buy-{game_name}-cd-key-digital-download-best-price/',
        ]

        for link in links:
            try:
                Validator.try_catch_link_exception(link)
                return link
            except WrongLinkException:
                print(f"{link} {TextStyle.RED}FAILED{TextStyle.RESET}")
                continue

        raise WrongLinkException('All URLs failed. Check for typos in game name or add more URLs to check list.')

    @staticmethod
    def set_display_name(game_name):
        char_row_limit = 41

        print_message = ""
        game_name_length = len(game_name)
        leftover = int(char_row_limit/2)-game_name_length
        for i in range(leftover):
            print_message += '-'
        print_message += game_name
        for i in range(leftover):
            print_message += '-'
        return print_message.upper()

