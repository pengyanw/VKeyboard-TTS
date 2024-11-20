import tkinter as tk


def create_size_controls(root, button_width, button_height, update_button_sizes):
    """Creates sliders for adjusting button width and height."""
    control_frame = tk.Frame(root)
    control_frame.grid(row=5, column=0, columnspan=12, sticky="ew", pady=10)

    # Button width slider
    tk.Label(control_frame, text="Button Width:").pack(side=tk.LEFT, padx=5)
    width_slider = tk.Scale(control_frame, from_=2, to=10, orient="horizontal", variable=button_width,
                            command=lambda x: update_button_sizes())
    width_slider.pack(side=tk.LEFT, padx=5)

    # Button height slider
    tk.Label(control_frame, text="Button Height:").pack(side=tk.LEFT, padx=5)
    height_slider = tk.Scale(control_frame, from_=1, to=5, orient="horizontal", variable=button_height,
                             command=lambda x: update_button_sizes())
    height_slider.pack(side=tk.LEFT, padx=5)


def get_cursor_coordinates(self):
    """Get and display the current cursor coordinates relative to the application window."""
    x = self.root.winfo_pointerx() - self.root.winfo_rootx()
    y = self.root.winfo_pointery() - self.root.winfo_rooty()
    self.coordinates_label.config(text=f"Cursor coordinates: x={x}, y={y}")
    # Schedule the function to run again after a short delay for continuous updating
    self.root.after(100, self.get_cursor_coordinates)
