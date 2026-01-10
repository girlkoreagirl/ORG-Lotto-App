import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd

# [1] 최상단 설정 - Streamlit Cloud 최적화
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 데이터 초기화 - 어떤 상황에서도 None이 발생하지 않도록 초기값 설정
if "nums" not in st.session_state:
    st.session_state["nums"] = [4, 12, 15, 37, 39, 44]
if "bonus" not in st.session_state:
    st.session_state["bonus"] = 33
if "rid" not in st.session_state:
    st.session_state["rid"] = 0

# [3] CSS 스타일 (왼쪽 이미지의 골드 디자인 100% 재현)
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
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:white;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# [4] 공 색상 로직
def get_c(n):
    if n<=10: return "#f1c40f"
    if n<=20: return "#3498db"
    if n<=30: return "#e74c3c"
    if n<=40: return "#95a5a6"
    return "#2ecc71"

# 결과 바 공 HTML 생성
b_html = ""
for n in st.session_state["nums"]:
    b_html += '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(n)+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;margin:0 2px;">'+str(n)+'</div>'
bonus_h = '<div style="width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#fff,'+get_c(st.session_state["bonus"])+');color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1.5px solid white;">'+str(st.session_state["bonus"])+'</div>'

# [5] 물리 엔진 HTML (f-string을 쓰지 않고 replace 방식으로 안전하게 조립)
html_template = """
<div style="background:#0e1117;border:1px solid #333;border-radius:20px;padding:30px;display:flex;flex-direction:column;align-items:center;box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <canvas id="l" width="400" height="350"></canvas>
    <div style="color:#666; font-size:10px; margin-top:15px;">AI PREDICTION RESULT</div>
    <div style="margin-top:5px;background:linear-gradient(180deg,#222,#000);padding:15px 40px;border-radius:50px;border:1px solid #444;display:flex;gap:12px;align-items:center;">
        NUMS_HERE <span style="color:white;font-weight:bold;font-size:20px;">+</span> BONUS_HERE
    </div>
    <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
</div>
<script>
    const c=document.getElementById("l"), x=c.getContext("2d"), balls=[];
    for(let i=1;i<=45;i++){
        balls.push({
            x:200+(Math.random()-0.5)*100, y:175+(Math.random()-0.5)*100,
            vx:(Math.random()-0.5)*16, vy:(Math.random()-0.5)*16,
            r:12, num:i, col: i<=10?"#f1c40f":i<=20?"#3498db":i<=30?"#e74c3c":i<=40?"#95a5a6":"#2ecc71"
        });
    }
    function draw(){
        x.clearRect(0,0,400,350);
        x.beginPath(); x.arc(200,175,150,0,Math.PI*2); x.fillStyle="#111"; x.fill(); x.strokeStyle="#444"; x.lineWidth=4; x.stroke();
        balls.forEach(b=>{
            b.x+=b.vx; b.y+=b.vy;
            const d=Math.sqrt((b.x-200)**2+(b.y-175)**2);
            if(d+b.r>150){
                const nx=(b.x-200)/d, ny=(b.y-175)/d, dot=b.vx*nx+b.vy*ny;
                b.vx-=2*dot*nx; b.vy-=2*dot*ny;
                b.x=200+nx*(150-b.r); b.y=175+ny*(150-b.r);
            }
            x.beginPath(); x.arc(b.x,b.y,b.r,0,Math.PI*2);
            let g=x.createRadialGradient(b.x-4,b.y-4,2,b.x,b.y,b.r);
            g.addColorStop(0,"#fff"); g.addColorStop(1,b.col);
            x.fillStyle=g; x.fill();
            x.fillStyle="black"; x.font="bold 10px Arial"; x.textAlign="center"; x.fillText(b.num,b.x,b.y+4);
        });
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

# 문자열 치환으로 안전하게 주입
final_html = html_template.replace("NUMS_HERE", b_html).replace("BONUS_HERE", bonus_h)

# [6] 에러 발생 원인인 key값을 문자열 상수로 처리
components.html(final_html, height=550, key="lotto_final_" + str(st.session_state["rid"]))

# [7] 실행 버튼 (사진의 골드 버튼 스타일)
if st.button("✨ 분석 완료! (다시 시도)"):
    r = random.sample(range(1, 46), 7)
    st.session_state["nums"] = sorted(r[:6])
    st.session_state["bonus"] = r[6]
    st.session_state["rid"] += 1
    st.rerun()

# [8] 하단 차트 및 안내
st.divider()
st.markdown("### 📊 번호 구간별 분석 가중치")
chart_val = [random.randint(15, 50) for _ in range(5)]
st.bar_chart(pd.DataFrame(chart_val, index=["1-10", "11-20", "21-30", "31-40", "41-45"]))

st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
