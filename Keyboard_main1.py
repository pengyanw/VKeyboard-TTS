import tkinter as tk
import pyttsx3
import time
import numpy as np
import threading
import os
import matplotlib.pyplot as plt
from collections import deque
from Tune_function import MouseInputEstimator  # Import the EMA filter class

class AdjustableKeyboard:
    def __init__(self):
        # Initialize the main application window
        self.flag = 0
        self.ini = time.time()
        self.root = tk.Tk()
        self.root.title("Adjustable Virtual Keyboard with Cursor Coordinates")
        self.root.geometry("1600x800")
        self.root.minsize(1000, 600)
        # Initialize TTS engine
        self.speak_init()

        # Initialize button size variables
        self.button_width = tk.IntVar(value=3)
        self.button_height = tk.IntVar(value=1)
        self.button_font_size = tk.IntVar(value=30)

        # Buffer to store the submitted text
        self.buffer = ""

        # List to store keyboard buttons
        self.buttons = []

        # Create the text entry box and keyboard UI
        self.create_text_entry()
        self.create_keyboard()
        self.create_size_controls()

        # Create a label for displaying coordinates
        self.coordinates_label = tk.Label(self.root, text="Cursor coordinates: x=0, y=0", font=("Timesnewroman", 10))
        self.coordinates_label.grid(row=6, column=0, columnspan=12, sticky="w", padx=10, pady=5)

        # Initialize the EMA filter
        self.ema_filter = MouseInputEstimator(n=20, alpha=0.5)  # Adjust 'n' and 'alpha' as needed

        # Other initializations
        self.mouse_coordinates = []  # Buffer to store raw mouse coordinates
        self.filtered_coordinates = []  # Buffer to store EMA-filtered coordinates

        # Start capturing mouse coordinates
        self.capture_mouse_coordinates()

        # Start updating the coordinates
        self.get_cursor_coordinates()

        # Start the main loop
        self.root.mainloop()

    def create_text_entry(self):
        """Create the text entry field."""
        self.text_entry = tk.Entry(self.root, font=("Arial", 20))
        self.text_entry.grid(row=0, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)

    def on_key_press(self, key):
        """Insert the pressed key character into the text entry."""
        self.text_entry.insert(tk.END, key)

    def delete_last(self):
        """Delete the last character from the text entry."""
        current_text = self.text_entry.get()
        if current_text:
            self.text_entry.delete(len(current_text) - 1)

    def clear_text(self):
        """Clear all text from the text entry."""
        self.text_entry.delete(0, tk.END)

    def update_button_sizes(self):
        """Update the width and height of all buttons based on slider values."""
        for row in self.buttons:
            if row == 1:
                for button in row:
                    button.config(width=self.button_width.get() * 20, height=self.button_height.get())

    def update_button_font_size(self):
        """Update the font size of all buttons based on slider value."""
        new_font_size = self.button_font_size.get()
        for row in self.buttons:
            for button in row:
                button.config(font=("Arial", new_font_size))

    def submit_and_clear_input(self):
        """Stores the current input in the buffer, prints it, and clears the entry field."""
        self.buffer = self.text_entry.get()  # Store the current text in buffer
        print(self.buffer)  # Print the stored text to the console
        self.clear_text()  # Clear the text entry field

    def create_keyboard(self):
        """Create the keyboard layout with wider first row buttons using columnspan."""
        keyboard_layout = [
            ['←', 'Clear', 'Enter', 'Speak'],  # First row
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],  # Second row
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],  # Third row
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ' ']  # Fourth row
        ]

        for row_index, row in enumerate(keyboard_layout, start=1):
            self.root.grid_rowconfigure(row_index, weight=1)  # Configure row resizing

            button_row = []

            for col_index, key in enumerate(row):
                # Configure grid columns for uniform resizing
                self.root.grid_columnconfigure(col_index, weight=1)

                if row_index == 1:
                    # For the first row, make buttons span two columns for wider appearance
                    btn = tk.Button(self.root, text=key, command=self.get_button_command(key), height=2)
                    btn.grid(row=row_index, column=col_index * 2, columnspan=2, sticky="nsew", padx=2, pady=2)
                else:
                    # Default size and placement for other rows
                    btn = tk.Button(self.root, text=key, command=self.get_button_command(key), width=5, height=2)
                    btn.grid(row=row_index, column=col_index, sticky="nsew", padx=2, pady=2)
                button_row.append(btn)
            self.buttons.append(button_row)
        self.update_button_sizes()
        self.update_button_font_size()

    def get_button_command(self, key):
        """Return the appropriate command for a given key."""
        if key == "←":
            return self.delete_last
        elif key == "Clear":
            return self.clear_text
        elif key == "Enter":
            return self.submit_and_clear_input
        elif key == "Speak":
            return self.speak_text
        else:
            return lambda k=key: self.on_key_press(k)

    def create_keyboard1(self):
        """Create the keyboard layout and add buttons."""
        keyboard_layout = [
            ['←', 'Clear', 'Enter', 'Speak'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ' ']
        ]

        for row_index, row in enumerate(keyboard_layout, start=1):
            self.root.grid_rowconfigure(row_index, weight=1)
            button_row = []
            for col_index, key in enumerate(row):
                self.root.grid_columnconfigure(col_index, weight=1)

                if key == "←":
                    btn = tk.Button(self.root, text=key, command=self.delete_last,
                                    width=5, height=2)
                elif key == "Clear":
                    btn = tk.Button(self.root, text=key, command=self.clear_text,
                                    width=5, height=2)
                elif key == "Enter":
                    btn = tk.Button(self.root, text=key, command=self.submit_and_clear_input,
                                    width=self.button_width.get(), height=self.button_height.get())
                elif key == "Speak":
                    btn = tk.Button(self.root, text=key, command=self.speak_text,
                                    width=5, height=2)
                else:
                    btn = tk.Button(self.root, text=key,
                                    command=lambda k=key: self.on_key_press(k),
                                    width=5, height=2)

                btn.grid(row=row_index, column=col_index, sticky="nsew", padx=2, pady=2)
                button_row.append(btn)

            self.buttons.append(button_row)
            self.update_button_sizes()
            self.update_button_font_size()

    def create_size_controls(self):
        """Create sliders for adjusting button width, height, and font size."""
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=5, column=0, columnspan=12, sticky="ew", pady=20)

        # Button width slider
        tk.Label(control_frame, text="Button Width:").pack(side=tk.LEFT, padx=10)
        width_slider = tk.Scale(control_frame, from_=1, to=20, orient="horizontal",
                                variable=self.button_width,
                                command=lambda x: self.update_button_sizes())
        width_slider.pack(side=tk.LEFT, padx=10)

        # Button height slider
        tk.Label(control_frame, text="Button Height:").pack(side=tk.LEFT, padx=10)
        height_slider = tk.Scale(control_frame, from_=1, to=10, orient="horizontal",
                                 variable=self.button_height,
                                 command=lambda x: self.update_button_sizes())
        height_slider.pack(side=tk.LEFT, padx=10)

        # Button font size slider
        tk.Label(control_frame, text="Button Font Size:").pack(side=tk.LEFT, padx=10)
        font_size_slider = tk.Scale(control_frame, from_=25, to=38, orient="horizontal",
                                    variable=self.button_font_size,
                                    command=lambda x: self.update_button_font_size())
        font_size_slider.pack(side=tk.LEFT, padx=10)



    def speak_text(self):
        """Convert the current text input to speech in a separate thread."""
        text = self.text_entry.get()
        if text.strip():  # Check if text is not empty
            threading.Thread(target=self._tts_worker, args=(text,), daemon=True).start()

    def _tts_worker(self, text):
        """Worker function to handle TTS in a separate thread."""
        # Create the TTS engine if it doesn't exist
        if not hasattr(self, 'tts_engine') or self.tts_engine is None:
            self.tts_engine = pyttsx3.init()
    
        # Set file path to save the audio
        output_dir = "tts_audio"
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        file_name = f"{text[:10].replace(' ', '_')}_tts.wav"  # Use first 10 characters of text as file name
        file_path = os.path.join(output_dir, file_name)
    
        # Save audio to WAV file
        #self.tts_engine.save_to_file(text, file_path)
    
        # Speak the text
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
        print(f"Audio saved to: {file_path}")

    def create_settings_ui(self):
        """Create UI for adjusting TTS parameters dynamically."""
        settings_frame = tk.Frame(self.root)
        settings_frame.grid(row=1, column=0, columnspan=12, sticky="ew", pady=10)

        # Rate adjustment slider
        tk.Label(settings_frame, text="Rate:").pack(side=tk.LEFT, padx=5)
        rate_slider = tk.Scale(settings_frame, from_=50, to=300, orient="horizontal",
                               command=lambda x: self.update_rate(int(x)))
        rate_slider.set(self.default_rate)
        rate_slider.pack(side=tk.LEFT, padx=5)

        # Volume adjustment slider
        tk.Label(settings_frame, text="Volume:").pack(side=tk.LEFT, padx=5)
        volume_slider = tk.Scale(settings_frame, from_=0, to=1, resolution=0.1, orient="horizontal",
                                 command=lambda x: self.update_volume(float(x)))
        volume_slider.set(self.default_volume)
        volume_slider.pack(side=tk.LEFT, padx=5)

        # Voice selection dropdown
        tk.Label(settings_frame, text="Voice:").pack(side=tk.LEFT, padx=5)
        voice_var = tk.StringVar()
        voice_menu = tk.OptionMenu(settings_frame, voice_var, *[voice.name for voice in self.voices],
                                   command=self.update_voice)
        voice_var.set(self.voices[self.current_voice_index].name)
        voice_menu.pack(side=tk.LEFT, padx=5)

    def speak_init(self):
        """Initialize the TTS engine, set default parameters, and print properties."""
        self.tts_engine = pyttsx3.init()
        self.default_rate = 120  # Default speech rate
        self.default_volume = 0.8  # Default volume
        self.current_voice_index = 1  # Default voice index
        self.voices = self.tts_engine.getProperty("voices")

        # Adjust voice settings
        self.tts_engine.setProperty("voice", self.voices[self.current_voice_index].id)  # Example: male voice

        # Apply default settings
        self.tts_engine.setProperty("rate", self.default_rate)
        self.tts_engine.setProperty("volume", self.default_volume)

        # Print current engine properties for debugging
        print(f"Rate: {self.tts_engine.getProperty('rate')}")
        print(f"Volume: {self.tts_engine.getProperty('volume')}")
        print(f"Voice: {self.voices[self.current_voice_index].name} (ID: {self.voices[self.current_voice_index].id})")

    def get_cursor_coordinates(self):
        """Get and display the current cursor coordinates relative to the application window."""
        # Get raw cursor coordinates
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()

        # Add raw coordinates to the EMA filter
        self.ema_filter.add_mouse_input(x, y)
        self.ema_filter.add_estimation_input(x, y)  # Use raw coordinates for estimation (can be modified)

        # Retrieve the current EMA-filtered value
        filtered_x, filtered_y = self.ema_filter.get_current_ema()[-1]  # Get the latest filtered coordinates

        # Update coordinates label with both raw and filtered values
        self.coordinates_label.config(
            text=f"Raw: x={x}, y={y} | Filtered: x={int(filtered_x)}, y={int(filtered_y)}"
        )

        # Schedule the next update
        self.root.after(100, self.get_cursor_coordinates)

    def capture_mouse_coordinates(self):
        """Capture and store the recent 10 seconds of mouse coordinates and plot them."""
        # Get raw cursor coordinates
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()

        # Add raw coordinates to the buffer
        self.mouse_coordinates.append((time.time(), x, y))  # Store with a timestamp

        # Keep only coordinates from the last 10 seconds
        current_time = time.time()
        self.mouse_coordinates = [
            coord for coord in self.mouse_coordinates if current_time - coord[0] <= 10
        ]

        # Add raw coordinates to EMA filter and retrieve filtered value
        self.ema_filter.add_mouse_input(x, y)
        self.ema_filter.add_estimation_input(x, y)
        filtered_x, filtered_y = self.ema_filter.get_current_ema()[-1]

        # Add filtered coordinates to the filtered buffer
        self.filtered_coordinates.append((time.time()+10, filtered_x, filtered_y))

        if current_time - self.ini >= 10 and (self.flag == 0):
            self.filtered_coordinates = [
            coord for coord in self.filtered_coordinates
            ]
            # Plot raw and filtered coordinates
            self.plot_coordinates()
            self.flag += 1


        # Schedule the next update after 10ms
        self.root.after(10, self.capture_mouse_coordinates)

    def plot_coordinates(self):
        """Plot raw and filtered mouse coordinates."""
        if not self.mouse_coordinates or not self.filtered_coordinates:
            return

        # Extract timestamps and coordinates
        raw_timestamps, raw_x, raw_y = zip(*self.mouse_coordinates)
        filtered_timestamps, filtered_x, filtered_y = zip(*self.filtered_coordinates)

        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(raw_timestamps, raw_x, label="Raw X", color="red")
        plt.plot(filtered_timestamps, filtered_x, label="Filtered X", color="blue")
        plt.xlabel("Time (s)")
        plt.ylabel("X Coordinate")
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(raw_timestamps, raw_y, label="Raw Y", color="orange")
        plt.plot(filtered_timestamps, filtered_y, label="Filtered Y", color="green")
        plt.xlabel("Time (s)")
        plt.ylabel("Y Coordinate")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()


# Run the AdjustableKeyboard
if __name__ == "__main__":
    x1 = AdjustableKeyboard()
