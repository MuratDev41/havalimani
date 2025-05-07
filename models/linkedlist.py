class Dugum:
    def __init__(self, yolcu_id):
        self.yolcu_id = yolcu_id
        self.sonraki = None

class KaraListe:
    def __init__(self):
        self.bas = None
    
    def ekle(self, yolcu_id):
        yeni_dugum = Dugum(yolcu_id)
        
        if not self.bas:
            self.bas = yeni_dugum
            return
        
        mevcut = self.bas
        while mevcut.sonraki:
            mevcut = mevcut.sonraki
        
        mevcut.sonraki = yeni_dugum
    
    def ara(self, yolcu_id):
        mevcut = self.bas
        
        while mevcut:
            if mevcut.yolcu_id == yolcu_id:
                return True
            mevcut = mevcut.sonraki
        
        return False
    
    def kaldir(self, yolcu_id):
        if not self.bas:
            return False
        
        if self.bas.yolcu_id == yolcu_id:
            self.bas = self.bas.sonraki
            return True
        
        mevcut = self.bas
        while mevcut.sonraki and mevcut.sonraki.yolcu_id != yolcu_id:
            mevcut = mevcut.sonraki
        
        if mevcut.sonraki:
            mevcut.sonraki = mevcut.sonraki.sonraki
            return True
        
        return False
    
    def tumunu_al(self):
        sonuc = []
        mevcut = self.bas
        
        while mevcut:
            sonuc.append(mevcut.yolcu_id)
            mevcut = mevcut.sonraki
        
        return sonuc
    
    def bos_mu(self):
        return self.bas is None
    
    def temizle(self):
        self.bas = None