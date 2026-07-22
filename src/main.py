import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import uuid
import calendar
from datetime import datetime, date
from PIL import Image, ImageTk  # pip install pillow
import sys


def resource_path(relative_path):
    """This part helps to find the correct path for resources when using PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

BASE_DIR = resource_path("")
if hasattr(sys, '_MEIPASS'):
    # Τρέχει ως .exe — αποθήκευση δίπλα στο εκτελέσιμο
    DATA_DIR = os.path.join(os.path.dirname(sys.executable), "data")
else:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")

# ── Μορφή ημερομηνίας: ΗΗ-ΜΜ παντού (χωρίς έτος στο UI) ──────────────────
DATE_FORMAT = "%d/%m"   
CURRENT_YEAR = datetime.now().year

# customize the months accordingly to your prefered language
GREEK_MONTHS = [
    "", "Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος",
    "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος",
    "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"
]

# Colors ──────────────────────────────────────────────────────────────────
CLR_BG        = "#F0F4F8"
CLR_PANEL     = "#FFFFFF"
CLR_HEADER    = "#1A3C5E"
CLR_ACCENT    = "#2980B9"
CLR_RESERVED  = "#E74C3C"
CLR_FREE      = "#27AE60"
CLR_TODAY     = "#F39C12"
CLR_TEXT      = "#2C3E50"
CLR_MUTED     = "#7F8C8D"
CLR_BORDER    = "#D5E0EC"

ROOM_COLORS = {
    "Τετράκλινο": "#8E44AD",
    "Τρίκλινο":   "#16A085",
    "Δίκλινο":    "#2980B9",
}

# ── JSON helpers ────────────────────────────────────────────────────────────
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ── Ημερομηνίες ────────────────────────────────────────────────────────────
def parse_date(text: str) -> date:
    """ΗΗ-ΜΜ → date (τρέχον έτος)"""
    d, m = map(int, text.strip().split("/"))
    return date(CURRENT_YEAR, m, d)

def fmt(d: date) -> str:
    """date → ΗΗ-ΜΜ"""
    return d.strftime(DATE_FORMAT)

def date_from_storage(s: str) -> date:
    """ΕΕΕΕ-ΜΜ-ΗΗ → date  (JSON αποθηκεύεται πλήρως για σωστή σύγκριση)"""
    return datetime.strptime(s, "%Y-%m-%d").date()

def to_storage(d: date) -> str:
    return d.strftime("%Y-%m-%d")

def dates_overlap(s1, e1, s2, e2):
    return s1 < e2 and e1 > s2

def validate_contact(contact: str) -> bool:
    return 0 <= len(contact.strip()) <= 100


# ══════════════════════════════════════════════════════════════════════════
class XeniosApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Xenios · Version_1.0")

        # Icon title bar (.ico)
        ico_path = os.path.join(BASE_DIR, "logo.ico")
        if os.path.exists(ico_path):
            self.root.iconbitmap(ico_path)

        # Logo header (.png)
        png_path = os.path.join(BASE_DIR, "logo.png")
        if os.path.exists(png_path):
            img = Image.open(png_path).resize((38, 38), Image.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(img)  # αποθήκευση σε self για να μην το κάνει garbage collect

        self.root.configure(bg=CLR_BG)
        self.root.minsize(1000, 680)

        self.rooms        = load_json(ROOMS_FILE)
        self.reservations = load_json(RESERVATIONS_FILE)

        # Ημερολόγιο: τρέχων μήνας
        today = date.today()
        self.cal_month = today.month
        self.cal_year  = today.year

        self._build_ui()
        self._refresh_calendar()

        # Auto-fit: μετρά τι χρειάζεται και ανοίγει εκεί
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # Κεντράρισμα στην οθόνη
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI skeleton ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Κεφαλίδα
        hdr = tk.Frame(self.root, bg=CLR_HEADER, height=54)
        hdr.pack(fill="x")
        if hasattr(self, '_logo_img'):
            tk.Label(hdr, image=self._logo_img, bg=CLR_HEADER).pack(side="left", padx=(16, 6), pady=8)
        tk.Label(hdr, text="XENIOS", bg=CLR_HEADER, fg="white",
                font=("Playwrite New Zealand", 18, "bold")).pack(side="left", padx=(0, 20), pady=12)
        tk.Label(hdr, text="CUSTOM RESERVATION SOLUTIONS", bg=CLR_HEADER,
                 fg="#A8C6E0", font=("Helvetica", 10)).pack(side="left", pady=14)

        # GitHub link 
        import webbrowser
        gh_lbl = tk.Label(hdr, text="🌐  GitHub Repository", bg=CLR_HEADER,
                          fg="#ECF011", font=("Helvetica", 9, "underline"),
                          cursor="hand2")
        gh_lbl.pack(side="right", padx=20, pady=14)
        gh_lbl.bind("<Button-1>",
                    lambda e: webbrowser.open("https://github.com/VasilisOuzas/Xenios"))
        gh_lbl.bind("<Enter>", lambda e: gh_lbl.config(fg="white"))
        gh_lbl.bind("<Leave>", lambda e: gh_lbl.config(fg="#ECF011"))

        # Notebook: Ημερολόγιο / Κράτηση / Διαθεσιμότητα
        style = ttk.Style()
        style.configure("TNotebook", background=CLR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"),
                        padding=[14, 6], background=CLR_BG)
        style.map("TNotebook.Tab", background=[("selected", CLR_PANEL)])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        self.tab_cal  = tk.Frame(self.notebook, bg=CLR_BG)
        self.tab_form = tk.Frame(self.notebook, bg=CLR_BG)
        self.tab_avail = tk.Frame(self.notebook, bg=CLR_BG)

        self.notebook.add(self.tab_cal,   text="📅  Ημερολόγιο")
        self.notebook.add(self.tab_form,  text="➕  Νέα Κράτηση")
        self.notebook.add(self.tab_avail, text="🔍  Διαθεσιμότητα")

        self._build_calendar_tab()
        self._build_form_tab()
        self._build_avail_tab()

    # ══════════════════════════════════════════════════════════════════════
    # TAB 1 · Calendar - Matrix
    # ══════════════════════════════════════════════════════════════════════
    def _build_calendar_tab(self):
        top = tk.Frame(self.tab_cal, bg=CLR_BG)
        top.pack(fill="x", padx=10, pady=6)

        btn_style = dict(bg=CLR_HEADER, fg="white",
                         font=("Helvetica", 11, "bold"),
                         relief="flat", cursor="hand2", padx=8)

        tk.Button(top, text="◀", command=self._prev_month, **btn_style).pack(side="left")
        self.month_label = tk.Label(top, text="", bg=CLR_BG,
                                    fg=CLR_HEADER, font=("Helvetica", 14, "bold"))
        self.month_label.pack(side="left", padx=14)
        tk.Button(top, text="▶", command=self._next_month, **btn_style).pack(side="left")

        # Υπόμνημα τύπων δωματίων
        legend = tk.Frame(top, bg=CLR_BG)
        legend.pack(side="right", padx=6)
        for rtype, color in ROOM_COLORS.items():
            dot = tk.Label(legend, text="■", fg=color, bg=CLR_BG, font=("Helvetica", 12))
            dot.pack(side="left")
            tk.Label(legend, text=rtype, bg=CLR_BG,
                     fg=CLR_TEXT, font=("Helvetica", 9)).pack(side="left", padx=(0, 8))

        # Canvas για ημερολόγιο (scrollable οριζόντια + κατακόρυφα)
        frame = tk.Frame(self.tab_cal, bg=CLR_BG)
        frame.pack(fill="both", expand=True, padx=10, pady=4)

        self.cal_canvas = tk.Canvas(frame, bg=CLR_PANEL,
                                    highlightthickness=1,
                                    highlightbackground=CLR_BORDER)

        sb_x = ttk.Scrollbar(frame, orient="horizontal",
                              command=self.cal_canvas.xview)
        sb_y = ttk.Scrollbar(frame, orient="vertical",
                              command=self.cal_canvas.yview)
        self.cal_canvas.configure(xscrollcommand=sb_x.set,
                                  yscrollcommand=sb_y.set)

        sb_x.pack(side="bottom", fill="x")
        sb_y.pack(side="right",  fill="y")
        self.cal_canvas.pack(fill="both", expand=True)

        # Mouse wheel για κατακόρυφο scroll
        self.cal_canvas.bind("<MouseWheel>",
            lambda e: self.cal_canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.cal_canvas.bind("<Shift-MouseWheel>",
            lambda e: self.cal_canvas.xview_scroll(-1*(e.delta//120), "units"))

        # Tooltip
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip.configure(bg=CLR_HEADER)
        self.tip_lbl = tk.Label(self.tooltip, bg=CLR_HEADER, fg="white",
                                font=("Helvetica", 9), padx=8, pady=4)
        self.tip_lbl.pack()

    def _prev_month(self):
        self.cal_month -= 1
        if self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1
        self._refresh_calendar()

    def _next_month(self):
        self.cal_month += 1
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        self._refresh_calendar()

    def _refresh_calendar(self):
        c = self.cal_canvas
        c.delete("all")

        year, month = self.cal_year, self.cal_month
        self.month_label.config(
            text=f"{GREEK_MONTHS[month]}  {year}")

        days_in_month = calendar.monthrange(year, month)[1]
        today = date.today()

        # Cell Dimentions 
        DAY_W   = 36   # width of day column
        ROW_H   = 34   # height of room row
        HDR_H   = 38   # height of day header
        LABEL_W = 110  # width of left room column

        total_w = LABEL_W + days_in_month * DAY_W + 4
        total_h = HDR_H + len(self.rooms) * ROW_H + 4
        c.configure(scrollregion=(0, 0, total_w, total_h))

        # ── Day Headlines ─────────────────────────────────────────────
        for d in range(1, days_in_month + 1):
            x = LABEL_W + (d - 1) * DAY_W
            day_obj = date(year, month, d)
            is_today = (day_obj == today)

            bg = CLR_TODAY if is_today else CLR_HEADER
            c.create_rectangle(x, 0, x + DAY_W, HDR_H, fill=bg, outline="")
            c.create_text(x + DAY_W / 2, HDR_H / 2,
                          text=str(d), fill="white",
                          font=("Helvetica", 9, "bold" if is_today else "normal"))

        # Γωνία
        c.create_rectangle(0, 0, LABEL_W, HDR_H, fill=CLR_HEADER, outline="")
        c.create_text(LABEL_W / 2, HDR_H / 2, text="Δωμάτιο",
                      fill="white", font=("Helvetica", 9, "bold"))

        # ── Room rows ────────────────────────────────────────────
        # Συγκεντρώνω κρατήσεις ανά δωμάτιο για τον τρέχοντα μήνα
        res_by_room: dict[str, list] = {r["id"]: [] for r in self.rooms}
        for res in self.reservations:
            rid = res["room_id"]
            if rid in res_by_room:
                res_by_room[rid].append(res)

        for row_idx, room in enumerate(self.rooms):
            y0 = HDR_H + row_idx * ROW_H
            y1 = y0 + ROW_H
            stripe = "#F7FAFD" if row_idx % 2 == 0 else CLR_PANEL

            # Φόντο γραμμής
            c.create_rectangle(0, y0, total_w, y1, fill=stripe, outline="")

            # Ετικέτα δωματίου
            rtype = room.get("type", "")
            rcolor = ROOM_COLORS.get(rtype, CLR_ACCENT)
            c.create_rectangle(0, y0, LABEL_W, y1, fill=rcolor, outline="")
            c.create_text(8, (y0 + y1) / 2,
                          text=f"  {room['number']}  {rtype.upper()}",
                          fill="white", font=("Helvetica", 8, "bold"),
                          anchor="w")

            # Κελιά ημερών
            for d in range(1, days_in_month + 1):
                x0 = LABEL_W + (d - 1) * DAY_W
                x1 = x0 + DAY_W
                # λεπτή διαχωριστική γραμμή
                c.create_line(x0, y0, x0, y1, fill=CLR_BORDER)

            # Οριζόντια γραμμή κάτω
            c.create_line(0, y1, total_w, y1, fill=CLR_BORDER)

            # Κρατήσεις ως χρωματιστές ταινίες
            for res in res_by_room[room["id"]]:
                try:
                    r_start = date_from_storage(res["checkin"])
                    r_end   = date_from_storage(res["checkout"])
                except Exception:
                    continue

                month_start = date(year, month, 1)
                month_end   = date(year, month, days_in_month)

                if r_end <= month_start or r_start > month_end:
                    continue

                clip_start = max(r_start, month_start)
                # clip_end: δεν ξεπερνά τη μέρα days_in_month+1 του μήνα
                month_after = date(year + (month // 12), (month % 12) + 1, 1)
                clip_end    = min(r_end, month_after)

                if clip_start >= clip_end:
                    continue

                bx0 = LABEL_W + (clip_start.day - 1) * DAY_W + 2
                # Αν clip_end είναι η 1η του επόμενου μήνα → εμφανίζεται μέχρι τέλος μήνα
                end_day = days_in_month if clip_end >= month_after else clip_end.day - 1
                end_day = max(end_day, clip_start.day)  # τουλάχιστον 1 μέρα
                bx1 = LABEL_W + end_day * DAY_W - 2
                by0, by1 = y0 + 5, y1 - 5

                tag = f"res_{res['id']}"
                rtype = room.get("type", "")
                bar_color = ROOM_COLORS.get(rtype, CLR_RESERVED)
                c.create_rectangle(bx0, by0, bx1, by1,
                                   fill=bar_color, outline="",
                                   tags=(tag,))
                # Κεντράρω το όνομα μέσα στην ταινία
                mid_x = (bx0 + bx1) / 2
                bar_width = bx1 - bx0
                suffix = ""
                if res.get("extra_bed"):  suffix += " 🛏️"
                if res.get("baby_cot"):   suffix += " 👶"

                full_name = res["name"] + suffix
                short_name = res["name"].split()[0][:10] + suffix

                # Εκτίμηση πλάτους κειμένου: ~6.5px ανά χαρακτήρα για Helvetica 8
                CHAR_WIDTH = 6.5
                display_name = full_name if len(full_name) * CHAR_WIDTH < bar_width - 8 else short_name

                c.create_text(mid_x, (by0 + by1) / 2,
                            text=display_name, fill="white",
                            font=("Helvetica", 8, "bold"),
                            tags=(tag,))

                # Tooltip
                extras_tip = []
                if res.get("extra_bed"): extras_tip.append("🛏️ Έξτρα ράντζο")
                if res.get("baby_cot"):  extras_tip.append("👶 Παρκοκρέβατο")
                extras_line = ("  |  " + "  ".join(extras_tip)) if extras_tip else ""
                tip_text = (f"{res['name']}  | Επικοινωνία: {res['contact']}{extras_line}\n"
                            f"Άφιξη: {fmt(r_start)}  Αναχ: {fmt(r_end)}\n"
                            f"Τιμή ανά βράδυ: {res.get('price_per_night', '—')}€")
                c.tag_bind(tag, "<Enter>",
                           lambda e, t=tip_text: self._show_tip(e, t))
                c.tag_bind(tag, "<Leave>", self._hide_tip)

    def _show_tip(self, event, text):
        self.tip_lbl.config(text=text)
        self.tooltip.geometry(f"+{event.x_root + 12}+{event.y_root + 8}")
        self.tooltip.deiconify()

    def _hide_tip(self, _event=None):
        self.tooltip.withdraw()

    # ══════════════════════════════════════════════════════════════════════
    # TAB 2 · Φόρμα κράτησης
    # ══════════════════════════════════════════════════════════════════════
    def _build_form_tab(self):
        wrap = tk.Frame(self.tab_form, bg=CLR_BG)
        wrap.pack(expand=True)

        card = tk.Frame(wrap, bg=CLR_PANEL, bd=0,
                        highlightthickness=1, highlightbackground=CLR_BORDER)
        card.pack(padx=40, pady=30, ipadx=20, ipady=20)

        tk.Label(card, text="Νέα Κράτηση", bg=CLR_PANEL,
                 fg=CLR_HEADER, font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, columnspan=4, pady=(0, 16), sticky="w")

        def lbl(text): return tk.Label(card, text=text, bg=CLR_PANEL,
                                       fg=CLR_TEXT, font=("Helvetica", 10))
        def entry(w=22): return tk.Entry(card, width=w,
                                         font=("Helvetica", 10),
                                         relief="solid", bd=1)

        # Γραμμή 1: Όνομα · Τηλέφωνο
        lbl("Ονοματεπώνυμο").grid(row=1, column=0, sticky="e", padx=(0, 6), pady=5)
        self.f_name = entry()
        self.f_name.grid(row=1, column=1, padx=(0, 20))

        lbl("Στοιχεία Επικοινωνίας").grid(row=1, column=2, sticky="e", padx=(0, 6))
        self.f_contact = entry(24)
        self.f_contact.grid(row=1, column=3)

        # Γραμμή 2: Δωμάτιο · Τιμή/βράδυ
        lbl("Δωμάτιο").grid(row=2, column=0, sticky="e", padx=(0, 6), pady=5)
        room_names = [f"{r['number']} ({r.get('type','')})" for r in self.rooms]
        self.f_room = ttk.Combobox(card, values=room_names, width=20,
                                   state="readonly", font=("Helvetica", 10))
        self.f_room.grid(row=2, column=1, padx=(0, 20))

        lbl("Τιμή/βράδυ (€)").grid(row=2, column=2, sticky="e", padx=(0, 6))
        self.f_price = entry(10)
        self.f_price.grid(row=2, column=3)

        # Γραμμή 3: Άφιξη · Αναχώρηση
        lbl("Άφιξη (ΗΗ/ΜΜ)").grid(row=3, column=0, sticky="e", padx=(0, 6), pady=5)
        self.f_checkin = entry(12)
        self.f_checkin.grid(row=3, column=1, padx=(0, 20))

        lbl("Αναχώρηση (ΗΗ/ΜΜ)").grid(row=3, column=2, sticky="e", padx=(0, 6))
        self.f_checkout = entry(12)
        self.f_checkout.grid(row=3, column=3)

        # Γραμμή 4: Extras
        self.f_extra_bed = tk.BooleanVar(value=False)
        self.f_baby_cot  = tk.BooleanVar(value=False)

        extras_frame = tk.Frame(card, bg=CLR_PANEL)
        extras_frame.grid(row=4, column=0, columnspan=4, pady=(10, 0), sticky="w", padx=(60, 0))

        tk.Checkbutton(extras_frame, text="🛏️  Έξτρα ράντζο",
                       variable=self.f_extra_bed, bg=CLR_PANEL,
                       fg=CLR_TEXT, font=("Helvetica", 10),
                       activebackground=CLR_PANEL, cursor="hand2").pack(side="left", padx=(0, 30))

        tk.Checkbutton(extras_frame, text="👶  Παρκοκρέβατο",
                       variable=self.f_baby_cot, bg=CLR_PANEL,
                       fg=CLR_TEXT, font=("Helvetica", 10),
                       activebackground=CLR_PANEL, cursor="hand2").pack(side="left")

        # Κουμπιά
        btn_row = tk.Frame(card, bg=CLR_PANEL)
        btn_row.grid(row=5, column=0, columnspan=4, pady=(18, 4))

        tk.Button(btn_row, text="✔  Προσθήκη Κράτησης",
                  bg=CLR_FREE, fg="white", relief="flat",
                  font=("Helvetica", 11, "bold"), cursor="hand2",
                  padx=14, pady=6,
                  command=self._add_reservation).pack(side="left", padx=8)

        tk.Button(btn_row, text="✖  Διαγραφή Επιλεγμένης",
                  bg=CLR_RESERVED, fg="white", relief="flat",
                  font=("Helvetica", 11, "bold"), cursor="hand2",
                  padx=14, pady=6,
                  command=self._delete_reservation).pack(side="left", padx=8)

        tk.Button(btn_row, text="✏️  Επεξεργασία",
                  bg=CLR_TODAY, fg="white", relief="flat",
                  font=("Helvetica", 11, "bold"), cursor="hand2",
                  padx=14, pady=6,
                  command=self._load_for_edit).pack(side="left", padx=8)

        self.f_status = tk.Label(card, text="", bg=CLR_PANEL,
                                 fg=CLR_ACCENT, font=("Helvetica", 10, "italic"),
                                 wraplength=480)
        self.f_status.grid(row=6, column=0, columnspan=4, pady=(8, 0))

        # Λίστα κρατήσεων
        sep = tk.Frame(self.tab_form, bg=CLR_BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=4)

        cols = ("room", "type", "name", "contact", "checkin", "checkout", "nights", "total")
        col_lbl = {
            "room": "Δωμάτιο", "type": "Τύπος", "name": "Πελάτης",
            "contact": "Στοιχεία Επικοινωνίας", "checkin": "Άφιξη", "checkout": "Αναχώρηση",
            "nights": "Νύχτες", "total": "Σύνολο (€)"
        }
        col_w = {"room": 80, "type": 90, "name": 160, "contact": 110,
                 "checkin": 75, "checkout": 80, "nights": 60, "total": 90}

        tree_frame = tk.Frame(self.tab_form, bg=CLR_BG)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                 show="headings", height=10,
                                 selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col_lbl[col])
            self.tree.column(col, width=col_w[col], anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self._refresh_list()

    def _add_reservation(self):
        try:
            name  = self.f_name.get().strip()
            contact = self.f_contact.get().strip()
            price_txt = self.f_price.get().strip()
            room_sel  = self.f_room.current()

            if room_sel < 0 or not name or not contact or not price_txt:
                messagebox.showerror("Σφάλμα", "Συμπλήρωσε όλα τα πεδία.")
                return

            try:
                price_per_night = float(price_txt)
            except ValueError:
                messagebox.showerror("Σφάλμα", "Εισάγαγε έγκυρη τιμή (αριθμός).")
                return

            checkin  = parse_date(self.f_checkin.get())
            checkout = parse_date(self.f_checkout.get())

            if checkin >= checkout:
                messagebox.showerror("Σφάλμα", "Η αναχώρηση πρέπει να είναι μετά την άφιξη.")
                return

            selected_room = self.rooms[room_sel]

            # Έλεγχος διαθεσιμότητας για το συγκεκριμένο δωμάτιο
            for res in self.reservations:
                if res["room_id"] != selected_room["id"]:
                    continue
                r_s = date_from_storage(res["checkin"])
                r_e = date_from_storage(res["checkout"])
                if dates_overlap(checkin, checkout, r_s, r_e):
                    messagebox.showerror(
                        "Μη διαθέσιμο",
                        f"Το δωμάτιο {selected_room['number']} είναι ήδη κρατημένο "
                        f"για αυτήν την περίοδο\n({fmt(r_s)} – {fmt(r_e)})."
                    )
                    return

            nights      = (checkout - checkin).days
            total_price = round(nights * price_per_night, 2)

            new_res = {
                "id":             str(uuid.uuid4()),
                "room_id":        selected_room["id"],
                "name":           name,
                "contact":        contact,
                "checkin":        to_storage(checkin),
                "checkout":       to_storage(checkout),
                "price_per_night": price_per_night,
                "total_price":    total_price,
                "extra_bed":      self.f_extra_bed.get(),
                "baby_cot":       self.f_baby_cot.get(),
            }

            self.reservations.append(new_res)
            save_json(RESERVATIONS_FILE, self.reservations)
            self._refresh_list()
            self._refresh_calendar()

            self.f_status.config(
                fg=CLR_FREE,
                text=f"✔  Κράτηση για {name} στο δωμάτιο {selected_room['number']} "
                     f"({nights} νύχτες × {price_per_night}€ = {total_price}€)"
            )
            # Καθαρισμός πεδίων
            for w in (self.f_name, self.f_contact, self.f_price,
                      self.f_checkin, self.f_checkout):
                w.delete(0, "end")
            self.f_room.set("")
            self.f_extra_bed.set(False)
            self.f_baby_cot.set(False)

        except ValueError as e:
            messagebox.showerror("Σφάλμα", "Χρησιμοποίησε τη μορφή ΗΗ/ΜΜ για τις ημερομηνίες.")

    def _delete_reservation(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Προσοχή", "Επίλεξε μια κράτηση από τη λίστα.")
            return
        vals = self.tree.item(sel[0])["values"]
        if not messagebox.askyesno("Διαγραφή",
                                   f"Να διαγραφεί η κράτηση για {vals[2]} "
                                   f"(δωμ. {vals[0]});"):
            return

        # Αναγνώριση μέσω UUID που αποθηκεύεται στο tag του treeview item
        item_id = self.tree.item(sel[0], "tags")[0]

        self.reservations = [
            r for r in self.reservations
            if r["id"] != item_id
        ]
        save_json(RESERVATIONS_FILE, self.reservations)
        self._refresh_list()
        self._refresh_calendar()
        self.f_status.config(fg=CLR_RESERVED, text="✖  Η κράτηση διαγράφηκε.")

    def _refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for res in sorted(self.reservations, key=lambda r: r["name"].lower()):
            room = next((r for r in self.rooms if r["id"] == res["room_id"]), None)
            if not room:
                continue
            r_s = date_from_storage(res["checkin"])
            r_e = date_from_storage(res["checkout"])
            nights = (r_e - r_s).days
            self.tree.insert("", "end", tags=(res["id"],), values=(
                room["number"],
                room.get("type", ""),
                res["name"],
                res["contact"],
                fmt(r_s),
                fmt(r_e),
                nights,
                f"{res['total_price']}€"
            ))

    def _load_for_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Προσοχή", "Επίλεξε μια κράτηση από τη λίστα.")
            return

        # Βρίσκουμε την κράτηση μέσω UUID (tag)
        res_id = self.tree.item(sel[0], "tags")[0]
        res = next((r for r in self.reservations if r["id"] == res_id), None)
        if not res:
            return

        # Γέμισμα πεδίων με τα υπάρχοντα στοιχεία
        self.f_name.delete(0, "end")
        self.f_name.insert(0, res["name"])

        self.f_contact.delete(0, "end")
        self.f_contact.insert(0, res.get("contact", ""))

        self.f_price.delete(0, "end")
        self.f_price.insert(0, str(res.get("price_per_night", "")))

        self.f_checkin.delete(0, "end")
        self.f_checkin.insert(0, fmt(date_from_storage(res["checkin"])))

        self.f_checkout.delete(0, "end")
        self.f_checkout.insert(0, fmt(date_from_storage(res["checkout"])))

        # Δωμάτιο
        room = next((r for r in self.rooms if r["id"] == res["room_id"]), None)
        if room:
            room_names = [f"{r['number']} ({r.get('type','')})" for r in self.rooms]
            idx = next((i for i, r in enumerate(self.rooms) if r["id"] == res["room_id"]), 0)
            self.f_room.current(idx)

        # Checkboxes
        self.f_extra_bed.set(res.get("extra_bed", False))
        self.f_baby_cot.set(res.get("baby_cot", False))

        # Διαγραφή παλιάς εγγραφής και αποθήκευση UUID για ενημέρωση
        self._editing_id = res_id
        self.reservations = [r for r in self.reservations if r["id"] != res_id]
        save_json(RESERVATIONS_FILE, self.reservations)
        self._refresh_list()
        self._refresh_calendar()

        self.f_status.config(
            fg=CLR_TODAY,
            text=f"✏️  Επεξεργασία κράτησης για {res['name']} — τροποποίησε τα πεδία και πάτα «Προσθήκη»."
        )
        # Εστίαση στην καρτέλα φόρμας
        self.notebook.select(self.tab_form)

    # ══════════════════════════════════════════════════════════════════════
    # TAB 3 · Διαθεσιμότητα (χειροκίνητη + συνολική)
    # ══════════════════════════════════════════════════════════════════════
    def _build_avail_tab(self):
        wrap = tk.Frame(self.tab_avail, bg=CLR_BG)
        wrap.pack(expand=True)

        card = tk.Frame(wrap, bg=CLR_PANEL,
                        highlightthickness=1, highlightbackground=CLR_BORDER)
        card.pack(padx=40, pady=30, ipadx=20, ipady=20)

        tk.Label(card, text="Έλεγχος Διαθεσιμότητας", bg=CLR_PANEL,
                 fg=CLR_HEADER, font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, columnspan=4, pady=(0, 14), sticky="w")

        def lbl(text): return tk.Label(card, text=text, bg=CLR_PANEL,
                                       fg=CLR_TEXT, font=("Helvetica", 10))
        def entry(w=14): return tk.Entry(card, width=w,
                                          font=("Helvetica", 10),
                                          relief="solid", bd=1)

        lbl("Άφιξη (ΗΗ/ΜΜ)").grid(row=1, column=0, sticky="e", padx=(0, 6), pady=6)
        self.a_checkin = entry()
        self.a_checkin.grid(row=1, column=1, padx=(0, 20))

        lbl("Αναχώρηση (ΗΗ/ΜΜ)").grid(row=1, column=2, sticky="e", padx=(0, 6))
        self.a_checkout = entry()
        self.a_checkout.grid(row=1, column=3)

        lbl("Τύπος δωματίου").grid(row=2, column=0, sticky="e", padx=(0, 6), pady=6)
        self.a_type = ttk.Combobox(card, values=["Όλοι", "Τετράκλινο",
                                                  "Τρίκλινο", "Δίκλινο"],
                                   width=13, state="readonly",
                                   font=("Helvetica", 10))
        self.a_type.current(0)
        self.a_type.grid(row=2, column=1, padx=(0, 20))

        tk.Button(card, text="🔍  Αναζήτηση",
                  bg=CLR_ACCENT, fg="white", relief="flat",
                  font=("Helvetica", 11, "bold"), cursor="hand2",
                  padx=12, pady=5,
                  command=self._check_availability).grid(
            row=3, column=0, columnspan=4, pady=14)

        # Αποτελέσματα
        self.a_result_frame = tk.Frame(card, bg=CLR_PANEL)
        self.a_result_frame.grid(row=4, column=0, columnspan=4, sticky="ew")

    def _check_availability(self):
        for w in self.a_result_frame.winfo_children():
            w.destroy()

        try:
            checkin  = parse_date(self.a_checkin.get())
            checkout = parse_date(self.a_checkout.get())
        except ValueError:
            messagebox.showerror("Σφάλμα", "Χρησιμοποίησε τη μορφή ΗΗ/ΜΜ.")
            return

        if checkin >= checkout:
            messagebox.showerror("Σφάλμα", "Η αναχώρηση πρέπει να είναι μετά την άφιξη.")
            return

        filter_type = self.a_type.get()
        nights = (checkout - checkin).days

        # Υπολογισμός διαθεσιμότητας
        free_rooms     = []
        reserved_rooms = []

        for room in self.rooms:
            if filter_type != "Όλοι" and room.get("type") != filter_type:
                continue

            occupied = False
            for res in self.reservations:
                if res["room_id"] != room["id"]:
                    continue
                if dates_overlap(checkin, checkout,
                                 date_from_storage(res["checkin"]),
                                 date_from_storage(res["checkout"])):
                    occupied = True
                    break
            (reserved_rooms if occupied else free_rooms).append(room)

        # ── Συνοπτικό banner ────────────────────────────────────────────
        total = len(free_rooms) + len(reserved_rooms)
        banner = tk.Frame(self.a_result_frame, bg=CLR_FREE if free_rooms else CLR_RESERVED)
        banner.pack(fill="x", pady=(8, 12))
        tk.Label(
            banner,
            text=f"  {len(free_rooms)} από {total} δωμάτια διαθέσιμα  "
                 f"({nights} νύχτες, {fmt(checkin)} – {fmt(checkout)})",
            bg=CLR_FREE if free_rooms else CLR_RESERVED,
            fg="white", font=("Helvetica", 11, "bold")
        ).pack(pady=6)

        # Breakdown ανά τύπο
        if filter_type == "Όλοι":
            breakdown = tk.Frame(self.a_result_frame, bg=CLR_PANEL)
            breakdown.pack(fill="x", pady=(0, 10))
            for rtype, color in ROOM_COLORS.items():
                free_t = sum(1 for r in free_rooms if r.get("type") == rtype)
                total_t = sum(1 for r in self.rooms if r.get("type") == rtype)
                tk.Label(breakdown,
                         text=f"■  {rtype}: "
                              f"{free_t}/{total_t} διαθέσιμα",
                         fg=color, bg=CLR_PANEL,
                         font=("Helvetica", 10, "bold")).pack(
                    anchor="w", padx=14, pady=1)

        # Διαθέσιμα δωμάτια
        if free_rooms:
            tk.Label(self.a_result_frame, text="Διαθέσιμα δωμάτια:",
                     bg=CLR_PANEL, fg=CLR_FREE,
                     font=("Helvetica", 10, "bold")).pack(anchor="w", padx=14)
            grid = tk.Frame(self.a_result_frame, bg=CLR_PANEL)
            grid.pack(anchor="w", padx=20, pady=4)
            for i, room in enumerate(free_rooms):
                color = ROOM_COLORS.get(room.get("type", ""), CLR_ACCENT)
                tk.Label(grid, text=f"✔ {room['number']} ({room.get('type','')})",
                         bg=CLR_PANEL, fg=color,
                         font=("Helvetica", 10)).grid(
                    row=i // 5, column=i % 5, sticky="w", padx=10, pady=2)

        # Κρατημένα
        if reserved_rooms:
            tk.Label(self.a_result_frame, text="Κρατημένα:",
                     bg=CLR_PANEL, fg=CLR_RESERVED,
                     font=("Helvetica", 10, "bold")).pack(anchor="w", padx=14, pady=(8, 0))
            grid2 = tk.Frame(self.a_result_frame, bg=CLR_PANEL)
            grid2.pack(anchor="w", padx=20, pady=4)
            for i, room in enumerate(reserved_rooms):
                tk.Label(grid2, text=f"✖ {room['number']} ({room.get('type','')})",
                         bg=CLR_PANEL, fg=CLR_MUTED,
                         font=("Helvetica", 10)).grid(
                    row=i // 5, column=i % 5, sticky="w", padx=10, pady=2)


# ── Εκκίνηση ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = XeniosApp(root)
    root.mainloop()
