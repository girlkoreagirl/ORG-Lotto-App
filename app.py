import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정 (무조건 최상단)
st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

# 2. [폭발 방지] 초기화 - 절대 None이 될 수 없게 빈 글자("")를 미리 박아둡니다.
if "nums" not in st.session_state: st.session_state.nums = []
if "html_code" not in st.session_state: st.session_state.html_code = ""
if "run_id" not in st.session_state: st.session_state.run_id = 0

st.title("💎 Fortune AI: 프리미엄 로또")
st.write(f"현재 시간: 2026-01-10 11:55 AM | 무결점 버전 소환 완료!")

# 3. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    # 번호 생성
    st.session_state.nums = sorted(random.sample(range(1, 46), 6))
    st.session_state.run_id += 1
    
    # HTML 코드 생성 (모든 데이터를 로컬 변수에 담아 안전하게 전달)
    sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"
    
    # HTML 본문 (절대로 깨지지 않는 구조)
    safe_html = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:4px solid gold; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-weight:bold; font-size:20px;'>💎 AI 데이터 분석 및 추첨 진행 중...</div>
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    </div>
    <script>
        const c = document.getElementById('lotto');
        const x = c.getContext('2d');
        const balls = [];
        for(let i=0; i<45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 15, col: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*20, vy: (Math.random()-0.5)*20
            }});
        }}
        function draw() {{
            x.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>385) b.vy *= -1;
                x.beginPath(); x.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = x.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
                g.addColorStop(0, 'white'); g.addColorStop(1, b.col);
                x.fillStyle = g; x.fill();
                x.strokeStyle = 'white'; x.stroke();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 대박을 기원합니다! 🎉'; }}, 2500);
    </script>
    """
    st.session_state.html_code = safe_html
    st.rerun()

# 4. [에러 제로 핵심] 화면 출력 로직
# .get()을 쓰고, str()로 강제 변환하며, 길이가 충분할 때만(진짜 코드가 들어있을 때만) 실행합니다.
display_content = str(st.session_state.get("html_code", ""))

if len(display_content) > 100: # "<div></div>" 같은 빈 태그가 아닐 때만 실행
    # key값을 변수에 담아 완벽하게 고정
    final_key = f"summon_id_{st.session_state.run_id}"
    
    try:
        components.html(
            display_content, 
            height=420, 
            key=final_key
        )
    except:
        st.write("애니메이션 준비 중...")

    # 5. 행운의 번호 공 표시
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

# 6. 하단 차트
st.divider()
st.subheader("📊 AI 구간별 데이터 가중치 현황")
import pandas as pd
chart_val = [random.randint(20, 70) for _ in range(5)]
st.bar_chart(pd.DataFrame(chart_val, index=["1-10", "11-20", "21-30", "31-40", "41-45"]))
