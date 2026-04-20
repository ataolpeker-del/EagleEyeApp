import streamlit as st
import yfinance as yf
import pandas as pd

# SAYFA AYARLARI
st.set_page_config(page_title="Eagle Eye | Radar & Dedikodu", page_icon="🎯", layout="wide")

# --- PİYASA DEDİKODUSU FONKSİYONU ---
def get_piyasa_dedikodusu(ticker_name, change, rsi_val):
    # Brent Petrol Bilgisi (Havacılık ve Tüpraş için kritik)
    try:
        brent = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        brent_status = "Yüksek" if brent > 85 else "Normal"
    except:
        brent_status = "Bilinmiyor"
    
    # Dinamik Yorum Mantığı
    if "THYAO" in ticker_name or "PGSUS" in ticker_name:
        if brent_status == "Yüksek" and change < 0:
            return f"✈️ Brent Petrol ${brent:.2f} seviyesinde. Yakıt maliyeti baskısı ve teknik düzeltme var. RSI: {rsi_val:.2f}."
        return f"🛫 Yolcu trafiği güçlü. RSI {rsi_val:.2f} seviyesinde, trend korunuyor."
    
    elif "ASELS" in ticker_name:
        return f"🛡️ Savunma sözleşmeleri ve jeopolitik riskler kağıdı diri tutuyor. RSI: {rsi_val:.2f}. Güvenli liman modu açık."
    
    elif "TUPRS" in ticker_name or "AYGAZ" in ticker_name:
        return f"🛢️ Rafineri marjları ve enerji talebi odaklı hareket. RSI: {rsi_val:.2f}. Brent Petrol hareketine duyarlı."
    
    elif "GEREL" in ticker_name or "KUVVA" in ticker_name:
        return f"🚨 Spekülatif hacim takibi yapılıyor. RSI: {rsi_val:.2f}. Ani KAP haberleri yönü belirleyebilir, stop-loss unutulmamalı."
    
    else:
        return f"📊 Genel piyasa endeksiyle korelasyon yüksek. RSI: {rsi_val:.2f}."

# --- RSI HESAPLAMA (BASİT) ---
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1+rs))

# --- ANA EKRAN ---
st.title("🎯 Eagle Radar & Simsar Fısıltıları")
st.caption(f"📅 Veriler anlık çekiliyor: {pd.Timestamp.now().strftime('%H:%M:%S')}")

portfoy = ["THYAO.IS", "PGSUS.IS", "ASELS.IS", "KUVVA.IS", "GEREL.IS", "TUPRS.IS", "AYGAZ.IS"]

cols = st.columns(3)

for i, h in enumerate(portfoy):
    with cols[i % 3]:
        t = yf.Ticker(h)
        try:
            # Teknik veriler için son 30 günü çek
            df = t.history(period="30d")
            fiyat = df['Close'].iloc[-1]
            degisim = ((fiyat - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
            rsi_list = calculate_rsi(df)
            current_rsi = rsi_list.iloc[-1]
            
            color = "#00ff00" if degisim > 0 else "#ff0000"
            
            # Kart Tasarımı
            st.markdown(f"""
            <div style="background-color:#161b22; padding:20px; border-radius:15px; border-left: 8px solid {color}; margin-bottom:10px;">
                <h3 style="margin:0;">{h.split('.')[0]}</h3>
                <h1 style="margin:0; color:white;">{fiyat:.2f} TL</h1>
                <p style="color:{color}; font-weight:bold; font-size:18px;">%{degisim:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # PİYASA DEDİKODUSU BUTONU
            if st.button(f"💬 {h.split('.')[0]} Neden Hareket Ediyor?", key=h):
                analiz = get_piyasa_dedikodusu(h, degisim, current_rsi)
                st.info(analiz)
                
        except Exception as e:
            st.error(f"{h} verisinde hata!")
