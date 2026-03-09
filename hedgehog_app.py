import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, requests, subprocess

class HedgehogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hedgehog Converter v5.0.0")
        self.root.geometry("850x700")
        
        try:
            self.icon_img = tk.PhotoImage(file='/usr/share/pixmaps/hedgehog.png')
            self.root.iconphoto(True, self.icon_img)
        except: pass

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        # Sekme Tanımlamaları
        self.tab1 = ttk.Frame(self.tabs); self.tabs.add(self.tab1, text=" ⚖️ Birimler ")
        self.tab2 = ttk.Frame(self.tabs); self.tabs.add(self.tab2, text=" 💰 Canlı Döviz ")
        self.tab3 = ttk.Frame(self.tabs); self.tabs.add(self.tab3, text=" 📦 Medya & Belge ")

        self.setup_unit_ui()
        self.setup_curr_ui()
        self.setup_media_ui()

    def setup_unit_ui(self):
        f = ttk.Frame(self.tab1, padding=20)
        f.pack(expand=True, fill="both")
        ttk.Label(f, text="Miktar:", font=("Arial", 11)).pack()
        self.u_val = ttk.Entry(f, font=("Arial", 12), width=20); self.u_val.pack(pady=5)
        self.u_type = ttk.Combobox(f, values=["KM -> Mil", "Metre -> Feet", "KG -> Pound", "Celsius -> Fahrenheit", "Litre -> Galon"], state="readonly", width=30)
        self.u_type.pack(pady=10); self.u_type.set("Dönüşüm Seçin")
        ttk.Button(f, text="HESAPLA", command=self.calc_units).pack(pady=10)

    def setup_curr_ui(self):
        f = ttk.Frame(self.tab2, padding=20)
        f.pack(expand=True, fill="both")
        ttk.Label(f, text="Miktar (USD/EUR/GBP):").pack()
        self.c_amt = ttk.Entry(f, font=("Arial", 12)); self.c_amt.pack(pady=5)
        self.c_sel = ttk.Combobox(f, values=["USD to TRY", "EUR to TRY", "GBP to TRY", "TRY to USD"], state="readonly")
        self.c_sel.pack(pady=5); self.c_sel.set("Kur Seçin")
        ttk.Button(f, text="GÜNCEL KUR İLE ÇEVİR", command=self.calc_curr).pack(pady=10)
        self.c_res = ttk.Label(f, text="Sonuç: --", font=("Arial", 15, "bold"), foreground="#2E8B57"); self.c_res.pack(pady=20)

    def setup_media_ui(self):
        f = ttk.Frame(self.tab3, padding=20)
        f.pack(expand=True, fill="both")
        self.f_path = tk.StringVar()
        ttk.Entry(f, textvariable=self.f_path, width=50).pack(pady=5)
        ttk.Button(f, text="Dosya Seç", command=lambda: self.f_path.set(filedialog.askopenfilename())).pack()
        self.m_act = ttk.Combobox(f, values=["PDF'i Word'e Çevir (DOCX)", "Word'ü PDF Yap", "Video Sıkıştır (MP4)", "Görsel Sıkıştır (JPG)", "Videodan Ses Ayıkla (MP3)"], state="readonly", width=40)
        self.m_act.pack(pady=15); self.m_act.set("İşlem Seçin")
        ttk.Button(f, text="İŞLEMİ BAŞLAT", command=self.run_media).pack()

    def calc_units(self):
        try:
            v = float(self.u_val.get()); t = self.u_type.get(); r = 0
            if "KM" in t: r = v * 0.621
            elif "Metre" in t: r = v * 3.28
            elif "KG" in t: r = v * 2.204
            elif "Celsius" in t: r = (v * 9/5) + 32
            elif "Litre" in t: r = v * 0.264
            messagebox.showinfo("Sonuç", f"Değer: {r:.2f}")
        except: messagebox.showerror("Hata", "Sayı girin!")

    def calc_curr(self):
        try:
            amt = float(self.c_amt.get()); sel = self.c_sel.get()
            data = requests.get("https://open.er-api.com/v6/latest/USD").json()["rates"]
            if "USD to TRY" in sel: res = amt * data["TRY"]
            elif "EUR to TRY" in sel: res = amt * (data["TRY"] / data["EUR"])
            elif "GBP to TRY" in sel: res = amt * (data["TRY"] / data["GBP"])
            elif "TRY to USD" in sel: res = amt / data["TRY"]
            self.c_res.config(text=f"Sonuç: {res:.2f} TL")
        except: messagebox.showerror("Hata", "Kur alınamadı!")

    def run_media(self):
        f = self.f_path.get(); a = self.m_act.get()
        if not f: return
        base = os.path.splitext(f)[0]
        try:
            if "PDF'i Word" in a:
                from pdf2docx import Converter
                cv = Converter(f); cv.convert(base+".docx"); cv.close()
            elif "Word" in a:
                subprocess.run(f'libreoffice --headless --convert-to pdf "{f}" --outdir "{os.path.dirname(f)}"', shell=True)
            elif "Video" in a:
                subprocess.run(f'ffmpeg -i "{f}" -vcodec libx265 -crf 28 "{base}_compressed.mp4"', shell=True)
            messagebox.showinfo("Başarılı", "İşlem Tamamlandı!")
        except Exception as e: messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HedgehogApp(root)
    root.mainloop()
