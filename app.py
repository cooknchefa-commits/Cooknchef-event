import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================
# 👇 [여기만 수정] 기사 주소든 폼 주소든 여기에 넣으세요!
# ==========================================
URL_1 = "https://cooknchefnews.com/news/view/1065578321085578"  # 1라운드 기사
URL_2 = "https://cooknchefnews.com/news/view/1065578393220176"  # 2라운드 기사
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

# 한국 시간 및 기간 설정
KST = ZoneInfo("Asia/Seoul")
ROUND1_END = datetime(2026, 1, 6, 17, 0, tzinfo=KST)
ROUND2_START = datetime(2026, 1, 7, 0, 0, tzinfo=KST)
ROUND2_END = datetime(2026, 1, 13, 17, 0, tzinfo=KST)

# 로직 시작
now = datetime.now(KST)
today_str = now.strftime("%Y-%m-%d")
today_code = DAILY_CODES.get(today_str, DAILY_CODES["default"])

target_url = None
status_msg = ""
round_color = "#E11D48"

if now <= ROUND1_END:
    target_url = URL_1
    status_msg = "1라운드 (결승 진출자 예측)"
elif ROUND2_START <= now <= ROUND2_END:
    target_url = URL_2
    status_msg = "2라운드 (최종 우승자 예측)"
    round_color = "#2563EB"
else:
    status_msg = "종료"

# 화면 디자인
st.markdown(f"""
    <style>
    .big-code {{font-size: 45px; font-weight: 900; color: {round_color}; text-align: center; margin: 0; letter-spacing: 2px;}}
    .info {{text-align: center; color: #555; margin-bottom: 20px; font-size: 15px;}}
    .stButton>button {{width: 100%; background-color: {round_color}; color: white; height: 50px; font-size: 18px; border-radius: 10px; font-weight: bold; border: none;}}
    .stButton>button:hover {{opacity: 0.9;}}
    </style>
    """, unsafe_allow_html=True)

if status_msg == "종료":
    st.error("🏁 이벤트 기간이 종료되었습니다.")
    st.stop()

# 전광판
st.markdown(f"<h4 style='text-align:center; margin:0; color:#666;'>📅 {today_str} 오늘의 코드</h4>", unsafe_allow_html=True)
st.markdown(f"<div class='big-code'>{today_code}</div>", unsafe_allow_html=True)
st.markdown(f"<p class='info'>현재 <b>{status_msg}</b> 진행 중!<br>아래에 코드를 입력하고 [확인]을 누르세요.</p>", unsafe_allow_html=True)

# 👇 [수정됨] 입력창을 폼(Form)으로 감싸서 '확인' 버튼을 강제로 만듦
with st.form("check_form"):
    user_input = st.text_input("코드 입력", placeholder="여기에 코드를 입력하세요")
    # 엔터 쳐도 되고, 이 버튼 눌러도 됨 (확실한 방법)
    submitted = st.form_submit_button("입력 확인")

if submitted or user_input:
    if user_input.upper().strip() == today_code:
        st.success("✅ 인증 성공! 아래 버튼이 생성되었습니다.")
        st.markdown(f"⬇️ **버튼을 눌러 접수 페이지로 이동** ⬇️")
        # 여기가 빨간 버튼 (URL로 이동)
        st.link_button("🚀 이동하기 (클릭)", target_url)
    else:
        st.error("❌ 코드가 틀렸거나, 유효기간이 지났습니다.")
