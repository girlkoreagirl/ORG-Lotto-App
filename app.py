import streamlit as st
import streamlit.components.v1 as components
import random

# [검증 1] 최상단 배치 확인
st.set_page_config(page_title="Fortune AI", layout="centered")

# [검증 2] session_state 안정성 확보 (딕셔너리 대신 개별 변수 사용)
if "nums" not in st.session_state:
    st.session_state.nums = [25, 28, 29, 36, 38, 39]
if "bonus" not in st.session_state:
    st.session_state.bonus = 22
if "rid" not in st.session_state:
    st.session_state.rid = 1

# [검증 3] CSS 적용 (골드 버튼 디자인 재현)
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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [검증 4] 입체감 있는 공 HTML 조립 (f-string 미사용)
def get_color(n):
    if n <= 10: return "#f1c40f"
    if n <= 20: return "#3498db"
    if n <= 30: return "#e74c3c"
    if n <= 40: return "#95a5a6"
    return "#2ecc71"

balls_html_part = ""
for n in st.session_state.nums:
    balls_html_part += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, ' + get_color(n) + ');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.5);">' + str(n) + '</div>'

bonus_html_part = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, ' + get_color(st.session_state.bonus) + ');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.5);">' + str(st.session_state.bonus) + '</div>'

# [검증 5] JS 중괄호 충돌 방지를 위한 템플릿 방식 (f-string 완전 배제)
html_template = """
<div style="background:#0e1117; border: 1px solid #333; border-radius:20px; padding:30px; display:flex; flex-direction:column; align-items:center;">
    <canvas id="lotto" width="400" height="350"></canvas>
    <div style="color:#f1c40f; font-size:12px; font-weight:bold; margin-top:15px; letter-spacing:1px;">EXTRACTION COMPLETE</div>
    <div style="margin-top:10px; background:linear-gradient(180deg, #222, #000); padding:15px 40px; border-radius:50px; border:1px solid #444; display:flex; gap:12px; align-items:center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);">
        REPLACE_BALLS <span style="color:white; font-weight:bold; font-size:20px; margin:0 5px;">+</span> REPLACE_BONUS
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
            x.beginPath(); x.arc(b.x,b.y,b.r,0,Math.PI*2);
            let g=x.createRadialGradient(b.x-4,b.y-4,2,b.x,b.y,b.r);
            g.addColorStop(0,'#fff'); g.addColorStop(1,b.col);
            x.fillStyle=g; x.fill();
            // [검증 완료] 공 숫자 표시 로직 탑재
            x.fillStyle='black'; x.font='bold 10px Arial'; x.textAlign='center'; x.fillText(b.num, b.x, b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

# 데이터 주입
final_html = html_template.replace("REPLACE_BALLS", balls_html_part).replace("REPLACE_BONUS", bonus_html_part)

# [검증 6] TypeError 방지를 위한 Key 문자열 강제 결합
components.html(final_html, height=550, key="v_" + str(st.session_state.rid))

if st.button("✨ 다시 분석하기"):
    r = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(r[:6])
    st.session_state.bonus = r[6]
    st.session_state.rid += 1
    st.rerun()

st.markdown("""
<div style="background-color: #0b1a2a; border-radius: 5px; padding: 15px; margin-top: 20px;">
    <p style="color: #3498db; margin: 0; font-
