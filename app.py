import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI 로또", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화 (에러 방지용 주머니)
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'update_key' not in st.session_state:
    st.session_state['update_key'] = 0

# 3. 메인 타이틀
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("사운드와 애니메이션이 포함된 무제한 버전입니다!")

# 4. 애니메이션 및 사운드 포함 HTML 생성 함수
def generate_rich_animation(nums):
    balls_json = str(nums)
    # 사운드 URL (벨소리 + 성공 사운드)
    start_sound = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"
    
    return f"""
    <div style='width:100%; height:420px; background:#000; border-radius:20px; border:3px solid #ffd700; position:relative; overflow:hidden; box-shadow: 0 0 20px rgba(255,215,0,0.3);'>
        <canvas id='lottoCanvas' style='width:100%; height:100%;'></canvas>
        <div id='info' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:20px; font-weight:bold; text-shadow: 2px 2px 4px #000;'>💎 AI 가중치 데이터 분석 중...</div>
        <!-- 사운드 재생 -->
        <audio autoplay><source src="{start_sound}" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('lottoCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 420;
        const balls = [];
        const targets = {balls_json};
        
        // 화려한 회전 공 45개 생성
        for(let i=1; i<=45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*380+20,
                r: 15, color: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*20, vy: (Math.random()-0.5)*20,
                num: i
            }});
        }}

        function animate() {{
            ctx.clearRect(0,0,600,420);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>405) b.vy *= -1;
                
                // 공 그리기
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let grad = ctx.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
                grad.addColorStop(0, '#fff'); grad.addColorStop(1, b.color);
                ctx.fillStyle = grad; ctx.fill();
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 1; ctx.stroke();
            }});
            requestAnimationFrame(animate);
        }}
        animate();
        setTimeout(() => {{ 
            document.getElementById('info').innerText = '✨ 분석 완료! 행운을 빕니다 ✨';
        }}, 2800);
    </script>
    """

# 5. 분석 시작 버튼 (제한 없음)
if st.button("🚀 AI 프리미엄 분석 시작 (무제한)", use_container_width=True, type="primary"):
    # 행운의 번호 추출
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    # 사운드와 애니메이션 합본 생성
    st.session_state['lotto_html'] = generate_rich_animation(st.session_state['numbers'])
    # 화면 갱신 키값 증가
    st.session_state['update_key'] += 1
    st.rerun()

# 6. 결과 출력 로직
current_html = st.session_state.get('lotto_html', "")
if current_html:
    # 애니메이션 및 사운드 표시
    components.html(current_html, height=440, key=f"rich_engine_{st.session_state['update_key']}")
    
    # 번호 결과 표시
    st.subheader("🔮 추출된 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(st.session_state['numbers']):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:55px; height:55px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:20px; margin:auto; 
            box-shadow: 0 6px 12px rgba(0,0,0,0.5); border: 2px solid #fff;'>
                {n}
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 위 버튼을 눌러 AI 분석을 시작하세요!")

# 7. 하단 통계 그래프
st.divider()
st.subheader("📊 AI 구간별 분석 가중치")
st.bar_chart([random.randint(15, 60) for _ in range(5)])
