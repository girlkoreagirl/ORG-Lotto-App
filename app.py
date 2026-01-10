import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 최상단 설정 - 모든 에러 방지의 시작
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화 - 타입을 명확히 고정
if "nums" not in st.session_state:
    st.session_state.nums = [4, 12, 15, 37, 39, 44]
if "bonus" not in st.session_state:
    st.session_state.bonus = 33
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS 스타일 (사진 속 골드 디자인 완벽 재현)
st.markdown("""
<style>
    .main { background-color: #000 !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) { text-align: center; }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        width: 100% !important;
        max-width: 500px !important;
        height: 60px !important;
        border: 2px solid #fff !important;
        font-size: 20px !important;
        box-shadow: 0 4px 15px rgba(241, 196, 15, 0.5) !important;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 공 색상 및 HTML 조립 로직 (f-string 대신 고전적 방식 사용)
def get_ball_color(n):
    if n <= 10: return "#f1c40f"
    elif n <= 20: return "#3498db"
    elif n <= 30: return "#e74c3c"
    elif n <= 40: return "#95a5a6"
    else: return "#2ecc71"

# 번호 공들을 HTML 문자열로 미리 생성
b_list_html = ""
for n in st.session_state.nums:
    b_list_html += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,' + get_ball_color(n) + ');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;margin:0 2px;box-shadow:0 2px 5px rgba(0,0,0,0.5);">' + str(n) + '</div>'

bonus_html = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,' + get_ball_color(st.session_state.bonus) + ');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.5);">' + str(st.session_state.bonus) + '</div>'

# [5] 물리 엔진 HTML 템플릿 (자바스크립트 중괄호 보호를 위해 분리)
html_template = """
<div style="background:#0e1117;border:1px solid #333;border-radius:20px;padding:30px;display:flex;flex-direction:column;align-items:center;">
    <canvas id="lottoCanvas" width="400" height="350"></canvas>
    <div style="color:#666; font-size:10px; margin-top:15px; letter-spacing:1px;">AI PREDICTION RESULT</div>
    <div style="margin-top:5px;background:linear-gradient(180deg,#222,#000);padding:15px 40px;border-radius:50px;border:1px solid #444;display:flex;gap:12px;align-items:center;">
        NUMS_PART <span style="color:white;font-weight:bold;font-size:20px;">+</span> BONUS_PART
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("lottoCanvas");
    const ctx = canvas.getContext("2d");
    const balls = [];
    const colors = ["#f1c40f", "#3498db", "#e74c3c", "#95a5a6", "#2ecc71"];

    for(let i=1; i<=45; i++){
        balls.push({
            x: 200 + (Math.random()-0.5)*100,
            y: 175 + (Math.random()-0.5)*100,
            vx: (Math.random()-0.5)*16,
            vy: (Math.random()-0.5)*16,
            r: 12,
            num: i,
            col: colors[Math.floor((i-1)/10)] || colors[4]
        });
    }

    function draw(){
        ctx.clearRect(0,0,400,350);
        ctx.beginPath();
        ctx.arc(200, 175, 150, 0, Math.PI*2);
        ctx.fillStyle = "#111";
        ctx.fill();
        ctx.strokeStyle = "#444";
        ctx.lineWidth = 4;
        ctx.stroke();

        balls.forEach(b => {
            b.x += b.vx; b.y += b.vy;
            const dist = Math.sqrt((b.x-200)**2 + (b.y-175)**2);
            if(dist + b.r > 150){
                const nx = (b.x-200)/dist;
                const ny = (b.y-175)/dist;
                const dot = b.vx*nx + b.vy*ny;
                b.vx -= 2*dot*nx;
                b.vy -= 2*dot*ny;
                b.x = 200 + nx*(150-b.r);
                b.y = 175 + ny*(150-b.r);
            }
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let grad = ctx.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
            grad.addColorStop(0, "#fff");
            grad.addColorStop(1, b.col);
            ctx.fillStyle = grad;
            ctx.fill();
            
            // 공에 숫자 쓰기 (사진처럼 구현)
            ctx.fillStyle = "black";
            ctx.font = "bold 10px Arial";
            ctx.textAlign = "center";
            ctx.fillText(b.num, b.x, b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

# 문자열 치환을 통한 데이터 주입
final_html_code = html_template.replace("NUMS_PART", b_list_html).replace("BONUS_PART", bonus_html)

# [6] 에러 발생 원인(key) 완전 격리
# key에 들어갈 문자열을 미리 변수로 빼서, 함수 호출 시 연산이 일어나지 않게 함
my_key = "lotto_v_" + str(st.session_state.rid)

# components.html 호출 (가장 안전한 형태)
components.html(final_html_code, height=550, key=my_key)

# [7] 실행 버튼 (사진의 골드 버튼 스타일)
if st.button("✨ 분석 완료! (다시 시도)"):
    selected = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(selected[:6])
    st.session_state.bonus = selected[6]
    st.session_state.rid += 1
    st.rerun()

# [8] 하단 차트
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_data = pd.DataFrame([random.randint(15, 50) for _ in range(5)], 
                          index=["1-10", "11-20", "21-30", "31-40", "41-45"], 
                          columns=["Weight"])
st.bar_chart(chart_data)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
