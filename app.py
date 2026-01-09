import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="Fortune AI 로또", page_icon="💎", layout="centered")

# 2. [에러 방지] 세션 상태 초기화 - 가장 먼저 실행되어야 함
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'update_key' not in st.session_state:
    st.session_state['update_key'] = 0

# 3. 타이틀 및 디자인
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("무제한 버전입니다. 마음껏 분석해 보세요!")

# 4. 애니메이션 생성 함수 (더 튼튼하게 수정)
def generate_balls_html(nums):
    balls_json = str(nums)
    return f"""
    <div style='width:100%; height:380px; background:#000; border-radius:15px; border:2px solid #444; position:relative; overflow:hidden;'>
        <canvas id='lottoCanvas' style='width:100%; height:100%;'></canvas>
        <div id='info' style='position:absolute; bottom:15px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-size:18px;'>AI 가중치 분석 및 추첨 중...</div>
    </div>
    <script>
        const canvas = document.getElementById('lottoCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 380;
        const balls = [];
        for(let i=0; i<35; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*340+20,
                r: 13, color: 'hsl('+(Math.random()*360)+', 70%, 60%)',
                vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15
            }});
        }}
        function anim() {{
            ctx.clearRect(0,0,600,380);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<13 || b.x>587) b.vx *= -1;
                if(b.y<13 || b.y>367) b.vy *= -1;
                ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                ctx.fillStyle = b.color; ctx.fill();
            }});
            requestAnimationFrame(anim);
        }}
        anim();
        setTimeout(() => {{ document.getElementById('info').innerText = '분석 완료! 행운을 빕니다.'; }}, 2500);
    </script>
    """

# 5. 분석 시작 버튼 (제한 없음)
if st.button("✨ AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    # 행운의 번호 생성
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    # 애니메이션 코드 생성
    st.session_state['lotto_html'] = generate_balls_html(st.session_state['numbers'])
    # 화면 갱신을 위한 키값 증가
    st.session_state['update_key'] += 1
    # 화면 리프레시
    st.rerun()

# 6. [에러 방지] 결과 출력 로직 (값이 있을 때만 실행)
# .get()을 사용하여 값이 없어도 에러가 나지 않게 함
current_html = st.session_state.get('lotto_html', "")
current_key = st.session_state.get('update_key', 0)

if current_html and len(current_html) > 0:
    try:
        # 애니메이션 표시
        components.html(current_html, height=400, key=f"engine_v_{current_key}")
        
        # 번호 출력
        st.subheader("🔮 추출된 행운의 번호")
        ball_cols = st.columns(6)
        for i, num in enumerate(st.session_state.get('numbers', [])):
            ball_cols[i].markdown(f"""
                <div style='background:linear-gradient(135deg, #f1c40f, #f39c12); color:black; 
                border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
                justify-content:center; font-weight:bold; margin:auto; box-shadow: 0 4px 6px rgba(0,0,0,0.5);'>
                    {num}
                </div>
            """, unsafe_allow_html=True)
    except:
        st.info("버튼을 눌러 분석을 시작해 주세요!")

# 7. 하단 통계 데이터
st.divider()
st.subheader("📊 AI 구간별 분석 가중치")
st.bar_chart([random.randint(15, 50) for _ in range(5)])
