import tkinter as tk

import font_manager as fonts                 # Module to configure font settings
from view_tracks import TrackViewer         # Module to view existing tracks
from create_track_list import TrackPlaylist # Module to create playlists
from update_track import UpdateTrack        # Module to update track ratings

# Function triggered when the "View Tracks" button is clicked
def view_tracks_clicked():
    status_lbl.configure(text="View Tracks button was clicked!")  # Update status label
    TrackViewer(tk.Toplevel(window))  # Open a new child window with the TrackViewer GUI

# Function triggered when the "Create Track List" button is clicked
def create_track_list():
    status_lbl.configure(text="Create Track button was clicked!")  # Update status label
    TrackPlaylist(tk.Toplevel(window))  # Open a new child window with the playlist creation interface

# Function triggered when the "Update Tracks" button is clicked
def update_tracks():
    status_lbl.configure(text="Update Track button was clicked!")  # Update status label
    UpdateTrack(tk.Toplevel(window))  # Open a new child window with the track update interface

# Initialize the main application window
window = tk.Tk()
window.geometry("520x150")             # Set window dimensions
window.title("JukeBox")                # Set the window title
window.configure(bg="gray")            # Set background color

fonts.configure()                      # Apply font settings

# Header label to instruct the user
header_lbl = tk.Label(
    window, 
    text="Select an option by clicking one of the buttons below"
)
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Button to open "View Tracks" window
view_tracks_btn = tk.Button(
    window, 
    text="View Tracks", 
    command=view_tracks_clicked
)
view_tracks_btn.grid(row=1, column=0, padx=10, pady=10)

# Button to open "Create Track List" window
create_track_list_btn = tk.Button(
    window, 
    text="Create Track List", 
    command=create_track_list
)
create_track_list_btn.grid(row=1, column=1, padx=10, pady=10)

# Button to open "Update Tracks" window
update_tracks_btn = tk.Button(
    window, 
    text="Update Tracks", 
    command=update_tracks
)
update_tracks_btn.grid(row=1, column=2, padx=10, pady=10)

# Status label to show feedback for user actions
status_lbl = tk.Label(
    window, 
    bg='gray', 
    text="", 
    font=("Helvetica", 10)
)
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Start the main application loop
window.mainloop()

# Redundant mainloop guard (not necessary since it’s already running above)
if __name__ == "__main__":
    window.mainloop()
