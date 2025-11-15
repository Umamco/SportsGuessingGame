import customtkinter as ctk
import json
import os


class PlayersHistoryPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        # ===============================
        # LOAD DATA
        # ===============================
        self.players_data = self.load_players()
        self.filtered_by_filters = self.players_data.copy()
        self.filtered_data = self.players_data.copy()

        # ===============================
        # PAGE TITLE
        # ===============================
        title = ctk.CTkLabel(
            self,
            text="📘 Players History",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="All game sessions played so far",
            font=("Arial", 15)
        )
        subtitle.pack(pady=(0, 10))

        # ======================================================
        # SEARCH BAR
        # ======================================================
        search_frame = ctk.CTkFrame(self, corner_radius=12)
        search_frame.pack(pady=5, padx=20, fill="x")

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=("Arial", 14, "bold")
        )
        search_label.pack(side="left", padx=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.apply_search)

        search_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="Player name, category, score, or date..."
        )
        search_entry.pack(side="left", padx=10, pady=10)
        search_entry.configure(textvariable=self.search_var)

        # ======================================================
        # SORT BAR + NAV BUTTONS (right side)
        # ======================================================
        sort_frame = ctk.CTkFrame(self, corner_radius=12)
        sort_frame.pack(pady=5, padx=20, fill="x")

        sort_label = ctk.CTkLabel(
            sort_frame,
            text="Sort By:",
            font=("Arial", 14, "bold")
        )
        sort_label.pack(side="left", padx=10)

        self.sort_var = ctk.StringVar(value="Most Recent")
        sort_options = ["Most Recent", "Highest Score", "Alphabetical (A–Z)"]

        sort_menu = ctk.CTkOptionMenu(
            sort_frame,
            values=sort_options,
            variable=self.sort_var,
            width=200,
            command=self.apply_sort
        )
        sort_menu.pack(side="left", padx=10, pady=10)

        # -----------------------------
        # Navigation Buttons (Right Side)
        # -----------------------------
        nav_frame = ctk.CTkFrame(sort_frame, fg_color="transparent")
        nav_frame.pack(side="right", padx=10)

        start_btn = ctk.CTkButton(
            nav_frame,
            text="🎮 Start Game",
            width=130,
            height=36,
            font=("Arial", 14, "bold"),
            command=self.master.show_registration
        )
        start_btn.pack(side="left", padx=5)

        home_btn = ctk.CTkButton(
            nav_frame,
            text="🏠 Home",
            width=110,
            height=36,
            font=("Arial", 14, "bold"),
            command=self.master.back_to_home
        )
        home_btn.pack(side="left", padx=5)

        # ======================================================
        # FILTER PANEL (Two Rows)
        # ======================================================
        filter_frame = ctk.CTkFrame(self, corner_radius=12)
        filter_frame.pack(pady=5, padx=20, fill="x")

        # ---------- Row 1 ----------
        row1 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)

        cat_label = ctk.CTkLabel(
            row1,
            text="Categories:",
            font=("Arial", 13, "bold")
        )
        cat_label.pack(side="left", padx=(0, 10))

        self.filter_tennis = ctk.BooleanVar(value=False)
        self.filter_premier = ctk.BooleanVar(value=False)
        self.filter_athletics = ctk.BooleanVar(value=False)

        cb_tennis = ctk.CTkCheckBox(
            row1,
            text="Tennis",
            variable=self.filter_tennis,
            font=("Arial", 12)
        )
        cb_tennis.pack(side="left", padx=5)

        cb_premier = ctk.CTkCheckBox(
            row1,
            text="Premier",
            variable=self.filter_premier,
            font=("Arial", 12)
        )
        cb_premier.pack(side="left", padx=5)

        cb_athletics = ctk.CTkCheckBox(
            row1,
            text="Athletics",
            variable=self.filter_athletics,
            font=("Arial", 12)
        )
        cb_athletics.pack(side="left", padx=5)

        hints_label = ctk.CTkLabel(
            row1,
            text="  Hints:",
            font=("Arial", 13, "bold")
        )
        hints_label.pack(side="left", padx=(20, 5))

        self.hints_filter_var = ctk.StringVar(value="Any")
        hints_options = ["Any", "No hints", "1–3 hints", "4+ hints"]

        hints_menu = ctk.CTkOptionMenu(
            row1,
            values=hints_options,
            variable=self.hints_filter_var,
            width=140
        )
        hints_menu.pack(side="left", padx=5)

        # ---------- Row 2 ----------
        row2 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)

        score_label = ctk.CTkLabel(
            row2,
            text="Score:",
            font=("Arial", 13, "bold")
        )
        score_label.pack(side="left", padx=(0, 5))

        self.score_min_var = ctk.StringVar(value="0")
        self.score_max_var = ctk.StringVar(value="9999")

        score_min_entry = ctk.CTkEntry(row2, width=60, textvariable=self.score_min_var)
        score_min_entry.pack(side="left")

        dash_label = ctk.CTkLabel(row2, text=" - ", font=("Arial", 13, "bold"))
        dash_label.pack(side="left")

        score_max_entry = ctk.CTkEntry(row2, width=60, textvariable=self.score_max_var)
        score_max_entry.pack(side="left", padx=(0, 10))

        date_label = ctk.CTkLabel(
            row2,
            text="Date(YMD):",
            font=("Arial", 13, "bold")
        )
        date_label.pack(side="left", padx=(10, 5))

        self.date_from_var = ctk.StringVar()
        self.date_to_var = ctk.StringVar()

        date_from_entry = ctk.CTkEntry(
            row2,
            width=90,
            textvariable=self.date_from_var,
            placeholder_text="From"
        )
        date_from_entry.pack(side="left")

        date_dash = ctk.CTkLabel(row2, text=" - ", font=("Arial", 13, "bold"))
        date_dash.pack(side="left")

        date_to_entry = ctk.CTkEntry(
            row2,
            width=90,
            textvariable=self.date_to_var,
            placeholder_text="To"
        )
        date_to_entry.pack(side="left", padx=(0, 10))

        apply_btn = ctk.CTkButton(
            row2,
            text="Apply Filters",
            width=100,
            command=self.apply_filters
        )
        apply_btn.pack(side="left", padx=(10, 5))

        reset_btn = ctk.CTkButton(
            row2,
            text="Reset Filters",
            width=120,
            fg_color="#555555",
            hover_color="#333333",
            command=self.reset_filters
        )
        reset_btn.pack(side="left", pady=3)

        # ======================================================
        # SCROLLABLE RESULTS LIST
        # ======================================================
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=400,
            corner_radius=15
        )
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.refresh_display(self.filtered_data)

    # ==================================================
    # LOAD DATA
    # ==================================================
    def load_players(self):
        if not os.path.exists("data/players.json"):
            return []
        try:
            with open("data/players.json", "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []

    # ==================================================
    # APPLY FILTERS
    # ==================================================
    def apply_filters(self):
        data = []

        cat_flags = {
            "tennis": self.filter_tennis.get(),
            "premier": self.filter_premier.get(),
            "athletics": self.filter_athletics.get()
        }
        any_cat_selected = any(cat_flags.values())

        try:
            min_score = int(self.score_min_var.get())
        except:
            min_score = 0

        try:
            max_score = int(self.score_max_var.get())
        except:
            max_score = 9999

        hints_mode = self.hints_filter_var.get()
        date_from = self.date_from_var.get().strip()
        date_to = self.date_to_var.get().strip()

        for record in self.players_data:

            if any_cat_selected:
                cats = record.get("categories", {})
                if not any(cats.get(k, False) for k, v in cat_flags.items() if v):
                    continue

            score = record.get("score", 0)
            if score < min_score or score > max_score:
                continue

            hints_used = record.get("hints_used", 0)
            if hints_mode == "No hints" and hints_used != 0:
                continue
            if hints_mode == "1–3 hints" and not (1 <= hints_used <= 3):
                continue
            if hints_mode == "4+ hints" and hints_used < 4:
                continue

            rec_date = record.get("date_time", "")[:10]

            if date_from and rec_date and rec_date < date_from:
                continue
            if date_to and rec_date and rec_date > date_to:
                continue

            data.append(record)

        self.filtered_by_filters = data
        self.apply_search()

    # ==================================================
    # RESET FILTERS
    # ==================================================
    def reset_filters(self):
        self.filter_tennis.set(False)
        self.filter_premier.set(False)
        self.filter_athletics.set(False)
        self.score_min_var.set("0")
        self.score_max_var.set("9999")
        self.hints_filter_var.set("Any")
        self.date_from_var.set("")
        self.date_to_var.set("")

        self.filtered_by_filters = self.players_data.copy()
        self.apply_search()

    # ==================================================
    # SEARCH
    # ==================================================
    def apply_search(self, *args):
        query = self.search_var.get().lower().strip()
        base = self.filtered_by_filters

        if not query:
            self.filtered_data = base.copy()
        else:
            self.filtered_data = [
                r for r in base
                if query in r.get("player_name", "").lower()
                or query in r.get("date_time", "").lower()
                or query in str(r.get("score", "")).lower()
                or query in " ".join(
                    k.lower() for k, v in r.get("categories", {}).items() if v
                )
            ]

        self.apply_sort(self.sort_var.get())

    # ==================================================
    # SORTING
    # ==================================================
    def apply_sort(self, choice):
        data = self.filtered_data

        if choice == "Most Recent":
            sorted_data = sorted(data, key=lambda x: x.get("date_time", ""), reverse=True)
        elif choice == "Highest Score":
            sorted_data = sorted(data, key=lambda x: x.get("score", 0), reverse=True)
        elif choice == "Alphabetical (A–Z)":
            sorted_data = sorted(data, key=lambda x: x.get("player_name", "").lower())
        else:
            sorted_data = data

        self.refresh_display(sorted_data)

    # ==================================================
    # REFRESH DISPLAY
    # ==================================================
    def refresh_display(self, data):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not data:
            empty = ctk.CTkLabel(
                self.scroll_frame,
                text="No results found.",
                font=("Arial", 16)
            )
            empty.pack(pady=20)
            return

        for record in data:
            self.display_record(self.scroll_frame, record)

    # ==================================================
    # DISPLAY INDIVIDUAL RECORD
    # ==================================================
    def display_record(self, parent, record: dict):
        block = ctk.CTkFrame(parent, corner_radius=12)
        block.pack(fill="x", padx=10, pady=8)

        title = ctk.CTkLabel(
            block,
            text=f"{record.get('player_name', 'Unknown')}  —  Score: {record.get('score', 0)}",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        title.pack(pady=(8, 0), padx=10, anchor="w")

        subline = ctk.CTkLabel(
            block,
            text=(
                f"Correct: {record.get('correct_answers', 0)} / {record.get('total_questions', 0)}     "
                f"Hints Used: {record.get('hints_used', 0)}"
            ),
            font=("Arial", 14),
            anchor="w"
        )
        subline.pack(pady=(2, 0), padx=10, anchor="w")

        cats = ", ".join(
            k.capitalize() for k, v in record.get("categories", {}).items() if v
        )
        cat_label = ctk.CTkLabel(
            block,
            text=f"Categories: {cats}",
            font=("Arial", 14),
            anchor="w"
        )
        cat_label.pack(pady=(2, 0), padx=10, anchor="w")

        date_label = ctk.CTkLabel(
            block,
            text=f"Played On: {record.get('date_time', 'Unknown')}",
            font=("Arial", 13),
            anchor="w"
        )
        date_label.pack(pady=(4, 10), padx=10, anchor="w")
