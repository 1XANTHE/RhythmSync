
# WELCOME TO MY MUSIC PLAYER MANAGER . ENJOY !!

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pygame
from mutagen.mp3 import MP3
from ttkthemes import ThemedStyle
import random

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("RhythmSync")
        self.root.geometry("900x800")
        self.root.resizable(False, False)
        self.root.config(bg="#242526")

        self.playlist = []
        self.current_index = 0
        self.paused = True
        self.shuffle_mode = False
        self.repeat_mode = False

        self.song_length = tk.StringVar()
        self.song_length.set("00:00")

        self.create_ui()

        pygame.mixer.init()
        self.update_playlist()

    def create_ui(self):
        style = ThemedStyle(self.root)
        style.theme_use('clam')

        heading_font = ('Papyrus', 40, 'bold')
        button_font = ('Segoe UI', 13, 'bold')
        list_font = ('Constantia', 12)

        heading_label = tk.Label(self.root, text="RhythmSync", font=heading_font, bg="#242526", fg="#D5FFF3")
        heading_label.pack(pady=20)

        self.song_list = tk.Listbox(self.root, bg="#1E1E1E", fg="#ffffff", selectbackground="#605D5F", selectforeground="#ffffff", height=20, width=70, font=list_font, bd=0, highlightthickness=0)
        self.song_list.pack(pady=10, padx=20)

        control_frame = tk.Frame(self.root, bg="#242526")
        control_frame.pack(pady=10)

        self.shuffle_button = tk.Button(control_frame, text="🔀", command=self.toggle_shuffle, font=button_font, bg="#3A0CA3", fg="#ffffff", height=1, width=4, bd=0, highlightthickness=0)
        self.shuffle_button.grid(row=0, column=0, padx=(20, 5))

        self.prev_button = tk.Button(control_frame, text="⏮️", command=self.prev_song, font=button_font, bg="#3A0CA3", fg="#ffffff", height=2, width=4, bd=0, highlightthickness=0)
        self.prev_button.grid(row=0, column=1, padx=5)

        self.play_button = tk.Button(control_frame, text="▶️", command=self.play_pause_music, font=button_font, bg="#43B581", fg="#ffffff", height=2, width=4, bd=0, highlightthickness=0)
        self.play_button.grid(row=0, column=2, padx=5)

        self.next_button = tk.Button(control_frame, text="⏭️", command=self.next_song, font=button_font, bg="#3A0CA3", fg="#ffffff", height=2, width=4, bd=0, highlightthickness=0)
        self.next_button.grid(row=0, column=3, padx=5)

        self.repeat_button = tk.Button(control_frame, text="🔁", command=self.toggle_repeat, font=button_font, bg="#3A0CA3", fg="#ffffff", height=1, width=4, bd=0, highlightthickness=0)
        self.repeat_button.grid(row=0, column=4, padx=(5, 20))

        self.time_slider = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=600, command=self.set_time)
        self.time_slider.pack()

        length_label = tk.Label(self.root, textvariable=self.song_length, font=button_font, bg="#242526", fg="#ffffff")
        length_label.pack(pady=5)

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Songs", command=self.add_songs)
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def add_songs(self):
        songs = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for song in songs:
            self.playlist.append(song)
        self.update_playlist()

    def update_playlist(self):
        self.song_list.delete(0, tk.END)
        for song in self.playlist:
            self.song_list.insert(tk.END, os.path.basename(song))

    def play_pause_music(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty.")
            return

        if self.paused:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def prev_song(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty.")
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_music()

    def next_song(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty.")
            return

        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)

        self.play_music()

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.shuffle_button.config(text="🔀", bg="#3A0CA3")
        else:
            self.shuffle_button.config(text="🔀", bg="#43B581")

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            self.repeat_button.config(text="🔁", bg="#3A0CA3")
        else:
            self.repeat_button.config(text="🔁", bg="#43B581")

    def set_time(self, value):
        song = MP3(self.playlist[self.current_index])
        length = song.info.length
        pygame.mixer.music.play(start=int(value) * length / 100)

    def update_time(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            self.time_slider.set((current_time / MP3(self.playlist[self.current_index]).info.length) * 100)
            minutes, seconds = divmod(current_time, 60)
            self.song_length.set("{:02}:{:02}".format(int(minutes), int(seconds)))
        else:
            self.paused = True

        self.root.after(1000, self.update_time) 

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    app.update_time()  
    root.mainloop()
