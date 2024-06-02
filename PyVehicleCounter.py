import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta


class Counter:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Counter App")
        self.root.geometry("500x400")

        # Variables
        self.selected_datetime = tk.StringVar()
        self.clock_text = tk.StringVar()
        self.clock_running = False
        self.key_press_label = tk.StringVar()
        self.key_press_label.set("Press a key after starting the clock")
        self.key_presses = {}  # Dictionary to store key presses and times

        # GUI components
        self.create_widgets()

        # Binding Key Press Event
        root.bind("<Key>", self.key_pressed)

    def create_widgets(self):
        # Date and Time Picker
        tk.Label(self.root, text="Select Date and Time:").pack(pady=10)

        self.date_entry = DateEntry(
            self.root,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            year=2024,
        )
        self.date_entry.pack(pady=10)

        self.time_entry = tk.Entry(
            self.root, textvariable=self.selected_datetime, font=("Helvetica", 12)
        )
        self.time_entry.pack(pady=10)

        # Start/Stop Button
        self.start_stop_button = tk.Button(
            self.root, text="Start", command=self.toggle_clock
        )
        self.start_stop_button.pack(pady=10)

        # Clock Label
        clock_label = tk.Label(
            self.root, textvariable=self.clock_text, font=("Helvetica", 14)
        )
        clock_label.pack(pady=20)

        # Key Press Label
        key_press_label = tk.Label(
            self.root, textvariable=self.key_press_label, font=("Helvetica", 12)
        )
        key_press_label.pack(pady=20)

    def toggle_clock(self):
        if self.clock_running:
            self.stop_clock()
        else:
            self.start_clock()

    def start_clock(self):
        try:
            selected_date = self.date_entry.get_date()
            selected_time = datetime.strptime(self.time_entry.get(), "%H:%M:%S").time()
            self.selected_datetime.set(selected_time.strftime("%H:%M:%S"))
            selected_datetime = datetime.combine(selected_date, selected_time)
        except ValueError:
            self.clock_text.set("Invalid date and time format")
            return

        self.clock_running = True
        self.date_entry.config(state="disabled")
        self.time_entry.config(state="disabled")
        self.start_stop_button.config(text="Stop")
        self.update_clock(selected_datetime)

    def stop_clock(self):
        self.clock_running = False
        self.date_entry.config(state="normal")
        self.time_entry.config(state="normal")
        self.start_stop_button.config(text="Start")
        self.print_summary()

    def update_clock(self, current_datetime):
        if not self.clock_running:
            return

        # Update clock label every second
        current_datetime += timedelta(seconds=1)
        self.clock_text.set(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, lambda: self.update_clock(current_datetime))

    def key_pressed(self, event):
        if self.clock_running:
            key_press_time = self.clock_text.get()
            key_char = event.char
            self.key_presses[key_press_time] = key_char

            self.key_press_label.set(f"Key Pressed: {key_char} at {key_press_time}")

    def print_summary(self):
        print("Key Press Summary:")
        for time, key in self.key_presses.items():
            print(f"{time}: {key}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Counter(root)
    root.mainloop()
