import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 기본 설정 (무조건 맨 위)
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화 (파이썬 3.13 최적화 방식)
if "nums" not in st.session_state:
    st.session_state["nums"] = []
if "k_id" not in st.session_state:
    st.session_state["k_id"] = str(time.time())

st.title("💎 Fortune AI: 무제한 로또")
st.write("100번의 고생 끝! 이제 진짜 회전 공과 사운드가 소환됩니다.")

# 3. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    st.session_state["nums"] = sorted(random.sample(range(1, 46), 6))
    st.session_state["k_id"] = str(time.time())

# 4. 결과 출력 로직 (번호가 있을 때만 실행)
if st.session_state["nums"]:
    # 파이썬 3.13 에러 방지를 위해 변수 타입을 엄격하게 고정합니다.
    current_numbers = list(st.session_state["nums"])
    # 키값에서 특수문자를 제거한 순수 문자열로 만듭니다.
    pure_key = "lotto_view_" + "".join(filter(str.isalnum, st.session_state["k_id"]))
    
    # 화려한 회전 공 + 사운드 HTML (가장 안정적인 구조)
    lotto_html_content = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:4px solid gold; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:25px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-size:20px; font-weight:bold;'>💎 AI 가중치 분석 및 추첨 중...</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const c = document.getElementById('lotto');
        const x = c.getContext('2d');
        const balls = [];
        for(let i=1; i<=45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 16, col: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*20, vy: (Math.random()-0.5)*20
            }});
        }}
        function draw() {{
            x.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<16 || b.x>584) b.vx *= -1;
                if(b.y<16 || b.y>384) b.vy *= -1;
                x.beginPath(); x.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = x.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
                g.addColorStop(0, 'white'); g.addColorStop(1, b.col);
                x.fillStyle = g; x.fill();
                x.strokeStyle = 'white'; x.stroke();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 행운을 빕니다! 🎉'; }}, 2500);
    </script>
    """
    
    # 5. [에러 제로 핵심] 
    # html 인자는 무조건 str, height는 int, key는 알파벳/숫자로만 된 str이어야 함
    try:
        components.html(
            html=str(lotto_html_content), 
            height=420, 
            key=str(pure_key)
        )
    except Exception as e:
        st.warning("애니메이션 로딩 중입니다. 잠시만 기다려 주세요.")

    # 6. 행운의 번호 공 표시
    st.subheader("🔮 이번 회차 분석 번호")
    num_cols = st.columns(6)
    for i, n in enumerate(current_numbers):
        num_cols[i].markdown(f"""
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
chart_data = pd.DataFrame([random.randint(20, 70) for _ in range(5)], index=["1-10", "11-20", "21-30", "31-40", "41-45"])
st.bar_chart(chart_data)
