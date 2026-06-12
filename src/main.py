import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ROOMS_FILE = os.path.join(DATA_DIR, "rooms.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def str_to_date(date_text):
    return datetime.strptime(date_text, "%Y-%m-%d").date()


def dates_overlap(start1, end1, start2, end2):
    return start1 < end2 and end1 > start2


class XeniosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Xenios - Reservation Manager")
        self.root.geometry("900x600")

        self.rooms = load_json(ROOMS_FILE)
        self.reservations = load_json(RESERVATIONS_FILE)

        self.create_widgets()
        self.refresh_reservation_list()

    def create_widgets(self):
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Full Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Phone").grid(row=0, column=2)
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=0, column=3)

        tk.Label(form_frame, text="Room Type").grid(row=1, column=0)
        self.room_type_combo = ttk.Combobox(form_frame, values=["single", "double", "suite"])
        self.room_type_combo.grid(row=1, column=1)

        tk.Label(form_frame, text="Check-in YYYY-MM-DD").grid(row=1, column=2)
        self.checkin_entry = tk.Entry(form_frame)
        self.checkin_entry.grid(row=1, column=3)

        tk.Label(form_frame, text="Check-out YYYY-MM-DD").grid(row=2, column=0)
        self.checkout_entry = tk.Entry(form_frame)
        self.checkout_entry.grid(row=2, column=1)

        tk.Button(form_frame, text="Check Availability", command=self.check_availability).grid(row=3, column=0, pady=10)
        tk.Button(form_frame, text="Add Reservation", command=self.add_reservation).grid(row=3, column=1, pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        columns = ("room", "type", "name", "phone", "checkin", "checkout", "price")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

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

                old_checkin = str_to_date(reservation["checkin"])
                old_checkout = str_to_date(reservation["checkout"])

                if dates_overlap(checkin, checkout, old_checkin, old_checkout):
                    room_is_free = False
                    break

            if room_is_free:
                available.append(room)

        return available

    def check_availability(self):
        try:
            room_type = self.room_type_combo.get()
            checkin = str_to_date(self.checkin_entry.get())
            checkout = str_to_date(self.checkout_entry.get())

            if checkin >= checkout:
                messagebox.showerror("Error", "Check-out must be after check-in.")
                return

            available_rooms = self.get_available_rooms(room_type, checkin, checkout)

            if available_rooms:
                text = "Available rooms: " + ", ".join(room["number"] for room in available_rooms)
            else:
                text = "No available rooms for this period."

            self.result_label.config(text=text)

        except ValueError:
            messagebox.showerror("Error", "Use date format YYYY-MM-DD.")

    def add_reservation(self):
        try:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            room_type = self.room_type_combo.get()
            checkin = str_to_date(self.checkin_entry.get())
            checkout = str_to_date(self.checkout_entry.get())

            if not name or not phone or not room_type:
                messagebox.showerror("Error", "Fill all fields.")
                return

            available_rooms = self.get_available_rooms(room_type, checkin, checkout)

            if not available_rooms:
                messagebox.showerror("Error", "No available room for this period.")
                return

            selected_room = available_rooms[0]

            nights = (checkout - checkin).days
            total_price = nights * selected_room["price"]

            new_reservation = {
                "id": len(self.reservations) + 1,
                "room_id": selected_room["id"],
                "name": name,
                "phone": phone,
                "checkin": str(checkin),
                "checkout": str(checkout),
                "price_per_night": selected_room["price"],
                "total_price": total_price
            }

            self.reservations.append(new_reservation)
            save_json(RESERVATIONS_FILE, self.reservations)

            self.refresh_reservation_list()
            self.result_label.config(text=f"Reservation added in room {selected_room['number']}.")

        except ValueError:
            messagebox.showerror("Error", "Use date format YYYY-MM-DD.")

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
                reservation["checkin"],
                reservation["checkout"],
                reservation["total_price"]
            ))


root = tk.Tk()
app = XeniosApp(root)
root.mainloop()
