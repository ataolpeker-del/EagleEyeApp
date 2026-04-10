import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Eagle Eye v1.0", page_icon="🦅")

st.title("🦅 Eagle Eye: Stratejik Analiz Paneli")
st.write("Hoş geldin patron. Borsadaki tüm veriler senin için taranıyor.")

# Analiz etmek istediğin hisseler
hisseler = ["ASELS.IS", "THYAO.IS", "TUPRS.IS", "SISE.IS", "EREGL.IS", "KCHOL.IS"]

def eagle_eye_analiz(ticker):
    hisse = yf.Ticker(ticker)
    info = hisse.info
    # Basit bir puanlama mantığı
    pddd = info.get('priceToBook', 1.5)
    fiyat = hisse.history(period='1d')['Close'].iloc[-1]
    
    if pddd < 1.2:
        return f"🌟 FIRSAT ({pddd})", fiyat, "İş Yatırım kriterine göre ucuz."
    else:
        return f"👀 İZLE ({pddd})", fiyat, "Dengeli seviye."

for h in hisseler:
    durum, fiyat, yorum = eagle_eye_analiz(h)
    with st.expander(f"{h.split('.')[0]} - {durum}"):
        st.write(f"**Güncel Fiyat:** {fiyat:.2f} TL")
        st.write(f"**Eagle Eye Yorumu:** {yorum}")

st.sidebar.info("Eagle Eye v1.0 - Makro-Stratejik Analiz Motoru")
