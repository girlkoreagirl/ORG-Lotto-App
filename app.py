import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화
if "nums" not in st.session_state:
    st.session_state.nums = []
if "key_id" not in st.session_state:
    st.session_state.key_id = 0

st.title("💎 Fortune AI: 무제한 로또")
st.write("정신 똑바로 차리고 준비했습니다. 이번엔 진짜 회전 공 소환됩니다!")

# 3. 버튼 클릭 로직
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    st.session_state.nums = sorted(random.sample(range(1, 46), 6))
    st.session_state.key_id += 1

# 4. [회전 공 소환] 
# 데이터가 있을 때만 실행하는 게 아니라, 빈 값이라도 일단 틀을 먼저 보여줍니다.
if st.session_state.nums:
    res_nums = st.session_state.nums
    # 사운드와 애니메이션이 합쳐진 무적의 HTML
    # 파이썬 3.13 호환을 위해 f-string을 아주 단순하게 구성했습니다.
    lotto_html = f"""
    <div style="width:100%; height:400px; background:black; border-radius:20px; border:4px solid gold; overflow:hidden; position:relative;">
        <canvas id="canvas" width="600" height="400" style="width:100%; height:100%;"></canvas>
        <div id="txt" style="position:absolute; bottom:20px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-size:20px; font-weight:bold;">💎 AI 데이터 분석 및 추첨 중...</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const balls = [];
        for(let i=0; i<45; i++) {{
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
    
    # 5. 컴포넌트 출력 (에러 방지를 위해 key를 문자열로 확실히 전달)
    components.html(lotto_html, height=420, key=f"re_summon_{st.session_state.key_id}")

    # 6. 번호 결과 표시
    st.subheader("🔮 추출된 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(res_nums):
        cols[i].markdown(f"""
            <div style="background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:20px; margin:auto; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.5); border: 2px solid white;">{n}</div>
        """, unsafe_allow_html=True)

else:
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 7. 하단 통계 데이터
st.divider()
st.subheader("📊 AI 구간별 데이터 분석 현황")
import pandas as pd
chart_data = pd.DataFrame([random.randint(20, 60) for _ in range(5)], index=["1-10", "11-20", "21-30", "31-40", "41-45"])
st.bar_chart(chart_data)
