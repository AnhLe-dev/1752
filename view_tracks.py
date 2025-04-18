import tkinter as tk
import tkinter.scrolledtext as tkst
import csv
from library_item import LibraryItem  # Custom class representing a music track
import track_library as lib           # Custom module handling the track database (dictionary)
import font_manager as fonts          # Module to configure custom fonts
from PIL import Image, ImageTk        # Used to handle and display album cover images

# Utility function: replaces the content of a text area with new content
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)  # Clear the existing content
    text_area.insert(1.0, content)   # Insert new content starting at the beginning

# Class to manage and display the track viewer GUI
class TrackViewer():
    def __init__(self, window):
        window.geometry("850x350")       # Set window size
        window.title("View Tracks")      # Set window title

        # Button to list all tracks from the library
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        # Label prompting user to enter a track number
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        # Entry box for inputting track number
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        # Button to view details of a specific track
        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)

        # Button to load additional songs from a CSV file
        load_csv_btn = tk.Button(window, text="Load More Songs from CSV", command=self.load_csv_clicked)
        load_csv_btn.grid(row=0, column=4, padx=10, pady=10)

        # Scrollable text box to display the full track list
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Text box to show details of a selected track
        self.track_txt = tk.Text(window, width=24, height=8, wrap="none")
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        # Label used to display status messages (e.g., which button was clicked)
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Label to show the album cover image of the selected track
        self.cover_img_label = tk.Label(window)
        self.cover_img_label.grid(row=1, column=4, padx=10, pady=10)

        # Optional: Automatically load the track list when the window opens
        # self.list_tracks_clicked()

        # Clear the track list area on startup
        set_text(self.list_txt, "")

    # Callback function for the "View Track" button
    def view_tracks_clicked(self):
        key = self.input_txt.get()            # Get the track number entered by the user
        name = lib.get_name(key)              # Try to get the name of the track from the library

        image_path = f"photos/{key}.jpg"      # Path to the corresponding album cover image
        try:
            img = Image.open(image_path)      # Try to open the image file
            img = img.resize((200, 200))      # Resize the image for display
            photo = ImageTk.PhotoImage(img)   # Convert image for Tkinter
            self.cover_img_label.config(image=photo)
            self.cover_img_label.image = photo  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            # If no image is found, clear the image display
            self.cover_img_label.config(image="")
            self.cover_img_label.image = None

        if name is not None:
            # If the track exists, retrieve and display full information
            artist = lib.get_artist(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)

            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}"
            set_text(self.track_txt, track_details)  # Display track details
        else:
            # If the track is not found, show an error message
            set_text(self.track_txt, f"Track {key} not found")

        self.status_lbl.configure(text="View Track button was clicked!")  # Update status message

    # Callback function for the "List All Tracks" button
    def list_tracks_clicked(self):
        track_list = lib.list_all()  # Get the full list of tracks from the library
        set_text(self.list_txt, track_list)  # Display the track list in the scrollable text area
        self.status_lbl.configure(text="List Tracks button was clicked!")  # Update status message

    # Callback function for the "Load More Songs from CSV" button
    def load_csv_clicked(self):        
        with open("new_tracks.csv", newline='') as data_file:
            data = csv.reader(data_file)
            next(data)  # Skip the header row

            for row in data:                     
                key = row[0]
                # Only add the track if it doesn't already exist in the library
                if lib.get_name(key) is None:
                    name = row[1]
                    artist = row[2]
                    rating = int(row[3])
                    play_count = int(row[4])

                    # Create a new LibraryItem and add it to the dictionary
                    new_item = LibraryItem(name, artist, rating)
                    new_item.play_count = play_count
                    lib.library[key] = new_item

        self.list_tracks_clicked()  # Refresh the track list after loading new songs

# Run the GUI application
if __name__ == "__main__":
    window = tk.Tk()         # Create the main application window
    fonts.configure()        # Apply font settings
    TrackViewer(window)      # Create and show the TrackViewer interface
    window.mainloop()        # Start the Tkinter event loop
