Keyboard_main.py
Description
This script implements an adjustable virtual keyboard designed for hands-free usage, incorporating cursor tracking and Text-to-Speech (TTS) functionality. The keyboard layout is customizable, with adjustable button sizes, fonts, and dimensions. It tracks the user's cursor coordinates and integrates real-time updates for interaction.

Features
Virtual Keyboard: Fully functional keyboard built with tkinter, supporting basic input actions like "Clear," "Enter," and "Speak."
Adjustable Design: Includes sliders to customize button width, height, and font size dynamically.
Mouse Tracking: Captures and displays cursor coordinates relative to the window in real-time.
Text-to-Speech Integration: Converts entered text into speech using pyttsx3, with adjustable speech rate, volume, and voice.
Threading for TTS: Ensures the GUI remains responsive while TTS processes text in the background.
How to Use:
Run the script using Python 3.
Adjust button sizes and font via the provided sliders.
Type into the text field using the virtual keyboard.
Use the "Speak" button to vocalize the entered text.
Key Functions:
create_keyboard: Generates the virtual keyboard layout.
speak_text: Converts the text input to speech.
capture_mouse_coordinates: Tracks and updates the cursor position every 10ms.
create_size_controls: Provides sliders for customizing the keyboard dimensions.
Game_class.py
Description
This script contains a simple interactive game called Click to Kill. The game involves clicking on moving targets to score points. It is implemented using the pygame library.

Features
Dynamic Target Movement: Targets move in random directions and bounce off walls.
Interactive Gameplay: Players click on targets to "kill" them and earn points.
Score Display: Continuously updates and displays the player's score during gameplay.
Adjustable Difficulty: Target speed and movement patterns can be modified.
How to Play:
Run the script using Python 3 with pygame installed.
Use the mouse to click on the moving targets.
Earn points for each successful hit.
The game ends when the user exits the window.
Key Functions:
spawn_target: Spawns a new target at a random location.
move_targets: Updates target positions and handles wall collisions.
check_click: Detects whether a click hits a target and removes it if so.
run: Manages the game loop and handles rendering, input, and updates.
Tune_function.py
Description
This script provides an implementation of the MouseInputEstimator, which applies an Exponential Moving Average (EMA) filter to mouse input data. It is designed for smoothing cursor movement and reducing noise, especially in applications involving gaze tracking or dynamic input.

Features
Exponential Moving Average (EMA): Smooths mouse inputs to reduce jitter and improve tracking precision.
Error Analysis: Computes the error between raw inputs and filtered outputs to evaluate performance.
Adjustable Parameters: Includes configurable n (buffer size) and alpha (smoothing factor).
How to Use:
Initialize MouseInputEstimator with the desired buffer size (n) and smoothing factor (alpha).
Add mouse or estimation inputs using add_mouse_input and add_estimation_input.
Retrieve the current EMA-filtered values using get_current_ema.
Key Functions:
add_mouse_input: Adds raw mouse input coordinates to the buffer.
add_estimation_input: Computes the EMA for new estimation inputs.
get_current_ema: Returns the latest EMA-filtered coordinates.
get_error: Calculates errors between raw inputs and filtered outputs.