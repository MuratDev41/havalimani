import tkinter as tk
from gui import BaggageSecurityUI
import json
import os
from models.yolcu import Yolcu
from models.queue import YolcuKuyrugu
from models.stack import BagajYigini
from models.linkedlist import KaraListe
from utils.olasılık import olasilik_kontrol

class BaggageSecuritySimulator:
    def __init__(self):
        # Veri yapılarını başlat
        self.passenger_queue = YolcuKuyrugu()
        self.suspicious_baggage_stack = BagajYigini()
        self.blacklist = self.kara_liste_yukle()
        
        # İstatistikler
        self.clean_passed = []
        self.alarm_count = 0
        self.blacklist_caught = 0
        
        # Eşya listelerini ve texture yollarını tanımla
        self.normal_items = [
            {"name": "Kitap", "texture": "book.png"},
            {"name": "Kıyafet", "texture": "clothing.jpg"},
            {"name": "Laptop", "texture": "laptop.jpeg"},
            {"name": "Şarj Aleti", "texture": "charger.webp"},
            {"name": "Kulaklık", "texture": "headphones.png"},
            {"name": "Su Şişesi", "texture": "waterbottle.webp"},
            {"name": "Atıştırmalık", "texture": "snacks.webp"},
            {"name": "Defter", "texture": "textbook.webp"},
            {"name": "Kalem", "texture": "pencil.webp"},
            {"name": "Güneş Gözlüğü", "texture": "sunglasses.png"},
            {"name": "Cüzdan", "texture": "wallet.webp"},
            {"name": "Anahtar", "texture": "key.webp"},
            {"name": "İlaç", "texture": "medication.png"},
            {"name": "Tuvalet Malzemeleri", "texture": "toiletpaper.png"},
            {"name": "Şemsiye", "texture": "umbrella.jpg"}
        ]
        
        self.dangerous_items = [
            {"name": "Bıçak", "texture": "knife.webp"},
            {"name": "Makas", "texture": "scissors.webp"},
            {"name": "Çakmak", "texture": "lighter.webp"},
            {"name": "100ml üzeri sıvı", "texture": "100ml.webp"},
            {"name": "Silah", "texture": "gun.jpg"},
            {"name": "Patlayıcı", "texture": "explosive.webp"},
            {"name": "Yanıcı Madde", "texture": "flamable.webp"}
        ]
        
        # GUI'yi oluştur
        self.root = tk.Tk()
        self.ui = BaggageSecurityUI(self.root, self)
        
    def kara_liste_yukle(self):
        """JSON dosyasından kara listeyi yükle"""
        blacklist = KaraListe()
        try:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            blacklist_file = os.path.join(data_dir, 'kara_liste.json')
            
            # Dizin yoksa oluştur
            os.makedirs(data_dir, exist_ok=True)
            
            if os.path.exists(blacklist_file):
                with open(blacklist_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for passenger_id in data.get("blacklisted_passengers", []):
                        blacklist.ekle(passenger_id)
            else:
                # Dosya yoksa varsayılan kara liste oluştur
                default_blacklist = [
                    "Yolcu #1",
                    "Yolcu #2",
                    "Yolcu #3",
                    "Yolcu #4",
                    "Yolcu #5"
                ]
                for passenger_id in default_blacklist:
                    blacklist.ekle(passenger_id)
                
                # Varsayılan kara listeyi kaydet
                self.kara_liste_kaydet(blacklist)
                
        except Exception as e:
            print(f"Kara liste yüklenirken hata oluştu: {e}")
            # Hata durumunda varsayılan kara liste oluştur
            for i in range(1, 6):
                blacklist.ekle(f"Yolcu #{i}")
                
        return blacklist
    
    def kara_liste_kaydet(self, blacklist=None):
        """Kara listeyi JSON dosyasına kaydet"""
        if blacklist is None:
            blacklist = self.blacklist
            
        try:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            blacklist_file = os.path.join(data_dir, 'kara_liste.json')
            
            # Dizin yoksa oluştur
            os.makedirs(data_dir, exist_ok=True)
            
            with open(blacklist_file, 'w', encoding='utf-8') as file:
                json.dump({
                    "blacklisted_passengers": blacklist.tumunu_al()
                }, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"Kara liste kaydedilirken hata oluştu: {e}")
    
    def kara_listeye_ekle(self, passenger_id):
        """Yolcuyu kara listeye ekle ve dosyaya kaydet"""
        self.blacklist.ekle(passenger_id)
        self.kara_liste_kaydet()
    
    def kara_listeden_cikar(self, passenger_id):
        """Yolcuyu kara listeden çıkar ve dosyaya kaydet"""
        self.blacklist.kaldir(passenger_id)
        self.kara_liste_kaydet()
    
    def calistir(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BaggageSecuritySimulator()
    app.calistir()