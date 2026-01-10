import streamlit as st
import streamlit.components.v1 as components
import random

# [1] 최상단 설정
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 상태 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [25, 28, 29, 36, 38, 39]
    st.session_state.bonus = 22
    st.session_state.rid = 0

# [3] CSS: 왼쪽 이미지의 골드 버튼 및 다크 테마 완벽 재현
st.markdown("""
<style>
    .main { background-color: #000000; }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        width: 100% !important;
        height: 55px !important;
        border: none !important;
        font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(241, 196, 15, 0.4) !important;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 0 20px #f1c40f !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white; font-size:2.5em;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 결과 바 HTML 생성 (색상 입체감 반영)
def get_color(n):
    if n <= 10: return "#f1c40f"
    if n <= 20: return "#3498db"
    if n <= 30: return "#e74c3c"
    if n <= 40: return "#95a5a6"
    return "#2ecc71"

balls_html = ""
for n in st.session_state.nums:
    balls_html += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, '+get_color(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.5);">'+str(n)+'</div>'

bonus_html = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, '+get_color(st.session_state.bonus)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.5);">'+str(st.session_state.bonus)+'</div>'

# [5] 물리 엔진 + 사운드 + 공 숫자 (JS 중괄호 충돌 방지 구조)
html_start = """
<div style="background:#0e1117; border: 1px solid #333; border-radius:20px; padding:30px; display:flex; flex-direction:column; align-items:center;">
    <canvas id="lotto" width="400" height="350"></canvas>
    <div style="color:#f1c40f; font-size:12px; font-weight:bold; margin-top:15px; letter-spacing:1px;">EXTRACTION COMPLETE</div>
    <div style="margin-top:10px; background:linear-gradient(180deg, #222, #000); padding:15px 40px; border-radius:50px; border:1px solid #444; display:flex; gap:12px; align-items:center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);">
"""
html_mid = balls_html + '<span style="color:white; font-weight:bold; font-size:20px; margin:0 5px;">+</span>' + bonus_html
html_end = """
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const c=document.getElementById('lotto'), x=c.getContext('2d'), balls=[];
    const colors=['#f1c40f','#3498db','#e74c3c','#95a5a6','#2ecc71'];
    for(let i=1; i<=45; i++){
        balls.push({
            x:200+(Math.random()-0.5)*100, y:175+(Math.random()-0.5)*100,
            vx:(Math.random()-0.5)*16, vy:(Math.random()-0.5)*16,
            r:12, num:i, col:colors[Math.floor((i-1)/10)] || colors[4]
        });
    }
    function draw(){
        x.clearRect(0,0,400,350);
        x.beginPath(); x.arc(200,175,150,0,Math.PI*2); x.fillStyle='#111'; x.fill(); x.strokeStyle='#444'; x.lineWidth=4; x.stroke();
        balls.forEach(b => {
            b.x+=b.vx; b.y+=b.vy;
            const d=Math.sqrt((b.x-200)**2+(b.y-175)**2);
            if(d+b.r>150){
                const nx=(b.x-200)/d, ny=(b.y-175)/d, dot=b.vx*nx+b.vy*ny;
                b.vx-=2*dot*nx; b.vy-=2*dot*ny;
                b.x=200+nx*(150-b.r); b.y=175+ny*(150-b.r);
            }
            // 공 그리기
            x.beginPath(); x.arc(b.x,b.y,b.r,0,Math.PI*2);
            let g=x.createRadialGradient(b.x-4,b.y-4,2,b.x,b.y,b.r);
            g.addColorStop(0,'#fff'); g.addColorStop(1,b.col);
            x.fillStyle=g; x.fill();
            // 공에 숫자 쓰기 (추가된 부분)
            x.fillStyle='black'; x.font='bold 10px Arial'; x.textAlign='center'; x.fillText(b.num, b.x, b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

final_html = html_start + html_mid + html_end
components.html(final_html, height=550, key="v_"+str(st.session_state.rid))

# [6] 하단 분석 버튼
if st.button("✨ 다시 분석하기"):
    r = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(r[:6])
    st.session_state.bonus = r[6]
    st.session_state.rid += 1
    st.rerun()

# [7] 하단 안내문 (이미지와 동일하게)
st.markdown("""
<div style="background-color: #0b1a2a; border-radius: 5px; padding: 15px; margin-top: 20px;">
    <p style="color: #3498db; margin: 0; font-size: 0.9em;">💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.</p>
</div>
""", unsafe_allow_html=True)
