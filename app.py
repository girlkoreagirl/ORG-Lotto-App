import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. 초기화 (에러 원천 차단)
if 'count' not in st.session_state: st.session_state['count'] = 0
if 'nums' not in st.session_state: st.session_state['nums'] = [1, 2, 3, 4, 5, 6] # 기본값

st.title("💎 Fortune AI: 프리미엄 로또")
st.write("회전 공 소환 완료! 무제한으로 분석하세요.")

# 3. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    st.session_state['nums'] = sorted(random.sample(range(1, 46), 6))
    st.session_state['count'] += 1
    # 버튼 누르면 자동으로 아래 코드가 실행되면서 공이 돌아갑니다.

# 4. [회전 공 소환] 애니메이션 HTML (가장 강력한 직접 삽입 방식)
# 버튼을 누를 때마다 key값이 바뀌어서 무조건 새로 돌아갑니다.
lotto_numbers = str(st.session_state['nums'])
sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"

html_code = f"""
<div style='width:100%; height:420px; background:black; border-radius:20px; border:4px solid #ffd700; overflow:hidden; position:relative;'>
    <canvas id='lottoCanvas' width='600' height='420' style='width:100%; height:100%;'></canvas>
    <div id='status' style='position:absolute; bottom:25px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:22px; font-weight:bold; text-shadow: 2px 2px 4px black;'>💎 AI 가중치 분석 및 추첨 진행 중...</div>
    <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
</div>
<script>
    const canvas = document.getElementById('lottoCanvas');
    const ctx = canvas.getContext('2d');
    const balls = [];
    // 화려한 공 45개 소환
    for(let i=1; i<=45; i++) {{
        balls.push({{
            x: Math.random()*560+20, y: Math.random()*380+20,
            r: 16, color: 'hsl('+(i*8)+', 80%, 60%)',
            vx: (Math.random()-0.5)*22, vy: (Math.random()-0.5)*22
        }});
    }}
    function draw() {{
        ctx.clearRect(0, 0, 600, 420);
        balls.forEach(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.x<16 || b.x>584) b.vx *= -1;
            if(b.y<16 || b.y>404) b.vy *= -1;
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            let g = ctx.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
            g.addColorStop(0, 'white'); g.addColorStop(1, b.color);
            ctx.fillStyle = g; ctx.fill();
            ctx.strokeStyle = 'white'; ctx.lineWidth = 1; ctx.stroke();
        }});
        requestAnimationFrame(draw);
    }}
    draw();
    setTimeout(() => {{ document.getElementById('status').innerText = '🎉 분석 완료! 행운을 빕니다! 🎉'; }}, 2800);
</script>
"""

# 애니메이션 강제 출력
components.html(html_code, height=440, key=f"summon_balls_{st.session_state['count']}")

# 5. 추출된 번호 공 표시
st.subheader("🔮 이번 회차 행운의 번호")
cols = st.columns(6)
for i, n in enumerate(st.session_state['nums']):
    cols[i].markdown(f"""
        <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
        border-radius:50%; width:55px; height:55px; display:flex; align-items:center; 
        justify-content:center; font-weight:bold; font-size:22px; margin:auto; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.5); border: 2px solid white;'>
            {n}
        </div>
    """, unsafe_allow_html=True)

# 6. 하단 차트 (항상 바뀜)
st.divider()
st.subheader("📊 AI 구간별 데이터 분석 현황")
st.bar_chart([random.randint(15, 70) for _ in range(5)])
