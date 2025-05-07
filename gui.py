import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import csv
from datetime import datetime
from models.yolcu import Yolcu
from utils.olasılık import olasilik_kontrol
from PIL import Image, ImageTk
import os


class BaggageSecurityUI:
    def __init__(self, root, simulator):
        self.root = root
        self.root.title("Havalimanı Bagaj Güvenlik Simülatörü")
        self.root.geometry("1000x600")
        self.simulator = simulator
        
        # Simülasyon durumu
        self.simulation_running = False
        
        # Karakter resimlerini yükle
        self.character_images = self.karakter_resimlerini_yukle()
        
        # Eşya resimlerini yükle
        self.item_images = self.esya_resimlerini_yukle()
        
        self.yolcu_kuyrugu_paneli_olustur()
        self.bagaj_yigini_paneli_olustur()
        self.kara_liste_paneli_olustur()
        self.log_paneli_olustur()
        self.kontrol_paneli_olustur()
        
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        # Pencere kapatma olayını yakala
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Pencere kapatıldığında çağrılır"""
        if self.simulation_running:
            self.simulation_running = False
            self.root.after(100, self.on_closing)  # Simülasyonun durmasını bekle
            return
        
        try:
            self.root.destroy()
        except:
            pass
    
    def karakter_resimlerini_yukle(self):
        """Karakter resimlerini yükle ve önbelleğe al"""
        images = {}
        characters_dir = os.path.join(os.path.dirname(__file__), 'assets', 'characters')
        
        for i in range(1, 14):  # 1'den 13'e kadar
            try:
                image_path = os.path.join(characters_dir, f"{i}.jpg")
                if os.path.exists(image_path):
                    # Resmi yükle
                    image = Image.open(image_path)
                    # RGBA moduna dönüştür
                    image = image.convert('RGBA')
                    
                    # Siyah pikselleri şeffaf yap
                    data = image.getdata()
                    new_data = []
                    for item in data:
                        # Eğer piksel siyaha yakınsa (R,G,B değerleri 40'dan küçükse) şeffaf yap
                        if item[0] < 40 and item[1] < 40 and item[2] < 40:
                            new_data.append((0, 0, 0, 0))  # Tamamen şeffaf
                        else:
                            new_data.append(item)
                    
                    image.putdata(new_data)
                    
                    # Resmi 100x100 boyutuna getir (UI'da gösterilecek boyut)
                    # Pixel art için NEAREST kullan (anti-aliasing yok)
                    image = image.resize((100, 100), Image.Resampling.NEAREST)
                    photo = ImageTk.PhotoImage(image)
                    images[i] = photo
                    
                    print(f"Image {i} loaded and resized to {image.size}")
            except Exception as e:
                print(f"Resim yüklenirken hata oluştu ({i}.jpg): {e}")
        
        return images
    
    def esya_resimlerini_yukle(self):
        """Eşya resimlerini yükle ve önbelleğe al"""
        images = {}
        safe_items_dir = os.path.join(os.path.dirname(__file__), 'assets', 'safe_items')
        dangerous_items_dir = os.path.join(os.path.dirname(__file__), 'assets', 'dangerous_items')
        
        # Güvenli eşyaları yükle
        for item_data in self.simulator.normal_items:
            try:
                image_path = os.path.join(safe_items_dir, item_data["texture"])
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.convert('RGBA')
                    
                    # Siyah ve beyaz pikselleri şeffaf yap
                    data = image.getdata()
                    new_data = []
                    for pixel in data:
                        # Eğer piksel siyaha veya beyaza yakınsa şeffaf yap
                        if (pixel[0] < 40 and pixel[1] < 40 and pixel[2] < 40) or \
                           (pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240):
                            new_data.append((0, 0, 0, 0))  # Tamamen şeffaf
                        else:
                            new_data.append(pixel)
                    
                    image.putdata(new_data)
                    
                    # Resmi 30x30 boyutuna getir
                    image = image.resize((30, 30), Image.Resampling.NEAREST)
                    photo = ImageTk.PhotoImage(image)
                    images[item_data["name"]] = photo
            except Exception as e:
                print(f"Resim yüklenirken hata oluştu ({item_data['texture']}): {e}")
        
        # Tehlikeli eşyaları yükle
        for item_data in self.simulator.dangerous_items:
            try:
                image_path = os.path.join(dangerous_items_dir, item_data["texture"])
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.convert('RGBA')
                    
                    # Siyah ve beyaz pikselleri şeffaf yap
                    data = image.getdata()
                    new_data = []
                    for pixel in data:
                        # Eğer piksel siyaha veya beyaza yakınsa şeffaf yap
                        if (pixel[0] < 40 and pixel[1] < 40 and pixel[2] < 40) or \
                           (pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240):
                            new_data.append((0, 0, 0, 0))  # Tamamen şeffaf
                        else:
                            new_data.append(pixel)
                    
                    image.putdata(new_data)
                    
                    # Resmi 30x30 boyutuna getir
                    image = image.resize((30, 30), Image.Resampling.NEAREST)
                    photo = ImageTk.PhotoImage(image)
                    images[item_data["name"]] = photo
            except Exception as e:
                print(f"Resim yüklenirken hata oluştu ({item_data['texture']}): {e}")
        
        return images
    
    def yolcu_kuyrugu_paneli_olustur(self):
        queue_frame = ttk.LabelFrame(self.root, text="Yolcu Kuyruğu")
        queue_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Canvas ve scrollbar oluştur
        self.queue_canvas = tk.Canvas(queue_frame)
        scrollbar = ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_canvas.yview)
        self.queue_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Scrollbar'ı yerleştir
        scrollbar.pack(side="right", fill="y")
        self.queue_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame oluştur ve canvas'a ekle
        self.queue_frame = ttk.Frame(self.queue_canvas)
        self.queue_canvas.create_window((0, 0), window=self.queue_frame, anchor="nw")
        
        # Canvas'ı güncelle
        self.queue_frame.bind("<Configure>", lambda e: self.queue_canvas.configure(scrollregion=self.queue_canvas.bbox("all")))
    
    def bagaj_yigini_paneli_olustur(self):
        stack_frame = ttk.LabelFrame(self.root, text="Bagaj Yığını")
        stack_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Canvas ve scrollbar oluştur
        self.stack_canvas = tk.Canvas(stack_frame)
        scrollbar = ttk.Scrollbar(stack_frame, orient="vertical", command=self.stack_canvas.yview)
        self.stack_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Scrollbar'ı yerleştir
        scrollbar.pack(side="right", fill="y")
        self.stack_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame oluştur ve canvas'a ekle
        self.stack_frame = ttk.Frame(self.stack_canvas)
        self.stack_canvas.create_window((0, 0), window=self.stack_frame, anchor="nw")
        
        # Canvas'ı güncelle
        self.stack_frame.bind("<Configure>", lambda e: self.stack_canvas.configure(scrollregion=self.stack_canvas.bbox("all")))
    
    def kara_liste_paneli_olustur(self):
        blacklist_frame = ttk.LabelFrame(self.root, text="Kara Listede Olan Yolcular")
        blacklist_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Kara liste listesi
        self.blacklist_listbox = tk.Listbox(blacklist_frame, width=30, height=15)
        self.blacklist_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Kara liste kontrol butonları
        control_frame = ttk.Frame(blacklist_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        add_btn = ttk.Button(control_frame, text="Ekle", command=self.kara_listeye_ekle)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(control_frame, text="Çıkar", command=self.kara_listeden_cikar)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Kara listeyi yükle
        self.kara_liste_guncelle()
    
    def kara_liste_guncelle(self):
        """Kara liste görünümünü güncelle"""
        self.blacklist_listbox.delete(0, tk.END)
        for passenger_id in self.simulator.blacklist.tumunu_al():
            self.blacklist_listbox.insert(tk.END, passenger_id)
    
    def kara_listeye_ekle(self):
        """Yeni yolcu ID'si al ve kara listeye ekle"""
        passenger_id = tk.simpledialog.askstring("Kara Liste", "Eklenecek yolcu ID'sini girin:")
        if passenger_id:
            self.simulator.kara_listeye_ekle(passenger_id)
            self.kara_liste_guncelle()
            self.log_mesaji(f"{passenger_id} kara listeye eklendi.")
    
    def kara_listeden_cikar(self):
        """Seçili yolcuyu kara listeden çıkar"""
        selection = self.blacklist_listbox.curselection()
        if selection:
            passenger_id = self.blacklist_listbox.get(selection[0])
            self.simulator.kara_listeden_cikar(passenger_id)
            self.kara_liste_guncelle()
            self.log_mesaji(f"{passenger_id} kara listeden çıkarıldı.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen çıkarılacak yolcuyu seçin.")
    
    def log_paneli_olustur(self):
        log_frame = ttk.LabelFrame(self.root, text="Log Paneli")
        log_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.log_text = tk.Text(log_frame, width=80, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def kontrol_paneli_olustur(self):
        control_frame = ttk.LabelFrame(self.root, text="Kontrol Paneli")
        control_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        load_btn = ttk.Button(control_frame, text="Veri Yükle", command=self.veri_yukle)
        load_btn.grid(row=0, column=0, padx=5, pady=5)
        
        new_passenger_btn = ttk.Button(control_frame, text="Yeni Yolcu", command=self.yeni_yolcu_ekle)
        new_passenger_btn.grid(row=0, column=1, padx=5, pady=5)
        
        start_btn = ttk.Button(control_frame, text="Simülasyonu Başlat", command=self.simulasyonu_baslat)
        start_btn.grid(row=0, column=2, padx=5, pady=5)
        
        report_btn = ttk.Button(control_frame, text="Raporu Göster", command=self.raporu_goster)
        report_btn.grid(row=0, column=3, padx=5, pady=5)
        
        export_btn = ttk.Button(control_frame, text="Raporu Dışa Aktar", command=self.raporu_disa_aktar)
        export_btn.grid(row=0, column=4, padx=5, pady=5)
    
    def log_mesaji(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  
    
    def yolcu_olustur(self):
        passenger_id = f"Yolcu #{random.randint(1, 100)}"
        passenger = Yolcu(passenger_id)
        
        # Rastgele bir karakter resmi seç
        character_num = random.randint(1, len(self.character_images))
        passenger.character_image = character_num
        
        num_items = random.randint(5, 10)
        for _ in range(num_items):
            if olasilik_kontrol(0.1):  
                item = random.choice(self.simulator.dangerous_items)
                passenger.esya_ekle(item["name"], True)
            else:
                item = random.choice(self.simulator.normal_items)
                passenger.esya_ekle(item["name"], False)
        
        return passenger
    
    def yolcu_kuyrugu_guncelle(self):
        # Mevcut yolcuları temizle
        for widget in self.queue_frame.winfo_children():
            widget.destroy()
        
        # Yolcuları göster
        for i, passenger in enumerate(self.simulator.passenger_queue.tum_yolculari_al()):
            frame = ttk.Frame(self.queue_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            # Karakter resmi için container frame
            image_container = ttk.Frame(frame, width=100, height=100)
            image_container.pack(side="left", padx=5)
            image_container.pack_propagate(False)  # Frame boyutunu koru
            
            # Karakter resmini göster
            if hasattr(passenger, 'character_image') and passenger.character_image in self.character_images:
                label = ttk.Label(image_container, image=self.character_images[passenger.character_image])
                label.pack(expand=True, fill="both")  # Resmi container'a sığdır
            
            # Yolcu bilgilerini göster
            info_label = ttk.Label(frame, text=f"{passenger.yolcu_id}")
            info_label.pack(side="left", padx=5)
    
    def veri_yukle(self):
        self.simulator.passenger_queue.temizle()
        
        for i in range(30):
            passenger = self.yolcu_olustur()
            self.simulator.passenger_queue.kuyruga_ekle(passenger)
        
        self.yolcu_kuyrugu_guncelle()
        self.log_mesaji(f"30 yolcu yüklendi.")
    
    def yeni_yolcu_ekle(self):
        passenger = self.yolcu_olustur()
        self.simulator.passenger_queue.kuyruga_ekle(passenger)
        self.yolcu_kuyrugu_guncelle()
        self.log_mesaji(f"Yeni yolcu eklendi: {passenger.yolcu_id}")
    
    def bagaj_kontrol(self, passenger):
        self.simulator.suspicious_baggage_stack.temizle()
        
        # Mevcut eşyaları temizle
        for widget in self.stack_frame.winfo_children():
            widget.destroy()
        
        has_dangerous_items = False
        
        for item in reversed(passenger.esyalari_al()):
            self.simulator.suspicious_baggage_stack.yigina_ekle(item)
            
            # Eşya frame'i oluştur
            item_frame = ttk.Frame(self.stack_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            # Eşya resmini göster
            item_name = item["item"]
            if item_name in self.item_images:
                label = ttk.Label(item_frame, image=self.item_images[item_name])
                label.pack(side="left", padx=5)
            
            # Eşya adını göster
            color = "red" if item["dangerous"] else "green"
            info_label = ttk.Label(item_frame, text=item_name, foreground=color)
            info_label.pack(side="left", padx=5)
            
            if item["dangerous"]:
                has_dangerous_items = True
        
        self.root.update()
        return has_dangerous_items
    
    def yigin_kontrol(self, passenger):
        has_alarm = False
        
        try:
            while not self.simulator.suspicious_baggage_stack.bos_mu():
                item = self.simulator.suspicious_baggage_stack.yigindan_cikar()
                
                # İlk eşyayı kaldır
                if self.stack_frame.winfo_exists() and self.stack_frame.winfo_children():
                    self.stack_frame.winfo_children()[0].destroy()
                
                self.root.update()
                self.root.after(200)  
                
                if item["dangerous"]:
                    has_alarm = True
                    self.log_mesaji(f"ALARM! Tehlikeli eşya bulundu: {item['item']}")
                    self.simulator.alarm_count += 1
        except Exception as e:
            print(f"Yığın kontrolü sırasında hata oluştu: {e}")
            return has_alarm
        
        return has_alarm
    
    def simulasyonu_baslat(self):
        """Simülasyonu başlat"""
        self.simulation_running = True
        if self.yolcu_isle():
            if self.simulation_running:  # Simülasyon hala çalışıyorsa devam et
                self.root.after(1000, self.simulasyonu_baslat)
        else:
            self.simulation_running = False
    
    def raporu_goster(self):
        report = f"""
Güvenlik Kontrol Raporu
====================
Toplam işlenen yolcu: {len(self.simulator.clean_passed) + self.simulator.alarm_count}
Alarm olayları: {self.simulator.alarm_count}
Yakalanan kara liste yolcuları: {self.simulator.blacklist_caught}
Temiz geçişler: {len(self.simulator.clean_passed)}
"""
        messagebox.showinfo("Simülasyon Raporu", report)
    
    def raporu_disa_aktar(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV dosyaları", "*.csv"), ("Tüm dosyalar", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Rapor Tipi", "Değer"])
                writer.writerow(["Toplam işlenen yolcu", len(self.simulator.clean_passed) + self.simulator.alarm_count])
                writer.writerow(["Alarm olayları", self.simulator.alarm_count])
                writer.writerow(["Yakalanan kara liste yolcuları", self.simulator.blacklist_caught])
                writer.writerow(["Temiz geçişler", len(self.simulator.clean_passed)])
            
            self.log_mesaji(f"Rapor {filename} dosyasına aktarıldı")
    
    def yolcu_isle(self):
        """Yolcuyu işle"""
        if not self.simulation_running:
            return False
            
        if self.simulator.passenger_queue.bos_mu():
            self.log_mesaji("Kuyrukta başka yolcu kalmadı.")
            self.simulation_running = False
            return False
        
        try:
            passenger = self.simulator.passenger_queue.kuyruktan_cikar()
            self.yolcu_kuyrugu_guncelle()
            
            self.log_mesaji(f"{passenger.yolcu_id} işleniyor")
            
            is_blacklisted = self.simulator.blacklist.ara(passenger.yolcu_id)
            if is_blacklisted:
                self.log_mesaji(f"UYARI: {passenger.yolcu_id} kara listede!")
                passenger.yuksek_risk = True
                self.simulator.blacklist_caught += 1
            
            has_dangerous_items = self.bagaj_kontrol(passenger)
            
            if has_dangerous_items or passenger.yuksek_risk:
                self.log_mesaji(f"{passenger.yolcu_id} bagajı detaylı kontrol için işaretlendi")
                
                alarm_triggered = self.yigin_kontrol(passenger)
                
                if alarm_triggered:
                    self.log_mesaji(f"{passenger.yolcu_id} yasaklı eşya taşıdığı için gözaltına alındı!")
                else:
                    self.log_mesaji(f"{passenger.yolcu_id} detaylı kontrolden sonra serbest bırakıldı")
                    self.simulator.clean_passed.append(passenger.yolcu_id)
            else:
                self.log_mesaji(f"{passenger.yolcu_id} güvenlik kontrolünden sorunsuz geçti")
                self.simulator.clean_passed.append(passenger.yolcu_id)
            
            return True
        except Exception as e:
            print(f"Yolcu işlenirken hata oluştu: {e}")
            self.simulation_running = False
            return False