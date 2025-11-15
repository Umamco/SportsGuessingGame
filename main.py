import customtkinter as ctk
from gui.home_page import HomePage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # WINDOW SETTINGS
        # -----------------------------
        self.title("Name Guessing Game")
        self.geometry("750x800")
        self.resizable(False, True)

        self.current_frame = None

        # -----------------------------
        # START WITH HOME PAGE
        # -----------------------------
        self.show_home()

    # ============================================================
    # NAVIGATION METHODS
    # ============================================================

    def clear_frame(self):
        """Destroy current frame safely."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    # -----------------------------
    # HOME PAGE
    # -----------------------------
    def show_home(self):
        self.clear_frame()
        self.current_frame = HomePage(self)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # REGISTRATION PAGE
    # -----------------------------
    def show_registration(self):
        self.clear_frame()
        from gui.registration_page import RegistrationPage
        self.current_frame = RegistrationPage(self)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # CATEGORY PAGE
    # -----------------------------
    def show_categories(self, player_name):
        self.clear_frame()
        from gui.category_page import CategoryPage
        self.current_frame = CategoryPage(self, player_name)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # GAME PAGE
    # -----------------------------
    def show_game(self, settings):
        self.clear_frame()
        from gui.game_page import GamePage
        self.current_frame = GamePage(self, settings)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # SUMMARY PAGE
    # -----------------------------
    def show_summary(self, data):
        self.clear_frame()
        from gui.summary_page import SummaryPage
        self.current_frame = SummaryPage(self, data)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # PLAYERS HISTORY PAGE
    # -----------------------------
    def show_players_history(self):
        self.clear_frame()
        from gui.players_history_page import PlayersHistoryPage
        self.current_frame = PlayersHistoryPage(self)
        self.current_frame.pack(fill="both", expand=True)

    # -----------------------------
    # BACK NAVIGATION (used by many pages)
    # -----------------------------
    def back_to_home(self):
        self.show_home()

    def back_to_categories(self, player_name=None):
        # If name not passed, fall back to previously stored name
        if player_name:
            self.show_categories(player_name)
        else:
            self.show_home()


# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
