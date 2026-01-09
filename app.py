import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정 (가장 최상단)
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. [에러 원천 봉쇄] 세션 상태 최우선 초기화
# 앱이 켜지자마자 "비어있음" 상태를 허용하지 않습니다. 가짜 데이터라도 미리 채웁니다.
if "lotto_html_content" not in st.session_state:
    st.session_state["lotto_html_content"] = "<div style='color:white;'>READY</div>"
if "nums" not in st.session_state:
    st.session_state["nums"] = [0, 0, 0, 0, 0, 0]
if "update_id" not in st.session_state:
    st.session_state["update_id"] = 0

st.title("💎 Fortune AI: 무제한 로또")
st.write("100번의 실패는 이제 끝입니다. 회전 공을 강제로 소환합니다!")

# 3. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작 (무제한)", use_container_width=True, type="primary"):
    # 번호 생성
    st.session_state["nums"] = sorted(random.sample(range(1, 46), 6))
    st.session_state["update_id"] += 1
    
    # [회전 공 & 사운드] HTML 코드 생성
    sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"
    
    # HTML을 하나의 큰 덩어리로 변수에 담습니다.
    new_html = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:4px solid gold; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-weight:bold; font-size:20px;'>💎 AI 가중치 데이터 분석 및 추첨 중...</div>
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('lotto');
        const ctx = canvas.getContext('2d');
        const balls = [];
        for(let i=0; i<45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 15, col: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18
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
        setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 대박을 기원합니다! 🎉'; }}, 2500);
    </script>
    """
    st.session_state["lotto_html_content"] = new_html
    st.rerun() # 데이터를 채운 후 즉시 화면 다시 그리기

# 4. [에러 0.0% 지점] 화면 출력 로직
# components.html이 받는 모든 인자를 str()과 int()로 강제 형변환합니다. (파이썬 3.13 에러 방지 핵심)
current_content = str(st.session_state.get("lotto_html_content", "<div></div>"))

# 내용이 "READY"가 아닐 때(버튼 클릭 후)만 화면에 그립니다.
if len(current_content) > 50:
    # key값을 미리 문자열 변수로 고정해서 전달
    final_key = "render_pass_" + str(st.session_state["update_id"])
    
    components.html(
        current_content, 
        height=420, 
        key=final_key
    )

    # 5. 행운의 번호 공 표시
    st.subheader("🔮 이번 회차 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(st.session_state["nums"]):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:55px; height:55px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:22px; margin:auto; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.5); border: 2px solid white;'>{n}</div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 6. 하단 차트
st.divider()
st.subheader("📊 AI 구간별 데이터 가중치 현황")
import pandas as pd
chart_data = pd.DataFrame([random.randint(20, 70) for _ in range(5)], index=["1-10", "11-20", "21-30", "31-40", "41-45"])
st.bar_chart(chart_data)
