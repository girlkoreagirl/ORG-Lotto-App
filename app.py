import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 시스템 설정 - 안정성 최우선
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [3, 5, 23, 27, 34, 38]
if "bonus" not in st.session_state:
    st.session_state.bonus = 6
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS: 왼쪽 사진의 와이드 골드 버튼 디자인 100% 복원
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) { text-align: center; }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        width: 100% !important;
        max-width: 600px !important;
        height: 60px !important;
        border: 2px solid #fff !important;
        font-size: 20px !important;
        box-shadow: 0 6px 20px rgba(241, 196, 15, 0.4) !important;
        transition: 0.2s;
    }
    .stButton>button:hover { transform: scale(1.01); background: #f1c40f !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; font-size:2.8em;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 결과 공 HTML 조각 생성 (입체감 있는 디자인)
def get_c(n):
    if n<=10: return "#f1c40f"
    elif n<=20: return "#3498db"
    elif n<=30: return "#e74c3c"
    elif n<=40: return "#95a5a6"
    else: return "#2ecc71"

b_list_h = ""
for n in st.session_state.nums:
    b_list_h += '<div style="width:40px;height:40px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;margin:0 4px;box-shadow:0 3px 6px rgba(0,0,0,0.5);">'+str(n)+'</div>'

bonus_h = '<div style="width:40px;height:40px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(st.session_state.bonus)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;box-shadow:0 3px 6px rgba(0,0,0,0.5);">'+str(st.session_state.bonus)+'</div>'

# [5] 물리 엔진 HTML (45개 공이 한 번에 배출되어 회전하는 로직)
html_template = """
<div style="background:#0e1117; border: 1px solid #333; border-radius:25px; padding:30px; display:flex; flex-direction:column; align-items:center; box-shadow: 0 15px 40px rgba(0,0,0,0.6);">
    <canvas id="lotto" width="450" height="380" style="background:transparent;"></canvas>
    <div style="color:#666; font-size:11px; margin-top:15px; letter-spacing:1px; font-weight:bold;">AI PREDICTION RESULT</div>
    <div style="margin-top:8px; background:linear-gradient(180deg,#222,#000); padding:18px 50px; border-radius:60px; border:1px solid #444; display:flex; gap:10px; align-items:center; box-shadow: inset 0 2px 15px rgba(0,0,0,0.7);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:24px; margin:0 8px;">+</span> REPLACE_BONUS
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("lotto");
    const ctx = canvas.getContext("2d");
    const centerX = 225, centerY = 190, radius = 170;
    const balls = [];

    // [반성 반영] 시작하자마자 45개 공이 한 번에 배출됨
    const colors = ["#f1c40f", "#3498db", "#e74c3c", "#95a5a6", "#2ecc71"];
    for(let i=1; i<=45; i++){
        balls.push({
            x: centerX + (Math.random()-0.5)*50,
            y: centerY + (Math.random()-0.5)*50,
            vx: (Math.random()-0.5)*20, 
            vy: (Math.random()-0.5)*20,
            r: 13, num: i, col: colors[Math.floor((i-1)/10)] || colors[4]
        });
    }

    function draw(){
        ctx.clearRect(0,0,450,380);
        
        // 원형 추출기 배경 (프리미엄 다크)
        ctx.beginPath(); ctx.arc(centerX, centerY, radius, 0, Math.PI*2);
        ctx.fillStyle = "#111"; ctx.fill(); ctx.strokeStyle = "#444"; ctx.lineWidth = 5; ctx.stroke();

        balls.forEach(b => {
            b.x += b.vx; b.y += b.vy;
            const dist = Math.sqrt((b.x-centerX)**2 + (b.y-centerY)**2);
            if(dist + b.r > radius){
                const nx = (b.x-centerX)/dist, ny = (b.y-centerY)/dist;
                const dot = b.vx*nx + b.vy*ny;
                b.vx -= 2*dot*nx; b.vy -= 2*dot*ny;
                b.x = centerX + nx*(radius-b.r);
                b.y = centerY + ny*(radius-b.r);
            }
            // 공 렌더링 (숫자 포함)
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

# HTML 안전 결합 (replace 방식)
final_html = html_template.replace("REPLACE_BALLS", b_list_h).replace("REPLACE_BONUS", bonus_h)

# [6] 에러 원천 차단
components.html(final_html, height=580)

# [7] 하단 분석 버튼 (와이드 황금색 디자인)
if st.button("✨ 분석 완료! (다시 시도)"):
    res = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(res[:6])
    st.session_state.bonus = res[6]
    st.session_state.rid += 1
    st.rerun()

# [8] 하단 차트 (사진 스타일 그대로 유지)
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_df = pd.DataFrame([50, 22, 27, 49, 21], index=["1-10", "11-20", "21-30", "31-40", "41-45"], columns=["가중치"])
st.bar_chart(chart_df)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
