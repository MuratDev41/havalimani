import random

def olasilik_kontrol(olasilik):
    if olasilik < 0 or olasilik > 1:
        raise ValueError("Olasılık 0 ile 1 arasında olmalıdır")
    
    return random.random() < olasilik

def tehlikeli_esya_olasiligi_olustur(risk_seviyesi='normal'):
    if risk_seviyesi == 'dusuk':
        return 0.05  # %5 şans
    elif risk_seviyesi == 'normal':
        return 0.1   # %10 şans
    elif risk_seviyesi == 'yuksek':
        return 0.2   # %20 şans
    else:
        raise ValueError("Risk seviyesi 'dusuk', 'normal' veya 'yuksek' olmalıdır")

def risk_puani_hesapla(yolcu, kara_liste_durumu):
    # Temel risk puanı
    risk_puani = 0.1
    
    # Kara listede ise riski artır
    if kara_liste_durumu:
        risk_puani += 0.5
    
    # Tehlikeli eşyalara göre riski artır
    tehlikeli_esyalar = sum(1 for item in yolcu.get_items() if item["dangerous"])
    if tehlikeli_esyalar > 0:
        risk_puani += min(0.3, tehlikeli_esyalar * 0.1)  # Tehlikeli eşyalardan maksimum 0.3
    
    # Puanın 1.0'ı geçmemesini sağla
    return min(1.0, risk_puani)

def kontrol_detayliligi_al(risk_puani):
    if risk_puani < 0.3:
        # Düşük risk - hızlı kontrol
        return {
            "kontrol_suresi": 5,
            "tespit_olasiligi": 0.7,
            "yanlis_pozitif_orani": 0.05
        }
    elif risk_puani < 0.6:
        # Orta risk - standart kontrol
        return {
            "kontrol_suresi": 10,
            "tespit_olasiligi": 0.85,
            "yanlis_pozitif_orani": 0.03
        }
    else:
        # Yüksek risk - detaylı kontrol
        return {
            "kontrol_suresi": 20,
            "tespit_olasiligi": 0.98,
            "yanlis_pozitif_orani": 0.01
        }

def tespit_simulasyonu(esya, tespit_olasiligi, yanlis_pozitif_orani):
    if esya["dangerous"]:
        # Tehlikeli eşyalar için tespit olasılığına bağlı
        return olasilik_kontrol(tespit_olasiligi)
    else:
        # Güvenli eşyalar için yanlış alarm oranına bağlı
        return olasilik_kontrol(yanlis_pozitif_orani)

def yolcu_gelis_orani_olustur(gun_saati):
    if gun_saati == 'sabah':
        return 8.0  # Yoğun saat
    elif gun_saati == 'ogle':
        return 5.0  # Orta
    elif gun_saati == 'aksam':
        return 6.0  # Orta-yüksek
    elif gun_saati == 'gece':
        return 2.0  # Düşük
    else:
        return 4.0  # Varsayılan

def rastgele_yolcu_id_olustur():
    return f"Yolcu #{random.randint(1, 999)}"

def rastgele_esya_sec(esya_listesi, tehlikeli_mi=False):
    if not esya_listesi:
        return "Bilinmeyen Eşya"
    return random.choice(esya_listesi)