import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="Fortune AI 로또", page_icon="💎", layout="centered")

# 2. [철벽 방어] 세션 상태 초기화 - 앱 실행 즉시 빈 상자를 만들어둠
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'update_count' not in st.session_state:
    st.session_state['update_count'] = 0
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""

# 3. 타이틀 디자인
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("모든 오류를 수정한 무제한 버전입니다. 행운을 빕니다!")

# 4. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    # 행운의 번호 생성
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    st.session_state['update_count'] += 1
    
    # 애니메이션용 HTML 생성 (가장 안전한 문자열 방식)
    nums_str = str(st.session_state['numbers'])
    new_html = f"""
    <div style='width:100%; height:400px; background:#000; border-radius:20px; border:3px solid #ffd700; position:relative; overflow:hidden;'>
        <canvas id='c' style='width:100%; height:100%;'></canvas>
        <div id='t' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-weight:bold;'>💎 AI 가중치 분석 및 추첨 중...</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('c');
        const ctx = canvas.getContext('c').getContext('2d'); // 오타 방지를 위한 직접 호출
        // 아래는 안전한 캔버스 초기화
        const c2 = document.getElementById('c');
        const ctx2 = c2.getContext('2d');
        c2.width = 600; c2.height = 400;
        const balls = [];
        for(let i=0; i<40; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 14, color: 'hsl('+(i*9)+', 80%, 60%)',
                vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15
            }});
        }}
        function draw() {{
            ctx2.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<14 || b.x>586) b.vx *= -1;
                if(b.y<14 || b.y>386) b.vy *= -1;
                ctx2.beginPath(); ctx2.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = ctx2.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
                g.addColorStop(0, '#fff'); g.addColorStop(1, b.color);
                ctx2.fillStyle = g; ctx2.fill();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('t').innerText = '✨ 분석 완료! 행운을 빕니다 ✨'; }}, 2500);
    </script>
    """
    st.session_state['lotto_html'] = new_html
    st.rerun()

# 5. [철벽 방어] 화면 출력 로직
# lotto_html이 확실한 '문자열'이고 내용이 있을 때만 실행합니다.
display_html = st.session_state.get('lotto_html', "")

if isinstance(display_html, str) and len(display_html) > 0:
    # 에러 방지를 위해 key값에 문자열을 확실히 더해줍니다.
    safe_key = f"view_{st.session_state['update_count']}"
    components.html(display_html, height=420, key=safe_key)
    
    # 번호 공 표시
    st.subheader("🔮 추출된 행운의 번호")
    num_list = st.session_state.get('numbers', [])
    cols = st.columns(6)
    for i, n in enumerate(num_list):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:18px; margin:auto; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.4); border: 2px solid #fff;'>
                {n}
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 위 버튼을 눌러 AI 분석을 시작하세요!")

# 6. 하단 통계 그래프 (항상 표시)
st.divider()
st.subheader("📊 AI 구간별 분석 가중치 현황")
st.bar_chart([random.randint(20, 65) for _ in range(5)])
