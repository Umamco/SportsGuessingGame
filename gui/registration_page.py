import customtkinter as ctk
import json
import os
from datetime import datetime
from tkinter import messagebox


class RegistrationPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_categories):
        super().__init__(master)

        self.switch_to_categories = switch_to_categories

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

        # Button
        register_btn = ctk.CTkButton(
            self,
            text="Register & Continue",
            width=200,
            height=40,
            command=self.register_player
        )
        register_btn.pack(pady=25)

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
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # auto-repair

    # =======================
    # SAVE PLAYER INFORMATION
    # =======================
    def register_player(self):
        name = self.name_var.get().strip()

        if name == "":
            messagebox.showwarning("Error", "Please enter your full name.")
            return

        players = self.safe_load()  # SAFE LOAD

        players.append({
            "player_name": name,
            "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        # Save file
        with open("data/players.json", "w") as f:
            json.dump(players, f, indent=4)

        # Move to category page
        self.switch_to_categories(name)
