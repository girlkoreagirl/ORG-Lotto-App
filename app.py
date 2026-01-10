import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 설정 및 배경 디자인
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# CSS: 사진 속의 고급스러운 블랙 배경과 황금색 버튼 스타일 구현
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(to bottom, #f1c40f, #d4ac0d);
        color: black !important;
        font-weight: bold;
        border-radius: 30px;
        width: 100%;
        max-width: 500px;
        height: 55px;
        border: none;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(241, 196, 15, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #f1c40f;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 초기화 (처음 실행 시 기본 번호 설정)
if "nums" not in st.session_state: st.session_state.nums = [6, 12, 15, 19, 30, 39]
if "bonus" not in st.session_state: st.session_state.bonus = 33
if "run_id" not in st.session_state: st.session_state.run_id = 0

# 제목 영역
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 0;'>💎 Fortune AI: 프리미엄 데이터 로또</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em;'>Developed by HAN31 창작소</p>", unsafe_allow_html=True)

# 3. 원형 물리 엔진 & 결과창 디자인 (HTML/JS)
sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"

# 번호 대역별 색상 정의
def get_ball_color(n):
    if n <= 10: return "radial-gradient(circle at 30% 30%, #fff, #f1c40f)" # 노랑
    if n <= 20: return "radial-gradient(circle at 30% 30%, #fff, #3498db)" # 파랑
    if n <= 30: return "radial-gradient(circle at 30% 30%, #fff, #e74c3c)" # 빨강
    if n <= 40: return "radial-gradient(circle at 30% 30%, #fff, #95a5a6)" # 회색
    return "radial-gradient(circle at 30% 30%, #fff, #2ecc71)" # 초록

# 결과바에 들어갈 공들의 HTML 생성
result_balls_html = "".join([
    f"<div style='width:38px; height:38px; border-radius:50%; background:{get_ball_color(n)}; color:black; display:flex; align-items:center; justify-content:center; font-weight:bold; border:1.5px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.5);'>{n}</div>" 
    for n in st.session_state.nums
])
bonus_ball_html = f"<div style='width:38px; height:38px; border-radius:50%; background:{get_ball_color(st.session_state.bonus)}; color:black; display:flex; align-items:center; justify-content:center; font-weight:bold; border:1.5px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.5);'>{st.session_state.bonus}</div>"

# 전체 애니메이션 및 결과창 레이아웃
html_content = f"""
<div style='background:#0e1117; display:flex; flex-direction:column; align-items:center; border: 1px solid #333; border-radius: 20px; padding: 25px; margin-top: 20px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);'>
    <!-- 원형 추출기 캔버스 -->
    <canvas id='lotto' width='400' height='350' style='background:transparent;'></canvas>
    
    <div style='color: #f1c40f; font-size: 12px; font-weight: bold; margin-top: 15px; letter-spacing: 2px;'>EXTRACTION COMPLETE</div>
    
    <!-- 프리미엄 결과 바 (Black Gradient) -->
    <div style='margin-top:10px; background:linear-gradient(180deg, #222, #000); padding: 15px 40px; border-radius: 50px; border: 1px solid #444; display: flex; gap: 12px; align-items: center; box-shadow: 0 5px 15px rgba(0,0,0,0.6);'>
        {result_balls_html}
        <span style='color:white; font-weight:bold; font-size: 22px; margin: 0 5px;'>+</span>
        {bonus_ball_html}
    </div>
    <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
</div>

<script>
    const c = document.getElementById('lotto');
    const x = c.getContext('2d');
    const centerX = 200, centerY = 175, radius = 150;
    const balls = [];
    const colors = ['#f1c40f', '#3498db', '#e74c3c', '#95a5a6', '#2ecc71'];

    // 45개 공 생성 및 초기 속도 설정
    for(let i=1; i<=45; i++) {{
        balls.push({{
            x: centerX + (Math.random()-0.5)*100,
            y: centerY + (Math.random()-0.5)*100,
            vx: (Math.random()-0.5)*18,
            vy: (Math.random()-0.5)*18,
            r: 11,
            num: i,
            col: colors[Math.floor((i-1)/10)] || colors[4]
        }});
    }}

    function draw() {{
        x.clearRect(0, 0, 400, 400);
        
        // 원형 통 그리기
        x.beginPath();
        x.arc(centerX, centerY, radius, 0, Math.PI*2);
        x.fillStyle = '#111';
        x.fill();
        x.strokeStyle = '#444';
        x.lineWidth = 4;
        x.stroke();

        balls.forEach(b => {{
            b.x += b.vx; b.y += b.vy;
            
            // 원형 벽 충돌 처리
            const dist = Math.sqrt((b.x-centerX)**2 + (b.y-centerY)**2);
            if(dist + b.r > radius) {{
                const nx = (b.x-centerX)/dist, ny = (b.y-centerY)/dist;
                const dot = b.vx*nx + b.vy*ny;
                b.vx -= 2*dot*nx; b.vy -= 2*dot*ny;
                b.x = centerX + nx*(radius-b.r);
                b.y = centerY + ny*(radius-b.r);
            }}

            // 공 그리기 (입체감 효과)
            x.beginPath();
            x.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let g = x.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
            g.addColorStop(0, '#fff'); g.addColorStop(1, b.col);
            x.fillStyle = g; x.fill();
            
            x.fillStyle = 'black'; 
            x.font = 'bold 9px Arial'; 
            x.textAlign='center';
            x.fillText(b.num, b.x, b.y+3);
        }});
        requestAnimationFrame(draw);
    }}
    draw();
</script>
"""

# 컴포넌트 출력 (key값을 주어 매번 새로 시작하게 함)
components.html(html_content, height=540, key=f"lotto_premium_{st.session_state.run_id}")

# 4. 분석 실행 버튼
st.write("") # 간격 조절
if st.button("✨ 다시 분석하기"):
    # 실제 번호 추출 로직 (6개 + 보너스 1개)
    picked = random.sample(range(1, 46), 7)
    st.session_state.nums = sorted(picked[:6])
    st.session_state.bonus = picked[6]
    st.session_state.run_id += 1
    st.rerun()

# 5. 하단 안내 텍스트
st.markdown("<p style='text-align: center; color: #555; font-size: 0.9em; margin-top: 20px;'>💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 AI 분석이 시작됩니다.</p>", unsafe_allow_html=True)
