from selenium.common import NoSuchElementException
from scraper import dataparser, validator
from scraper.utils.validator import WrongLinkException

FAILED_IMAGE = 'https://pbs.twimg.com/profile_images/1042019157972320256/STolLU9B_400x400.jpg'

def run(game_name, interface):
    def errorprint(exception: str, msg: str) -> None:
        interface.console_print_red(3.0, "FAILED")
        interface.console_print(5.0, f"{exception}:")
        interface.console_print(6.0, f"{msg}")
        interface.console_print(7.0, '-------------------------------------------------')

    try:
        interface.console_print(0.0, '\n\n\n\n\n\n\n\n\n\n\n\n\n', text_color='white')
        interface.console_print(1.0, f'----{validator.set_display_name(validator.validate_game_name(game_name).upper())}----')
        interface.console_print(2.0, "Validating URLs...")
        interface.update_idletasks()

        validated_url = validator.check_link_with_gamename(validator.validate_game_name(game_name))
        dataparser.get_soup(validated_url)

        if validated_url:
            interface.console_print_green(3.0, 'URL validated successfully!')
            interface.update_idletasks()

            interface.console_print(5.0, 'Game found at:')
            interface.update_idletasks()

            interface.console_print(6.0, dataparser.url)
            interface.update_idletasks()

            interface.console_print(8.0, "Parsing validated URL...")
            interface.update_idletasks()
            coupons = dataparser.parse()

            if coupons:
                interface.console_print_green(9.0, f'Parse successful!')
                interface.update_idletasks()

            interface.console_print(10.0, '-------------------------------------------------')
            interface.console_print(11.0, 'scroll down to see earlier lookups')
            interface.update_idletasks()

            interface.update_picture(dataparser.get_game_picture())
            interface.Frame.content_print(interface.frame, coupons)

    except WrongLinkException:
        errorprint("WrongLinkException",
                   "All URLs failed. Check for typos in game name or add more URLs to check list.")
        interface.update_picture(FAILED_IMAGE)
    except NoSuchElementException:
        errorprint("NoSuchElementException", "Critical error encountered when parsing merchant information. "
                                             f"Report issue or check for typos when entering game name.")
        interface.update_picture(FAILED_IMAGE)
