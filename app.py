import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 초기 설정
st.set_page_config(page_title="Fortune AI", layout="centered")

# 2. 데이터 초기화
if "nums" not in st.session_state:
    st.session_state.nums = [25, 28, 29, 36, 38, 39]
    st.session_state.bonus = 22
    st.session_state.rid = 1

# 3. 스타일 설정
st.markdown("<style>.main {background-color:#000;}.stButton>button {background:linear-gradient(#f1c40f,#d4ac0d)!important;color:black!important;font-weight:bold!important;border-radius:30px!important;width:100%!important;height:55px!important;border:none!important;font-size:18px!important;box-shadow:0 4px 15px rgba(241,196,15,0.4)!important;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:white;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# 4. 결과바 공 생성 함수
def get_c(n):
    if n<=10: return "#f1c40f"
    if n<=20: return "#3498db"
    if n<=30: return "#e74c3c"
    if n<=40: return "#95a5a6"
    return "#2ecc71"

b_html = ""
for n in st.session_state.nums:
    b_html += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;margin:0 2px;">'+str(n)+'</div>'
bonus_h = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(st.session_state.bonus)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid white;">'+str(st.session_state.bonus)+'</div>'

# 5. 애니메이션 (에러의 주범인 중괄호 충돌을 피하기 위해 + 결합 사용)
html_start = '<div style="background:#0e1117;border:1px solid #333;border-radius:20px;padding:30px;display:flex;flex-direction:column;align-items:center;"><canvas id="l" width="400" height="350"></canvas><div style="color:#f1c40f;font-size:12px;font-weight:bold;margin-top:15px;">EXTRACTION COMPLETE</div><div style="margin-top:10px;background:linear-gradient(180deg,#222,#000);padding:15px 40px;border-radius:50px;border:1px solid #444;display:flex;gap:12px;align-items:center;">'
html_mid = b_html + '<span style="color:white;font-weight:bold;font-size:20px;">+</span>' + bonus_h
html_end = '</div><audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio></div><script>const c=document.getElementById("l"),x=c.getContext("2d"),balls=[];for(let i=1;i<=45;i++){balls.push({x:200,y:175,vx:(Math.random()-0.5)*15,vy:(Math.random()-0.5)*15,r:12,num:i,col:i<=10?"#f1c40f":i<=20?"#3498db":i<=30?"#e74c3c":i<=40?"#95a5a6":"#2ecc71"})}function draw(){x.clearRect(0,0,400,350);x.beginPath();x.arc(200,175,150,0,Math.PI*2);x.fillStyle="#111";x.fill();x.strokeStyle="#444";x.lineWidth=4;x.stroke();balls.forEach(b=>{b.x+=b.vx;b.y+=b.vy;const d=Math.sqrt((b.x-200)**2+(b.y-175)**2);if(d+b.r>150){const nx=(b.x-200)/d,ny=(b.y-175)/d,dot=b.vx*nx+b.vy*ny;b.vx-=2*dot*nx;b.vy-=2*dot*ny;b.x=200+nx*(150-b.r);b.y=175+ny*(150-b.r)}x.beginPath();x.arc(b.x,b.y,b.r,0,Math.PI*2);let g=x.createRadialGradient(b.x-4,b.y-4,2,b.x,b.y,b.r);g.addColorStop(0,"#fff");g.addColorStop(1,b.col);x.fillStyle=g;x.fill();x.fillStyle="black";x.font="bold 10px Arial";x.textAlign="center";x.fillText(b.num,b.x,b.y+4)});requestAnimationFrame(draw)}draw();</script>'

components.html(html_start + html_mid + html_end, height=550, key="lotto_final_" + str(st.session_state.rid))

# 6. 실행 버튼
if st.button("✨ 다시 분석하기"):
    r = random.sample(range(1, 46), 7)
    st.session_state.nums, st.session_state.bonus = sorted(r[:6]), r[6]
    st.session_state.rid += 1
    st.rerun()

# 7. 하단 안내문
st.markdown("<div style='background-color:#0b1a2a;border-radius:5px;padding:15px;margin-top:20px;'><p style='color:#3498db;margin:0;font-size:0.9em;'>💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.</p></div>", unsafe_allow_html=True)
