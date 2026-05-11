import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project To-Do List Sekolah")
        self.root.geometry("900x580")
        self.root.configure(bg="#ffffff")

        self.file_data = "tugas_sekolah_data.json"
        self.tugas_list = self.muat_data()

        self.color_sidebar = "#2C3E50"
        self.color_accent = "#3498DB"
        self.color_bg = "#ECF0F1"
        self.color_success = "#27AE60"
        self.color_danger = "#E74C3C"

        # SIDEBAR
        self.sidebar = tk.Frame(root, bg=self.color_sidebar, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="INPUT TUGAS", fg="white", bg=self.color_sidebar, font=("Verdana", 14, "bold")).pack(pady=(30, 20))
        tk.Label(self.sidebar, text="Nama Tugas:", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_judul = tk.Entry(self.sidebar, font=("Arial", 11), bd=0)
        self.ent_judul.pack(padx=20, pady=(5, 15), fill="x")

        tk.Label(self.sidebar, text="Detail / Catatan:", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_detail = tk.Entry(self.sidebar, font=("Arial", 11), bd=0)
        self.ent_detail.pack(padx=20, pady=(5, 15), fill="x")

        tk.Label(self.sidebar, text="Deadline (YYYY-MM-DD):", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_deadline = tk.Entry(self.sidebar, font=("Arial", 11), bd=0)
        self.ent_deadline.pack(padx=20, pady=(5, 5), fill="x")
        
        self.btn_tambah = tk.Button(self.sidebar, text=" SIMPAN TUGAS + ", command=self.tambah_tugas, bg=self.color_success, fg="white", font=("Arial", 10, "bold"), bd=0, cursor="hand2", pady=10)
        self.btn_tambah.pack(padx=20, pady=25, fill="x")

        # MAIN AREA
        self.main_area = tk.Frame(root, bg=self.color_bg)
        self.main_area.pack(side="right", fill="both", expand=True)

        self.header_frame = tk.Frame(self.main_area, bg="white", height=70)
        self.header_frame.pack(fill="x")
        tk.Label(self.header_frame, text="Daftar Tugas & Deadline Saya", font=("Verdana", 16), bg="white", fg="#2C3E50").pack(side="left", padx=20, pady=20)

        self.table_frame = tk.Frame(self.main_area, bg=self.color_bg, padx=20, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=("Arial", 10))
        
        self.tree = ttk.Treeview(self.table_frame, columns=("judul", "detail", "deadline", "status"), show="headings")
        self.tree.heading("judul", text="Tugas"); self.tree.heading("detail", text="Detail"); self.tree.heading("deadline", text="Deadline"); self.tree.heading("status", text="Status Urgensi")
        self.tree.column("judul", width=150); self.tree.column("detail", width=200); self.tree.column("deadline", width=100, anchor="center"); self.tree.column("status", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.action_frame = tk.Frame(self.main_area, bg=self.color_bg)
        self.action_frame.pack(fill="x", padx=20, pady=20)

        self.btn_selesai = tk.Button(self.action_frame, text=" Tandai Selesai ✅ ", command=self.tandai_selesai, bg=self.color_accent, fg="white", bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2")
        self.btn_selesai.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(self.action_frame, text=" Hapus Tugas 🗑️ ", command=self.hapus_tugas, bg=self.color_danger, fg="white", bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2")
        self.btn_hapus.pack(side="right", padx=5)

        self.tampilkan_data()
        self.root.after(1000, self.cek_reminder) # Ini yang menjalankan reminder saat buka

    def muat_data(self):
        if os.path.exists(self.file_data):
            try:
                with open(self.file_data, 'r') as file:
                    return json.load(file)
            except: return []
        return []

    def simpan_data(self):
        with open(self.file_data, 'w') as file:
            json.dump(self.tugas_list, file, indent=4)

    def tambah_tugas(self):
        judul = self.ent_judul.get(); detail = self.ent_detail.get(); deadline = self.ent_deadline.get()
        if not judul or not deadline:
            messagebox.showwarning("Input Kosong", "Isi Nama Tugas dan Deadline ya!")
            return
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
            self.tugas_list.append({"judul": judul, "detail": detail, "deadline": deadline, "selesai": False})
            self.simpan_data(); self.tampilkan_data()
            self.ent_judul.delete(0, tk.END); self.ent_detail.delete(0, tk.END); self.ent_deadline.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Format tanggal: YYYY-MM-DD")

    def tandai_selesai(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Tugas", "Klik dulu tugas yang sudah selesai!")
            return
        index = self.tree.index(selected)
        self.tugas_list[index]["selesai"] = True
        self.simpan_data(); self.tampilkan_data()

    def hapus_tugas(self):
        selected = self.tree.selection()
        if not selected: return
        if messagebox.askyesno("Hapus", "Yakin ingin menghapus tugas ini?"):
            index = self.tree.index(selected); del self.tugas_list[index]
            self.simpan_data(); self.tampilkan_data()

    def tampilkan_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        hari_ini = datetime.now().date()
        for t in self.tugas_list:
            if t.get("selesai"): status = "✅ SELESAI"
            else:
                deadline_tgl = datetime.strptime(t['deadline'], "%Y-%m-%d").date()
                selisih = (deadline_tgl - hari_ini).days
                if selisih < 0: status = "❌ Terlewat"
                elif selisih <= 3: status = f"⚠️ {selisih} Hari Lagi!"
                else: status = f"⏳ {selisih} Hari"
            self.tree.insert("", tk.END, values=(t['judul'], t['detail'], t['deadline'], status))

    def cek_reminder(self):
        hari_ini = datetime.now().date()
        daftar_mendesak = []
        for t in self.tugas_list:
            if not t.get("selesai", False):
                deadline_tgl = datetime.strptime(t['deadline'], "%Y-%m-%d").date()
                selisih = (deadline_tgl - hari_ini).days
                if 0 <= selisih <= 3:
                    daftar_mendesak.append(f"• {t['judul']} (Deadline: {t['deadline']} - {selisih} hari lagi)")
        if daftar_mendesak:
            messagebox.showwarning("REMINDER DEADLINE", "TUGAS BERIKUT HARUS SEGERA DIKERJAKAN:\n\n" + "\n".join(daftar_mendesak))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTodoApp(root)
    root.mainloop()
