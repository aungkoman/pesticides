import streamlit as st
import pandas as pd
from PIL import Image
from google import genai

# Streamlit Page Setting
st.set_page_config(page_title="Pesticide & Medicine Verifier", page_icon="🔬", layout="centered")

st.title("🔬 AI Medicine & Pesticide Verifier")
st.write("ဆေးဘူး သို့မဟုတ် စိုက်ပျိုးရေးဆေးပုံကို Upload တင်ပြီး Approved/Banned စစ်ဆေးပါ။")


#  API KEY 

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_medicine_name(pil_image):
    """Gemini AI သုံးပြီး ပုံထဲက ဆေးနာမည် သို့မဟုတ် ပါဝင်ပစ္စည်းကို ဖတ်ခြင်း"""
    try:
        prompt = (
            "Identify the main chemical name, active ingredient, or trade name of the pesticide/medicine shown in this image. "
            "Return ONLY the extracted name in plain text. No extra words, no punctuation. "
            "Example output: Gaucho 600 FS"
        )
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=[pil_image, prompt]
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return None

def check_status(detected_text, csv_path="final.csv"):

    try:
        # df = pd.read_csv(csv_path)
        df = pd.read_csv(csv_path, encoding='latin-1')
        
        # clean
        df['trade_name_lower'] = df['trade_name'].astype(str).str.lower().str.strip()
        df['active_lower'] = df['active_ingredient'].astype(str).str.lower().str.strip()
        search_text = detected_text.lower().strip()
        
       
        result = df[(df['trade_name_lower'] == search_text) | (df['active_lower'] == search_text)]
        
   
        if result.empty:
            result = df[
                df['trade_name_lower'].str.contains(search_text, na=False) | 
                df['active_lower'].str.contains(search_text, na=False)
            ]
            

        if result.empty:
            result = df[
                df['trade_name_lower'].apply(lambda x: x in search_text if pd.notna(x) else False) |
                df['active_lower'].apply(lambda x: x in search_text if pd.notna(x) else False)
            ]
            
        if not result.empty:
            row = result.iloc[0]
            active_ing = row['active_ingredient'] if pd.notna(row['active_ingredient']) else "-"
            trade_nm = row['trade_name'] if pd.notna(row['trade_name']) else "-"
            
            return {
                "found": True,
                "trade_name": trade_nm,
                "active_ingredient": active_ing,
                "status": str(row['status']).strip().lower()
            }
        else:
            return {"found": False}
            
    except Exception as e:
        st.error(f"Dataset File Error: {e}")
        return None

# --- UI  ---
uploaded_file = st.file_uploader("ကြိုက်နှစ်သက်ရာ ဆေးဘူးပုံကို ရွေးချယ်တင်ပါ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="တင်လိုက်သော ဆေးဘူးပုံ", use_container_width=True)
    
    if st.button("စစ်ဆေးမည် (Verify Now)"):
        with st.spinner("AI က ဆေးအမည်ကို ဖတ်ပြီး Dataset ထဲမှာ တိုက်စစ်နေပါတယ်..."):
            
            detected_name = extract_medicine_name(image)
            
            if detected_name:
                st.info(f"🔍 **AI ဖတ်မိသော အမည်/စာသား:** {detected_name}")
                st.divider()
                
                res = check_status(detected_name)
                
                if res and res["found"]:
                    st.subheader("📊 ရလဒ်အဖြေ (Result)")
                    st.write(f"**ဆေးအမည် (Trade Name):** {res['trade_name']}")
                    st.write(f"**ပါဝင်ပစ္စည်း (Active Ingredient):** {res['active_ingredient']}")
                    
                    if res["status"] == "approved":
                        st.success("✅ APPROVED (အသုံးပြုရန် ခွင့်ပြုထားသော ဆေးဖြစ်သည်)")
                    elif res["status"] == "banned":
                        st.error("❌ BANNED (ပိတ်ပင်တားမြစ်ထားသော ဆေးဖြစ်သည်)")
                    else:
                        st.warning(f"⚠️ STATUS: {res['status'].upper()}")
                else:
                    st.warning(f"⚠️ NOT FOUND: '{detected_name}' ကို သင့်ရဲ့ `final.csv` Dataset ထဲမှာ ရှာမတွေ့ပါ။")