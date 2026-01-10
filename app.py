import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 시스템 설정 - 빈칸 없는 최상단 배치
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [5, 9, 14, 15, 19, 39]
if "bonus" not in st.session_state:
    st.session_state.bonus = 36
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS: 사진 속 통합 박스 디자인 및 와이드 황금 버튼 완벽 구현
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    /* 전체 요소를 감싸는 프리미엄 카드 박스 */
    .premium-card {
        background-color: #0e1117;
        border: 2px solid #333;
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        text-align: center;
        margin-bottom: 30px;
    }
    /* 박스 안 하단에 위치한 넓고 화려한 버튼 */
    div.stButton > button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 40px !important;
        width: 100% !important;
        max-width: 600px !important;
        height: 65px !important;
        border: 2px solid #fff !important;
        font-size: 22px !important;
        box-shadow: 0 8px 25px rgba(241, 196, 15, 0.4) !important;
        transition: 0.2s;
        margin: 10px auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; font-size:2.8em;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 결과 공 HTML 조각 생성
def get_c(n):
    if n<=10: return "#f1c40f"
    elif n<=20: return "#3498db"
    elif n<=30: return "#e74c3c"
    elif n<=40: return "#95a5a6"
    else: return "#2ecc71"

b_list_h = ""
for n in st.session_state.nums:
    b_list_h += '<div style="width:42px;height:42px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;margin:0 5px;box-shadow:0 4px 8px rgba(0,0,0,0.6);">'+str(n)+'</div>'

bonus_h = '<div style="width:42px;height:42px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(st.session_state.bonus)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;box-shadow:0 4px 8px rgba(0,0,0,0.6);">'+str(st.session_state.bonus)+'</div>'

# [5] 물리 엔진 HTML (중앙에서 하나씩 배출되는 Sequential Spawning 로직)
html_template = """
<div style="display:flex; flex-direction:column; align-items:center; font-family:sans-serif;">
    <canvas id="l" width="460" height="380" style="background:transparent;"></canvas>
    <div style="color:#666; font-size:11px; margin-top:20px; letter-spacing:1px; font-weight:bold;">AI PREDICTION RESULT</div>
    <div style="margin-top:10px; background:linear-gradient(180deg,#222,#000); padding:20px 50px; border-radius:60px; border:1.5px solid #555; display:flex; gap:12px; align-items:center; box-shadow: inset 0 3px 20px rgba(0,0,0,0.8);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:26px; margin:0 10px;">+</span> REPLACE_BONUS
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("l");
    const ctx = canvas.getContext("2d");
    const centerX = 230, centerY = 190, radius = 175;
    
    const pool = [];
    const activeBalls = [];
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
        ctx.clearRect(0,0,460,380);
        ctx.beginPath(); ctx.arc(centerX, centerY, radius, 0, Math.PI*2);
        ctx.fillStyle = "#111"; ctx.fill(); ctx.strokeStyle = "#555"; ctx.lineWidth = 6; ctx.stroke();

        // [순차 배출 로직] 8프레임마다 하나씩 중앙에서 톡 튀어나오게 함
        if(pool.length > 0 && frameCount % 8 === 0){
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

final_html = html_template.replace("REPLACE_BALLS", b_list_h).replace("REPLACE_BONUS", bonus_h)

# [6] 통합 박스 레이아웃 출력
with st.container():
    # 상단 카드 시작
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    # 1. 애니메이션 & 결과 바
    components.html(final_html, height=620)
    
    # 2. 분석 완료 버튼 (박스 내부 배치)
    if st.button("✨ 분석 완료! (다시 시도)"):
        res = random.sample(range(1, 46), 7)
        st.session_state.nums = sorted(res[:6])
        st.session_state.bonus = res[6]
        st.session_state.rid += 1
        st.rerun()
    
    # 상단 카드 끝
    st.markdown('</div>', unsafe_allow_html=True)

# [7] 하단 차트 (사진 데이터 유지)
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_df = pd.DataFrame([50, 22, 27, 49, 21], index=["1-10", "11-20", "21-30", "31-40", "41-45"], columns=["가중치"])
st.bar_chart(chart_df)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
