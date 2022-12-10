from tkinter import *
from utils import about_messagebox

# ------------------ CONSTANTS ---------------- #
TIME_IN_SECONDS = 5
LABEL_INITIAL_TEXT = f"Start typing! {TIME_IN_SECONDS} seconds without typing will result in a complete text wipe."
FONT = 'Fira Code'
TITLE_TEXT_FONT = (FONT, 16)
MAIN_TEXT_FONT = (FONT, 16)
BACKGROUND = '#959595'
TEXT_BACKGROUND = '#BBBBBB'
COLOR_RED = '#FF0000'
COLOR_ORANGE = '#FF9900'
COLOR_YELLOW = '#FFFF00'
COLOR_LIGHT_GREEN = '#99FF99'
COLOR_GREEN = '#00FF00'
COLOR_BLUE = '#33CCFF'
# --------------------------------------------- #


class GUI(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master: Tk = master
        self.master.title('Disappearing Text Writing App')
        self.master.resizable(width=False, height=False)

        # icon = ImageTk.PhotoImage(Image.open(io.BytesIO(ICON)))
        # self.master.wm_iconphoto(False, icon)

        self.grid(row=0, column=0, sticky=N + W + E + S)
        self.configure(pady=30, padx=30)

        # This string represents the timer event.
        self.timer = ''

        self.text = ''
        self.timer_text_label = None
        self.timer_text_var = None
        self.main_text_area = None

        self.create_widgets()
        self.register_event_listeners()

    def create_widgets(self):

        my_menu = Menu(self.master)
        self.master.config(menu=my_menu)
        self.master.option_add('*tearOff', False)
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label='File', menu=file_menu)
        help_menu = Menu(my_menu)
        my_menu.add_cascade(label='Help', menu=help_menu)
        file_menu.add_command(label='Quit', command=self.master.quit)
        help_menu.add_command(label='About', command=about_messagebox)

        self.configure(bg=BACKGROUND)

        # Create
        self.timer_text_var = StringVar(value=LABEL_INITIAL_TEXT)
        self.timer_text_label = Label(self, textvariable=self.timer_text_var)
        self.main_text_area = Text(self)

        # Configure
        self.timer_text_label.grid(row=0, column=0)
        self.main_text_area.grid(row=1, column=0)
        self.timer_text_label.configure(font=TITLE_TEXT_FONT,
                                        foreground=COLOR_BLUE,
                                        background=BACKGROUND)
        self.main_text_area.configure(font=MAIN_TEXT_FONT, wrap='word')
        self.main_text_area.configure(padx=20, pady=20)
        self.main_text_area.configure(highlightbackground=COLOR_BLUE,
                                      highlightcolor=COLOR_BLUE,
                                      highlightthickness=2,
                                      borderwidth=0,
                                      background=TEXT_BACKGROUND)

    def register_event_listeners(self):

        # <KeyRelease>, otherwise the event triggers before we have the input.
        self.main_text_area.bind('<KeyRelease>', self.revalidate_state)

    def revalidate_state(self, *args):

        text = self.main_text_area.get('1.0', 'end-1c')

        if text == '':
            self.reset_state()

        elif text != self.text:
            self.start_timer()

        self.text = text

    def start_timer(self):

        self.reset_timer()
        self.count_down(TIME_IN_SECONDS)

    def reset_state(self):

        text = self.main_text_area.get('1.0', 'end-1c')

        if text == '':
            self.timer_text_var.set(LABEL_INITIAL_TEXT)
            self.timer_text_label.configure(foreground=COLOR_BLUE)

        else:
            self.timer_text_var.set("Annnddd.... It's gone!")

        self.main_text_area.delete('1.0', END)
        self.main_text_area.configure(highlightbackground=COLOR_BLUE,
                                      highlightcolor=COLOR_BLUE)

        self.reset_timer()

    def reset_timer(self):

        if self.timer:
            self.master.after_cancel(self.timer)

    def count_down(self, count):

        minute = count // 60
        second = count % 60

        self.timer_text_var.set(f'Time remaining: {minute:02}:{second:02}')

        if count >= 0:

            self.change_border_color(count)

            self.timer = self.master.after(1000, self.count_down, count - 1)

        else:
            # Erase text and reset title
            self.reset_state()

    def change_border_color(self, time):
        match time:
            case 4:
                color = COLOR_GREEN
            case 3:
                color = COLOR_LIGHT_GREEN
            case 2:
                color = COLOR_YELLOW
            case 1:
                color = COLOR_ORANGE
            case 0:
                color = COLOR_RED
            case _:
                color = COLOR_BLUE
        self.main_text_area.configure(highlightbackground=color,
                                      highlightcolor=color)
        self.timer_text_label.configure(foreground=color)
