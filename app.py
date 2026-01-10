import streamlit as st
import streamlit.components.v1 as components
import random

# [1] 초기 설정 - 에러 방지를 위해 무조건 첫 줄 배치
st.set_page_config(page_title="Fortune AI", layout="centered")

# [2] 상태 관리 - 데이터가 누락되지 않도록 딕셔너리 형태로 안전하게 초기화
if "data" not in st.session_state:
    st.session_state["data"] = {
        "nums": [6, 12, 15, 19, 30, 39],
        "bonus": 33,
        "run_id": 0
    }

st.markdown("<h1 style='text-align: center;'>💎 Fortune AI: 프리미엄 로또</h1>", unsafe_allow_html=True)

# [3] CSS 스타일 정의 (HTML 내부에 포함시켜 충돌 방지)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button {
        background: linear-gradient(#f1c40f, #d4ac0d) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        width: 100% !important;
        height: 55px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# [4] 자바스크립트 충돌 제로 템플릿 (f-string 절대 사용 금지)
# 파이썬 3.13의 f-string 에러를 피하기 위해 일반 문자열(docstring)만 사용합니다.
html_template = """
<div id="container" style="background:#111; border-radius:20px; padding:20px; display:flex; flex-direction:column; align-items:center; font-family:sans-serif;">
    <canvas id="lottoCanvas" width="400" height="300"></canvas>
    <div id="resultBar" style="margin-top:20px; background:#000; padding:15px 30px; border-radius:50px; display:flex; gap:10px; align-items:center; border:1px solid #444;">
        <!-- 결과 공이 여기에 동적으로 삽입됨 -->
    </div>
</div>

<script>
    // 1. 데이터 주입 (파이썬에서 치환할 부분)
    const winningNums = [VAR_NUMS];
    const bonusNum = VAR_BONUS;

    // 2. 결과 바 생성
    const bar = document.getElementById('resultBar');
    winningNums.forEach(n => {
        bar.innerHTML += `<div style="width:35px;height:35px;border-radius:50%;background:white;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;border:1px solid #ccc;">${n}</div>`;
    });
    bar.innerHTML += `<span style="color:white;font-weight:bold;">+</span>`;
    bar.innerHTML += `<div style="width:35px;height:35px;border-radius:50%;background:#3498db;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;">${bonusNum}</div>`;

    // 3. 물리 엔진 (Canvas 애니메이션)
    const canvas = document.getElementById('lottoCanvas');
    const ctx = canvas.getContext('2d');
    const balls = [];
    for(let i=1; i<=45; i++) {
        balls.push({
            x: 200, y: 150, 
            vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15, 
            r: 11, col: 'hsl('+(i*8)+',75%,60%)'
        });
    }

    function animate() {
        ctx.clearRect(0,0,400,300);
        ctx.beginPath(); ctx.arc(200,150,145,0,Math.PI*2); ctx.fillStyle='#050505'; ctx.fill();
        balls.forEach(b => {
            b.x += b.vx; b.y += b.vy;
            const d = Math.sqrt((b.x-200)**2 + (b.y-150)**2);
            if(d+b.r > 145) {
                const nx=(b.x-200)/d, ny=(b.y-150)/d, dot=b.vx*nx+b.vy*ny;
                b.vx-=2*dot*nx; b.vy-=2*dot*ny;
                b.x=200+nx*(145-b.r); b.y=150+ny*(145-b.r);
            }
            ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,Math.PI*2); ctx.fillStyle=b.col; ctx.fill();
        });
        requestAnimationFrame(animate);
    }
    animate();
</script>
"""

# [5] 데이터 안전 치환 (문자열 연산만 사용)
current_nums_str = ", ".join(map(str, st.session_state["data"]["nums"]))
final_html = html_template.replace("VAR_NUMS", current_nums_str)
final_html = final_html.replace("VAR_BONUS", str(st.session_state["data"]["bonus"]))

# [6] 화면 출력 - key값도 안전하게 문자열로 전달
components.html(final_html, height=520, key=str(st.session_state["data"]["run_id"]))

# [7] 버튼 로직
if st.button("🚀 AI 프리미엄 분석 다시 시도"):
    new_res = random.sample(range(1, 46), 7)
    st.session_state["data"]["nums"] = sorted(new_res[:6])
    st.session_state["data"]["bonus"] = new_res[6]
    st.session_state["data"]["run_id"] += 1
    st.rerun()

st.info("💡 베테랑 로직 적용 완료. 물리 엔진과 함께 AI 번호가 추출됩니다.")
