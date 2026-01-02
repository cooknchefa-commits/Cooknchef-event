import streamlit as st
from datetime import datetime, timedelta

# ==========================================
# 👇 [설정] 구글폼 주소
# ==========================================
URL_1 = "https://cooknchefnews.com/news/view/1065578321085578" # 1라운드 기사
URL_2 = "https://cooknchefnews.com/news/view/1065578393220176" # 2라운드 기사
# ==========================================

# 날짜별 암호
DAILY_CODES = {
    "2026-01-02": "COOK",   "2026-01-03": "CHEF",
    "2026-01-04": "FOOD",   "2026-01-05": "TASTE",
    "2026-01-06": "YUMMY",  "2026-01-07": "WINNER",
    "2026-01-08": "MASTER", "2026-01-09": "LEGEND",
    "2026-01-10": "GLOBAL", "2026-01-11": "TOP",
    "2026-01-12": "FINAL",  "2026-01-13": "VICTORY",
    "default": "COOK"
}

# 한국 시간 계산
now = datetime.utcnow() + timedelta(hours=9)
today_str = now.strftime("%Y-%m-%d")

# 기간 설정
ROUND1_END = datetime(2026, 1, 6, 17, 0)
ROUND2_START = datetime(2026, 1, 7, 0, 0)
ROUND2_END = datetime(2026, 1, 13, 17, 0)

target_url = URL_1 
status_msg = "1라운드 진행 중"
round_color = "#E11D48"

if now <= ROUND1_END:
    target_url = URL_1
    status_msg = "1라운드 (결승 진출자 예측)"
elif now >= ROUND2_START and now <= ROUND2_END:
    target_url = URL_2
    status_msg = "2라운드 (최종 우승자 예측)"
    round_color = "#2563EB"
elif now > ROUND2_END:
    status_msg = "종료"

# --- 스타일 (공통) ---
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{padding: 2rem 1rem !important;}}
    .big-code {{font-size: 50px; font-weight: 900; color: {round_color}; text-align: center; margin: 10px 0; letter-spacing: 2px;}}
    .info {{text-align: center; color: #555; margin-bottom: 20px; font-size: 16px;}}
    .stButton>button {{width: 100%; background-color: {round_color}; color: white; height: 55px; font-size: 20px; border-radius: 10px; font-weight: bold; border: none;}}
    .stButton>button:hover {{opacity: 0.9;}}
    </style>
    """, unsafe_allow_html=True)

today_code = DAILY_CODES.get(today_str, DAILY_CODES["default"])

if status_msg == "종료":
    st.error("🏁 이벤트가 종료되었습니다.")
    st.stop()

# ==========================================
# 👇 [핵심] 모드 결정 로직 (?mode=input)
# ==========================================
query_params = st.query_params
mode = query_params.get("mode", "billboard") # 기본값은 전광판

if mode == "input":
    # ----------------------------------
    # [모드 2] 입력창 (검문소)
    # ----------------------------------
    st.markdown(f"<h4 style='text-align:center;'>🔐 이벤트 입장하기</h4>", unsafe_allow_html=True)
    st.markdown(f"<p class='info'>기사에서 확인한 <b>오늘의 코드</b>를 입력하세요.</p>", unsafe_allow_html=True)
    
    with st.form("check_form"):
        user_input = st.text_input("코드 입력", placeholder="코드를 입력하세요")
        submitted = st.form_submit_button("입력 확인")

    if submitted:
        if user_input.upper().strip() == today_code:
            st.success("✅ 인증 성공! 아래 버튼을 누르세요.")
            st.link_button("🚀 접수하러 가기 (Click)", target_url)
        else:
            st.error("❌ 코드가 틀렸습니다. 기사를 다시 확인하세요.")

else:
    # ----------------------------------
    # [모드 1] 전광판 (기본 화면)
    # ----------------------------------
    st.markdown(f"<h4 style='text-align:center; color:#666;'>📅 {today_str} 오늘의 코드</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-code'>{today_code}</div>", unsafe_allow_html=True)
    st.markdown(f"<p class='info'><b>{status_msg}</b><br>이 코드를 기억하고 하단 배너를 클릭하세요!</p>", unsafe_allow_html=True)
