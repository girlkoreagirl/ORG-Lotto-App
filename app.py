import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 설정 (가장 먼저 실행)
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화 (파이썬 3.13 에러 방지용)
if "nums" not in st.session_state:
    st.session_state.nums = []
if "key_id" not in st.session_state:
    st.session_state.key_id = 0

st.title("💎 Fortune AI: 무제한 로또")
st.write("로딩 안내문 삭제! 이제 진짜 회전 공과 사운드를 즉시 소환합니다.")

# 3. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    st.session_state.nums = sorted(random.sample(range(1, 46), 6))
    st.session_state.key_id += 1

# 4. [회전 공 & 사운드 소환] 
# 데이터가 없을 때는 안내를 하고, 버튼을 누르는 순간 HTML을 강제로 화면에 뿌립니다.
if st.session_state.nums:
    # 사운드 및 화려한 회전 공 HTML (에러 방지를 위해 변수 처리를 최소화함)
    lotto_html = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:4px solid #ffd700; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='txt' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:20px; font-weight:bold;'>💎 AI 데이터 분석 및 추첨 진행 중...</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('lotto');
        const ctx = canvas.getContext('2d');
        const balls = [];
        // 화려한 공 45개 소환
        for(let i=1; i<=45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 15, col: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*20, vy: (Math.random()-0.5)*20
            }});
        }}
        function draw() {{
            ctx.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>385) b.vy *= -1;
                ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = ctx.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
                g.addColorStop(0, 'white'); g.addColorStop(1, b.col);
                ctx.fillStyle = g; ctx.fill();
                ctx.strokeStyle = 'white'; ctx.stroke();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('txt').innerText = '🎉 분석 완료! 행운을 빕니다! 🎉'; }}, 2500);
    </script>
    """
    
    # 5. [중요] 컴포넌트 호출 (key값을 정수로 만들어 에러 방지)
    components.html(lotto_html, height=420, key=f"summon_id_{st.session_state.key_id}")

    # 6. 행운의 번호 공 표시
    st.subheader("🔮 이번 회차 분석 번호")
    cols = st.columns(6)
    for i, n in enumerate(st.session_state.nums):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:55px; height:55px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:22px; margin:auto; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.5); border: 2px solid white;'>{n}</div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 7. 하단 차트
st.divider()
st.subheader("📊 AI 구간별 데이터 가중치 현황")
import pandas as pd
chart_val = [random.randint(20, 70) for _ in range(5)]
st.bar_chart(pd.DataFrame(chart_val, index=["1-10", "11-20", "21-30", "31-40", "41-45"]))
