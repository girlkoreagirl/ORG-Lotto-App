 import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 시스템 설정
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [11, 15, 16, 18, 33, 38]
if "bonus" not in st.session_state:
    st.session_state.bonus = 6
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS: 우측 이미지의 작고 빛나는 버튼 및 레이아웃 재현
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    
    /* 상단 장식 바 */
    .top-divider {
        width: 100%;
        height: 35px;
        background-color: #1a1c23;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 30px;
    }

    /* 우측 이미지 스타일의 작고 빛나는 버튼 */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        text-align: center;
        display: flex;
        justify-content: center;
    }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 40px !important;
        padding: 10px 40px !important;
        width: auto !important;
        height: 50px !important;
        border: 2px solid #fff !important;
        font-size: 16px !important;
        box-shadow: 0 0 20px rgba(241, 196, 15, 0.6) !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(241, 196, 15, 0.9) !important;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h1 style='text-align:center; color:white; font-size:2.5em; margin-bottom:0;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; margin-top:0;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# 상단 회색 바 (우측 이미지 재현)
st.markdown('<div class="top-divider"></div>', unsafe_allow_html=True)

# [4] 결과 공 HTML 조각
def get_c(n):
    if n<=10: return "#f1c40f"
    elif n<=20: return "#3498db"
    elif n<=30: return "#e74c3c"
    elif n<=40: return "#95a5a6"
    else: return "#2ecc71"

b_list_h = ""
for n in st.session_state.nums:
    b_list_h += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;margin:0 4px;box-shadow:0 3px 6px rgba(0,0,0,0.5);">'+str(n)+'</div>'

bonus_h = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(st.session_state.bonus)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;box-shadow:0 3px 6px rgba(0,0,0,0.5);">'+str(st.session_state.bonus)+'</div>'

# [5] 우측 이미지 스타일의 캔버스 및 결과바 (통합 컴포넌트)
html_animation = """
<div style="display:flex; flex-direction:column; align-items:center; font-family:sans-serif;">
    <canvas id="lotto" width="450" height="380" style="background:transparent;"></canvas>
    <div style="color:#666; font-size:11px; margin-top:20px; letter-spacing:1px; font-weight:bold;">AI PREDICTION RESULT</div>
    <div style="margin-top:10px; background:linear-gradient(180deg,#222,#000); padding:15px 45px; border-radius:60px; border:1px solid #444; display:flex; gap:10px; align-items:center; box-shadow: inset 0 2px 15px rgba(0,0,0,0.7);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:24px; margin:0 8px;">+</span> REPLACE_BONUS
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("lotto");
    const ctx = canvas.getContext("2d");
    const centerX = 225, centerY = 190, radius = 170;
    const pool = [], activeBalls = [];
    let frameCount = 0;

    const colors = ["#f1c40f", "#3498db", "#e74c3c", "#95a5a6", "#2ecc71"];
    for(let i=1; i<=45; i++){
        pool.push({
            x: centerX, y: centerY,
            vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18,
            r: 13, num: i, col: colors[Math.floor((i-1)/10)] || colors[4]
        });
    }

    function draw(){
        ctx.clearRect(0,0,450,380);
        ctx.beginPath(); ctx.arc(centerX, centerY, radius, 0, Math.PI*2);
        ctx.fillStyle = "#111"; ctx.fill(); ctx.strokeStyle = "#444"; ctx.lineWidth = 5; ctx.stroke();

        if(pool.length > 0 && frameCount % 6 === 0){
            activeBalls.push(pool.shift());
        }
        frameCount++;

        activeBalls.forEach(b => {
            b.x += b.vx; b.y += b.vy;
            const dist = Math.sqrt((b.x-centerX)**2 + (b.y-centerY)**2);
            if(dist + b.r > radius){
                const nx = (b.x-centerX)/dist, ny = (b.y-centerY)/dist;
                const dot = b.vx*nx + b.vy*ny;
                b.vx -= 2*dot*nx; b.vy -= 2*dot*ny;
                b.x = centerX + nx*(radius-b.r);
                b.y = centerY + ny*(radius-b.r);
            }
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let g = ctx.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
            g.addColorStop(0, "#fff"); g.addColorStop(1, b.col);
            ctx.fillStyle = g; ctx.fill();
            ctx.fillStyle = "black"; ctx.font = "bold 11px Arial"; ctx.textAlign = "center";
            ctx.fillText(b.num, b.x, b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

final_html = html_animation.replace("REPLACE_BALLS", b_list_h).replace("REPLACE_BONUS", bonus_h)
components.html(final_html, height=580)

# [6] 작고 빛나는 버튼 (우측 이미지 핵심)
if st.button("✨ 분석 완료! (다시 시도)"):
    res = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(res[:6])
    st.session_state.bonus = res[6]
    st.session_state.rid += 1
    st.rerun()

# [7] 하단 차트
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_df = pd.DataFrame([40, 42, 28, 23, 35], index=["1-10", "11-20", "21-30", "31-40", "41-45"], columns=["가중치"])
st.bar_chart(chart_df)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
