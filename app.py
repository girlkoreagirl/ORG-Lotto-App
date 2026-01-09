import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI 로또", page_icon="💎", layout="centered")

# 2. [필수] 세션 상태 초기화 - 에러 방지를 위해 가장 먼저 실행
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'update_key' not in st.session_state:
    st.session_state['update_key'] = 0

# 3. 메인 타이틀
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("사용 제한 없는 무제한 버전입니다. 행운을 빕니다!")

# 4. 화려한 애니메이션 및 사운드 생성 함수
def get_lotto_ui(nums):
    balls_json = str(nums)
    # 신나는 벨소리 URL
    sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"
    
    return f"""
    <div style='width:100%; height:420px; background:#000; border-radius:20px; border:3px solid #ffd700; position:relative; overflow:hidden;'>
        <canvas id='lottoCanvas' style='width:100%; height:100%;'></canvas>
        <div id='statusText' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:20px; font-weight:bold;'>💎 AI 엔진 가동 및 추첨 중...</div>
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('lottoCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 420;
        const balls = [];
        
        // 45개의 화려한 회전 공 생성
        for(let i=1; i<=45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*380+20,
                r: 15, color: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18
            }});
        }}

        function loop() {{
            ctx.clearRect(0,0,600,420);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>405) b.vy *= -1;
                
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = ctx.createRadialGradient(b.x-5, b.y-5, 2, b.x, b.y, b.r);
                g.addColorStop(0, '#fff'); g.addColorStop(1, b.color);
                ctx.fillStyle = g; ctx.fill();
                ctx.strokeStyle = '#fff'; ctx.stroke();
            }});
            requestAnimationFrame(loop);
        }}
        loop();
        setTimeout(() => {{ document.getElementById('statusText').innerText = '✨ 분석 완료! ✨'; }}, 2500);
    </script>
    """

# 5. 분석 시작 버튼 (무제한)
if st.button("🚀 AI 프리미엄 분석 시작 (무제한)", use_container_width=True, type="primary"):
    # 번호 생성
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    # UI 코드 생성
    st.session_state['lotto_html'] = get_lotto_ui(st.session_state['numbers'])
    # 키값 증가 (화면 갱신용)
    st.session_state['update_key'] += 1
    st.rerun()

# 6. [에러 해결 지점] 결과 출력 로직
# .get()을 사용하고 변수를 따로 빼서 가장 안전하게 호출합니다.
current_content = st.session_state.get('lotto_html', "")
current_key_val = str(st.session_state.get('update_key', 0))

if current_content and len(current_content) > 0:
    try:
        # 애니메이션 표시
        components.html(current_content, height=440, key="lotto_view_" + current_key_val)
        
        # 번호 결과 표시
        st.subheader("🔮 추출된 행운의 번호")
        num_cols = st.columns(6)
        res_nums = st.session_state.get('numbers', [])
        for i, val in enumerate(res_nums):
            num_cols[i].markdown(f"""
                <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
                border-radius:50%; width:55px; height:55px; display:flex; align-items:center; 
                justify-content:center; font-weight:bold; font-size:20px; margin:auto; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.5); border: 2px solid #fff;'>
                    {val}
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.write("화면을 불러오는 중입니다. 잠시만 기다려 주세요.")

# 7. 하단 통계 그래프
st.divider()
st.subheader("📊 AI 구간별 분석 가중치")
st.bar_chart([random.randint(15, 65) for _ in range(5)])
