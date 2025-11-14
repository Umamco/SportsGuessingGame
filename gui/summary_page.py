import customtkinter as ctk


class SummaryPage(ctk.CTkFrame):
    def __init__(self, master, summary_data: dict):
        super().__init__(master)

        self.master = master
        self.summary_data = summary_data

        title = ctk.CTkLabel(self,
                             text="Game Summary",
                             font=("Arial", 26, "bold"))
        title.pack(pady=(25, 10))

        name_label = ctk.CTkLabel(
            self,
            text=f"Player: {summary_data['player_name']}",
            font=("Arial", 18)
        )
        name_label.pack(pady=5)

        score_label = ctk.CTkLabel(
            self,
            text=f"Total Score: {summary_data['score']}",
            font=("Arial", 18, "bold")
        )
        score_label.pack(pady=5)

        correct_label = ctk.CTkLabel(
            self,
            text=f"Correct Answers: {summary_data['correct_answers']} / {summary_data['total_questions']}",
            font=("Arial", 16)
        )
        correct_label.pack(pady=5)

        attempts_label = ctk.CTkLabel(
            self,
            text=f"Questions Attempted: {summary_data['questions_attempted']}",
            font=("Arial", 16)
        )
        attempts_label.pack(pady=5)

        hints_label = ctk.CTkLabel(
            self,
            text=f"Hints Used: {summary_data['hints_used']}",
            font=("Arial", 16)
        )
        hints_label.pack(pady=5)

        date_label = ctk.CTkLabel(
            self,
            text=f"Date & Time: {summary_data['date_time']}",
            font=("Arial", 14, "italic")
        )
        date_label.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(self, corner_radius=15)
        btn_frame.pack(pady=20)

        play_again_btn = ctk.CTkButton(
            btn_frame,
            text="Play Again",
            width=140,
            command=self.play_again
        )
        play_again_btn.pack(side="left", padx=10, pady=10)

        home_btn = ctk.CTkButton(
            btn_frame,
            text="Back to Categories",
            width=160,
            command=self.back_to_categories
        )
        home_btn.pack(side="left", padx=10, pady=10)

        exit_btn = ctk.CTkButton(
            btn_frame,
            text="Exit",
            width=120,
            fg_color="red",
            hover_color="#aa0000",
            command=self.master.destroy
        )
        exit_btn.pack(side="left", padx=10, pady=10)

    def play_again(self):
        # Go straight to category selection for same player
        player_name = self.summary_data["player_name"]
        self.master.show_categories(player_name)

    def back_to_categories(self):
        player_name = self.summary_data["player_name"]
        self.master.show_categories(player_name)
