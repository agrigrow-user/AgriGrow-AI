# Execute this statement.
# Import threading.
import threading
# Import datetime from datetime.
from datetime import datetime
# Import tkinter as tk.
import tkinter as tk
# Import ttk from tkinter.
from tkinter import ttk

# Import Image, ImageTk from PIL.
from PIL import Image, ImageTk

# Import ( from core.
from core import (
    # Execute this statement.
    FEATURES,
    # Execute this statement.
    FEATURE_LABELS,
    # Execute this statement.
    append_history,
    # Execute this statement.
    compute_sensitivity,
    # Execute this statement.
    crop_tip,
    # Execute this statement.
    explain_features
# Close the previous block or structure.
)
# Import resource_path from paths.
from paths import resource_path
# Import detect_location, fetch_weather, search_locations from weather.
from weather import detect_location, fetch_weather, search_locations

# Set COLORS.
COLORS = {
    # Execute this statement.
    'bg': '#F4F6F2',
    # Execute this statement.
    'card': '#FFFFFF',
    # Execute this statement.
    'text': '#1F2A1F',
    # Execute this statement.
    'muted': '#5F6F5F',
    # Execute this statement.
    'primary': '#2F7D32',
    # Execute this statement.
    'primary_dark': '#256528',
    # Execute this statement.
    'accent': '#E2EAE0',
    # Execute this statement.
    'shadow': '#DDE5DD',
    # Execute this statement.
    'error_bg': '#FDECEC',
    # Execute this statement.
    'error_text': '#A10F0F',
    # Execute this statement.
    'warning_bg': '#FFF4CC',
    # Execute this statement.
    'warning_text': '#8A5D00',
    # Execute this statement.
    'input_bg': '#F8FBF7'
# Close the previous block or structure.
}

# Set HERO_IMAGE_PATH.
HERO_IMAGE_PATH = resource_path('Images/herosection_image.png')
# Set ENABLE_MULTI_MODEL_UI.
ENABLE_MULTI_MODEL_UI = False
# Set ENABLE_LOCATION_AUTOCOMPLETE.
ENABLE_LOCATION_AUTOCOMPLETE = True


# Define function style_app.
def style_app(root: tk.Tk) -> ttk.Style:
    # Set style.
    style = ttk.Style(root)
    # Start a protected block for error handling.
    try:
        # Call style.theme_use.
        style.theme_use('clam')
    # Handle an error case.
    except tk.TclError:
        # Do nothing (placeholder).
        pass

    # Set style.configure('TFrame', background.
    style.configure('TFrame', background=COLORS['bg'])
    # Set style.configure('TLabel', background.
    style.configure('TLabel', background=COLORS['bg'], foreground=COLORS['text'], font=('Segoe UI', 10))
    # Set style.configure('Title.TLabel', background.
    style.configure('Title.TLabel', background=COLORS['bg'], foreground=COLORS['text'], font=('Segoe UI', 20, 'bold'))
    # Set style.configure('Subtitle.TLabel', background.
    style.configure('Subtitle.TLabel', background=COLORS['bg'], foreground=COLORS['muted'], font=('Segoe UI', 11))
    # Set style.configure('Section.TLabel', background.
    style.configure('Section.TLabel', background=COLORS['bg'], foreground=COLORS['text'], font=('Segoe UI', 12, 'bold'))
    # Set style.configure('Card.TFrame', background.
    style.configure('Card.TFrame', background=COLORS['card'])
    # Set style.configure('Card.TLabel', background.
    style.configure('Card.TLabel', background=COLORS['card'], foreground=COLORS['text'], font=('Segoe UI', 10))
    # Set style.configure('Muted.TLabel', background.
    style.configure('Muted.TLabel', background=COLORS['bg'], foreground=COLORS['muted'], font=('Segoe UI', 10))
    # Set style.configure('Error.TLabel', background.
    style.configure('Error.TLabel', background=COLORS['bg'], foreground=COLORS['error_text'], font=('Segoe UI', 9))
    # Set style.configure('Green.Horizontal.TProgressbar', background.
    style.configure('Green.Horizontal.TProgressbar', background=COLORS['primary'], troughcolor=COLORS['accent'])
    # Return the computed value.
    return style


# Define function add_placeholder.
def add_placeholder(entry: tk.Entry, text: str):
    # Call entry.insert.
    entry.insert(0, text)
    # Set entry.config(fg.
    entry.config(fg=COLORS['muted'])
    # Set entry._placeholder.
    entry._placeholder = text
    # Set entry._placeholder_active.
    entry._placeholder_active = True

    # Define function on_focus_in.
    def on_focus_in(_event):
        # Check condition and run block if true.
        if getattr(entry, '_placeholder_active', False):
            # Call entry.delete.
            entry.delete(0, tk.END)
            # Set entry.config(fg.
            entry.config(fg=COLORS['text'])
            # Set entry._placeholder_active.
            entry._placeholder_active = False

    # Define function on_focus_out.
    def on_focus_out(_event):
        # Check condition and run block if true.
        if not entry.get().strip():
            # Call entry.insert.
            entry.insert(0, text)
            # Set entry.config(fg.
            entry.config(fg=COLORS['muted'])
            # Set entry._placeholder_active.
            entry._placeholder_active = True

    # Call entry.bind.
    entry.bind('<FocusIn>', on_focus_in)
    # Call entry.bind.
    entry.bind('<FocusOut>', on_focus_out)


# Define function get_entry_value.
def get_entry_value(entry: tk.Entry) -> str:
    # Check condition and run block if true.
    if getattr(entry, '_placeholder_active', False):
        # Return the computed value.
        return ''
    # Return the computed value.
    return entry.get().strip()


# Define function set_entry_value.
def set_entry_value(entry: tk.Entry, value: str):
    # Set entry.configure(state.
    entry.configure(state='normal')
    # Call entry.delete.
    entry.delete(0, tk.END)
    # Call entry.insert.
    entry.insert(0, value)
    # Set entry.config(fg.
    entry.config(fg=COLORS['text'])
    # Set entry._placeholder_active.
    entry._placeholder_active = False


# Define function reset_entry.
def reset_entry(entry: tk.Entry):
    # Set entry.configure(state.
    entry.configure(state='normal')
    # Call entry.delete.
    entry.delete(0, tk.END)
    # Set placeholder.
    placeholder = getattr(entry, '_placeholder', '')
    # Check condition and run block if true.
    if placeholder:
        # Call entry.insert.
        entry.insert(0, placeholder)
        # Set entry.config(fg.
        entry.config(fg=COLORS['muted'])
        # Set entry._placeholder_active.
        entry._placeholder_active = True
    # Fallback branch when conditions do not match.
    else:
        # Set entry.config(fg.
        entry.config(fg=COLORS['text'])
        # Set entry._placeholder_active.
        entry._placeholder_active = False


# Define function format_confidence_note.
def format_confidence_note(confidence: float, alternatives: list) -> str:
    # Check condition and run block if true.
    if not alternatives:
        # Return the computed value.
        return 'Confidence is the model probability for the top crop.'
    # Set top2.
    top2 = float(alternatives[0][1])
    # Set gap.
    gap = max(confidence - top2, 0.0)
    # Check condition and run block if true.
    if confidence < 0.45 or gap < 0.10:
        # Return the computed value.
        return f'Low confidence: similar crops compete (top gap {gap * 100:.1f}%).'
    # Check condition and run block if true.
    if gap < 0.20:
        # Return the computed value.
        return f'Moderate confidence (top gap {gap * 100:.1f}%).'
    # Return the computed value.
    return f'Clear separation from next option (top gap {gap * 100:.1f}%).'


# Define function make_card.
def make_card(parent, padding=16, shadow_pad=2):
    # Set shadow.
    shadow = tk.Frame(parent, bg=COLORS['shadow'])
    # Set card.
    card = tk.Frame(shadow, bg=COLORS['card'], padx=padding, pady=padding)
    # Set card.pack(padx.
    card.pack(padx=shadow_pad, pady=shadow_pad, fill='both', expand=True)
    # Return the computed value.
    return shadow, card


# Define class CropApp.
class CropApp(tk.Tk):
    # Define function __init__.
    def __init__(self, state):
        # Call super.
        super().__init__()
        # Set self.state.
        self.state = state
        # Call self.title.
        self.title('AgriYield AI - Crop Recommendation')
        # Call self.geometry.
        self.geometry('1180x780')
        # Call self.minsize.
        self.minsize(1050, 720)
        # Set self.configure(bg.
        self.configure(bg=COLORS['bg'])

        # Call style_app.
        style_app(self)

        # Set self.header.
        self.header = tk.Frame(self, bg=COLORS['card'], height=60)
        # Set self.header.pack(fill.
        self.header.pack(fill='x')

        # Set brand.
        brand = tk.Label(self.header, text='AgriGrow', bg=COLORS['card'], fg=COLORS['text'],
                         # Set font.
                         font=('Segoe UI', 12, 'bold'))
        # Set brand.pack(side.
        brand.pack(side='left', padx=18)

        # Set nav.
        nav = tk.Frame(self.header, bg=COLORS['card'])
        # Set nav.pack(side.
        nav.pack(side='right', padx=12)

        # Set self.nav_buttons.
        self.nav_buttons = {}
        # Loop over items in a sequence.
        for name, target in [
            # Execute this statement.
            ('Home', 'HomeFrame'),
            # Execute this statement.
            ('My Fields', 'DashboardFrame'),
            # Execute this statement.
            ('Reports', 'ResultsFrame'),
            # Execute this statement.
            ('History', 'HistoryFrame')
        # Execute this statement.
        ]:
            # Set btn.
            btn = tk.Button(nav, text=name, command=lambda t=target: self.show_frame(t),
                            # Set bg.
                            bg=COLORS['card'], fg=COLORS['text'], bd=0, highlightthickness=0,
                            # Set activebackground.
                            activebackground=COLORS['card'], activeforeground=COLORS['primary'])
            # Set btn.pack(side.
            btn.pack(side='left', padx=10, pady=10)
            # Set self.nav_buttons[target].
            self.nav_buttons[target] = btn

        # Set avatar.
        avatar = tk.Label(self.header, text='A', bg=COLORS['accent'], fg=COLORS['primary'],
                          # Set font.
                          font=('Segoe UI', 10, 'bold'), width=3, height=1)
        # Set avatar.pack(side.
        avatar.pack(side='right', padx=10)

        # Set self.container.
        self.container = tk.Frame(self, bg=COLORS['bg'])
        # Set self.container.pack(fill.
        self.container.pack(fill='both', expand=True)
        # Set self.container.grid_rowconfigure(0, weight.
        self.container.grid_rowconfigure(0, weight=1)
        # Set self.container.grid_columnconfigure(0, weight.
        self.container.grid_columnconfigure(0, weight=1)

        # Set self.frames.
        self.frames = {}
        # Loop over items in a sequence.
        for FrameClass in (HomeFrame, DashboardFrame, ResultsFrame, HistoryFrame):
            # Set frame.
            frame = FrameClass(self.container, self, self.state)
            # Set frame.grid(row.
            frame.grid(row=0, column=0, sticky='nsew')
            # Set self.frames[FrameClass.__name__].
            self.frames[FrameClass.__name__] = frame

        # Call self.show_frame.
        self.show_frame('HomeFrame')

    # Define function show_frame.
    def show_frame(self, name: str):
        # Set frame.
        frame = self.frames[name]
        # Call frame.tkraise.
        frame.tkraise()
        # Loop over items in a sequence.
        for target, btn in self.nav_buttons.items():
            # Check condition and run block if true.
            if target == name:
                # Set btn.configure(fg.
                btn.configure(fg=COLORS['primary'])
            # Fallback branch when conditions do not match.
            else:
                # Set btn.configure(fg.
                btn.configure(fg=COLORS['text'])

    # Define function show_results.
    def show_results(self, result: dict):
        # Set results_frame.
        results_frame = self.frames['ResultsFrame']
        # Call results_frame.update_results.
        results_frame.update_results(result)
        # Call self.show_frame.
        self.show_frame('ResultsFrame')

    # Define function update_location.
    def update_location(self, query: str, display: str | None = None):
        # Check condition and run block if true.
        if not query:
            # Return the computed value.
            return
        # Set self.state.current_location.
        self.state.current_location = query
        # Set self.state.current_location_display.
        self.state.current_location_display = display or query
        # Set home.
        home = self.frames.get('HomeFrame')
        # Check condition and run block if true.
        if home and hasattr(home, 'update_location'):
            # Call home.update_location.
            home.update_location(self.state.current_location_display)

    # Define function refresh_history.
    def refresh_history(self):
        # Set history_frame.
        history_frame = self.frames['HistoryFrame']
        # Call history_frame.refresh.
        history_frame.refresh()


# Define class HomeFrame.
class HomeFrame(ttk.Frame):
    # Define function __init__.
    def __init__(self, parent, app: CropApp, state):
        # Call super.
        super().__init__(parent)
        # Set self.app.
        self.app = app
        # Set self.state.
        self.state = state
        # Set self.hero_image.
        self.hero_image = None
        # Set self.hero_photo.
        self.hero_photo = None

        # Set hero_shadow, hero_wrap.
        hero_shadow, hero_wrap = make_card(self, padding=0)
        # Set hero_shadow.pack(padx.
        hero_shadow.pack(padx=24, pady=(18, 8), fill='x')
        # Set self.hero_canvas.
        self.hero_canvas = tk.Canvas(hero_wrap, height=320, bg=COLORS['bg'], highlightthickness=0)
        # Set self.hero_canvas.pack(fill.
        self.hero_canvas.pack(fill='x')
        # Call self.hero_canvas.bind.
        self.hero_canvas.bind('<Configure>', self._resize_hero)

        # Set stats.
        stats = tk.Frame(self, bg=COLORS['bg'])
        # Set stats.pack(padx.
        stats.pack(padx=24, pady=10, fill='x')

        # Set acc_text.
        acc_text = 'Model Accuracy'
        # Check condition and run block if true.
        if state.best_accuracy is not None:
            # Set acc_text.
            acc_text = f'Best Accuracy: {state.best_accuracy * 100:.1f}%'

        # Set model_count.
        model_count = len(state.models)
        # Execute this statement.
        model_label = f'{model_count} Model' if model_count == 1 else f'{model_count} Models'
        # Loop over items in a sequence.
        for value, label in [
            # Execute this statement.
            (acc_text.split(':')[-1].strip() if ':' in acc_text else acc_text, 'Accuracy'),
            # Execute this statement.
            (model_label.split()[0], 'Models'),
            # Execute this statement.
            ('22', 'Crops'),
            # Execute this statement.
            ('Live', 'Weather')
        # Execute this statement.
        ]:
            # Set card_shadow, card.
            card_shadow, card = make_card(stats, padding=12)
            # Set card_shadow.pack(side.
            card_shadow.pack(side='left', padx=8)
            # Set tk.Label(card, text.
            tk.Label(card, text=value, bg=COLORS['card'], fg=COLORS['primary'],
                     # Set font.
                     font=('Segoe UI', 12, 'bold')).pack()
            # Set tk.Label(card, text.
            tk.Label(card, text=label, bg=COLORS['card'], fg=COLORS['muted'],
                     # Set font.
                     font=('Segoe UI', 9)).pack()

        # Set location_row.
        location_row = tk.Frame(self, bg=COLORS['bg'])
        # Set location_row.pack(padx.
        location_row.pack(padx=24, pady=(0, 6), fill='x')
        # Set tk.Label(location_row, text.
        tk.Label(location_row, text='Current Location:', bg=COLORS['bg'], fg=COLORS['muted'],
                 # Set font.
                 font=('Segoe UI', 9, 'bold')).pack(side='left')
        # Set self.location_var.
        self.location_var = tk.StringVar(value='Detecting location...')
        # Set self.location_value.
        self.location_value = tk.Label(location_row, textvariable=self.location_var,
                                       # Set bg.
                                       bg=COLORS['bg'], fg=COLORS['text'])
        # Set self.location_value.pack(side.
        self.location_value.pack(side='left', padx=(6, 0))
        # Call self.update_location.
        self.update_location(state.current_location_display or state.current_location)

        # Set sections.
        sections = tk.Frame(self, bg=COLORS['bg'])
        # Set sections.pack(padx.
        sections.pack(padx=24, pady=20, fill='x')

        # Set tk.Label(sections, text.
        tk.Label(sections, text='Precision Farming Services', bg=COLORS['bg'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        # Set tk.Label(sections, text.
        tk.Label(sections, text='Everything you need to maximize your harvest', bg=COLORS['bg'],
                 # Set fg.
                 fg=COLORS['muted']).pack(anchor='w', pady=(2, 10))

        # Set cards.
        cards = tk.Frame(sections, bg=COLORS['bg'])
        # Set cards.pack(fill.
        cards.pack(fill='x')

        # Loop over items in a sequence.
        for title, desc in [
            # Execute this statement.
            ('Soil Analysis', 'Deep insights into NPK levels and pH.'),
            # Execute this statement.
            ('Crop Advice', 'Recommendations based on your inputs.'),
            # Execute this statement.
            ('Weather Alerts', 'Real-time data for climate awareness.')
        # Execute this statement.
        ]:
            # Set card_shadow, card.
            card_shadow, card = make_card(cards, padding=14)
            # Set card_shadow.pack(side.
            card_shadow.pack(side='left', padx=8, fill='x', expand=True)
            # Set tk.Label(card, text.
            tk.Label(card, text=title, bg=COLORS['card'], fg=COLORS['text'],
                     # Set font.
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')
            # Set tk.Label(card, text.
            tk.Label(card, text=desc, bg=COLORS['card'], fg=COLORS['muted'], wraplength=250,
                     # Set font.
                     font=('Segoe UI', 9)).pack(anchor='w', pady=(4, 0))

    # Define function _resize_hero.
    def _resize_hero(self, event):
        # Set width.
        width = max(1, event.width)
        # Set height.
        height = max(1, event.height)
        # Check condition and run block if true.
        if self.hero_image is None:
            # Start a protected block for error handling.
            try:
                # Set self.hero_image.
                self.hero_image = Image.open(HERO_IMAGE_PATH)
            # Handle an error case.
            except Exception:
                # Call self.hero_canvas.delete.
                self.hero_canvas.delete('all')
                # Set self.hero_canvas.create_text(24, 60, anchor.
                self.hero_canvas.create_text(24, 60, anchor='nw', text='Grow the Right Crop for Your Soil',
                                             # Set fill.
                                             fill=COLORS['text'], font=('Segoe UI', 20, 'bold'))
                # Return the computed value.
                return

        # Set img.
        img = self.hero_image.resize((width, height), Image.LANCZOS)
        # Set self.hero_photo.
        self.hero_photo = ImageTk.PhotoImage(img)
        # Call self.hero_canvas.delete.
        self.hero_canvas.delete('all')
        # Set self.hero_canvas.create_image(0, 0, anchor.
        self.hero_canvas.create_image(0, 0, anchor='nw', image=self.hero_photo)
        # Set self.hero_canvas.create_rectangle(0, 0, width, height, fill.
        self.hero_canvas.create_rectangle(0, 0, width, height, fill='#000000', stipple='gray25', outline='')

        # Set pill_x, pill_y, pill_w, pill_h.
        pill_x, pill_y, pill_w, pill_h = 30, 36, 220, 26
        # Call self.hero_canvas.create_rectangle.
        self.hero_canvas.create_rectangle(pill_x, pill_y, pill_x + pill_w, pill_y + pill_h,
                                          # Set fill.
                                          fill='#356F3C', outline='')
        # Set self.hero_canvas.create_text(pill_x + 10, pill_y + 6, anchor.
        self.hero_canvas.create_text(pill_x + 10, pill_y + 6, anchor='nw',
                                     # Set text.
                                     text='AI-POWERED SOIL INTELLIGENCE',
                                     # Set fill.
                                     fill='#DFF2E2', font=('Segoe UI', 8, 'bold'))

        # Set self.hero_canvas.create_text(30, 80, anchor.
        self.hero_canvas.create_text(30, 80, anchor='nw', text='Grow the Right Crop\nfor Your Soil',
                                     # Set fill.
                                     fill='white', font=('Segoe UI', 24, 'bold'))
        # Set self.hero_canvas.create_text(30, 160, anchor.
        self.hero_canvas.create_text(30, 160, anchor='nw',
                                     # Set text.
                                     text='Optimize your yield with AI-driven crop recommendations\n'
                                          # Execute this statement.
                                          'tailored to your soil and climate.',
                                     # Set fill.
                                     fill='#E8F2E9', font=('Segoe UI', 10))

        # Set btn.
        btn = tk.Button(self.hero_canvas, text='Get Started',
                        # Set command.
                        command=lambda: self.app.show_frame('DashboardFrame'),
                        # Set bg.
                        bg=COLORS['primary'], fg='white', bd=0, padx=16, pady=8)
        # Set self.hero_canvas.create_window(30, 230, anchor.
        self.hero_canvas.create_window(30, 230, anchor='nw', window=btn)
        # Set secondary.
        secondary = tk.Button(self.hero_canvas, text='How it Works',
                              # Set command.
                              command=lambda: self.app.show_frame('DashboardFrame'),
                              # Set bg.
                              bg='#2E3B2E', fg='white', bd=0, padx=16, pady=8)
        # Set self.hero_canvas.create_window(150, 230, anchor.
        self.hero_canvas.create_window(150, 230, anchor='nw', window=secondary)

    # Define function update_location.
    def update_location(self, location: str | None):
        # Set text.
        text = location.strip() if location else 'Detecting location...'
        # Call self.location_var.set.
        self.location_var.set(text)

# Define class DashboardFrame.
class DashboardFrame(ttk.Frame):
    # Define function __init__.
    def __init__(self, parent, app: CropApp, state):
        # Call super.
        super().__init__(parent)
        # Set self.app.
        self.app = app
        # Set self.state.
        self.state = state
        # Set self.recent_locations.
        self.recent_locations = []
        # Set self.location_choices.
        self.location_choices = {}
        # Set self.search_job.
        self.search_job = None
        # Set self.search_token.
        self.search_token = 0
        # Set self.auto_fetch_done.
        self.auto_fetch_done = False

        # Set self.banner_var.
        self.banner_var = tk.StringVar(value='')
        # Set self.banner.
        self.banner = tk.Frame(self, bg=COLORS['error_bg'], padx=10, pady=6)
        # Set self.banner_label.
        self.banner_label = tk.Label(self.banner, textvariable=self.banner_var, bg=COLORS['error_bg'],
                                     # Set fg.
                                     fg=COLORS['error_text'], font=('Segoe UI', 10, 'bold'))
        # Set self.banner_label.pack(side.
        self.banner_label.pack(side='left')
        # Call self.banner.pack_forget.
        self.banner.pack_forget()

        # Set header.
        header = tk.Frame(self, bg=COLORS['bg'])
        # Set header.pack(padx.
        header.pack(padx=24, pady=(20, 10), fill='x')

        # Set header_top.
        header_top = tk.Frame(header, bg=COLORS['bg'])
        # Set header_top.pack(fill.
        header_top.pack(fill='x')
        # Set tk.Label(header_top, text.
        tk.Label(header_top, text='Crop Recommendation System', bg=COLORS['bg'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 18, 'bold')).pack(side='left', anchor='w')

        # Set actions.
        actions = tk.Frame(header_top, bg=COLORS['bg'])
        # Set actions.pack(side.
        actions.pack(side='right')
        # Set self.clear_btn.
        self.clear_btn = tk.Button(actions, text='Clear Form', command=self.clear_form,
                                   # Set bg.
                                   bg=COLORS['accent'], fg=COLORS['text'], bd=0, padx=14, pady=8)
        # Set self.clear_btn.pack(side.
        self.clear_btn.pack(side='left', padx=(0, 8))
        # Set self.submit_btn.
        self.submit_btn = tk.Button(actions, text='Get Recommendation', command=self.on_submit,
                                    # Set bg.
                                    bg=COLORS['primary'], fg='white', bd=0, padx=18, pady=10)
        # Set self.submit_btn.pack(side.
        self.submit_btn.pack(side='left')

        # Set tk.Label(header, text.
        tk.Label(header, text='Enter soil and weather parameters for AI recommendations.',
                 # Set bg.
                 bg=COLORS['bg'], fg=COLORS['muted']).pack(anchor='w')

        # Check condition and run block if true.
        if ENABLE_MULTI_MODEL_UI:
            # Set model_row.
            model_row = tk.Frame(self, bg=COLORS['bg'])
            # Set model_row.pack(padx.
            model_row.pack(padx=24, pady=(6, 4), fill='x')

            # Set tk.Label(model_row, text.
            tk.Label(model_row, text='Model Selection', bg=COLORS['bg'], fg=COLORS['text'],
                     # Set font.
                     font=('Segoe UI', 10, 'bold')).pack(side='left')

            # Set self.model_var.
            self.model_var = tk.StringVar(value=self.state.active_model_name)
            # Set self.model_combo.
            self.model_combo = ttk.Combobox(model_row, textvariable=self.model_var,
                                            # Set values.
                                            values=list(self.state.models.keys()), width=24, state='readonly')
            # Set self.model_combo.pack(side.
            self.model_combo.pack(side='left', padx=10)
            # Call self.model_combo.bind.
            self.model_combo.bind('<<ComboboxSelected>>', self.on_model_change)

            # Set self.model_acc_label.
            self.model_acc_label = tk.Label(model_row, text='', bg=COLORS['bg'], fg=COLORS['muted'])
            # Set self.model_acc_label.pack(side.
            self.model_acc_label.pack(side='left', padx=12)
            # Call self.refresh_model_accuracy.
            self.refresh_model_accuracy()

        # Set content.
        content = tk.Frame(self, bg=COLORS['bg'])
        # Set content.pack(padx.
        content.pack(padx=24, pady=6, fill='x')

        # Set left_shadow, left.
        left_shadow, left = make_card(content, padding=18)
        # Set left_shadow.pack(side.
        left_shadow.pack(side='left', padx=(0, 12), fill='both', expand=True)

        # Set right_shadow, right.
        right_shadow, right = make_card(content, padding=18)
        # Set right_shadow.pack(side.
        right_shadow.pack(side='left', fill='both', expand=True)

        # Set tk.Label(left, text.
        tk.Label(left, text='Soil Composition', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')

        # Set self.fields.
        self.fields = {}
        # Set self.error_vars.
        self.error_vars = {}

        # Define function add_entry.
        def add_entry(parent_frame, key, placeholder=''):
            # Set label.
            label = FEATURE_LABELS[key]
            # Set tk.Label(parent_frame, text.
            tk.Label(parent_frame, text=label, bg=COLORS['card'], fg=COLORS['muted'],
                     # Set font.
                     font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(10, 2))
            # Set entry.
            entry = tk.Entry(parent_frame, width=24, bg=COLORS['input_bg'], fg=COLORS['text'],
                             # Set relief.
                             relief='flat', highlightthickness=1, highlightbackground=COLORS['accent'])
            # Set entry.pack(anchor.
            entry.pack(anchor='w', ipady=4)
            # Check condition and run block if true.
            if placeholder:
                # Call add_placeholder.
                add_placeholder(entry, placeholder)
            # Set err_var.
            err_var = tk.StringVar(value='')
            # Set err_label.
            err_label = tk.Label(parent_frame, textvariable=err_var, bg=COLORS['card'],
                                 # Set fg.
                                 fg=COLORS['error_text'], font=('Segoe UI', 8))
            # Set err_label.pack(anchor.
            err_label.pack(anchor='w')
            # Set self.fields[key].
            self.fields[key] = entry
            # Set self.error_vars[key].
            self.error_vars[key] = err_var

        # Call add_entry.
        add_entry(left, 'N', 'e.g. 90')
        # Call add_entry.
        add_entry(left, 'P', 'e.g. 42')
        # Call add_entry.
        add_entry(left, 'K', 'e.g. 43')
        # Call add_entry.
        add_entry(left, 'ph', 'e.g. 6.5')

        # Set tk.Label(right, text.
        tk.Label(right, text='Environmental Data', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w')

        # Set self.use_live.
        self.use_live = tk.BooleanVar(value=True)
        # Set live_row.
        live_row = tk.Frame(right, bg=COLORS['card'])
        # Set live_row.pack(fill.
        live_row.pack(fill='x', pady=(10, 6))
        # Set tk.Label(live_row, text.
        tk.Label(live_row, text='Use live weather', bg=COLORS['card'], fg=COLORS['muted']).pack(side='left')
        # Set ttk.Checkbutton(live_row, variable.
        ttk.Checkbutton(live_row, variable=self.use_live, command=self.toggle_live).pack(side='right')

        # Set location_row.
        location_row = tk.Frame(right, bg=COLORS['card'])
        # Set location_row.pack(fill.
        location_row.pack(fill='x', pady=(6, 8))
        # Set tk.Label(location_row, text.
        tk.Label(location_row, text='City/Region', bg=COLORS['card'], fg=COLORS['muted'],
                 # Set font.
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        # Set self.location_var.
        self.location_var = tk.StringVar()
        # Set self.location_combo.
        self.location_combo = ttk.Combobox(location_row, textvariable=self.location_var, width=26)
        # Set self.location_combo.pack(side.
        self.location_combo.pack(side='left', pady=(2, 0), ipady=2)
        # Check condition and run block if true.
        if ENABLE_LOCATION_AUTOCOMPLETE:
            # Call self.location_combo.bind.
            self.location_combo.bind('<KeyRelease>', self.on_location_type)
            # Call self.location_combo.bind.
            self.location_combo.bind('<<ComboboxSelected>>', self.on_location_select)

        # Set self.detect_btn.
        self.detect_btn = tk.Button(location_row, text='Detect', command=lambda: self.on_detect_location(auto_fetch=True),
                                    # Set bg.
                                    bg=COLORS['accent'], fg=COLORS['text'], bd=0, padx=8, pady=6)
        # Set self.detect_btn.pack(side.
        self.detect_btn.pack(side='left', padx=6)

        # Set self.fetch_btn.
        self.fetch_btn = tk.Button(location_row, text='Fetch Live', command=self.on_fetch_weather,
                                   # Set bg.
                                   bg=COLORS['accent'], fg=COLORS['text'], bd=0, padx=10, pady=6)
        # Set self.fetch_btn.pack(side.
        self.fetch_btn.pack(side='left', padx=6)

        # Set self.search_btn.
        self.search_btn = tk.Button(location_row, text='Search', command=self.on_search_location,
                                    # Set bg.
                                    bg=COLORS['accent'], fg=COLORS['text'], bd=0, padx=10, pady=6)
        # Set self.search_btn.pack(side.
        self.search_btn.pack(side='left', padx=6)

        # Set recent_row.
        recent_row = tk.Frame(right, bg=COLORS['card'])
        # Set recent_row.pack(fill.
        recent_row.pack(fill='x', pady=(6, 10))
        # Set tk.Label(recent_row, text.
        tk.Label(recent_row, text='Recent Locations', bg=COLORS['card'], fg=COLORS['muted'],
                 # Set font.
                 font=('Segoe UI', 9, 'bold')).pack(side='left')
        # Set self.recent_var.
        self.recent_var = tk.StringVar()
        # Set self.recent_combo.
        self.recent_combo = ttk.Combobox(recent_row, textvariable=self.recent_var,
                                         # Set values.
                                         values=self.recent_locations, width=24, state='readonly')
        # Set self.recent_combo.pack(side.
        self.recent_combo.pack(side='left', padx=8)
        # Call self.recent_combo.bind.
        self.recent_combo.bind('<<ComboboxSelected>>', self.on_recent_select)

        # Check condition and run block if true.
        if self.state.current_location_display or self.state.current_location:
            # Call self.set_current_location.
            self.set_current_location(
                # Execute this statement.
                self.state.current_location_display or self.state.current_location,
                # Execute this statement.
                self.state.current_location,
                # Set update_recent.
                update_recent=False
            # Close the previous block or structure.
            )

        # Call add_entry.
        add_entry(right, 'temperature', 'e.g. 25')
        # Call add_entry.
        add_entry(right, 'humidity', 'e.g. 70')
        # Call add_entry.
        add_entry(right, 'rainfall', 'e.g. 200')

        # Set self.weather_info.
        self.weather_info = tk.Frame(right, bg=COLORS['accent'], padx=10, pady=10)
        # Set self.weather_info.pack(fill.
        self.weather_info.pack(fill='x', pady=(10, 0))
        # Set tk.Label(self.weather_info, text.
        tk.Label(self.weather_info, text='Weather Snapshot', bg=COLORS['accent'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        # Set self.weather_detail.
        self.weather_detail = tk.Label(self.weather_info, text='No weather fetched yet.', bg=COLORS['accent'],
                                       # Set fg.
                                       fg=COLORS['muted'], justify='left')
        # Set self.weather_detail.pack(anchor.
        self.weather_detail.pack(anchor='w', pady=(4, 0))

        # Set tk.Label(right, text.
        tk.Label(right, text='Recommendation Preview', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(12, 0))
        # Set self.preview_crop.
        self.preview_crop = tk.Label(right, text='No recommendation yet.',
                                     # Set bg.
                                     bg=COLORS['card'], fg=COLORS['muted'])
        # Set self.preview_crop.pack(anchor.
        self.preview_crop.pack(anchor='w', pady=(6, 2))
        # Set self.preview_conf.
        self.preview_conf = tk.Label(right, text='', bg=COLORS['card'], fg=COLORS['muted'])
        # Set self.preview_conf.pack(anchor.
        self.preview_conf.pack(anchor='w')
        # Set self.preview_alt.
        self.preview_alt = tk.Label(right, text='', bg=COLORS['card'], fg=COLORS['muted'])
        # Set self.preview_alt.pack(anchor.
        self.preview_alt.pack(anchor='w', pady=(0, 4))
        # Set self.preview_note.
        self.preview_note = tk.Label(right, text='', bg=COLORS['card'], fg=COLORS['muted'],
                                     # Set wraplength.
                                     wraplength=320, justify='left')
        # Set self.preview_note.pack(anchor.
        self.preview_note.pack(anchor='w', pady=(0, 4))
        # Set self.view_results_btn.
        self.view_results_btn = tk.Button(right, text='View Detailed Results',
                                          # Set command.
                                          command=lambda: self.app.show_frame('ResultsFrame'),
                                          # Set bg.
                                          bg=COLORS['accent'], fg=COLORS['text'], bd=0, padx=12, pady=6)
        # Set self.view_results_btn.pack(anchor.
        self.view_results_btn.pack(anchor='w', pady=(6, 0))

        # Check condition and run block if true.
        if ENABLE_MULTI_MODEL_UI:
            # Set comparison.
            comparison = tk.Frame(self, bg=COLORS['card'], padx=14, pady=12, bd=1, relief='solid')
            # Set comparison.pack(padx.
            comparison.pack(padx=24, pady=(0, 16), fill='x')
            # Set tk.Label(comparison, text.
            tk.Label(comparison, text='Model Comparison', bg=COLORS['card'], fg=COLORS['text'],
                     # Set font.
                     font=('Segoe UI', 11, 'bold')).pack(anchor='w')

            # Set self.model_list.
            self.model_list = tk.Frame(comparison, bg=COLORS['card'])
            # Set self.model_list.pack(fill.
            self.model_list.pack(fill='x', pady=(6, 0))
            # Set self.model_rows.
            self.model_rows = {}
            # Loop over items in a sequence.
            for name in self.state.models.keys():
                # Set row.
                row = tk.Frame(self.model_list, bg=COLORS['card'])
                # Set row.pack(fill.
                row.pack(fill='x')
                # Set name_label.
                name_label = tk.Label(row, text=name, bg=COLORS['card'], fg=COLORS['text'])
                # Set name_label.pack(side.
                name_label.pack(side='left')
                # Set acc_label.
                acc_label = tk.Label(row, text='-', bg=COLORS['card'], fg=COLORS['muted'])
                # Set acc_label.pack(side.
                acc_label.pack(side='right')
                # Set self.model_rows[name].
                self.model_rows[name] = (name_label, acc_label)

            # Call self.refresh_model_list.
            self.refresh_model_list()
        # Call self.toggle_live.
        self.toggle_live()
        # Call self.after.
        self.after(400, self.auto_detect_fetch)

    # Define function refresh_model_accuracy.
    def refresh_model_accuracy(self):
        # Set acc.
        acc = self.state.accuracies.get(self.state.active_model_name) if self.state.accuracies else None
        # Check condition and run block if true.
        if acc is None:
            # Set text.
            text = 'Accuracy: n/a'
        # Fallback branch when conditions do not match.
        else:
            # Set text.
            text = f'Accuracy: {acc * 100:.1f}%'
        # Set self.model_acc_label.config(text.
        self.model_acc_label.config(text=text)

    # Define function refresh_model_list.
    def refresh_model_list(self):
        # Loop over items in a sequence.
        for name, (name_label, acc_label) in self.model_rows.items():
            # Set acc.
            acc = self.state.accuracies.get(name) if self.state.accuracies else None
            # Set acc_text.
            acc_text = f'{acc * 100:.1f}%' if acc is not None else 'n/a'
            # Set acc_label.config(text.
            acc_label.config(text=acc_text)
            # Check condition and run block if true.
            if name == self.state.active_model_name:
                # Set name_label.config(fg.
                name_label.config(fg=COLORS['primary'])
            # Fallback branch when conditions do not match.
            else:
                # Set name_label.config(fg.
                name_label.config(fg=COLORS['text'])

    # Define function on_model_change.
    def on_model_change(self, _event=None):
        # Set selected.
        selected = self.model_var.get()
        # Check condition and run block if true.
        if selected in self.state.models:
            # Set self.state.active_model_name.
            self.state.active_model_name = selected
            # Call self.refresh_model_accuracy.
            self.refresh_model_accuracy()
            # Call self.refresh_model_list.
            self.refresh_model_list()

    # Define function toggle_live.
    def toggle_live(self):
        # Set use_live.
        use_live = self.use_live.get()
        # Loop over items in a sequence.
        for key in ['temperature', 'humidity', 'rainfall']:
            # Set self.fields[key].configure(state.
            self.fields[key].configure(state='normal')
        # Set self.fetch_btn.configure(state.
        self.fetch_btn.configure(state='normal' if use_live else 'disabled')
        # Set self.detect_btn.configure(state.
        self.detect_btn.configure(state='normal' if use_live else 'disabled')
        # Set self.search_btn.configure(state.
        self.search_btn.configure(state='normal' if use_live else 'disabled')

    # Define function show_banner.
    def show_banner(self, message: str, level: str = 'error'):
        # Check condition and run block if true.
        if message:
            # Check condition and run block if true.
            if level == 'warning':
                # Set self.banner.configure(bg.
                self.banner.configure(bg=COLORS['warning_bg'])
                # Set self.banner_label.configure(bg.
                self.banner_label.configure(bg=COLORS['warning_bg'], fg=COLORS['warning_text'])
            # Fallback branch when conditions do not match.
            else:
                # Set self.banner.configure(bg.
                self.banner.configure(bg=COLORS['error_bg'])
                # Set self.banner_label.configure(bg.
                self.banner_label.configure(bg=COLORS['error_bg'], fg=COLORS['error_text'])
            # Call self.banner_var.set.
            self.banner_var.set(message)
            # Set self.banner.pack(padx.
            self.banner.pack(padx=24, pady=(10, 0), fill='x')
        # Fallback branch when conditions do not match.
        else:
            # Call self.banner_var.set.
            self.banner_var.set('')
            # Call self.banner.pack_forget.
            self.banner.pack_forget()

    # Define function enable_manual_weather.
    def enable_manual_weather(self, message: str):
        # Call self.use_live.set.
        self.use_live.set(False)
        # Call self.toggle_live.
        self.toggle_live()
        # Set hint.
        hint = 'Weather fetch failed. You can enter values manually.'
        # Check condition and run block if true.
        if message:
            # Set self.show_banner(f'{message} {hint}', level.
            self.show_banner(f'{message} {hint}', level='error')
        # Fallback branch when conditions do not match.
        else:
            # Set self.show_banner(hint, level.
            self.show_banner(hint, level='error')

    # Define function clear_errors.
    def clear_errors(self):
        # Loop over items in a sequence.
        for err in self.error_vars.values():
            # Call err.set.
            err.set('')
        # Call self.show_banner.
        self.show_banner('')

    # Define function clear_form.
    def clear_form(self):
        # Loop over items in a sequence.
        for entry in self.fields.values():
            # Call reset_entry.
            reset_entry(entry)
        # Call self.location_var.set.
        self.location_var.set('')
        # Call self.use_live.set.
        self.use_live.set(True)
        # Call self.toggle_live.
        self.toggle_live()
        # Set self.weather_detail.config(text.
        self.weather_detail.config(text='No weather fetched yet.')
        # Call self.clear_suggestions.
        self.clear_suggestions()
        # Call self.clear_errors.
        self.clear_errors()
        # Check condition and run block if true.
        if self.state.current_location_display or self.state.current_location:
            # Call self.set_current_location.
            self.set_current_location(
                # Execute this statement.
                self.state.current_location_display or self.state.current_location,
                # Execute this statement.
                self.state.current_location,
                # Set update_recent.
                update_recent=False
            # Close the previous block or structure.
            )

    # Define function validate_inputs.
    def validate_inputs(self) -> tuple:
        # Call self.clear_errors.
        self.clear_errors()
        # Set values.
        values = {}
        # Set has_error.
        has_error = False
        # Set has_warning.
        has_warning = False

        # Loop over items in a sequence.
        for key in FEATURES:
            # Set raw.
            raw = get_entry_value(self.fields[key])
            # Check condition and run block if true.
            if not raw:
                # Execute this statement.
                self.error_vars[key].set('Required field')
                # Set has_error.
                has_error = True
                # Skip to the next loop iteration.
                continue
            # Start a protected block for error handling.
            try:
                # Set val.
                val = float(raw)
            # Handle an error case.
            except ValueError:
                # Execute this statement.
                self.error_vars[key].set('Enter a numeric value')
                # Set has_error.
                has_error = True
                # Skip to the next loop iteration.
                continue

            # Set rng.
            rng = self.state.validation_ranges.get(key, {})
            # Set min_val.
            min_val = rng.get('min')
            # Set max_val.
            max_val = rng.get('max')
            # Set rec_min.
            rec_min = rng.get('rec_min')
            # Set rec_max.
            rec_max = rng.get('rec_max')
            # Set data_min.
            data_min = rng.get('data_min')
            # Set data_max.
            data_max = rng.get('data_max')

            # Check condition and run block if true.
            if min_val is not None and (val < min_val or val > max_val):
                # Execute this statement.
                self.error_vars[key].set(f'Expected {min_val:.1f}-{max_val:.1f}')
                # Set has_error.
                has_error = True
                # Skip to the next loop iteration.
                continue

            # Set warn.
            warn = False
            # Check condition and run block if true.
            if rec_min is not None and rec_max is not None and (val < rec_min or val > rec_max):
                # Set warn.
                warn = True
            # Check condition and run block if true.
            if data_min is not None and data_max is not None and (val < data_min or val > data_max):
                # Set warn.
                warn = True
            # Check condition and run block if true.
            if warn:
                # Set has_warning.
                has_warning = True

            # Set values[key].
            values[key] = val

        # Check condition and run block if true.
        if has_error:
            # Set self.show_banner('Please correct the highlighted fields.', level.
            self.show_banner('Please correct the highlighted fields.', level='error')
            # Return the computed value.
            return {}, False

        # Check condition and run block if true.
        if has_warning:
            # Set self.show_banner('Some values are outside typical training ranges.', level.
            self.show_banner('Some values are outside typical training ranges.', level='warning')
        # Fallback branch when conditions do not match.
        else:
            # Call self.show_banner.
            self.show_banner('')

        # Return the computed value.
        return values, True

    # Define function on_recent_select.
    def on_recent_select(self, _event=None):
        # Set selection.
        selection = self.recent_var.get().strip()
        # Check condition and run block if true.
        if selection:
            # Set query.
            query = self.location_choices.get(selection, selection)
            # Call self.location_var.set.
            self.location_var.set(query)
            # Check condition and run block if true.
            if self.use_live.get():
                # Call self.on_fetch_weather.
                self.on_fetch_weather()

    # Define function on_location_select.
    def on_location_select(self, _event=None):
        # Set selection.
        selection = self.location_var.get().strip()
        # Check condition and run block if true.
        if selection and self.use_live.get():
            # Call self.on_fetch_weather.
            self.on_fetch_weather()

    # Define function on_location_type.
    def on_location_type(self, _event=None):
        # Check condition and run block if true.
        if not ENABLE_LOCATION_AUTOCOMPLETE:
            # Return the computed value.
            return
        # Check condition and run block if true.
        if not self.use_live.get():
            # Return the computed value.
            return
        # Set query.
        query = self.location_var.get().strip()
        # Check condition and run block if true.
        if len(query) < 3:
            # Call self.clear_suggestions.
            self.clear_suggestions()
            # Return the computed value.
            return
        # Check condition and run block if true.
        if self.search_job is not None:
            # Start a protected block for error handling.
            try:
                # Call self.after_cancel.
                self.after_cancel(self.search_job)
            # Handle an error case.
            except Exception:
                # Do nothing (placeholder).
                pass
        # Set self.search_job.
        self.search_job = self.after(450, lambda q=query: self.auto_search_locations(q))

    # Define function auto_search_locations.
    def auto_search_locations(self, query: str):
        # Set self.search_token +.
        self.search_token += 1
        # Set token.
        token = self.search_token

        # Define function worker.
        def worker():
            # Start a protected block for error handling.
            try:
                # Set results.
                results = search_locations(query, limit=6)
                # Call self.app.after.
                self.app.after(0, lambda: self.apply_auto_search_results(results, token))
            # Handle an error case.
            except Exception:
                # Call self.app.after.
                self.app.after(0, self.clear_suggestions)

        # Set threading.Thread(target.
        threading.Thread(target=worker, daemon=True).start()

    # Define function apply_auto_search_results.
    def apply_auto_search_results(self, results: list[str], token: int):
        # Check condition and run block if true.
        if token != self.search_token:
            # Return the computed value.
            return
        # Call self.update_suggestions.
        self.update_suggestions(results)

    # Define function update_suggestions.
    def update_suggestions(self, results: list[str]):
        # Check condition and run block if true.
        if not ENABLE_LOCATION_AUTOCOMPLETE:
            # Return the computed value.
            return
        # Set self.location_choices.
        self.location_choices = {}
        # Check condition and run block if true.
        if not results:
            # Call self.clear_suggestions.
            self.clear_suggestions()
            # Return the computed value.
            return
        # Loop over items in a sequence.
        for display in results:
            # Set parts.
            parts = [p.strip() for p in display.split(',')]
            # Check condition and run block if true.
            if len(parts) >= 2:
                # Set query.
                query = f"{parts[0]},{parts[-1]}"
            # Fallback branch when conditions do not match.
            else:
                # Set query.
                query = display
            # Set self.location_choices[display].
            self.location_choices[display] = query
        # Set self.location_combo['values'].
        self.location_combo['values'] = results
        # Start a protected block for error handling.
        try:
            # Call self.location_combo.event_generate.
            self.location_combo.event_generate('<Down>')
        # Handle an error case.
        except Exception:
            # Do nothing (placeholder).
            pass

    # Define function clear_suggestions.
    def clear_suggestions(self):
        # Check condition and run block if true.
        if not ENABLE_LOCATION_AUTOCOMPLETE:
            # Return the computed value.
            return
        # Set self.location_combo['values'].
        self.location_combo['values'] = []

    # Define function set_current_location.
    def set_current_location(self, display: str, query: str | None = None, update_recent: bool = True):
        # Set display.
        display = (display or '').strip()
        # Check condition and run block if true.
        if not display:
            # Return the computed value.
            return
        # Check condition and run block if true.
        if not query:
            # Set query.
            query = display
        # Set self.location_choices[display].
        self.location_choices[display] = query
        # Set current_values.
        current_values = list(self.location_combo['values']) if self.location_combo['values'] else []
        # Check condition and run block if true.
        if display not in current_values:
            # Set self.location_combo['values'].
            self.location_combo['values'] = [display] + current_values
        # Call self.location_var.set.
        self.location_var.set(display)

        # Check condition and run block if true.
        if update_recent:
            # Check condition and run block if true.
            if display not in self.recent_locations:
                # Call self.recent_locations.insert.
                self.recent_locations.insert(0, display)
                # Set self.recent_locations.
                self.recent_locations = self.recent_locations[:6]
                # Set self.recent_combo['values'].
                self.recent_combo['values'] = self.recent_locations

        # Call self.app.update_location.
        self.app.update_location(query, display)

    # Define function auto_detect_fetch.
    def auto_detect_fetch(self):
        # Check condition and run block if true.
        if self.auto_fetch_done or not self.use_live.get():
            # Return the computed value.
            return
        # Check condition and run block if true.
        if self.location_var.get().strip():
            # Return the computed value.
            return
        # Set self.auto_fetch_done.
        self.auto_fetch_done = True
        # Set self.on_detect_location(auto_fetch.
        self.on_detect_location(auto_fetch=True)

    # Define function on_fetch_weather.
    def on_fetch_weather(self):
        # Set city_display.
        city_display = self.location_var.get().strip()
        # Set city.
        city = self.location_choices.get(city_display, city_display)
        # Check condition and run block if true.
        if not city:
            # Set self.show_banner('Please enter a city or region to fetch weather.', level.
            self.show_banner('Please enter a city or region to fetch weather.', level='error')
            # Return the computed value.
            return

        # Set self.show_banner('Fetching weather data...', level.
        self.show_banner('Fetching weather data...', level='warning')

        # Define function worker.
        def worker():
            # Start a protected block for error handling.
            try:
                # Set weather.
                weather = fetch_weather(city)
                # Call self.app.after.
                self.app.after(0, lambda: self.apply_weather(weather, city))
            # Handle an error case.
            except Exception as e:
                # Set err.
                err = str(e)
                # Set self.app.after(0, lambda err.
                self.app.after(0, lambda err=err: self.enable_manual_weather(err))

        # Set threading.Thread(target.
        threading.Thread(target=worker, daemon=True).start()

    # Define function on_search_location.
    def on_search_location(self):
        # Set query.
        query = self.location_var.get().strip()
        # Check condition and run block if true.
        if not query:
            # Set self.show_banner('Enter a city name to search.', level.
            self.show_banner('Enter a city name to search.', level='error')
            # Return the computed value.
            return

        # Set self.show_banner('Searching locations...', level.
        self.show_banner('Searching locations...', level='warning')

        # Define function worker.
        def worker():
            # Start a protected block for error handling.
            try:
                # Set results.
                results = search_locations(query, limit=6)
                # Call self.app.after.
                self.app.after(0, lambda: self.apply_search_results(results))
            # Handle an error case.
            except Exception as e:
                # Set err.
                err = str(e)
                # Set self.app.after(0, lambda err.
                self.app.after(0, lambda err=err: self.show_banner(err, level='error'))

        # Set threading.Thread(target.
        threading.Thread(target=worker, daemon=True).start()

    # Define function apply_search_results.
    def apply_search_results(self, results: list[str]):
        # Check condition and run block if true.
        if not results:
            # Set self.show_banner('No locations found.', level.
            self.show_banner('No locations found.', level='warning')
            # Return the computed value.
            return

        # Call self.update_suggestions.
        self.update_suggestions(results)
        # Set self.location_combo['values'].
        self.location_combo['values'] = results
        # Call self.location_var.set.
        self.location_var.set(results[0])
        # Call self.show_banner.
        self.show_banner('')

    # Define function on_detect_location.
    def on_detect_location(self, auto_fetch=False):
        # Set self.show_banner('Detecting location...', level.
        self.show_banner('Detecting location...', level='warning')

        # Define function worker.
        def worker():
            # Start a protected block for error handling.
            try:
                # Set location.
                location = detect_location()
                # Call self.app.after.
                self.app.after(0, lambda: self.apply_location(location, auto_fetch))
            # Handle an error case.
            except Exception as e:
                # Set err.
                err = str(e)
                # Set self.app.after(0, lambda err.
                self.app.after(0, lambda err=err: self.show_banner(f'{err} You can type a city and click Fetch Live.', level='error'))

        # Set threading.Thread(target.
        threading.Thread(target=worker, daemon=True).start()

    # Define function apply_location.
    def apply_location(self, location: str, auto_fetch=False):
        # Set self.set_current_location(location, location, update_recent.
        self.set_current_location(location, location, update_recent=True)
        # Check condition and run block if true.
        if auto_fetch:
            # Call self.on_fetch_weather.
            self.on_fetch_weather()
        # Fallback branch when conditions do not match.
        else:
            # Call self.show_banner.
            self.show_banner('')

    # Define function apply_weather.
    def apply_weather(self, weather: dict, city: str):
        # Call self.show_banner.
        self.show_banner('')
        # Loop over items in a sequence.
        for key in ['temperature', 'humidity', 'rainfall']:
            # Call set_entry_value.
            set_entry_value(self.fields[key], f"{weather[key]:.2f}")
        # Call self.toggle_live.
        self.toggle_live()

        # Set location_name.
        location_name = weather.get('resolved_name') or city
        # Check condition and run block if true.
        if weather.get('country'):
            # Set location_name.
            location_name = f"{location_name}, {weather.get('country')}"

        # Set info.
        info = (
            # Execute this statement.
            f"Location: {location_name}\n"
            # Execute this statement.
            f"Feels like: {weather.get('feels_like', 0.0):.1f} C\n"
            # Execute this statement.
            f"Wind: {weather.get('wind_speed', 0.0):.1f} m/s | Pressure: {weather.get('pressure', 0.0):.0f} hPa\n"
            # Execute this statement.
            f"Clouds: {weather.get('clouds', 0.0):.0f}% | Rain: {weather.get('rainfall', 0.0):.2f} mm"
        # Close the previous block or structure.
        )
        # Set source.
        source = weather.get('rain_source', 'none')
        # Check condition and run block if true.
        if source == 'forecast':
            # Set info +.
            info += ' (short-term forecast)'
        # Check an alternative condition.
        elif source == 'current':
            # Set info +.
            info += ' (current)'
        # Set self.weather_detail.config(text.
        self.weather_detail.config(text=info)

        # Set self.set_current_location(location_name, city, update_recent.
        self.set_current_location(location_name, city, update_recent=True)

    # Define function on_submit.
    def on_submit(self):
        # Set values, valid.
        values, valid = self.validate_inputs()
        # Check condition and run block if true.
        if not valid:
            # Return the computed value.
            return

        # Set model.
        model = self.state.active_model()
        # Set X.
        X = [[values[f] for f in FEATURES]]
        # Set proba.
        proba = model.predict_proba(X)[0]
        # Set classes.
        classes = model.classes_

        # Set top_idx.
        top_idx = list(reversed(proba.argsort()))
        # Set top1.
        top1 = classes[top_idx[0]]
        # Set conf.
        conf = float(proba[top_idx[0]])
        # Set alternatives.
        alternatives = [(classes[i], float(proba[i])) for i in top_idx[1:4]]

        # Set explanations.
        explanations = explain_features(top1, values, self.state.stats)
        # Set tip.
        tip = crop_tip(top1)
        # Set sensitivity.
        sensitivity = compute_sensitivity(model, values, top1, self.state.validation_ranges)

        # Set result.
        result = {
            # Execute this statement.
            'timestamp': datetime.now(),
            # Execute this statement.
            'model': self.state.active_model_name,
            # Execute this statement.
            'inputs': values,
            # Execute this statement.
            'top1': top1,
            # Execute this statement.
            'confidence': conf,
            # Execute this statement.
            'alternatives': alternatives,
            # Execute this statement.
            'explanations': explanations,
            # Execute this statement.
            'tip': tip,
            # Execute this statement.
            'sensitivity': sensitivity
        # Close the previous block or structure.
        }

        # Call self.state.history.append.
        self.state.history.append(result)
        # Call append_history.
        append_history(result)
        # Call self.app.refresh_history.
        self.app.refresh_history()
        # Update results screen data but keep user on this page.
        # Execute this statement.
        self.app.frames['ResultsFrame'].update_results(result)

        # Set self.preview_crop.config(text.
        self.preview_crop.config(text=f'Recommended Crop: {top1.title()}')
        # Set self.preview_conf.config(text.
        self.preview_conf.config(text=f'Confidence: {conf * 100:.1f}%')
        # Check condition and run block if true.
        if alternatives:
            # Set alt_text.
            alt_text = ', '.join([f'{name.title()} ({score * 100:.1f}%)' for name, score in alternatives])
            # Set self.preview_alt.config(text.
            self.preview_alt.config(text=f'Alternatives: {alt_text}')
        # Fallback branch when conditions do not match.
        else:
            # Set self.preview_alt.config(text.
            self.preview_alt.config(text='Alternatives: -')
        # Set self.preview_note.config(text.
        self.preview_note.config(text=format_confidence_note(conf, alternatives))


# Define class ResultsFrame.
class ResultsFrame(ttk.Frame):
    # Define function __init__.
    def __init__(self, parent, app: CropApp, state):
        # Call super.
        super().__init__(parent)
        # Set self.app.
        self.app = app
        # Set self.state.
        self.state = state

        # Set header.
        header = tk.Frame(self, bg=COLORS['bg'])
        # Set header.pack(padx.
        header.pack(padx=24, pady=(20, 10), fill='x')
        # Set tk.Label(header, text.
        tk.Label(header, text='Recommendation Results', bg=COLORS['bg'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        # Set tk.Label(header, text.
        tk.Label(header, text='Based on your soil and local climate data.', bg=COLORS['bg'],
                 # Set fg.
                 fg=COLORS['muted']).pack(anchor='w')

        # Set self.main.
        self.main = tk.Frame(self, bg=COLORS['bg'])
        # Set self.main.pack(padx.
        self.main.pack(padx=24, pady=8, fill='both', expand=True)

        # Set left_shadow, left.
        left_shadow, left = make_card(self.main, padding=16)
        # Set left_shadow.pack(side.
        left_shadow.pack(side='left', fill='both', expand=True)

        # Set right_shadow, right.
        right_shadow, right = make_card(self.main, padding=16)
        # Set right_shadow.pack(side.
        right_shadow.pack(side='left', padx=(12, 0), fill='both', expand=True)

        # Set self.model_label.
        self.model_label = tk.Label(left, text='Model: -', bg=COLORS['card'], fg=COLORS['muted'])
        # Set self.model_label.pack(anchor.
        self.model_label.pack(anchor='w')

        # Set self.crop_label.
        self.crop_label = tk.Label(left, text='-', bg=COLORS['card'], fg=COLORS['text'],
                                   # Set font.
                                   font=('Segoe UI', 16, 'bold'))
        # Set self.crop_label.pack(anchor.
        self.crop_label.pack(anchor='w')

        # Set self.conf_label.
        self.conf_label = tk.Label(left, text='Confidence: -', bg=COLORS['card'], fg=COLORS['muted'])
        # Set self.conf_label.pack(anchor.
        self.conf_label.pack(anchor='w', pady=(6, 6))

        # Set self.progress.
        self.progress = ttk.Progressbar(left, style='Green.Horizontal.TProgressbar', length=280, maximum=100)
        # Set self.progress.pack(anchor.
        self.progress.pack(anchor='w', pady=(0, 12))

        # Set self.conf_note.
        self.conf_note = tk.Label(left, text='', bg=COLORS['card'], fg=COLORS['muted'],
                                  # Set wraplength.
                                  wraplength=280, justify='left')
        # Set self.conf_note.pack(anchor.
        self.conf_note.pack(anchor='w', pady=(0, 10))

        # Set tk.Label(left, text.
        tk.Label(left, text='Alternatives', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        # Set self.alt_container.
        self.alt_container = tk.Frame(left, bg=COLORS['card'])
        # Set self.alt_container.pack(anchor.
        self.alt_container.pack(anchor='w', pady=(6, 0), fill='x')

        # Set tk.Label(right, text.
        tk.Label(right, text='Why this crop?', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        # Set self.explain_container.
        self.explain_container = tk.Frame(right, bg=COLORS['card'])
        # Set self.explain_container.pack(anchor.
        self.explain_container.pack(anchor='w', pady=(6, 10), fill='x')

        # Set tk.Label(right, text.
        tk.Label(right, text='Sensitivity Analysis', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        # Set self.sensitivity_container.
        self.sensitivity_container = tk.Frame(right, bg=COLORS['card'])
        # Set self.sensitivity_container.pack(anchor.
        self.sensitivity_container.pack(anchor='w', pady=(6, 10), fill='x')

        # Set tk.Label(right, text.
        tk.Label(right, text='Quick Tip', bg=COLORS['card'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        # Set self.tip_label.
        self.tip_label = tk.Label(right, text='-', bg=COLORS['card'], fg=COLORS['muted'],
                                  # Set wraplength.
                                  wraplength=320, justify='left')
        # Set self.tip_label.pack(anchor.
        self.tip_label.pack(anchor='w', pady=(6, 0))

        # Set actions.
        actions = tk.Frame(self, bg=COLORS['bg'])
        # Set actions.pack(padx.
        actions.pack(padx=24, pady=16, fill='x')

        # Set tk.Button(actions, text.
        tk.Button(actions, text='Back to Dashboard', command=lambda: self.app.show_frame('DashboardFrame'),
                  # Set bg.
                  bg=COLORS['primary'], fg='white', bd=0, padx=16, pady=10).pack(side='right')

    # Define function update_results.
    def update_results(self, result: dict):
        # Set crop.
        crop = result.get('top1', '-')
        # Set confidence.
        confidence = result.get('confidence', 0.0)
        # Set model_name.
        model_name = result.get('model', '-')
        # Set self.model_label.config(text.
        self.model_label.config(text=f'Model: {model_name}')
        # Set self.crop_label.config(text.
        self.crop_label.config(text=crop.title())
        # Set self.conf_label.config(text.
        self.conf_label.config(text=f'Confidence: {confidence * 100:.1f}%')
        # Set self.progress['value'].
        self.progress['value'] = confidence * 100
        # Set self.conf_note.config(text.
        self.conf_note.config(text=format_confidence_note(confidence, result.get('alternatives', [])))

        # Loop over items in a sequence.
        for child in self.alt_container.winfo_children():
            # Call child.destroy.
            child.destroy()
        # Loop over items in a sequence.
        for name, score in result.get('alternatives', []):
            # Set row.
            row = tk.Frame(self.alt_container, bg=COLORS['card'])
            # Set row.pack(anchor.
            row.pack(anchor='w', fill='x')
            # Set tk.Label(row, text.
            tk.Label(row, text=name.title(), bg=COLORS['card'], fg=COLORS['text']).pack(side='left')
            # Set tk.Label(row, text.
            tk.Label(row, text=f'{score * 100:.1f}%', bg=COLORS['card'], fg=COLORS['muted']).pack(side='right')

        # Loop over items in a sequence.
        for child in self.explain_container.winfo_children():
            # Call child.destroy.
            child.destroy()
        # Loop over items in a sequence.
        for text in result.get('explanations', []):
            # Set tk.Label(self.explain_container, text.
            tk.Label(self.explain_container, text='- ' + text, bg=COLORS['card'], fg=COLORS['muted'],
                     # Set wraplength.
                     wraplength=320, justify='left').pack(anchor='w')

        # Loop over items in a sequence.
        for child in self.sensitivity_container.winfo_children():
            # Call child.destroy.
            child.destroy()
        # Loop over items in a sequence.
        for item in result.get('sensitivity', [])[:4]:
            # Set label.
            label = FEATURE_LABELS.get(item['feature'], item['feature'])
            # Set up.
            up = item['delta_up'] * 100
            # Set down.
            down = item['delta_down'] * 100
            # Set text.
            text = f"{label}: +{up:.1f}% / {down:.1f}%"
            # Set tk.Label(self.sensitivity_container, text.
            tk.Label(self.sensitivity_container, text='- ' + text, bg=COLORS['card'], fg=COLORS['muted'],
                     # Set wraplength.
                     wraplength=320, justify='left').pack(anchor='w')

        # Set self.tip_label.config(text.
        self.tip_label.config(text=result.get('tip', '-'))


# Define class HistoryFrame.
class HistoryFrame(ttk.Frame):
    # Define function __init__.
    def __init__(self, parent, app: CropApp, state):
        # Call super.
        super().__init__(parent)
        # Set self.app.
        self.app = app
        # Set self.state.
        self.state = state

        # Set header.
        header = tk.Frame(self, bg=COLORS['bg'])
        # Set header.pack(padx.
        header.pack(padx=24, pady=(20, 10), fill='x')
        # Set tk.Label(header, text.
        tk.Label(header, text='Prediction History', bg=COLORS['bg'], fg=COLORS['text'],
                 # Set font.
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        # Set tk.Label(header, text.
        tk.Label(header, text='Recent recommendations and confidence scores.', bg=COLORS['bg'],
                 # Set fg.
                 fg=COLORS['muted']).pack(anchor='w')

        # Set self.summary.
        self.summary = tk.Label(header, text='', bg=COLORS['bg'], fg=COLORS['muted'])
        # Set self.summary.pack(anchor.
        self.summary.pack(anchor='w', pady=(6, 0))

        # Set self.table.
        self.table = ttk.Treeview(self, columns=('time', 'model', 'crop', 'confidence'), show='headings', height=12)
        # Set self.table.heading('time', text.
        self.table.heading('time', text='Time')
        # Set self.table.heading('model', text.
        self.table.heading('model', text='Model')
        # Set self.table.heading('crop', text.
        self.table.heading('crop', text='Crop')
        # Set self.table.heading('confidence', text.
        self.table.heading('confidence', text='Confidence')
        # Set self.table.column('time', width.
        self.table.column('time', width=200)
        # Set self.table.column('model', width.
        self.table.column('model', width=160)
        # Set self.table.column('crop', width.
        self.table.column('crop', width=160)
        # Set self.table.column('confidence', width.
        self.table.column('confidence', width=120)
        # Set self.table.pack(padx.
        self.table.pack(padx=24, pady=12, fill='x')

        # Call self.refresh.
        self.refresh()

    # Define function refresh.
    def refresh(self):
        # Loop over items in a sequence.
        for row in self.table.get_children():
            # Call self.table.delete.
            self.table.delete(row)

        # Set history.
        history = self.state.history[-50:]
        # Loop over items in a sequence.
        for item in reversed(history):
            # Set ts.
            ts = item['timestamp'].strftime('%Y-%m-%d %H:%M')
            # Set crop.
            crop = item.get('top1', '-').title()
            # Set conf.
            conf = f"{item.get('confidence', 0.0) * 100:.1f}%"
            # Set model.
            model = item.get('model', '-')
            # Set self.table.insert('', 'end', values.
            self.table.insert('', 'end', values=(ts, model, crop, conf))

        # Check condition and run block if true.
        if history:
            # Set avg_conf.
            avg_conf = sum(i.get('confidence', 0.0) for i in history) / len(history)
            # Set crop_counts.
            crop_counts = {}
            # Loop over items in a sequence.
            for item in history:
                # Set crop.
                crop = item.get('top1', '-')
                # Set crop_counts[crop].
                crop_counts[crop] = crop_counts.get(crop, 0) + 1
            # Set top_crop.
            top_crop = max(crop_counts, key=crop_counts.get)
            # Set summary.
            summary = f'Total predictions: {len(history)} | Top crop: {top_crop.title()} | Avg confidence: {avg_conf * 100:.1f}%'
        # Fallback branch when conditions do not match.
        else:
            # Set summary.
            summary = 'No predictions yet.'
        # Set self.summary.config(text.
        self.summary.config(text=summary)
