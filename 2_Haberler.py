import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# SAYFA AYARLARI
st.set_page_config(page_title="Eagle Eye | Haber & KAP", page_icon="🗞️", layout="wide")

# ANLIK GÜNCELLEME İÇİN ZAMAN DAMGASI
su_an = datetime.now().strftime("%H:%M:%S")

st.title("🗞️ Haber Merkezi & KAP Analiz")
st.subheader(f"🕒 Son Güncelleme: {su_an}")
st.caption("Veriler her girişte canlı olarak taranır ve listelenir.")

# TAKİP LİSTESİ
portfoy = ["THYAO.IS", "PGSUS.IS", "ASELS.IS", "KUVVA.IS", "GEREL.IS", "TUPRS.IS", "AYGAZ.IS"]

st.markdown("---")

# HABER ÇEKME VE ANALİZ MODÜLÜ
for h in portfoy:
    with st.container():
        ticker = yf.Ticker(h)
        h_name = h.split('.')[0]
        
        # Haberleri çek
        news = ticker.news
        
        # Tasarım: Hisse Başlığı
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### 🦅 {h_name}")
            # Fiyat bilgisini de yanına ekleyelim ki haberle bağ kuralım
            fiyat = ticker.history(period="1d")['Close'].iloc[-1]
            st.metric("Anlık Fiyat", f"{fiyat:.2f} TL")
            
        with col2:
            if news:
                st.write("**Son Gelişmeler:**")
                for item in news[:3]: # En güncel 3 haberi getir
                    # Haber başlığı ve linki
                    st.markdown(f"🔹 **[{item['title']}]({item['link']})**")
                    st.caption(f"Kaynak: {item['publisher']} | Yayınlanma: {datetime.fromtimestamp(item['providerPublishTime']).strftime('%d/%m/%Y %H:%M')}")
                    
                    # Basit Duygu Analizi (Simsar Gözüyle)
                    baslik = item['title'].lower()
                    if any(x in baslik for x in ['artış', 'kâr', 'rekor', 'yükseliş', 'anlaşma', 'ihale']):
                        st.success("Eagle Eye Yorumu: Pozitif Haber Akışı ✨")
                    elif any(x in baslik for x in ['düşüş', 'zarar', 'kayıp', 'iptal', 'risk']):
                        st.error("Eagle Eye Yorumu: Dikkat, Baskı Yaratabilir ⚠️")
            else:
                st.info(f"{h_name} için son 24 saatte yeni bir haber akışı saptanmadı. Piyasa sakin.")
        
        st.markdown("---")

# EKSTRA PİYASA MANŞETLERİ (Global)
st.sidebar.markdown("### 🌍 Küresel Manşetler")
market_news = yf.Ticker("^XU100").news # BIST 100 genel haberleri
if market_news:
    for mn in market_news[:5]:
        st.sidebar.write(f"- [{mn['title']}]({mn['link']})")
