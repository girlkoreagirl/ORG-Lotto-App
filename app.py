import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 설정 (가장 안전한 기본 설정)
st.set_page_config(page_title="Fortune AI", layout="centered")

# 2. 상태 관리 (딕셔너리 없이 가장 원시적인 변수 사용)
if "nums" not in st.session_state:
    st.session_state.nums = [6, 12, 15, 19, 30, 39]
if "bonus" not in st.session_state:
    st.session_state.bonus = 33
if "rid" not in st.session_state:
    st.session_state.rid = 0

st.title("💎 Fortune AI: 프리미엄 로또")

# 3. HTML 조립 (에러 원인인 f-string과 .replace()를 아예 안 씀)
# 문자열을 조각조각 더해서 만드는 가장 원시적이고 안전한 방식입니다.

# 숫자 공 HTML 생성
ball_html = ""
for n in st.session_state.nums:
    ball_html += '<div style="width:35px;height:35px;border-radius:50%;background:white;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;margin:2px;border:1px solid #ccc;">' + str(n) + '</div>'

# 전체 HTML 뼈대 (자바스크립트 중괄호와 파이썬이 부딪히지 않게 설계)
html_start = """
<div style="background:#111; border-radius:20px; padding:20px; display:flex; flex-direction:column; align-items:center; font-family:sans-serif;">
    <canvas id="l" width="400" height="300"></canvas>
    <div style="margin-top:20px; background:#000; padding:15px 30px; border-radius:50px; display:flex; gap:10px; align-items:center; border:1px solid #444;">
"""
html_mid = ball_html + '<span style="color:white; font-weight:bold;">+</span>' + \
           '<div style="width:35px;height:35px;border-radius:50%;background:#3498db;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;">' + str(st.session_state.bonus) + '</div>'
html_end = """
    </div>
</div>
<script>
    const c=document.getElementById('l'),x=c.getContext('2d'),balls=[];
    for(let i=1;i<=45;i++) balls.push({x:200,y:150,vx:(Math.random()-0.5)*15,vy:(Math.random()-0.5)*15,r:11,col:'hsl('+(i*8)+',75%,60%)'});
    function d(){
        x.clearRect(0,0,400,300);x.beginPath();x.arc(200,150,145,0,Math.PI*2);x.fillStyle='#050505';x.fill();
        balls.forEach(b=>{
            b.x+=b.vx;b.y+=b.vy;const dist=Math.sqrt((b.x-200)**2+(b.y-150)**2);
            if(dist+b.r>145){
                const nx=(b.x-200)/dist,ny=(b.y-150)/dist,dot=b.vx*nx+b.vy*ny;
                b.vx-=2*dot*nx;b.vy-=2*dot*ny;
                b.x=200+nx*(145-b.r);b.y=150+ny*(145-b.r);
            }
            x.beginPath();x.arc(b.x,b.y,b.r,0,Math.PI*2);x.fillStyle=b.col;x.fill();
        });requestAnimationFrame(d);
    }d();
</script>
"""

final_html = html_start + html_mid + html_end

# 4. 화면 출력 (TypeError를 유발하는 key 인자를 아예 제거함)
# 버튼을 누르면 어차피 Streamlit이 재실행되므로 애니메이션은 다시 시작됩니다.
components.html(final_html, height=500)

# 5. 하단 버튼
if st.button("🚀 AI 분석 다시 시도"):
    res = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(res[:6])
    st.session_state.bonus = res[6]
    st.session_state.rid += 1
    st.rerun()
