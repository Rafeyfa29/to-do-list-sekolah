import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project To-Do List Sekolah - Pro Version")
        self.root.geometry("1000x650")
        self.root.configure(bg="#ffffff")

        self.file_data = "tugas_sekolah_data.json"
        self.tugas_list = self.muat_data()

        # Konfigurasi Warna
        self.color_sidebar = "#2C3E50"
        self.color_accent = "#3498DB"
        self.color_bg = "#ECF0F1"
        self.color_success = "#27AE60"
        self.color_danger = "#E74C3C"
        self.color_edit = "#F39C12"

        # --- SIDEBAR (INPUT) ---
        self.sidebar = tk.Frame(root, bg=self.color_sidebar, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="INPUT TUGAS", fg="white", bg=self.color_sidebar, font=("Verdana", 14, "bold")).pack(pady=(30, 20))
        
        tk.Label(self.sidebar, text="Nama Tugas:", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_judul = tk.Entry(self.sidebar, font=("Arial", 11), bd=0); self.ent_judul.pack(padx=20, pady=(5, 15), fill="x")

        tk.Label(self.sidebar, text="Detail / Catatan:", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_detail = tk.Entry(self.sidebar, font=("Arial", 11), bd=0); self.ent_detail.pack(padx=20, pady=(5, 15), fill="x")

        tk.Label(self.sidebar, text="Deadline (YYYY-MM-DD):", fg="#BDC3C7", bg=self.color_sidebar).pack(anchor="w", padx=20)
        self.ent_deadline = tk.Entry(self.sidebar, font=("Arial", 11), bd=0); self.ent_deadline.pack(padx=20, pady=(5, 5), fill="x")
        
        self.btn_tambah = tk.Button(self.sidebar, text=" SIMPAN TUGAS + ", command=self.tambah_tugas, bg=self.color_success, fg="white", font=("Arial", 10, "bold"), bd=0, cursor="hand2", pady=10)
        self.btn_tambah.pack(padx=20, pady=25, fill="x")

        # --- MAIN AREA ---
        self.main_area = tk.Frame(root, bg=self.color_bg)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Header Area
        self.header_frame = tk.Frame(self.main_area, bg="white", height=100)
        self.header_frame.pack(fill="x")
        
        tk.Label(self.header_frame, text="Daftar Tugas Saya", font=("Verdana", 20, "bold"), bg="white", fg="#2C3E50").pack(side="left", padx=20, pady=20)
        
        # Label Statistik
        self.lbl_stats = tk.Label(self.header_frame, text="", font=("Arial", 10, "bold"), bg="#D6DBDF", fg="#2C3E50", padx=15, pady=10)
        self.lbl_stats.pack(side="right", padx=20)

        # Tabel Area (BAGIAN YANG DIPERBAIKI)
        self.table_frame = tk.Frame(self.main_area, bg=self.color_bg, padx=20, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        style = ttk.Style(); style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#D6DBDF", font=("Arial", 10, "bold"))
        
        # Di sini tadi table_frame kurang "self."
        self.tree = ttk.Treeview(self.table_frame, columns=("judul", "detail", "deadline", "status"), show="headings")
        self.tree.heading("judul", text="Tugas"); self.tree.heading("detail", text="Detail"); self.tree.heading("deadline", text="Deadline"); self.tree.heading("status", text="Status Urgensi")
        self.tree.column("judul", width=150); self.tree.column("detail", width=200); self.tree.column("deadline", width=100, anchor="center"); self.tree.column("status", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Tombol Aksi di Bawah
        self.action_frame = tk.Frame(self.main_area, bg=self.color_bg)
        self.action_frame.pack(fill="x", padx=20, pady=20)

        tk.Button(self.action_frame, text=" Tandai Selesai ✅ ", command=self.tandai_selesai, bg=self.color_success, fg="white", bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2").pack(side="left", padx=5)
        tk.Button(self.action_frame, text=" Edit Tugas ✏️ ", command=self.buka_jendela_edit, bg=self.color_edit, fg="white", bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2").pack(side="left", padx=5)
        tk.Button(self.action_frame, text=" Hapus Tugas 🗑️ ", command=self.hapus_tugas, bg=self.color_danger, fg="white", bd=0, padx=15, pady=8, font=("Arial", 9, "bold"), cursor="hand2").pack(side="right", padx=5)

        self.tampilkan_data()
        self.root.after(1000, self.cek_reminder)

    # --- FUNGSI LOGIKA ---
    def muat_data(self):
        if os.path.exists(self.file_data):
            try:
                with open(self.file_data, 'r') as file: return json.load(file)
            except: return []
        return []

    def simpan_data(self):
        with open(self.file_data, 'w') as file: json.dump(self.tugas_list, file, indent=4)

    def tambah_tugas(self):
        j, d, dl = self.ent_judul.get(), self.ent_detail.get(), self.ent_deadline.get()
        if not j or not dl:
            messagebox.showwarning("Peringatan", "Nama Tugas & Deadline harus diisi!")
            return
        try:
            datetime.strptime(dl, "%Y-%m-%d")
            self.tugas_list.append({"judul": j, "detail": d, "deadline": dl, "selesai": False})
            self.simpan_data(); self.tampilkan_data()
            self.ent_judul.delete(0, 'end'); self.ent_detail.delete(0, 'end'); self.ent_deadline.delete(0, 'end')
        except: messagebox.showerror("Error", "Format tanggal: YYYY-MM-DD")

    def tandai_selesai(self):
        selected = self.tree.selection()
        if selected:
            item_values = self.tree.item(selected)['values']
            for t in self.tugas_list:
                if t['judul'] == item_values[0] and t['deadline'] == item_values[2]:
                    t['selesai'] = True; break
            self.simpan_data(); self.tampilkan_data()

    def hapus_tugas(self):
        selected = self.tree.selection()
        if selected and messagebox.askyesno("Hapus", "Hapus tugas ini?"):
            item_values = self.tree.item(selected)['values']
            self.tugas_list = [t for t in self.tugas_list if not (t['judul'] == item_values[0] and t['deadline'] == item_values[2])]
            self.simpan_data(); self.tampilkan_data()

    def buka_jendela_edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih", "Pilih tugas yang ingin diedit!")
            return
        
        item_values = self.tree.item(selected)['values']
        self.edit_win = tk.Toplevel(self.root)
        self.edit_win.title("Edit Tugas")
        self.edit_win.geometry("300x400")
        self.edit_win.configure(bg="#f8f9fa")

        tk.Label(self.edit_win, text="EDIT TUGAS", font=("Arial", 12, "bold"), bg="#f8f9fa").pack(pady=10)
        tk.Label(self.edit_win, text="Judul:", bg="#f8f9fa").pack()
        ent_judul_edit = tk.Entry(self.edit_win); ent_judul_edit.pack(pady=5); ent_judul_edit.insert(0, item_values[0])
        tk.Label(self.edit_win, text="Detail:", bg="#f8f9fa").pack()
        ent_detail_edit = tk.Entry(self.edit_win); ent_detail_edit.pack(pady=5); ent_detail_edit.insert(0, item_values[1])
        tk.Label(self.edit_win, text="Deadline:", bg="#f8f9fa").pack()
        ent_deadline_edit = tk.Entry(self.edit_win); ent_deadline_edit.pack(pady=5); ent_deadline_edit.insert(0, item_values[2])
        
        def simpan_perubahan():
            for t in self.tugas_list:
                if t['judul'] == item_values[0] and t['deadline'] == item_values[2]:
                    t['judul'] = ent_judul_edit.get(); t['detail'] = ent_detail_edit.get(); t['deadline'] = ent_deadline_edit.get()
                    break
            self.simpan_data(); self.tampilkan_data(); self.edit_win.destroy()

        tk.Button(self.edit_win, text="Simpan Perubahan", command=simpan_perubahan, bg=self.color_edit, fg="white").pack(pady=20)

    def tampilkan_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
                # Ganti baris 153 dengan ini:
        self.tugas_list.sort(key=lambda x: (x.get('selesai', False), x.get('deadline', '')))
        hari_ini = datetime.now().date()
        selesai_count = 0
        for t in self.tugas_list:
            if t.get("selesai"):
                status = "✅ SELESAI"; selesai_count += 1
            else:
                dl = datetime.strptime(t['deadline'], "%Y-%m-%d").date()
                sisa = (dl - hari_ini).days
                if sisa < 0: status = "❌ Terlewat"
                elif sisa <= 3: status = f"⚠️ {sisa} Hari Lagi!"
                else: status = f"⏳ {sisa} Hari"
            self.tree.insert("", tk.END, values=(t['judul'], t['detail'], t['deadline'], status))
        total = len(self.tugas_list); belum = total - selesai_count
        self.lbl_stats.config(text=f"📊 TOTAL: {total}  |  ✅ SELESAI: {selesai_count}  |  ⏳ BELUM: {belum}")

    def cek_reminder(self):
        hari_ini = datetime.now().date()
        mendesak = [f"• {t['judul']} ({t['deadline']})" for t in self.tugas_list if not t.get("selesai") and 0 <= (datetime.strptime(t['deadline'], "%Y-%m-%d").date() - hari_ini).days <= 3]
        if mendesak: messagebox.showwarning("REMINDER DEADLINE", "Tugas Mendatang:\n\n" + "\n".join(mendesak))

if __name__ == "__main__":
    root = tk.Tk(); app = ModernTodoApp(root); root.mainloop()
