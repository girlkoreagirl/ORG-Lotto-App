import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI: 프리미엄 데이터 로또", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화 (데이터 보관함)
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'render_key' not in st.session_state:
    st.session_state['render_key'] = 0

# 3. 사이드바 정보
with st.sidebar:
    st.header("💎 HAN31 창작소")
    st.write("사용 제한이 없는 무제한 버전입니다.")
    if st.button("♻️ 앱 초기화"):
        st.session_state.clear()
        st.rerun()

# 4. 메인 화면 타이틀
st.title("💎 Fortune AI: 프리미엄 데이터 로또")
st.write("Powered by Advanced Physics Engine | Developed by HAN31 창작소")

# 5. 애니메이션 생성 함수
def get_animation_html(nums):
    balls_json = str(nums)
    return f"""
    <div id='container' style='width:100%; height:400px; background:#000; border-radius:20px; border:2px solid #333; position:relative;'>
        <canvas id='canvas' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-weight:bold; font-family:sans-serif;'>AI 분석 중...</div>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 400;
        const balls = [];
        const targets = {balls_json};
        
        for(let i=0; i<30; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 12, color: 'hsl('+(Math.random()*360)+', 70%, 60%)',
                vx: (Math.random()-0.5)*12, vy: (Math.random()-0.5)*12
            }});
        }}

        function draw() {{
            ctx.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<12 || b.x>588) b.vx *= -1;
                if(b.y<12 || b.y>388) b.vy *= -1;
                ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                ctx.fillStyle = b.color; ctx.fill();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('msg').innerText = '분석 완료!'; }}, 2500);
    </script>
    """

# 6. 분석 시작 버튼
if st.button("✨ AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    # 번호 생성
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    # 애니메이션 생성
    st.session_state['lotto_html'] = get_animation_html(st.session_state['numbers'])
    # 화면 갱신을 위한 키값 변경
    st.session_state['render_key'] += 1
    st.rerun()

# 7. 결과 출력 (에러 방지 로직 포함)
if st.session_state['lotto_html']:
    # 애니메이션 표시
    components.html(
        st.session_state['lotto_html'], 
        height=420, 
        key=f"engine_{st.session_state['render_key']}"
    )
    
    # 번호 공 표시
    st.subheader("🔮 추출된 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(st.session_state['numbers']):
        cols[i].markdown(f"""
            <div style='background:linear-gradient(135deg, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; margin:auto; box-shadow: 0 4px 8px rgba(0,0,0,0.3);'>
                {n}
            </div>
        """, unsafe_allow_html=True)

# 8. 하단 데이터 차트
st.divider()
st.subheader("📊 AI 구간별 데이터 가중치")
st.bar_chart({
    "1-10": random.randint(25, 50),
    "11-20": random.randint(25, 50),
    "21-30": random.randint(25, 50),
    "31-40": random.randint(25, 50),
    "41-45": random.randint(25, 50)
})
