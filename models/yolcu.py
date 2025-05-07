class Yolcu:
    def __init__(self, yolcu_id):
        self.yolcu_id = yolcu_id
        self.bagaj_esyalari = []  # Yolcunun bagajındaki eşyaların listesi
        self.yuksek_risk = False   # Yüksek riskli yolcular için bayrak (kara listede)
    
    def esya_ekle(self, esya, tehlikeli_mi=False):
        self.bagaj_esyalari.append({"item": esya, "dangerous": tehlikeli_mi})
    
    def esyalari_al(self):
        return self.bagaj_esyalari
    
    def __str__(self):
        return f"{self.yolcu_id} - {'Yüksek Risk' if self.yuksek_risk else 'Normal'} - {len(self.bagaj_esyalari)} eşya"