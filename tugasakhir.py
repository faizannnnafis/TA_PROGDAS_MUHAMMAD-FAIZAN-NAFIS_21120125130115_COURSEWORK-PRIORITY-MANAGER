import tkinter as tk
from tkinter import messagebox
from datetime import datetime

daftar_tugas = []

def sort_tugas_by_deadline(tugas_list):
    tugas_list.sort(key=lambda x: x[1])
    return tugas_list

def tambah_tugas(entry_nama, entry_deadline, entry_estimasi, listbox_tugas):
    nama = entry_nama.get()
    deadline_str = entry_deadline.get()
    estimasi_str = entry_estimasi.get()

    if not nama or not deadline_str or not estimasi_str:
        messagebox.showerror("Error", "Semua kolom harus diisi.")
        return

    try:
        estimasi_menit = int(estimasi_str)
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        
        tugas_baru = [nama, deadline, estimasi_menit]
        
        daftar_tugas.append(tugas_baru)
        
        entry_nama.delete(0, tk.END)
        entry_deadline.delete(0, tk.END)
        entry_estimasi.delete(0, tk.END)
        
        update_listbox(listbox_tugas)
        messagebox.showinfo("Success", f"Tugas '{nama}' berhasil ditambahkan.")

    except ValueError:
        messagebox.showerror("Error", "Format deadline (YYYY-MM-DD HH:MM) atau Estimasi (angka) salah.")

def selesaikan_tugas_terakhir(listbox_tugas):
    if not daftar_tugas:
        messagebox.showinfo("Info", "Tidak ada tugas dalam daftar (Stack kosong).")
        return

    tugas_selesai = daftar_tugas.pop()
    nama_selesai = tugas_selesai[0]
    
    update_listbox(listbox_tugas)
    messagebox.showinfo("Tugas Selesai", f"Tugas '{nama_selesai}' telah diselesaikan dan dihapus.")

def update_listbox(listbox_tugas):
    listbox_tugas.delete(0, tk.END)
    
    sorted_tugas = sort_tugas_by_deadline(daftar_tugas)

    for i, tugas in enumerate(sorted_tugas):
        nama, deadline, estimasi_menit = tugas[0], tugas[1], tugas[2]
        
        status = "⏳ Belum Selesai"
        warna = "SystemWindow"
        
        if datetime.now() > deadline:
            status = "🔴 TERLAMBAT!"
            warna = "red" 
        
        teks_tugas = (f"{i + 1}. {nama} | Deadline: {deadline.strftime('%Y-%m-%d %H:%M')} "
                      f"| Estimasi: {estimasi_menit} mnt | Status: {status}")
        
        listbox_tugas.insert(tk.END, teks_tugas)
        
        if warna == "red":
             listbox_tugas.itemconfig(tk.END, {'bg': 'red', 'fg': 'white'})

def setup_gui():
    root = tk.Tk()
    root.title("Aplikasi Pencatat Tugas GUI Dasar")
    
    frame_input = tk