class BagajYigini:
    def __init__(self):
        self.ogeler = []
    
    def yigina_ekle(self, oge):
        self.ogeler.append(oge)
    
    def yigindan_cikar(self):
        if self.bos_mu():
            raise IndexError("Boş yığından çıkarılamaz")
        return self.ogeler.pop()
    
    def ust_ogeyi_goster(self):
        if self.bos_mu():
            raise IndexError("Boş yığından gösterilemez")
        return self.ogeler[-1]
    
    def bos_mu(self):
        return len(self.ogeler) == 0
    
    def boyut(self):
        return len(self.ogeler)
    
    def temizle(self):
        self.ogeler = []
    
    def tum_ogeleri_al(self):
        return self.ogeler.copy()