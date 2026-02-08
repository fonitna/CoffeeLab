import streamlit as st
from datetime import datetime

# ===============================
# App Config
# ===============================
st.set_page_config(
    page_title="Coffee Shop System",
    page_icon="☕",
    layout="centered"
)

# ===============================
# Global CSS (Coffee Background)
# ===============================
st.markdown("""
<style>
/* Background ทั้งหน้า */
.stApp {
    background-color: #f3eee9;
}

/* กล่องเนื้อหาหลัก */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ปุ่มหลัก */
div.stButton > button {
    background-color: #6f4e37;
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #5c3d2e;
}

/* Radio button spacing */
.stRadio > div {
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Session State
# ===============================
if "orders" not in st.session_state:
    st.session_state.orders = []

# ===============================
# Data (TH / EN)
# ===============================
flavor_main = {
    'A': 'เปรี้ยวสดชื่น (Bright & Fresh 🍋)',
    'B': 'หวานอมเปรี้ยว (Sweet & Balanced 🍑)',
    'C': 'ขมกลมกล่อม (Bold & Smooth 🍫)'
}

flavor_sub = {
    'A': {
        '1': 'เลมอน / ส้ม (Lemon / Orange)',
        '4': 'ทรอปิคอล ฟรุต / ช็อกโกแลต (Tropical / Chocolate)'
    },
    'B': {
        '2': 'เนคทารีน / พีช (Nectarine / Peach)',
        '5': 'ดอกไม้ / แบล็คที (Floral / Black Tea)'
    },
    'C': {
        '3': 'มิกซ์เบอร์รี / เบอร์กามอท (Mixed Berry / Bergamot)',
        '6': 'มะม่วงสุก (Ripe Mango)'
    }
}

coffee_bean = {
    'ETH': 'เอธิโอเปีย (Ethiopia)',
    'MCT': 'แม่จันใต้ (Mae Chan Tai, TH)'
}

brew_recipe = {
    '50': 'TDS 50 – เบา (Light Body)',
    '60': 'TDS 60 – สมดุล (Balanced)',
    '70': 'TDS 70 – เข้ม (Full Body)'
}

barista_rule = {
    ('A', '1'): {'bean': 'ETH', 'recipe': '50'},
    ('A', '4'): {'bean': 'MCT', 'recipe': '60'},
    ('B', '2'): {'bean': 'ETH', 'recipe': '60'},
    ('C', '6'): {'bean': 'MCT', 'recipe': '70'}
}

# ===============================
# Header
# ===============================
st.markdown("""
<div style="text-align:center;">
    <h2>☕ Coffee Recommendation System</h2>
    <p style="color:#6f4e37;">
        ระบบแนะนำกาแฟสำหรับหน้าร้าน<br>
        Smart Order • Consistent Quality
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===============================
# CUSTOMER VIEW
# ===============================
st.markdown("## 👤 ลูกค้าเลือกเมนูกาแฟ")

main_choice = st.radio(
    "เลือกรสชาติหลัก (Choose coffee style)",
    options=list(flavor_main.keys()),
    format_func=lambda x: flavor_main[x]
)

sub_choice = st.radio(
    "เลือกกลิ่นรส (Choose aroma profile)",
    options=list(flavor_sub[main_choice].keys()),
    format_func=lambda x: flavor_sub[main_choice][x]
)

# ===============================
# Order Summary
# ===============================
st.divider()
st.markdown("### 🧾 สรุปออเดอร์")

st.markdown(
    f"""
    <div style="
        background:#ffffff;
        padding:16px;
        border-radius:16px;
        border:1px solid #e0dcd7;
    ">
        <b>☕ รสชาติ</b><br>
        {flavor_main[main_choice]}<br><br>
        <b>🌿 กลิ่นรส</b><br>
        {flavor_sub[main_choice][sub_choice]}
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# Place Order
# ===============================
place_order = st.button("☕ ส่งออเดอร์ให้บาริสต้า", use_container_width=True)

if place_order:
    rule_key = (main_choice, sub_choice)

    if rule_key in barista_rule:
        rec = barista_rule[rule_key]
        st.session_state.orders.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "bean": coffee_bean[rec['bean']],
            "recipe": brew_recipe[rec['recipe']]
        })
        st.success("ส่งออเดอร์เรียบร้อย ☕")
    else:
        st.warning("ยังไม่มีสูตรที่เหมาะสม")

# ===============================
# BARISTA VIEW
# ===============================
st.divider()
st.markdown("## 👨‍🍳 หน้าจอบาริสต้า")

if st.session_state.orders:
    latest = st.session_state.orders[0]

    st.markdown(
        f"""
        <div style="
            background:#fff7e6;
            padding:16px;
            border-radius:16px;
        ">
            ⏰ <b>เวลา:</b> {latest['time']}<br><br>
            🌍 <b>เมล็ดกาแฟ:</b><br>
            {latest['bean']}<br><br>
            💧 <b>สูตรน้ำชง:</b><br>
            {latest['recipe']}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("รอออเดอร์จากลูกค้า…")

# ===============================
# OWNER VALUE
# ===============================
st.divider()
st.markdown("## 👨‍💼 มุมมองเจ้าของร้าน (Owner Insight)")

total_orders = len(st.session_state.orders)
st.write(f"📊 จำนวนออเดอร์วันนี้: **{total_orders} แก้ว**")

# ===============================
# Footer
# ===============================
st.divider()
st.markdown(
    "<p style='text-align:center; font-size:12px; color:gray;'>Commercial Demo – Coffee Shop System</p>",
    unsafe_allow_html=True
)
