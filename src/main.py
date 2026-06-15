import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")

DISPLAY_FORMAT = "%d-%m-%Y"   # Αυτό βλέπει ο χρήστης
STORAGE_FORMAT = "%Y-%m-%d"   # Αυτό αποθηκεύεται στο JSON


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def display_to_storage(date_text):
    """DD-MM-YYYY → YYYY-MM-DD (για αποθήκευση/σύγκριση)"""
    return datetime.strptime(date_text, DISPLAY_FORMAT).strftime(STORAGE_FORMAT)


def storage_to_display(date_text):
    """YYYY-MM-DD → DD-MM-YYYY (για εμφάνιση)"""
    return datetime.strptime(date_text, STORAGE_FORMAT).strftime(DISPLAY_FORMAT)


def str_to_date(date_text):
    """DD-MM-YYYY → date object"""
    return datetime.strptime(date_text, DISPLAY_FORMAT).date()


def storage_str_to_date(date_text):
    """YYYY-MM-DD → date object (για σύγκριση κρατήσεων από JSON)"""
    return datetime.strptime(date_text, STORAGE_FORMAT).date()


def dates_overlap(start1, end1, start2, end2):
    return start1 < end2 and end1 > start2


def validate_phone(phone):
    digits = phone.replace(" ", "").replace("-", "").replace("+", "")
    return digits.isdigit() and 8 <= len(digits) <= 15


class XeniosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xenios - Διαχείριση Κρατήσεων")
        self.root.geometry("960x620")

        self.rooms = load_json(ROOMS_FILE)
        self.reservations = load_json(RESERVATIONS_FILE)

        self.create_widgets()
        self.refresh_reservation_list()

    def create_widgets(self):
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Ονοματεπώνυμο").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.name_entry = tk.Entry(form_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Τηλέφωνο").grid(row=0, column=2, padx=5, sticky="e")
        self.phone_entry = tk.Entry(form_frame, width=16)
        self.phone_entry.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Τύπος Δωματίου").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.room_type_combo = ttk.Combobox(form_frame, values=["single", "double", "suite"], width=17, state="readonly")
        self.room_type_combo.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Άφιξη (ΗΗ-ΜΜ-ΕΕΕΕ)").grid(row=1, column=2, padx=5, sticky="e")
        self.checkin_entry = tk.Entry(form_frame, width=16)
        self.checkin_entry.grid(row=1, column=3, padx=5)

        tk.Label(form_frame, text="Αναχώρηση (ΗΗ-ΜΜ-ΕΕΕΕ)").grid(row=2, column=0, padx=5, pady=4, sticky="e")
        self.checkout_entry = tk.Entry(form_frame, width=16)
        self.checkout_entry.grid(row=2, column=1, padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=4)

        tk.Button(btn_frame, text="Έλεγχος Διαθεσιμότητας", command=self.check_availability).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Προσθήκη Κράτησης", command=self.add_reservation).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Διαγραφή Κράτησης", command=self.delete_reservation, fg="red").pack(side="left", padx=6)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 10))
        self.result_label.pack(pady=2)

        columns = ("room", "type", "name", "phone", "checkin", "checkout", "price")
        col_labels = {
            "room": "Δωμάτιο", "type": "Τύπος", "name": "Όνομα",
            "phone": "Τηλέφωνο", "checkin": "Άφιξη",
            "checkout": "Αναχώρηση", "price": "Σύνολο (€)"
        }

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col_labels[col])
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def get_available_rooms(self, room_type, checkin, checkout):
        available = []
        for room in self.rooms:
            if room["type"] != room_type:
                continue
            room_is_free = True
            for reservation in self.reservations:
                if reservation["room_id"] != room["id"]:
                    continue
                # Κρατήσεις στο JSON είναι YYYY-MM-DD
                old_checkin = storage_str_to_date(reservation["checkin"])
                old_checkout = storage_str_to_date(reservation["checkout"])
                if dates_overlap(checkin, checkout, old_checkin, old_checkout):
                    room_is_free = False
                    break
            if room_is_free:
                available.append(room)
        return available

    def check_availability(self):
        try:
            room_type = self.room_type_combo.get()
            checkin = str_to_date(self.checkin_entry.get().strip())
            checkout = str_to_date(self.checkout_entry.get().strip())

            if checkin >= checkout:
                messagebox.showerror("Σφάλμα", "Η αναχώρηση πρέπει να είναι μετά την άφιξη.")
                return

            available_rooms = self.get_available_rooms(room_type, checkin, checkout)

            if available_rooms:
                text = "Διαθέσιμα δωμάτια: " + ", ".join(r["number"] for r in available_rooms)
            else:
                text = "Δεν υπάρχουν διαθέσιμα δωμάτια για αυτήν την περίοδο."

            self.result_label.config(text=text)

        except ValueError:
            messagebox.showerror("Σφάλμα", "Χρησιμοποίησε τη μορφή ΗΗ-ΜΜ-ΕΕΕΕ.")

    def add_reservation(self):
        try:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            room_type = self.room_type_combo.get()
            checkin = str_to_date(self.checkin_entry.get().strip())
            checkout = str_to_date(self.checkout_entry.get().strip())

            if not name or not phone or not room_type:
                messagebox.showerror("Σφάλμα", "Συμπλήρωσε όλα τα πεδία.")
                return

            if not validate_phone(phone):
                messagebox.showerror("Σφάλμα", "Μη έγκυρος αριθμός τηλεφώνου.")
                return

            if checkin >= checkout:
                messagebox.showerror("Σφάλμα", "Η αναχώρηση πρέπει να είναι μετά την άφιξη.")
                return

            available_rooms = self.get_available_rooms(room_type, checkin, checkout)
            if not available_rooms:
                messagebox.showerror("Σφάλμα", "Δεν υπάρχει διαθέσιμο δωμάτιο.")
                return

            selected_room = available_rooms[0]
            nights = (checkout - checkin).days
            total_price = nights * selected_room["price"]

            new_reservation = {
                "id": str(uuid.uuid4()),          # ✅ UUID αντί για len()+1
                "room_id": selected_room["id"],
                "name": name,
                "phone": phone,
                "checkin": checkin.strftime(STORAGE_FORMAT),    # αποθήκευση YYYY-MM-DD
                "checkout": checkout.strftime(STORAGE_FORMAT),
                "price_per_night": selected_room["price"],
                "total_price": total_price
            }

            self.reservations.append(new_reservation)
            save_json(RESERVATIONS_FILE, self.reservations)
            self.refresh_reservation_list()
            self.result_label.config(text=f"✅ Κράτηση στο δωμάτιο {selected_room['number']} ({nights} διανυκτερεύσεις, {total_price}€).")

        except ValueError:
            messagebox.showerror("Σφάλμα", "Χρησιμοποίησε τη μορφή ΗΗ-ΜΜ-ΕΕΕΕ.")

    def delete_reservation(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επίλεξε μια κράτηση για διαγραφή.")
            return

        item = self.tree.item(selected[0])
        values = item["values"]
        # Αναγνώριση κράτησης με room number + name + checkin (display format)
        res_checkin_storage = datetime.strptime(values[4], DISPLAY_FORMAT).strftime(STORAGE_FORMAT)

        confirm = messagebox.askyesno("Διαγραφή", f"Να διαγραφεί η κράτηση για {values[2]} (δωμ. {values[0]});")
        if not confirm:
            return

        self.reservations = [
            r for r in self.reservations
            if not (
                next(rm for rm in self.rooms if rm["id"] == r["room_id"])["number"] == values[0]
                and r["name"] == values[2]
                and r["checkin"] == res_checkin_storage
            )
        ]

        save_json(RESERVATIONS_FILE, self.reservations)
        self.refresh_reservation_list()
        self.result_label.config(text="🗑️ Η κράτηση διαγράφηκε.")

    def refresh_reservation_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for reservation in self.reservations:
            room = next(r for r in self.rooms if r["id"] == reservation["room_id"])
            self.tree.insert("", "end", values=(
                room["number"],
                room["type"],
                reservation["name"],
                reservation["phone"],
                storage_to_display(reservation["checkin"]),     # ✅ DD-MM-YYYY στην εμφάνιση
                storage_to_display(reservation["checkout"]),
                f"{reservation['total_price']}€"
            ))


root = tk.Tk()
app = XeniosApp(root)
root.mainloop()
