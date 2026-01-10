import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 시스템 설정
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [3, 5, 23, 27, 34, 38]
if "bonus" not in st.session_state:
    st.session_state.bonus = 6
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS: 사진 속 광폭 황금색 버튼 디자인 완벽 구현
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) { text-align: center; }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 40px !important;
        width: 100% !important;
        max-width: 650px !important;
        height: 65px !important;
        border: 2px solid #fff !important;
        font-size: 22px !important;
        box-shadow: 0 8px 25px rgba(241, 196, 15, 0.5) !important;
        transition: 0.2s;
        margin-top: 20px;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 0 30px #f1c40f !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; font-size:2.8em;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 결과창 공 HTML (입체감 강화)
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

# [5] 물리 엔진 HTML (소환 속도를 대폭 늦춰서 하나씩 나오는 것을 확실히 보여줌)
html_template = """
<div style="background:#0e1117; border: 1px solid #333; border-radius:30px; padding:35px; display:flex; flex-direction:column; align-items:center; box-shadow: 0 20px 50px rgba(0,0,0,0.7);">
    <canvas id="lotto" width="460" height="380" style="background:transparent;"></canvas>
    <div style="color:#f1c40f; font-size:12px; font-weight:bold; margin-top:20px; letter-spacing:2px;">EXTRACTION COMPLETE</div>
    <div style="margin-top:10px; background:linear-gradient(180deg,#222,#000); padding:20px 50px; border-radius:60px; border:1.5px solid #555; display:flex; gap:12px; align-items:center; box-shadow: inset 0 3px 20px rgba(0,0,0,0.8);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:26px; margin:0 10px;">+</span> REPLACE_BONUS
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("lotto");
    const ctx = canvas.getContext("2d");
    const centerX = 230, centerY = 190, radius = 175;
    
    const pool = [];
    const activeBalls = [];
    let frameCount = 0;

    // 45개 전체 공 생성
    const colors = ["#f1c40f", "#3498db", "#e74c3c", "#95a5a6", "#2ecc71"];
    for(let i=1; i<=45; i++){
        pool.push({
            x: centerX, y: centerY - 10,
            vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18,
            r: 13, num: i, col: colors[Math.floor((i-1)/10)] || colors[4]
        });
    }

    function draw(){
        ctx.clearRect(0,0,460,380);
        
        // 원형 추출기 테두리
        ctx.beginPath(); ctx.arc(centerX, centerY, radius, 0, Math.PI*2);
        ctx.fillStyle = "#111"; ctx.fill(); ctx.strokeStyle = "#555"; ctx.lineWidth = 6; ctx.stroke();

        // [순차 소환 대폭 강화] 10프레임마다 하나씩 배출 (이제 확실히 하나씩 보입니다)
        if(pool.length > 0 && frameCount % 10 === 0){
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
            // 공 그리기
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let g = ctx.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
            g.addColorStop(0, "#fff"); g.addColorStop(1, b.col);
            ctx.fillStyle = g; ctx.fill();
            // 숫자 쓰기
            ctx.fillStyle = "black"; ctx.font = "bold 11px Arial"; ctx.textAlign = "center";
            ctx.fillText(b.num, b.x, b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

# HTML 데이터 주입
final_html = html_template.replace("REPLACE_BALLS", b_list_h).replace("REPLACE_BONUS", bonus_h)

# [6] 에러 원천 차단 (key 제거하여 TypeError 완벽 방지)
components.html(final_html, height=620)

# [7] 하단 분석 버튼
if st.button("✨ 분석 완료! (다시 시도)"):
    res = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(res[:6])
    st.session_state.bonus = res[6]
    st.session_state.rid += 1
    st.rerun()

# [8] 하단 차트
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_df = pd.DataFrame([50, 22, 27, 49, 21], index=["1-10", "11-20", "21-30", "31-40", "41-45"], columns=["가중치"])
st.bar_chart(chart_df)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
