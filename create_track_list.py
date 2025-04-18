import tkinter as tk
import tkinter.scrolledtext as tkst

import track_library as lib  # Custom module for track management
import font_manager as fonts  # Custom module for font configuration

# Utility function to safely set content for a Text or ScrolledText widget
def set_text(text_area, content):
    text_area.configure(state=tk.NORMAL)  # Allow editing
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)
    text_area.configure(state=tk.DISABLED)  # Disable editing again

# Main Playlist class
class TrackPlaylist():
    def __init__(self, window):
        self.window = window
        window.title("Create_Track_List")
        self.current_track_index = 0  # Index of currently selected/playing track
        self.playlist_keys = []  # List of track keys in the playlist

        # Input field for entering track number
        self.input_entry = tk.Entry(window, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label prompting user to enter track number
        enter_track_lbl = tk.Label(window, text="Enter Track Number:")
        enter_track_lbl.grid(row=0, column=0, padx=10, pady=5)

        # Button to add a track to the playlist
        add_btn = tk.Button(window, text="Add to Playlist", command=self.add_track_clicked)
        add_btn.grid(row=0, column=2, padx=10, pady=5)

        # --- Row 1: Error Label ---
        self.error_lbl = tk.Label(window, text="", fg="red")  # Error message display
        self.error_lbl.grid(row=1, column=0, columnspan=3, padx=10, pady=2)

        # --- Row 2-3: Playlist Display Area ---
        playlist_lbl = tk.Label(window, text="Playlist")
        playlist_lbl.grid(row=2, column=0, columnspan=2, padx=10, pady=(5,0))

        self.playlist_txt = tkst.ScrolledText(window, width=50, height=8, wrap="none", state=tk.DISABLED)
        self.playlist_txt.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Previous track button
        previous_btn = tk.Button(window, text="Previous", command=self.play_previous_track)
        previous_btn.grid(row=2, column=0, sticky="w", padx=10)

        # Next track button
        next_btn = tk.Button(window, text="Next", command=self.play_next_track)
        next_btn.grid(row=2, column=1, sticky="e", padx=10)

        # --- Track Information Area ---
        infor_lbl = tk.Label(window, text="Information")
        infor_lbl.grid(row=2, column=2, padx=10, pady=(5,0))

        self.track_infor_txt = tk.Text(window, width=30, height=8, wrap="none")
        self.track_infor_txt.grid(row=3, column=2, sticky="w", padx=10, pady=10)

        # Button to play current track from playlist
        play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist_clicked)
        play_btn.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Button to clear/reset the playlist
        reset_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist_clicked)
        reset_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # --- Song Library Display ---
        all_tracks_lbl = tk.Label(window, text="Song List:")
        all_tracks_lbl.grid(row=5, column=0, columnspan=3, padx=10, pady=(10,0), sticky="w")

        self.all_tracks_txt = tkst.ScrolledText(window, width=60, height=10, wrap="none", state=tk.DISABLED)
        self.all_tracks_txt.grid(row=6, column=0, columnspan=3, padx=10, pady=(0,10), sticky="ew")

        # Load all tracks from the library into the display area
        self.load_all_tracks()

        # Clear any initial error messages
        self.update_error_message("")

    # Update the red error label message
    def update_error_message(self, message):
        self.error_lbl.config(text=message)

    # Action when 'Add to Playlist' button is clicked
    def add_track_clicked(self):
        track_key = self.input_entry.get().strip()  # Get user input
        self.update_error_message("")  # Clear previous error

        if not track_key:
            self.update_error_message("Error: Please enter a track number.")
            return

        track_name = lib.get_name(track_key)
        if track_name:
            if track_key not in self.playlist_keys:
                self.playlist_keys.append(track_key)
                self.update_playlist_display()
                self.input_entry.delete(0, tk.END)  # Clear the input field
            else:
                self.update_error_message(f"Error: Track {track_key} is already in the playlist.")
        else:
            self.update_error_message(f"Error: Track {track_key} not found in the library.")

    # Update playlist display area with track info
    def update_playlist_display(self):
        playlist_content = ""
        for key in self.playlist_keys:
            name = lib.get_name(key)
            artist = lib.get_artist(key)
            if name and artist:
                playlist_content += f"{key}: {name} - {artist}\n"
        set_text(self.playlist_txt, playlist_content if playlist_content else "Playlist is empty.")

    # Play the current track in playlist and show detailed info
    def play_playlist_clicked(self):
        if not self.playlist_keys:
            self.update_error_message("Playlist is empty. Add tracks first.")
            return

        key = self.playlist_keys[self.current_track_index]
        lib.increment_play_count(key)
        name = lib.get_name(key)
        artist = lib.get_artist(key)
        play_count = lib.get_play_count(key)
        rating = lib.get_rating(key)

        play_info = f" Playing: {name}\n {artist}\n rating: {rating} \n  Plays: {play_count}"
        set_text(self.track_infor_txt, play_info)
        self.show_track_info(key)
        self.load_all_tracks()  # Reload library info (if updated)

    # Reset/clear the playlist and UI components
    def reset_playlist_clicked(self):
        self.playlist_keys = []
        self.update_playlist_display()
        self.current_track_index = 0
        set_text(self.track_infor_txt, "")
        self.update_error_message("Playlist reset.")
        self.input_entry.delete(0, tk.END)

    # Load and display all tracks from the library
    def load_all_tracks(self):
        all_tracks_content = lib.list_all()
        set_text(self.all_tracks_txt, all_tracks_content if all_tracks_content else "Library is empty.")

    # Go to next track in playlist and update the info display
    def play_next_track(self):
        if not self.playlist_keys:
            self.update_error_message("Playlist is empty.")
            return

        if self.current_track_index < len(self.playlist_keys) - 1:
            self.current_track_index += 1
            self.show_track_info(self.playlist_keys[self.current_track_index])
        else:
            self.update_error_message("Already at the last track.")

    # Go to previous track in playlist and update the info display
    def play_previous_track(self):
        if not self.playlist_keys:
            self.update_error_message("Playlist is empty.")
            return

        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.show_track_info(self.playlist_keys[self.current_track_index])
        else:
            self.update_error_message("Already at the first track.")

    # Display track information in the text area
    def show_track_info(self, key):
        name = lib.get_name(key)
        artist = lib.get_artist(key)
        play_count = lib.get_play_count(key)
        rating = lib.get_rating(key)
        play_info = f"Playing: {name}\n{artist}\nRating: {rating}\nPlays: {play_count}"
        set_text(self.track_infor_txt, play_info)

# --- Main run block ---
if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()  # Apply font settings from external module
    TrackPlaylist(window)
    window.mainloop()
