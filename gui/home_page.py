import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        # -----------------------------
        # TITLE
        # -----------------------------
        title = ctk.CTkLabel(
            self,
            text="🏆 Name Guessing Game",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(40, 25))

        # -----------------------------
        # START GAME CARD
        # -----------------------------
        start_card = ctk.CTkButton(
            self,
            text="Start Game",
            width=260,
            height=60,
            font=("Arial", 20, "bold"),
            corner_radius=18,
            command=self.master.show_registration
        )
        start_card.pack(pady=15)

        # -----------------------------
        # PLAYER HISTORY CARD
        # -----------------------------
        history_card = ctk.CTkButton(
            self,
            text="Players History",
            width=260,
            height=60,
            font=("Arial", 20, "bold"),
            corner_radius=18,
            command=self.master.show_players_history
        )
        history_card.pack(pady=15)

        # -----------------------------
        # EXIT CARD
        # -----------------------------
        exit_card = ctk.CTkButton(
            self,
            text="Exit",
            width=260,
            height=60,
            font=("Arial", 20, "bold"),
            corner_radius=18,
            fg_color="red",
            hover_color="#9b0000",
            command=self.master.destroy
        )
        exit_card.pack(pady=25)
