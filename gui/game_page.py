import customtkinter as ctk
import json
import os
import random
from datetime import datetime
from tkinter import messagebox


class GamePage(ctk.CTkFrame):
    def __init__(self, master, settings: dict):
        super().__init__(master)

        self.master = master
        self.settings = settings
        self.player_name = settings["player_name"]
        self.theme = settings["theme"]
        self.q_count = settings["q_count"]
        self.selected_categories = settings["categories"]

        # Apply theme
        ctk.set_appearance_mode(self.theme)

        # --------------------------
        # Load questions safely
        # --------------------------
        self.questions = self._load_questions()
        self.total_questions = len(self.questions)

        if self.total_questions == 0:
            messagebox.showerror("Error",
                                 "No questions found for selected categories.")
            self.master.show_categories(self.player_name)
            return

        # Pick unique sample
        self.total_questions = min(self.total_questions, self.q_count)
        self.questions = random.sample(self.questions, self.total_questions)

        # Game state
        self.current_index = -1
        self.current_question = None
        self.time_left = 0
        self.timer_id = None

        self.total_score = 0
        self.correct_count = 0
        self.attempted_count = 0
        self.hints_used = 0
        self.current_hint_penalty = 0
        self.used_hint_types = set()

        # ----------------------------
        # UI Layout
        # ----------------------------
        top_frame = ctk.CTkFrame(self, corner_radius=15)
        top_frame.pack(fill="x", padx=20, pady=(15, 5))

        player_label = ctk.CTkLabel(
            top_frame,
            text=f"Player: {self.player_name}",
            font=("Arial", 16, "bold")
        )
        player_label.pack(side="left", padx=10, pady=10)

        self.q_info_label = ctk.CTkLabel(
            top_frame,
            text="Question: 0 / 0",
            font=("Arial", 16)
        )
        self.q_info_label.pack(side="right", padx=10, pady=10)

        mid_frame = ctk.CTkFrame(self, corner_radius=15)
        mid_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.achievement_label = ctk.CTkLabel(
            mid_frame,
            text="Achievement will appear here.",
            font=("Arial", 16),
            wraplength=520,
            justify="left"
        )
        self.achievement_label.pack(pady=(15, 10), padx=15)

        self.hint_display_label = ctk.CTkLabel(
            mid_frame,
            text="Hint: (none used yet)",
            font=("Arial", 15, "italic")
        )
        self.hint_display_label.pack(pady=(5, 15))

        entry_frame = ctk.CTkFrame(mid_frame, corner_radius=15)
        entry_frame.pack(pady=10, padx=15, fill="x")


        ans_label = ctk.CTkLabel(entry_frame,
                                 text="Your guess (full name):",
                                 font=("Arial", 15))
        ans_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.answer_var = ctk.StringVar()
        self.answer_entry = ctk.CTkEntry(entry_frame,
                                         textvariable=self.answer_var,
                                         width=400,
                                         height=40,
                                         placeholder_text="Type the name here")
        self.answer_entry.pack(pady=10, padx=10)

        submit_btn = ctk.CTkButton(entry_frame,
                                   text="Submit Answer",
                                   width=160,
                                   command=self.check_answer)
        submit_btn.pack(pady=(0, 15))

        bottom_frame = ctk.CTkFrame(self, corner_radius=15)
        bottom_frame.pack(fill="x", padx=20, pady=(5, 15))

        self.timer_label = ctk.CTkLabel(bottom_frame,
                                        text="Time left: 120s",
                                        font=("Arial", 16, "bold"))
        self.timer_label.pack(side="left", padx=10, pady=10)

        self.score_label = ctk.CTkLabel(bottom_frame,
                                        text="Score: 0",
                                        font=("Arial", 16, "bold"))
        self.score_label.pack(side="right", padx=10, pady=10)

        hint_frame = ctk.CTkFrame(self, corner_radius=15)
        hint_frame.pack(fill="x", padx=20, pady=(0, 10))

        hint_title = ctk.CTkLabel(hint_frame,
                                  text="Hints (cost points):",
                                  font=("Arial", 15, "bold"))
        hint_title.pack(pady=(8, 5))

        self.btn_hint_first = ctk.CTkButton(
            hint_frame, text="Reveal 1st Letter (-2)", width=160,
            command=self.use_hint_first
        )
        self.btn_hint_first.pack(side="left", padx=10, pady=10)

        self.btn_hint_two = ctk.CTkButton(
            hint_frame, text="Reveal 2 Letters (-4)", width=160,
            command=self.use_hint_two
        )
        self.btn_hint_two.pack(side="left", padx=10, pady=10)

        self.btn_hint_half = ctk.CTkButton(
            hint_frame, text="Reveal Half Name (-6)", width=160,
            command=self.use_hint_half
        )
        self.btn_hint_half.pack(side="left", padx=10, pady=10)

        # Start
        self.next_question()

    # ==========================
    # Load & filter questions
    # ==========================
    def _load_questions(self):
        if not os.path.exists("data/questions.json"):
            return []

        try:
            with open("data/questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Corrupted file → empty list

        pool = []
        if self.selected_categories.get("premier"):
            pool.extend(data.get("premier_league", []))
        if self.selected_categories.get("tennis"):
            pool.extend(data.get("tennis", []))
        if self.selected_categories.get("athletics"):
            pool.extend(data.get("athletics", []))

        return pool

    # ==========================
    # Timer Handling
    # ==========================
    def start_timer(self):
        self.time_left = 120
        self.update_timer()

    def update_timer(self):
        self.timer_label.configure(text=f"Time left: {self.time_left}s")

        if self.time_left <= 0:
            messagebox.showinfo("Time's up!",
                                "Time is up for this question.\nMoving to the next one.")
            self.attempted_count += 1
            self.next_question()
        else:
            self.time_left -= 1
            self.timer_id = self.after(1000, self.update_timer)

    def cancel_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    # ==========================
    # Question Flow
    # ==========================
    def next_question(self):
        self.cancel_timer()
        self.current_index += 1

        if self.current_index >= self.total_questions:
            self.finish_game()
            return

        # Reset hints
        self.current_hint_penalty = 0
        self.used_hint_types = set()
        self.hint_display_label.configure(text="Hint: (none used yet)")
        self.btn_hint_first.configure(state="normal")
        self.btn_hint_two.configure(state="normal")
        self.btn_hint_half.configure(state="normal")

        # Load question
        self.current_question = self.questions[self.current_index]
        achievement_text = self.current_question["achievement"]
        self.achievement_label.configure(text=achievement_text)

        self.q_info_label.configure(
            text=f"Question: {self.current_index + 1} / {self.total_questions}"
        )

        self.answer_var.set("")
        self.answer_entry.focus()

        self.start_timer()

    # ==========================
    # Hint Helpers
    # ==========================
    def _build_hint(self, reveal_count: int):
        name = self.current_question["name"]
        reveal_count = min(reveal_count, len(name))
        return name[:reveal_count] + "*" * (len(name) - reveal_count)

    def use_hint_first(self):
        if "first" in self.used_hint_types:
            return
        self.used_hint_types.add("first")
        self.current_hint_penalty += 2
        self.hints_used += 1
        hint_text = self._build_hint(1)
        self.hint_display_label.configure(text=f"Hint: {hint_text}")
        self.btn_hint_first.configure(state="disabled")

    def use_hint_two(self):
        if "two" in self.used_hint_types:
            return
        self.used_hint_types.add("two")
        self.current_hint_penalty += 4
        self.hints_used += 1
        hint_text = self._build_hint(2)
        self.hint_display_label.configure(text=f"Hint: {hint_text}")
        self.btn_hint_two.configure(state="disabled")

    def use_hint_half(self):
        if "half" in self.used_hint_types:
            return
        self.used_hint_types.add("half")
        self.current_hint_penalty += 6
        self.hints_used += 1
        half = len(self.current_question["name"]) // 2
        hint_text = self._build_hint(half)
        self.hint_display_label.configure(text=f"Hint: {hint_text}")
        self.btn_hint_half.configure(state="disabled")

    # ==========================
    # Answer Checking
    # ==========================
    def check_answer(self):
        if self.current_question is None:
            return

        self.cancel_timer()

        user_ans = self.answer_var.get().strip().lower()
        correct_ans = self.current_question["name"].strip().lower()

        self.attempted_count += 1

        if user_ans == "":
            messagebox.showwarning("No answer",
                                   "Please enter a name before submitting.")
            self.next_question()
            return

        if user_ans == correct_ans:
            self.correct_count += 1
            question_score = max(0, 10 - self.current_hint_penalty)
            self.total_score += question_score
            self.score_label.configure(text=f"Score: {self.total_score}")

            messagebox.showinfo("Correct!",
                                f"Well done!\nYou scored {question_score} points.")
        else:
            messagebox.showinfo("Incorrect",
                                f"Incorrect.\nThe correct answer was: {self.current_question['name']}")

        self.next_question()

    # ==========================
    # Finish Game and Save
    # ==========================
    def finish_game(self):
        self.cancel_timer()

        summary_data = {
            "player_name": self.player_name,
            "score": self.total_score,
            "correct_answers": self.correct_count,
            "questions_attempted": self.attempted_count,
            "total_questions": self.total_questions,
            "hints_used": self.hints_used,
            "categories": self.selected_categories,
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # CHAMPION CHECK
        # =====================
        try:
            with open("data/champion.json", "r") as f:
                champion = json.load(f)

            # Auto-repair if champion is not a dict (e.g. list or invalid)
            if not isinstance(champion, dict):
                champion = {"score": 0}

        except (json.JSONDecodeError, FileNotFoundError):
            champion = {"score": 0}  # default champion

        # Compare with current champion
        if self.total_score > champion.get("score", 0):
            new_champion = {
                "champion_name": self.player_name,
                "score": self.total_score,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "categories": self.selected_categories,
                "correct_answers": self.correct_count,
                "total_questions": self.total_questions,
                "hints_used": self.hints_used
            }

            # Save new champion
            with open("data/champion.json", "w") as f:
                json.dump(new_champion, f, indent=4)

            messagebox.showinfo(
                "New Champion!",
                "🎉 Congratulations! You are the new champion!"
            )


        # =====================
        # SAVE GAME SESSION HISTORY
        # =====================
        try:
            with open("data/players.json", "r") as f:
                players = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            players = []  # auto-repair

        players.append(summary_data)

        with open("data/players.json", "w") as f:
            json.dump(players, f, indent=4)

        # =====================
        # Show Summary Screen
        # =====================
        self.master.show_summary(summary_data)

