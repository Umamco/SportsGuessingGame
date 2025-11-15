import customtkinter as ctk
import json
import os
from datetime import datetime
from tkinter import messagebox


class RegistrationPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        # Title
        title = ctk.CTkLabel(self, text="Player Registration",
                             font=("Arial", 28, "bold"))
        title.pack(pady=30)

        # Input field
        self.name_var = ctk.StringVar()
        name_label = ctk.CTkLabel(self, text="Enter your full name:",
                                  font=("Arial", 16))
        name_label.pack(pady=(10, 5))

        self.name_entry = ctk.CTkEntry(self, width=300, height=40,
                                       textvariable=self.name_var,
                                       placeholder_text="e.g., Amin Umar")
        self.name_entry.pack(pady=10)

        # Register button
        register_btn = ctk.CTkButton(
            self,
            text="Register & Continue",
            width=200,
            height=40,
            command=self.register_player
        )
        register_btn.pack(pady=25)

        # ===============================
        # NAVIGATION BUTTONS (NEW)
        # ===============================
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=10)

        home_btn = ctk.CTkButton(
            nav_frame,
            text="🏠 Home",
            width=140,
            command=self.master.back_to_home
        )
        home_btn.pack(side="left", padx=10)

        history_btn = ctk.CTkButton(
            nav_frame,
            text="📘 Players History",
            width=160,
            command=self.master.show_players_history
        )
        history_btn.pack(side="left", padx=10)

        # Ensure data folder exists
        os.makedirs("data", exist_ok=True)

        # Ensure players.json exists
        if not os.path.exists("data/players.json"):
            with open("data/players.json", "w") as f:
                json.dump([], f, indent=4)

    # =======================
    # SAFE JSON LOADING
    # =======================
    def safe_load(self):
        try:
            with open("data/players.json", "r") as f:
                return json.load(f)
        except:
            return []

    # =======================
    # SAVE PLAYER INFORMATION
    # =======================
    def register_player(self):
        name = self.name_var.get().strip()

        if name == "":
            messagebox.showwarning("Error", "Please enter your full name.")
            return

        players = self.safe_load()

        players.append({
            "player_name": name,
            "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        with open("data/players.json", "w") as f:
            json.dump(players, f, indent=4)

        # Move to categories
        self.master.show_categories(name)
