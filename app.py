import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 시스템 설정
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [12, 24, 30, 32, 36, 42]
if "bonus" not in st.session_state:
    st.session_state.bonus = 40
if "rid" not in st.session_state:
    st.session_state.rid = 0

# [3] CSS: 전체 요소를 하나의 박스로 묶고 버튼 디자인 적용
st.markdown("""
<style>
    .main { background-color: #0e1117 !important; }
    /* 전체를 감싸는 프리미엄 박스 스타일 */
    .premium-container {
        background-color: #0e1117;
        border: 1px solid #333;
        border-radius: 25px;
        padding: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        text-align: center;
    }
    /* 버튼 스타일 (박스 안 하단 배치) */
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 35px !important;
        width: 100% !important;
        max-width: 550px !important;
        height: 60px !important;
        border: 2px solid #fff !important;
        font-size: 20px !important;
        box-shadow: 0 6px 20px rgba(241, 196, 15, 0.4) !important;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; font-size:2.8em;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 결과 공 HTML 조각 (색상 및 입체감)
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

# [5] 물리 엔진 HTML (공이 하나씩 중앙에서 튀어나오는 로직)
# 디자인을 유지하기 위해 별도의 div 없이 카드 내부 구성품으로 제작
html_content = """
<div style="display:flex; flex-direction:column; align-items:center; font-family:sans-serif;">
    <canvas id="lotto" width="450" height="360" style="background:transparent;"></canvas>
    <div style="color:#666; font-size:11px; margin-top:15px; letter-spacing:1px; font-weight:bold;">AI PREDICTION RESULT</div>
    <div style="margin-top:8px; background:linear-gradient(180deg,#222,#000); padding:18px 45px; border-radius:60px; border:1px solid #444; display:flex; gap:10px; align-items:center; box-shadow: inset 0 2px 15px rgba(0,0,0,0.7);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:24px; margin:0 8px;">+</span> REPLACE_BONUS
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById("lotto");
    const ctx = canvas.getContext("2d");
    const centerX = 225, centerY = 180, radius = 165;
    
    const pool = [];
    const activeBalls = [];
    let frameCount = 0;

    // 45개 공 데이터를 풀에 준비
    const colors = ["#f1c40f", "#3498db", "#e74c3c", "#95a5a6", "#2ecc71"];
    for(let i=1; i<=45; i++){
        pool.push({
            x: centerX, y: centerY,
            vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18,
            r: 13, num: i, col: colors[Math.floor((i-1)/10)] || colors[4]
        });
    }

    function draw(){
        ctx.clearRect(0,0,450,360);
        
        // 원형 통 배경
        ctx.beginPath(); ctx.arc(centerX, centerY, radius, 0, Math.PI*2);
        ctx.fillStyle = "#111"; ctx.fill(); ctx.strokeStyle = "#444"; ctx.lineWidth = 5; ctx.stroke();

        // [순차 배출 로직] 5프레임마다 공 하나씩 중앙에서 발사
        if(pool.length > 0 && frameCount % 5 === 0){
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
            // 공 렌더링
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

# HTML 데이터 치환
final_html = html_content.replace("REPLACE_BALLS", b_list_h).replace("REPLACE_BONUS", bonus_h)

# [6] 메인 인터페이스 (통합 박스 구현)
with st.container():
    # CSS 클래스를 적용하기 위해 HTML로 컨테이너 시작
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    
    # 애니메이션 및 결과 바
    components.html(final_html, height=520)
    
    # 같은 네모 칸 안에 들어가는 버튼
    if st.button("✨ 분석 완료! (다시 시도)"):
        res = random.sample(range(1, 46), 7)
        st.session_state.nums = sorted(res[:6])
        st.session_state.bonus = res[6]
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# [7] 하단 차트
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_df = pd.DataFrame([42, 45, 28, 23, 35], index=["1-10", "11-20", "21-30", "31-40", "41-45"], columns=["가중치"])
st.bar_chart(chart_df)

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
