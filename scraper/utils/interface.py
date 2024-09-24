import customtkinter as ct
from PIL import Image
import requests
from io import BytesIO
from scraper.main import run
import webbrowser

ct.set_appearance_mode('dark')
ct.set_default_color_theme('dark-blue')

BLUE_BUTTON_COLOR = '#134B70'


class Interface(ct.CTk):

    logo = ct.CTkImage(dark_image=Image.open(fp='scraper/images/logo.jpg', mode='r'), size=(200, 200))

    def __init__(self):
        super().__init__()

        self.frame = Interface.Frame(master=self, width=310, height=450)
        self.frame.grid(row=0, column=3, pady=20, rowspan=20, sticky="w")

        self.geometry("600x500")
        self.title('tomelioProductions')

        self.entry = ct.CTkEntry(self, placeholder_text='Enter game name here...', width=200)
        self.entry.grid(row=1, column=0, columnspan=3, rowspan=1)
        self.entry.focus_force()

        self.image_label = ct.CTkLabel(self, image=Interface.logo, text="")
        self.image_label.grid(row=0, column=0, columnspan=3, padx=30, pady=20)

        self.go_button = ct.CTkButton(self, text="Get coupons", fg_color=BLUE_BUTTON_COLOR, command=self.get_game_and_run)
        self.go_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.textbox = Interface.Textbox(master=self, width=220, height=150, activate_scrollbars=True)
        self.textbox.configure(state="disabled", wrap="word")
        self.textbox.grid(row=3, column=0, columnspan=3)

    class Frame(ct.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

        @staticmethod
        def go_to_store(url: str) -> None:
            webbrowser.open(url)

        def content_print(self, coupons: list[dict]):
            num = -1
            for coupon in coupons:
                print(coupon)
                num += 1
                new_frame = ct.CTkFrame(self, width=310, height=55)
                new_frame.configure()
                new_frame.grid(row=num, column=3, rowspan=1, columnspan=2, pady=10)

                store_button = ct.CTkButton(new_frame, width=50, height=55, fg_color="#6C946F", text='Store', command=lambda url=coupon['Link']: self.go_to_store(url))
                store_button.configure(state='normal')
                store_button.grid(row=0, column=3)

                merchant_label = ct.CTkLabel(new_frame, width=100, height=55, fg_color="#201E43", text=coupon["Merchant"])
                merchant_label.grid(row=0, column=0)

                discount_percentage_label = ct.CTkLabel(new_frame, width=115, height=25, fg_color=BLUE_BUTTON_COLOR, text=coupon["Discount"])
                discount_percentage_label.grid(row=0, column=1, sticky="nw")

                discount_code_button = ct.CTkButton(new_frame, width=115, height=30, fg_color="#4379F2", text=coupon["Coupon code"], command=lambda code=coupon["Coupon code"]: Interface.clipboard_append(self, code))
                discount_code_button.grid(row=0, column=1, sticky="se")

                price_label = ct.CTkLabel(new_frame, width=60, height=55, fg_color="#508C9B", text=coupon["Final price"])
                price_label.grid(row=0, column=4)

    class Textbox(ct.CTkTextbox):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

    @staticmethod
    def update_picture(url: str) -> None:
        image = Image.open(BytesIO(requests.get(url).content))
        Interface.logo.configure(dark_image=image, size=(200, 200))

    def get_game_and_run(self):
        if self.entry.get():
            self.frame.destroy()
            self.frame = Interface.Frame(master=self, width=310, height=450)
            self.frame.grid(row=0, column=3, pady=20, rowspan=20, sticky="w")
            run(self.entry.get(), self)
        else:
            self.console_print(0.0, 'Field cannot be empty.')

    @staticmethod
    def first_number_of(number):
        number_str = str(number)
        cleaned_str = number_str.lstrip('-').replace('.', '')
        first_digit = int(cleaned_str[0])
        return first_digit

    def console_print(self, index: float, text: str, **kwargs: str):
        settings = {'text_color': "white"}
        settings = {**settings, **kwargs}

        self.textbox.configure(text_color=settings['text_color'])
        self.textbox.configure(state='normal')
        self.textbox.insert(index, text+'\n')
        self.textbox.configure(state='disabled')

    def console_print_green(self, index: float, text: str):
        self.textbox.configure(state='normal')
        self.textbox.insert(index, text+'\n')
        self.textbox.tag_add("green", index, f"{Interface.first_number_of(index)}.99")
        self.textbox.tag_config("green", foreground="#86D293")
        self.textbox.configure(state='disabled')

    def console_print_red(self, index: float, text: str):
        self.textbox.configure(state='normal')
        self.textbox.insert(index, text+'\n')
        self.textbox.tag_add("red", "0.0", f"10.99")
        self.textbox.tag_config("red", foreground="red")
        self.textbox.configure(state='disabled')

