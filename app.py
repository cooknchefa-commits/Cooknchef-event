import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# --- [설정 1] 사장님이 구글폼 주소 넣을 곳 ---
URL_1 = "https://cooknchefnews.com/news/view/1065578321085578"
URL_2 = "https://cooknchefnews.com/news/view/1065578393220176"

# --- [설정 2] 날짜별 암호 (1월 13일까지 완벽 세팅) ---
# 구글폼 응답확인(정규식)에는 아래 단어들을 다 넣어두면 좋지만,
# 귀찮으면 그냥 Streamlit 믿고 안 해도 됩니다. (서버가 막아주니까요)
DAILY_CODES = {
    # 1라운드 (결승 진출자)
    "2026-01-02": "COOK",   "2026-01-03": "CHEF",
    "2026-01-04": "FOOD",   "2026-01-05": "TASTE",
    "2026-01-06": "YUMMY",
    
    # 2라운드 (최종 우승자) - 승리 관련 단어들
    "2026-01-07": "WINNER", "2026-01-08": "MASTER",
    "2026-01-09": "LEGEND", "2026-01-10": "GLOBAL",
    "2026-01-11": "TOP",    "2026-01-12": "FINAL",
    "2026-01-13": "VICTORY",
    
    "default": "COOK" # 혹시 설정 안 된 날짜용
}

# --- [설정 3] 기간 세팅 (자동 분기점) ---
KST = ZoneInfo("Asia/Seoul")
# 1라운드 종료: 1월 6일 오후 5시
ROUND1_END = datetime(2026, 1, 6, 17, 0, tzinfo=KST)
# 2라운드 시작: 1월 7일 0시
ROUND2_START = datetime(2026, 1, 7, 0, 0, tzinfo=KST)
# 2라운드 종료: 1월 13일 오후 5시
ROUND2_END = datetime(2026, 1, 13, 17, 0, tzinfo=KST)

# --- [로직] 날짜 계산 및 라우팅 ---
now = datetime.now(KST)
today_str = now.strftime("%Y-%m-%d")
today_code = DAILY_CODES.get(today_str, DAILY_CODES["default"])

target_url = None
status_msg = ""
round_color = "#E11D48" # 기본 빨강

if now <= ROUND1_END:
    target_url = URL_1
    status_msg = "1라운드 (결승 진출자 예측)"
    round_color = "#E11D48" # 1라운드 빨강
elif ROUND2_START <= now <= ROUND2_END:
    target_url = URL_2
    status_msg = "2라운드 (최종 우승자 예측)"
    round_color = "#2563EB" # 2라운드 파랑 (구분되게)
else:
    status_msg = "종료"

# --- [화면] 디자인 및 기능 ---
st.markdown(f"""
    <style>
    .big-code {{font-size: 45px; font-weight: 900; color: {round_color}; text-align: center; margin: 0; letter-spacing: 2px;}}
    .info {{text-align: center; color: #555; margin-bottom: 20px; font-size: 15px;}}
    .stButton>button {{width: 100%; background-color: {round_color}; color: white; height: 55px; font-size: 20px; border-radius: 10px; font-weight: bold; border: none;}}
    .stButton>button:hover {{opacity: 0.9;}}
    </style>
    """, unsafe_allow_html=True)

# 1. 종료 시 차단
if status_msg == "종료":
    st.error("🏁 이벤트 기간이 모두 종료되었습니다.")
    st.stop()

# 2. 전광판 (기사 중간에 보일 때 예쁨)
st.markdown(f"<h4 style='text-align:center; margin:0; color:#666;'>📅 {today_str} 오늘의 코드</h4>", unsafe_allow_html=True)
st.markdown(f"<div class='big-code'>{today_code}</div>", unsafe_allow_html=True)
st.markdown(f"<p class='info'>현재 <b>{status_msg}</b> 진행 중!<br>아래 창에 코드를 입력하세요.</p>", unsafe_allow_html=True)

# 3. 검문소 (입력해야 버튼 줌)
user_input = st.text_input("코드 입력", placeholder="여기에 코드를 입력하세요", label_visibility="collapsed")

if user_input:
    if user_input.upper().strip() == today_code:
        st.success("✅ 인증 성공! 아래 버튼이 생성되었습니다.")
        st.markdown(f"⬇️ **버튼을 눌러 {status_msg} 접수하기** ⬇️")
        st.link_button("🚀 구글폼으로 이동하기 (Click)", target_url)
    else:
        st.error("❌ 코드가 틀렸거나, 유효기간(어제 코드)이 지났습니다.")