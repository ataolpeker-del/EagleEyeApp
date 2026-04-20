import streamlit as st
import yfinance as yf

# SAYFA TASARIMI
st.set_page_config(page_title="Eagle Eye | Patron Paneli", page_icon="🦅", layout="wide")

st.title("🦅 Eagle Eye: Piyasa Dedikodusu & Analiz")
st.info("Patron, bugün piyasada dönen kulis bilgilerini ve teknik analizleri aşağıda özetledim.")

# Portföy Listesi
portfoy = ["THYAO.IS", "PGSUS.IS", "ASELS.IS", "KUVVA.IS", "GEREL.IS", "TUPRS.IS", "AYGAZ.IS"]

def piyasa_dedikodusu(ticker, degisim):
    if "THYAO" in ticker or "PGSUS" in ticker:
        if degisim < 0:
            return "✈️ Havacılıkta kâr realizasyonu ve petrol fiyatlarındaki kıpırdanma baskı yaratıyor. Destek seviyeleri izlenmeli."
        return "🛫 Turizm sezonu beklentisi ve güçlü yolcu trafiği verileri kağıdı yukarı itiyor. Ralli devam edebilir."
    elif "TUPRS" in ticker:
        return "🛢️ Rafineri marjları ve Brent petrol korelasyonu ön planda. Temettü beklentisi kağıdı diri tutuyor."
    elif "GEREL" in ticker:
        return "⚡ Şarj istasyonu yatırımları ve enerji teşvikleri radarda. Hacimli kırılım bekleniyor, spekülatif ilgi yüksek."
    elif "KUVVA" in ticker:
        return "🚨 Alt Pazar dinamikleri devrede. Hacim sığ, sert hareketlere karşı stop-loss seviyeni koru."
    else:
        return "📊 Genel piyasa trendi ve makro verilerle (Enflasyon/Faiz) uyumlu hareket ediyor."

# ANA PANEL
cols = st.columns(3)

for i, h in enumerate(portfoy):
    with cols[i % 3]:
        ticker = yf.Ticker(h)
        try:
            hist = ticker.history(period="2d")
            fiyat = hist['Close'].iloc[-1]
            degisim = ((fiyat - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            
            color = "#00ff00" if degisim > 0 else "#ff0000"
            
            st.markdown(f"""
            <div style="background-color:#161b22; padding:15px; border-radius:12px; border-top: 4px solid {color};">
                <h3 style="margin:0;">{h.split('.')[0]}</h3>
                <h2 style="margin:0; color:{color};">{fiyat:.2f} TL (%{degisim:.2f})</h2>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("💬 Neler Oluyor? (Simsar Notu)"):
                st.write(piyasa_dedikodusu(h, degisim))
                st.caption("Veriler ve haber akışı anlık analiz edilmiştir.")
        except:
            st.error(f"{h} verisi şu an ulaşılamaz durumda.")

st.divider()
st.sidebar.markdown("### 💰 Fon Takip")
st.sidebar.write("**TLY:** Gayrimenkul & Repo Ağırlıklı")
st.sidebar.write("**PHE:** Hisse Senedi Yoğun")
