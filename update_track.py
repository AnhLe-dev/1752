import tkinter as tk
import tkinter.scrolledtext as tkst

import track_library as lib          # Custom module handling track data (library)
import font_manager as fonts         # Module to configure application fonts

# Utility function to update the content of a text widget
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)  # Clear existing content
    text_area.insert(1.0, content)   # Insert new content at the top

# Class representing the Update Track interface
class UpdateTrack():
    def __init__(self, window):
        self.window = window
        window.title("Update_Track")         # Set the window title
        window.geometry("650x500")           # Set the window size

        # Label prompting user to enter a track number
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        # Entry field for inputting track number
        self.input_txt = tk.Entry(window, width=5)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        # Button to trigger the track rating update
        check_track_btn = tk.Button(window, text="Update Track Rating", command=self.update_track_click)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)

        # Entry field for inputting the new rating
        self.input_rating_txt = tk.Entry(window, width=5)
        self.input_rating_txt.grid(row=0, column=4, padx=10, pady=10)

        # Scrollable text area to display track details or messages
        self.list_txt = tkst.ScrolledText(window, width=50, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Label to show status or feedback messages
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

    # Callback function when the "Update Track Rating" button is clicked
    def update_track_click(self):
        key = self.input_txt.get()                    # Get the entered track number
        new_rating = int(self.input_rating_txt.get()) # Get the new rating
        name = lib.get_name(key)                      # Try to find the track by key

        if name is not None:
            if 1 <= new_rating <= 5:
                lib.set_rating(key, new_rating)       # Update the rating in the library
                artist = lib.get_artist(key)
                rating = lib.get_rating(key)
                play_count = lib.get_play_count(key)

                # Format and display updated track information
                track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}"
                set_text(self.list_txt, track_details)
            else:
                # Show error if rating is out of valid range
                set_text(self.list_txt, f"Rating should be between 1 and 5")
        else:
            # Show error if track does not exist
            set_text(self.list_txt, f"Track {key} not found")

        # Update the status label to confirm button was pressed
        self.status_lbl.configure(text="Update Track button was clicked!")

# Launch the application
if __name__ == "__main__":
    window = tk.Tk()            # Create the main window
    fonts.configure()           # Apply font settings
    app = UpdateTrack(window)   # Initialize the UpdateTrack GUI
    window.mainloop()           # Start the Tkinter event loop
