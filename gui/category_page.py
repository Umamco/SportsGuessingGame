import customtkinter as ctk
from tkinter import messagebox


class CategoryPage(ctk.CTkFrame):
    def __init__(self, master, player_name):
        super().__init__(master)

        self.master = master
        self.player_name = player_name

        # ----------------------------
        # Title
        # ----------------------------
        title = ctk.CTkLabel(self, text=f"Welcome {self.player_name}",
                             font=("Arial", 26, "bold"))
        title.pack(pady=(20, 10))

        sub_title = ctk.CTkLabel(self,
                                 text="Please select your game settings",
                                 font=("Arial", 16))
        sub_title.pack(pady=(0, 20))

        # ----------------------------
        # THEME SELECTION
        # ----------------------------
        theme_frame = ctk.CTkFrame(self, corner_radius=15)
        theme_frame.pack(pady=10, padx=20, fill="x")

        theme_label = ctk.CTkLabel(theme_frame, text="Choose Theme:",
                                   font=("Arial", 16, "bold"))
        theme_label.pack(pady=10)

        self.theme_var = ctk.StringVar(value="dark")
        theme_options = ["light", "dark", "system"]

        self.theme_menu = ctk.CTkOptionMenu(theme_frame,
                                            values=theme_options,
                                            variable=self.theme_var,
                                            width=200,
                                            command=self.switch_theme)
        self.theme_menu.pack(pady=(0, 15))

        # ----------------------------
        # CATEGORY SELECTION
        # ----------------------------
        category_frame = ctk.CTkFrame(self, corner_radius=15)
        category_frame.pack(pady=10, padx=20, fill="both", expand=True)

        cat_label = ctk.CTkLabel(category_frame,
                                 text="Select Categories",
                                 font=("Arial", 18, "bold"))
        cat_label.pack(pady=10)

        # Checkboxes
        self.tennis_var = ctk.BooleanVar()
        self.premier_var = ctk.BooleanVar()
        self.athletics_var = ctk.BooleanVar()

        self.cb_tennis = ctk.CTkCheckBox(
            category_frame,
            text="Tennis (2000 - Present)",
            variable=self.tennis_var,
            font=("Arial", 15)
        )
        self.cb_tennis.pack(anchor="w", padx=20, pady=5)

        self.cb_premier = ctk.CTkCheckBox(
            category_frame,
            text="Premier League (2000 - Present)",
            variable=self.premier_var,
            font=("Arial", 15)
        )
        self.cb_premier.pack(anchor="w", padx=20, pady=5)

        self.cb_athletics = ctk.CTkCheckBox(
            category_frame,
            text="Athletics (100m & 200m, 2000 - Present)",
            variable=self.athletics_var,
            font=("Arial", 15)
        )
        self.cb_athletics.pack(anchor="w", padx=20, pady=5)

        # ----------------------------
        # DESCRIPTION BOX
        # ----------------------------
        desc_box = ctk.CTkTextbox(category_frame,
                                  width=520,
                                  height=130,
                                  font=("Arial", 14))
        desc_box.insert("0.0",
            "✔ Tennis: Grand Slam champions and finalists since the year 2000.\n"
            "✔ Premier League: Top scorers, title winners, star performers.\n"
            "✔ Athletics: Olympic & World Champions in 100m and 200m.\n\n"
            "Choose one or more categories to begin your challenge."
        )
        desc_box.configure(state="disabled")
        desc_box.pack(pady=10, padx=10)

        # ----------------------------
        # QUESTION COUNT SELECTOR
        # ----------------------------
        question_frame = ctk.CTkFrame(self, corner_radius=15)
        question_frame.pack(pady=10, padx=20, fill="x")

        q_label = ctk.CTkLabel(question_frame,
                               text="How many questions?",
                               font=("Arial", 16, "bold"))
        q_label.pack(pady=(10, 0))

        self.q_var = ctk.StringVar(value="10")
        q_options = ["5", "10", "15", "20", "Custom"]

        self.q_menu = ctk.CTkOptionMenu(question_frame,
                                        values=q_options,
                                        variable=self.q_var,
                                        width=200,
                                        command=self.show_custom_entry)
        self.q_menu.pack(pady=10)

        # Custom question entry (hidden by default)
        self.custom_q_entry = ctk.CTkEntry(question_frame,
                                           width=200,
                                           placeholder_text="Enter number")
        self.custom_q_entry.pack(pady=5)
        self.custom_q_entry.pack_forget()

        # ----------------------------
        # START BUTTON
        # ----------------------------
        start_btn = ctk.CTkButton(self,
                                  text="Start Game",
                                  width=220,
                                  height=45,
                                  font=("Arial", 17, "bold"),
                                  command=self.start_game)
        start_btn.pack(pady=25)

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
        if not (self.tennis_var.get() or self.premier_var.get() or self.athletics_var.get()):
            messagebox.showwarning("Error",
                                   "You must select at least one category.")
            return

        # Determine question count
        q_choice = self.q_var.get()
        if q_choice == "Custom":
            try:
                q_count = int(self.custom_q_entry.get())
                if q_count < 1:
                    raise ValueError
            except Exception:
                messagebox.showwarning("Error",
                                       "Enter a valid positive number.")
                return
        else:
            q_count = int(q_choice)

        # Package game settings
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

        # Call next screen (Game Page)
        self.master.show_game(settings)
