import cv2
import numpy as np

# 1. Video dosyasını yükle
video_path = r"C:\Users\hulya\OneDrive\Masaüstü\konveyor.mp4" 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("[HATA] Video dosyası bulunamadı!")
    exit()

sise_sayaci = 0
sise_kutuda_mi = False  # Şişenin kutuda olup olmadığını takip eder

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    yukseklik, genislik, _ = frame.shape

    # --- YEŞİL KUTU (TAM KAHVERENGİ ŞİŞELERİN ÜZERİNE AYARLANDI) ---
    roi_x1 = int(genislik * 0.40)   
    roi_y1 = int(yukseklik * 0.20)  # Üst sınır (Kahverengi şişelerin başladığı yer)
    roi_x2 = int(genislik * 0.60)   
    roi_y2 = int(yukseklik * 0.38)  # Alt sınır (Çubuklara inmeden, şişede bitiyor)

    # 2. Sadece kutunun içini al ve KAHVERENGİ rengi süz (Maskeleme)
    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Kahverengi/Koyu Amber şişeleri yakalamak için renk aralığı
    dusuk_kahve = (0, 40, 20)
    yuksek_kahve = (30, 255, 150)
    
    maske = cv2.inRange(hsv, dusuk_kahve, yuksek_kahve)
    kahve_piksel_sayisi = cv2.countNonZero(maske)

    # --- SAYIM MANTIĞI ---
    # Kutunun içinde yeteri kadar kahverengi piksel (şişe gövdesi) varsa say
    # Videonuzdaki şişenin boyutuna göre 800 değerini artırıp azaltabilirsiniz
    if kahve_piksel_sayisi > 800: 
        if not sise_kutuda_mi:
            sise_sayaci += 1
            sise_kutuda_mi = True
            kutu_renk = (0, 0, 255) # Şişe girince kutu KIRMIZI olur
    else:
        sise_kutuda_mi = False
        kutu_renk = (0, 255, 0) # Kutu boşken YEŞİL olur

    # Ekrana kutuyu ve sayacı çiz
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), kutu_renk, 3)
    cv2.putText(frame, f"Kahve Piksel: {kahve_piksel_sayisi}", (roi_x1, roi_y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, kutu_renk, 2)
    
    cv2.putText(frame, f"Toplam Sise: {sise_sayaci}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Kahverengi Sise Sayici", frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()