import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "data_tugas.json"

class Tugas:
    def __init__(self, nama, deadline, estimasi_menit):
        self.nama = nama
        self.deadline = deadline
        self.estimasi = estimasi_menit

    def sisa_waktu_setelah_estimasi(self, now):
        total_sisa = self.deadline - now
        return total_sisa - timedelta(minutes=self.estimasi)

    def sampai_deadline(self, now):
        return self.deadline - now


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Coursework Priority Manager")
        self.root.geometry("950x600")
        self.root.configure(bg="#0A1F44")

        self.daftar_tugas = []
        self.filtered_tugas = None
        self.selected_key = None

        self.load_data()
        self.setup_ui()
        self.auto_update()

    def save_data(self):
        data = []
        for t in self.daftar_tugas:
            data.append({
                "nama": t.nama,
                "deadline": t.deadline.strftime("%Y-%m-%d %H:%M"),
                "estimasi": t.estimasi
            })
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                return

        for item in data:
            nama = item["nama"]
            deadline = datetime.strptime(item["deadline"], "%Y-%m-%d %H:%M")
            estimasi = item["estimasi"]
            self.daftar_tugas.append(Tugas(nama, deadline, estimasi))

    def setup_ui(self):

        label_style = {"bg": "#0A1F44", "fg": "white"}
        tk.Label(self.root, text="Coursework Priority Manager",
                 font=("Arial", 22, "bold"), **label_style).pack(pady=8)

        frame_input = tk.Frame(self.root, bg="#0A1F44")
        frame_input.pack(pady=8)

        tk.Label(frame_input, text="Nama Tugas:", font=("Arial", 14), **label_style).grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frame_input, font=("Arial", 14), width=40)
        self.ent_nama.grid(row=0, column=1, padx=10, pady=4)

        tk.Label(frame_input, text="Deadline (YYYY-MM-DD HH:MM):", font=("Arial", 14), **label_style).grid(row=1, column=0, sticky="w")
        self.ent_deadline = tk.Entry(frame_input, font=("Arial", 14), width=40)
        self.ent_deadline.grid(row=1, column=1, padx=10, pady=4)

        tk.Label(frame_input, text="Estimasi (menit):", font=("Arial", 14), **label_style).grid(row=2, column=0, sticky="w")
        self.ent_estimasi = tk.Entry(frame_input, font=("Arial", 14), width=40)
        self.ent_estimasi.grid(row=2, column=1, padx=10, pady=4)

        tk.Button(frame_input, text="Tambah Tugas", font=("Arial", 13), bg="red", fg="white",
                  command=self.tambah_tugas).grid(row=3, column=0, columnspan=2, pady=10)

        frame_list = tk.Frame(self.root, bg="#0A1F44")
        frame_list.pack(pady=6, padx=6, fill="both", expand=True)

        title_bar = tk.Frame(frame_list, bg="#0A1F44")
        title_bar.pack(fill="x")

        tk.Label(title_bar, text="Daftar Tugas", bg="#0A1F44", fg="white",
                 font=("Arial", 18, "bold")).pack(side="top")

        search_frame = tk.Frame(title_bar, bg="#0A1F44")
        search_frame.pack(side="right", padx=10)

        tk.Label(search_frame, text="Cari Tugas:", bg="#0A1F44", fg="white",
         font=("Arial", 14, "bold")).pack(side="left")

        self.ent_cari = tk.Entry(search_frame, width=20)
        self.ent_cari.pack(side="left", padx=5)

        tk.Button(search_frame, text="Cari", bg="orange", fg="black",
          font=("Arial", 12), padx=10, pady=3,
          command=self.cari_tugas).pack(side="left", padx=5)

        tk.Button(search_frame, text="Reset", bg="gray", fg="white",
          font=("Arial", 12), padx=10, pady=3,
          command=self.reset_cari).pack(side="left", padx=5)

        inner = tk.Frame(frame_list, bg="white")
        inner.pack(fill="both", expand=True, padx=10, pady=6)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", foreground="black", fieldbackground="white",
                        bordercolor="#777777", borderwidth=1, rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#0A1F44", foreground="white",
                        font=("Arial", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#0A1F44")])


        columns = ("nama", "countdown", "ket", "deadline", "estimasi")
        self.table = ttk.Treeview(inner, columns=columns, show="headings", height=15)
        self.table.pack(side="left", fill="both", expand=True)

        self.table.heading("nama", text="Nama Tugas")
        self.table.heading("countdown", text="Countdown")
        self.table.heading("ket", text="Keterangan")
        self.table.heading("deadline", text="Deadline")
        self.table.heading("estimasi", text="Estimasi")

        self.table.column("nama", width=200)
        self.table.column("countdown", width=120)
        self.table.column("ket", width=150)
        self.table.column("deadline", width=180)
        self.table.column("estimasi", width=120)

        scrollbar = tk.Scrollbar(inner, command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.config(yscrollcommand=scrollbar.set)

        self.table.tag_configure("late", background="red")
        self.table.tag_configure("urgent", background="orange")
        self.table.tag_configure("near", background="yellow")
        self.table.tag_configure("safe", background="white")

        self.table.bind("<Button-1>", self.toggle_select)

        tk.Frame(self.root, height=2, bg="#5A7494").pack(fill="x", padx=10, pady=(8, 0))

        btn_frame = tk.Frame(self.root, bg="#0A1F44")
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Tandai Tugas Selesai", font=("Arial", 13),
                  bg="green", fg="white", command=self.tandai_selesai).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Edit Tugas", font=("Arial", 13),
                  bg="blue", fg="white", command=self.edit_tugas).pack(side="left", padx=10)

        frame_summary = tk.Frame(self.root, bg="#0A1F44")
        frame_summary.pack(pady=(5, 10), fill="x", padx=10)

        summary_style = {"bg": "#0A1F44", "fg": "white", "font": ("Arial", 12)}
        tk.Label(frame_summary, text="Jumlah Tugas Saat Ini:", **summary_style).pack(side="left", padx=10)

        self.lbl_safe = tk.Label(frame_summary, text="Aman: 0", **summary_style)
        self.lbl_safe.pack(side="left", padx=10)

        self.lbl_near = tk.Label(frame_summary, text="Dekat: 0", **summary_style)
        self.lbl_near.pack(side="left", padx=10)

        self.lbl_urgent = tk.Label(frame_summary, text="Gawat: 0", **summary_style)
        self.lbl_urgent.pack(side="left", padx=10)

        self.lbl_late = tk.Label(frame_summary, text="Terlambat: 0", **summary_style)
        self.lbl_late.pack(side="left", padx=10)

    def cari_tugas(self):
        keyword = self.ent_cari.get().strip().lower()
        if keyword == "":
            return

        self.filtered_tugas = []
        for t in self.daftar_tugas:
            if keyword in t.nama.lower():
                self.filtered_tugas.append(t)

        self.update_listbox(filtered=True)

    def reset_cari(self):
        self.ent_cari.delete(0, tk.END)
        self.filtered_tugas = None
        self.update_listbox()

    def toggle_select(self, event):
        row = self.table.identify_row(event.y)
        if row == "":
            return "break"
        values = self.table.item(row, "values")
        if not values:
            return "break"

        key = (values[0], values[3])

        def apply_toggle():
            if self.selected_key == key:
                self.selected_key = None
                self.table.selection_remove(row)
            else:
                self.selected_key = key
                self.table.selection_set(row)

        self.root.after(1, apply_toggle)
        return "break"

    def tambah_tugas(self):
        nama = self.ent_nama.get().strip()
        dl = self.ent_deadline.get().strip()
        est = self.ent_estimasi.get().strip()

        if not nama or not dl or not est:
            messagebox.showerror("Error", "Semua data harus diisi")
            return

        try:
            deadline = datetime.strptime(dl, "%Y-%m-%d %H:%M")
            estimasi = int(est)
        except:
            messagebox.showerror("Error", "Format deadline atau estimasi salah")
            return

        tugas = Tugas(nama, deadline, estimasi)
        self.daftar_tugas.append(tugas)
        self.save_data()

        self.ent_nama.delete(0, tk.END)
        self.ent_deadline.delete(0, tk.END)
        self.ent_estimasi.delete(0, tk.END)

        self.update_listbox()
        messagebox.showinfo("Berhasil", "Tugas berhasil ditambahkan")

    def format_timedelta(self, td):
        if td.total_seconds() < 0:
            return "00h 00m 00s"
        total = int(td.total_seconds())
        days, rem = divmod(total, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)

        parts = []
        if days:
            parts.append(f"{days}d")
        parts.append(f"{hours:02d}h")
        parts.append(f"{minutes:02d}m")
        parts.append(f"{seconds:02d}s")

        return " ".join(parts)

    def sort_prioritas(self):
        now = datetime.now()

        def key_func(t):
            terlambat = now >= t.deadline
            sisa = t.sisa_waktu_setelah_estimasi(now).total_seconds()
            if sisa < 0:
                sisa = 0
            return (0 if terlambat else 1, sisa)

        self.daftar_tugas.sort(key=key_func)

    def update_listbox(self, filtered=False):
        previous_key = self.selected_key
        self.sort_prioritas()

        for r in self.table.get_children():
            self.table.delete(r)

        now = datetime.now()
        safe_count = near_count = urgent_count = late_count = 0

        source = self.filtered_tugas if filtered and self.filtered_tugas is not None else self.daftar_tugas

        for tugas in source:
            sisa_setelah = tugas.sisa_waktu_setelah_estimasi(now)
            sampai_dl = tugas.sampai_deadline(now)

            if now >= tugas.deadline:
                keterangan = "TERLAMBAT !!!"
                tag = "late"
                countdown = "00h 00m 00s"
                late_count += 1
            else:
                if sisa_setelah.total_seconds() < 0:
                    keterangan = "Gawat !!"
                    tag = "urgent"
                    urgent_count += 1
                elif sampai_dl <= timedelta(hours=24):
                    keterangan = "Deadline Sudah Dekat !"
                    tag = "near"
                    near_count += 1
                else:
                    keterangan = "Masih Aman"
                    tag = "safe"
                    safe_count += 1

                countdown = self.format_timedelta(sisa_setelah)

            key = (tugas.nama, tugas.deadline.strftime("%Y-%m-%d %H:%M"))

            row_id = self.table.insert(
                "",
                tk.END,
                values=(
                    tugas.nama,
                    countdown,
                    keterangan,
                    tugas.deadline.strftime("%Y-%m-%d %H:%M"),
                    f"{tugas.estimasi} menit"
                ),
                tags=(tag,)
            )

            if previous_key == key:
                self.table.selection_set(row_id)
                self.selected_key = key

        self.lbl_safe.config(text=f"Aman: {safe_count}")
        self.lbl_near.config(text=f"Dekat: {near_count}")
        self.lbl_urgent.config(text=f"Gawat: {urgent_count}")
        self.lbl_late.config(text=f"Terlambat: {late_count}")

    def auto_update(self):
        self.update_listbox(filtered=self.filtered_tugas is not None)
        self.root.after(1000, self.auto_update)

    def tandai_selesai(self):
        if not self.selected_key:
            messagebox.showinfo("Info", "Pilih tugas yang sudah selesai")
            return

        nama, deadline = self.selected_key

        for t in self.daftar_tugas:
            if t.nama == nama and t.deadline.strftime("%Y-%m-%d %H:%M") == deadline:
                self.daftar_tugas.remove(t)
                break

        self.save_data()
        self.selected_key = None
        self.update_listbox()

    def edit_tugas(self):
        if not self.selected_key:
            messagebox.showinfo("Info", "Pilih tugas yang ingin diedit")
            return

        nama, deadline = self.selected_key

        for t in self.daftar_tugas:
            if t.nama == nama and t.deadline.strftime("%Y-%m-%d %H:%M") == deadline:
                tugas_edit = t
                break

        popup = tk.Toplevel(self.root)
        popup.title("Edit Tugas")
        popup.geometry("350x250")
        popup.configure(bg="#0A1F44")

        tk.Label(popup, text="Nama Tugas:", fg="white", bg="#0A1F44").pack(pady=5)
        ent_nama = tk.Entry(popup)
        ent_nama.insert(0, tugas_edit.nama)
        ent_nama.pack()

        tk.Label(popup, text="Deadline (YYYY-MM-DD HH:MM):", fg="white", bg="#0A1F44").pack(pady=5)
        ent_deadline = tk.Entry(popup)
        ent_deadline.insert(0, tugas_edit.deadline.strftime("%Y-%m-%d %H:%M"))
        ent_deadline.pack()

        tk.Label(popup, text="Estimasi (menit):", fg="white", bg="#0A1F44").pack(pady=5)
        ent_estimasi = tk.Entry(popup)
        ent_estimasi.insert(0, tugas_edit.estimasi)
        ent_estimasi.pack()

        def simpan_edit():
            try:
                tugas_edit.nama = ent_nama.get().strip()
                tugas_edit.deadline = datetime.strptime(ent_deadline.get().strip(), "%Y-%m-%d %H:%M")
                tugas_edit.estimasi = int(ent_estimasi.get().strip())
            except:
                messagebox.showerror("Error", "Format data salah")
                return

            self.save_data()
            self.update_listbox()
            popup.destroy()

        tk.Button(popup, text="Simpan", bg="green", fg="white", command=simpan_edit).pack(pady=10)


root = tk.Tk()
app = App(root)
root.mainloop()
