import streamlit as st
import yfinance as yf
import pandas as pd

# SAYFA AYARLARI
st.set_page_config(page_title="Eagle Eye | Radar", page_icon="🎯", layout="wide")

st.title("🎯 Eagle Radar: Anlık Durum Analizi")
st.markdown("---")

# TAKİP LİSTESİ (Senin Portföyün)
portfoy = ["THYAO.IS", "PGSUS.IS", "ASELS.IS", "KUVVA.IS", "GEREL.IS", "TUPRS.IS", "AYGAZ.IS"]

# ANALİZ MOTORU
def anlik_yorum(ticker, data):
    fiyat = data['Close'].iloc[-1]
    degisim = ((fiyat - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
    
    # Simsar Mantığı: Teknik ve Temel Notlar
    if "THYAO" in ticker:
        notum = "Turizm sezonu fiyatlanıyor. 312 TL desteği kritik."
    elif "GEREL" in ticker:
        notum = "Enerji teşvikleri radarda. Hacim artışı 'Patlama' sinyali olabilir."
    elif "KUVVA" in ticker:
        notum = "Alt Pazar spekülasyonu yüksek. Stop-loss'suz işlem yapma."
    elif "ASELS" in ticker:
        notum = "Savunma sanayii siparişleri güçlü. RSI yorgunluğu izlenmeli."
    else:
        notum = "BIST genel trendiyle uyumlu hareket ediyor."
    
    return notum, degisim

# PANEL TASARIMI
cols = st.columns(3)

for i, h in enumerate(portfoy):
    with cols[i % 3]:
        t = yf.Ticker(h)
        try:
            # Son 5 günlük veriyi çek
            hist = t.history(period="5d")
            fiyat = hist['Close'].iloc[-1]
            yorum, degisim = anlik_yorum(h, hist)
            
            color = "#00ff00" if degisim > 0 else "#ff0000"
            
            # Şık Kart Tasarımı
            st.markdown(f"""
            <div style="background-color:#161b22; padding:20px; border-radius:15px; border-left: 8px solid {color}; margin-bottom:15px; border-right: 1px solid #333; border-top: 1px solid #333; border-bottom: 1px solid #333;">
                <h3 style="margin:0; color:white;">{h.split('.')[0]}</h3>
                <h1 style="margin:0; color:white;">{fiyat:.2f} <span style="font-size:18px;">TL</span></h1>
                <p style="color:{color}; font-weight:bold; font-size:20px; margin:0;">%{degisim:.2f}</p>
                <hr style="border:0.1px solid #333; margin:10px 0;">
                <p style="font-size:14px; color:#aaa;"><b>Simsar Notu:</b><br>{yorum}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hızlı Grafik
            with st.expander("📈 Son 5 Günlük Grafik"):
                st.line_chart(hist['Close'])
        except:
            st.error(f"{h} verisi çekilemedi.")

st.sidebar.info("Radar sayfası her açıldığında veriler o saniyenin fiyatlarıyla güncellenir.")
