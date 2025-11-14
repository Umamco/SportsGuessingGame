import customtkinter as ctk
from gui.registration_page import RegistrationPage
from gui.category_page import CategoryPage
from gui.game_page import GamePage
from gui.summary_page import SummaryPage


class NameGuessingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sports Name Guessing Game")
        self.geometry("700x600")

        # Default appearance until player chooses
        ctk.set_appearance_mode("dark")

        self.current_frame = None

        # Start with registration
        self.show_registration()

    # -----------------------------
    # Show registration screen
    # -----------------------------
    def show_registration(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = RegistrationPage(
            self,
            switch_to_categories=self.show_categories
        )
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # Show category selection
    # -----------------------------
    def show_categories(self, player_name):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CategoryPage(
            self,
            player_name=player_name
        )
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # Show game page
    # -----------------------------
    def show_game(self, settings: dict):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = GamePage(self, settings)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # Show summary page
    # -----------------------------
    def show_summary(self, summary_data: dict):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = SummaryPage(self, summary_data)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = NameGuessingApp()
    app.mainloop()