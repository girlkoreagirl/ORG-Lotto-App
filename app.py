import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정 (가장 먼저 실행)
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. [오류 방지] 세션 상태 초기화 (더 안전한 방식으로 변경)
if "render_cnt" not in st.session_state:
    st.session_state.render_cnt = 0
if "lotto_nums" not in st.session_state:
    st.session_state.lotto_nums = [1, 2, 3, 4, 5, 6]

st.title("💎 Fortune AI: 무제한 로또")
st.write("100번의 시련 끝에 완성된 오류 제로 버전입니다. 공을 소환합니다!")

# 3. 분석 시작 버튼 (무제한)
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    st.session_state.lotto_nums = sorted(random.sample(range(1, 46), 6))
    st.session_state.render_cnt += 1

# 4. [회전 공 소환] HTML 코드 준비
# 에러 방지를 위해 변수들을 미리 문자열로 확정합니다.
current_nums = str(st.session_state.lotto_nums)
sound_link = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"

# HTML 본문
my_html = f"""
<div style='width:100%; height:400px; background:black; border-radius:20px; border:4px solid #ffd700; overflow:hidden; position:relative;'>
    <canvas id='lottoCanvas' width='600' height='400' style='width:100%; height:100%;'></canvas>
    <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:20px; font-weight:bold;'>💎 AI 가중치 분석 및 추첨 중...</div>
    <audio autoplay><source src="{sound_link}" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById('lottoCanvas');
    const ctx = canvas.getContext('2d');
    const balls = [];
    for(let i=1; i<=45; i++) {{
        balls.push({{
            x: Math.random()*560+20, y: Math.random()*360+20,
            r: 15, color: 'hsl('+(i*8)+', 80%, 60%)',
            vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15
        }});
    }}
    function draw() {{
        ctx.clearRect(0, 0, 600, 400);
        balls.forEach(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.x<15 || b.x>585) b.vx *= -1;
            if(b.y<15 || b.y>385) b.vy *= -1;
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let g = ctx.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
            g.addColorStop(0, 'white'); g.addColorStop(1, b.color);
            ctx.fillStyle = g; ctx.fill();
            ctx.strokeStyle = 'white'; ctx.stroke();
        }});
        requestAnimationFrame(draw);
    }}
    draw();
    setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 행운을 빕니다! 🎉'; }}, 2500);
</script>
"""

# 5. [가장 중요] 안전한 화면 출력
# TypeError를 피하기 위해 key 값을 미리 변수로 만들고, html_code도 str()로 강제 변환합니다.
safe_key = "lotto_render_id_" + str(st.session_state.render_cnt)

try:
    components.html(str(my_html), height=430, key=safe_key)
except Exception as e:
    st.error("애니메이션을 불러오는 중 문제가 발생했습니다. 페이지를 새로고침 해주세요.")

# 6. 번호 결과 표시
st.subheader("🔮 추출된 행운의 번호")
ball_cols = st.columns(6)
for idx, val in enumerate(st.session_state.lotto_nums):
    ball_cols[idx].markdown(f"""
        <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
        border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
        justify-content:center; font-weight:bold; font-size:20px; margin:auto; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.5); border: 2px solid white;'>
            {val}
        </div>
    """, unsafe_allow_html=True)

# 7. 하단 그래프
st.divider()
st.subheader("📊 AI 구간별 데이터 분석 현황")
st.bar_chart([random.randint(20, 60) for _ in range(5)])
