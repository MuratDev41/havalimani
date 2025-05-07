class YolcuKuyrugu:
    def __init__(self):
        self.ogeler = []
    
    def kuyruga_ekle(self, yolcu):
        self.ogeler.append(yolcu)
    
    def kuyruktan_cikar(self):
        if self.bos_mu():
            raise IndexError("Boş kuyruktan çıkarılamaz")
        return self.ogeler.pop(0)
    
    def ilk_ogeyi_goster(self):
        if self.bos_mu():
            raise IndexError("Boş kuyruktan gösterilemez")
        return self.ogeler[0]
    
    def bos_mu(self):
        return len(self.ogeler) == 0
    
    def boyut(self):
        return len(self.ogeler)
    
    def temizle(self):
        self.ogeler = []
    
    def tum_yolculari_al(self):
        return self.ogeler.copy()