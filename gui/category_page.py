import customtkinter as ctk
from tkinter import messagebox
import json


class CategoryPage(ctk.CTkFrame):

    def __init__(self, master, player_name):
        super().__init__(master)

        self.master = master
        self.player_name = player_name

        # Load champion data @ startup
        self.champion_data = self.load_champion()

        # =============================
        # Title
        # =============================
        title = ctk.CTkLabel(
            self,
            text=f"Welcome {self.player_name}",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(20, 10))

        sub_title = ctk.CTkLabel(
            self,
            text="Please select your game settings",
            font=("Arial", 16)
        )
        sub_title.pack(pady=(0, 20))

        # ----------------------------
        # THEME SELECTION
        # ----------------------------
        theme_frame = ctk.CTkFrame(self, corner_radius=15)
        theme_frame.pack(pady=10, padx=20, fill="x")

        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Choose Theme:",
            font=("Arial", 16, "bold")
        )
        theme_label.pack(pady=10)

        self.theme_var = ctk.StringVar(value="dark")
        theme_options = ["light", "dark", "system"]

        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=theme_options,
            variable=self.theme_var,
            width=200,
            command=self.switch_theme
        )
        self.theme_menu.pack(pady=(0, 15))


        # ----------------------------
        # CHAMPION BOX (Fixed height with scroll)
        # ----------------------------
        champion_frame = ctk.CTkFrame(self, corner_radius=15, height=140)
        champion_frame.pack(pady=10, padx=20, fill="x")
        champion_frame.pack_propagate(False)

        scroll_area = ctk.CTkTextbox(
            champion_frame,
            width=500,
            height=130,
            font=("Arial", 14),
            fg_color="transparent",
        )
        scroll_area.pack(fill="both", expand=True, padx=10, pady=5)
        scroll_area.configure(state="normal")

        scroll_area.insert("end", "🥇 Current Champion\n\n")

        if self.champion_data["score"] == 0:
            scroll_area.insert("end", "No champion yet.\nBe the first to set a record!")
        else:
            scroll_area.insert(
                "end",
                f"Name: {self.champion_data['champion_name']}\n"
                f"Score to Beat: {self.champion_data['score']}\n"
                f"Date: {self.champion_data['date']}\n\n"
                "Categories Played:\n"
            )

            for key, val in self.champion_data["categories"].items():
                if val:
                    scroll_area.insert("end", f"   • {key.capitalize()}\n")

        # IMPORTANT → disable textbox ALWAYS
        scroll_area.configure(state="disabled")


        # ----------------------------
        # CATEGORY ~ DESCRIPTION PANEL
        # ----------------------------
        panel = ctk.CTkFrame(self, corner_radius=15)
        panel.pack(pady=10, padx=20, fill="both", expand=True)

        # Left side: Category checkboxes
        left_frame = ctk.CTkFrame(panel, corner_radius=10)
        left_frame.pack(
            side="left",
            fill="y",
            expand=False,
            padx=(10, 10),
            pady=10
        )

        cat_label = ctk.CTkLabel(
            left_frame,
            text="Select Categories",
            font=("Arial", 16, "bold")
        )
        cat_label.pack(pady=(10, 5))

        # Checkboxes
        self.tennis_var = ctk.BooleanVar()
        self.premier_var = ctk.BooleanVar()
        self.athletics_var = ctk.BooleanVar()

        self.cb_tennis = ctk.CTkCheckBox(
            left_frame,
            text="Tennis (2000 - Present)",
            variable=self.tennis_var,
            font=("Arial", 14)
        )
        self.cb_tennis.pack(anchor="w", padx=10, pady=5)

        self.cb_premier = ctk.CTkCheckBox(
            left_frame,
            text="Premier League (2000 - Present)",
            variable=self.premier_var,
            font=("Arial", 14)
        )
        self.cb_premier.pack(anchor="w", padx=10, pady=5)

        self.cb_athletics = ctk.CTkCheckBox(
            left_frame,
            text="Athletics (100m & 200m, 2000 - Present)",
            variable=self.athletics_var,
            font=("Arial", 12)
        )
        self.cb_athletics.pack(anchor="w", padx=10, pady=5)

        # Right side: Description
        right_frame = ctk.CTkFrame(panel, corner_radius=10)
        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(0, 10),
            pady=10
        )

        info_label = ctk.CTkLabel(
            right_frame,
            text="Category Information",
            font=("Arial", 14, "bold")
        )
        info_label.pack(pady=(10, 5))

        desc_box = ctk.CTkTextbox(
            right_frame,
            width=480,
            height=110,
            font=("Arial", 12)
        )
        desc_box.insert(
            "0.0",
            "✔ Tennis: Grand Slam champions and finalists since the year 2000.\n"
            "✔ Premier League: Top scorers, title winners, star performers.\n"
            "✔ Athletics: Olympic & World Champions in 100m and 200m.\n\n"
            "Choose one or more categories to begin your challenge."
        )
        desc_box.configure(state="disabled")
        desc_box.pack(fill="both", expand=True, padx=10, pady=10)

        # ----------------------------
        # QUESTION COUNT SELECTOR
        # ----------------------------
        question_frame = ctk.CTkFrame(self, corner_radius=15)
        question_frame.pack(pady=10, padx=20, fill="x")

        q_label = ctk.CTkLabel(
            question_frame,
            text="How many questions?",
            font=("Arial", 14, "bold")
        )
        q_label.pack(pady=(10, 0))

        self.q_var = ctk.StringVar(value="10")
        q_options = ["5", "10", "15", "20", "Custom"]

        self.q_menu = ctk.CTkOptionMenu(
            question_frame,
            values=q_options,
            variable=self.q_var,
            width=200,
            command=self.show_custom_entry
        )
        self.q_menu.pack(pady=10)

        self.custom_q_entry = ctk.CTkEntry(
            question_frame,
            width=200,
            placeholder_text="Enter number"
        )
        self.custom_q_entry.pack(pady=5)
        self.custom_q_entry.pack_forget()

        # ----------------------------
        # START BUTTON
        # ----------------------------
        start_btn = ctk.CTkButton(
            self,
            text="Start Game",
            width=220,
            height=45,
            font=("Arial", 17, "bold"),
            command=self.start_game
        )
        start_btn.pack(pady=10)

    # =====================================
    # Change theme dynamically
    # =====================================
    def switch_theme(self, choice):
        ctk.set_appearance_mode(choice)

    # =====================================
    # Show custom question input
    # =====================================
    def show_custom_entry(self, choice):
        if choice == "Custom":
            self.custom_q_entry.pack()
        else:
            self.custom_q_entry.pack_forget()

    # =====================================
    # Validate inputs and start game
    # =====================================
    def start_game(self):
        if not (
            self.tennis_var.get()
            or self.premier_var.get()
            or self.athletics_var.get()
        ):
            messagebox.showwarning(
                "Error",
                "You must select at least one category."
            )
            return

        q_choice = self.q_var.get()
        if q_choice == "Custom":
            try:
                q_count = int(self.custom_q_entry.get())
                if q_count < 1:
                    raise ValueError
            except Exception:
                messagebox.showwarning(
                    "Error",
                    "Enter a valid positive number."
                )
                return
        else:
            q_count = int(q_choice)

        settings = {
            "player_name": self.player_name,
            "categories": {
                "tennis": self.tennis_var.get(),
                "premier": self.premier_var.get(),
                "athletics": self.athletics_var.get()
            },
            "q_count": q_count,
            "theme": self.theme_var.get()
        }

        self.master.show_game(settings)

    def load_champion(self):
        try:
            with open("data/champion.json", "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    return {
                        "champion_name": "No champion yet",
                        "score": 0,
                        "date": "",
                        "categories": {},
                        "correct_answers": 0,
                        "total_questions": 0,
                        "hints_used": 0
                    }
        except (json.JSONDecodeError, FileNotFoundError):
            return {
                "champion_name": "No champion yet",
                "score": 0,
                "date": "",
                "categories": {},
                "correct_answers": 0,
                "total_questions": 0,
                "hints_used": 0
            }
