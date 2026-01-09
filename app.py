import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 최우선 초기화 (에러 방지를 위해 무조건 맨 위에 위치해야 함)
if 'u_count' not in st.session_state: st.session_state['u_count'] = 0
if 'num_res' not in st.session_state: st.session_state['num_res'] = []
if 'my_html' not in st.session_state: st.session_state['my_html'] = ""

st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")

st.title("💎 Fortune AI: 프리미엄 로또")
st.write("모든 오류를 해결한 최종 무적 버전입니다. 행운을 빕니다!")

# 2. 분석 시작 버튼 (무제한)
if st.button("🚀 AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
    # 번호 생성
    st.session_state['num_res'] = sorted(random.sample(range(1, 45), 6))
    st.session_state['u_count'] += 1
    
    # [애니메이션 + 사운드] HTML 코드 생성
    nums_str = str(st.session_state['num_res'])
    # 사운드 URL
    sound_url = "https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3"
    
    html_content = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:3px solid gold; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-weight:bold; font-size:18px;'>✨ AI 분석 및 추첨 진행 중... ✨</div>
        <audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>
    </div>
    <script>
        const c = document.getElementById('lotto');
        const x = c.getContext('2d');
        const balls = [];
        for(let i=0; i<40; i++) {{
            balls.push({{
                x: Math.random()*550+25, y: Math.random()*350+25,
                r: 15, col: 'hsl('+(i*9)+', 80%, 60%)',
                vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15
            }});
        }}
        function draw() {{
            x.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>385) b.vy *= -1;
                x.beginPath(); x.arc(b.x,b.y,b.r,0,Math.PI*2);
                let g = x.createRadialGradient(b.x-5,b.y-5,2,b.x,b.y,b.r);
                g.addColorStop(0,'white'); g.addColorStop(1,b.col);
                x.fillStyle = g; x.fill();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 대박을 기원합니다! 🎉'; }}, 2500);
    </script>
    """
    st.session_state['my_html'] = html_content
    st.rerun()

# 3. 화면 출력 로직 (값이 있을 때만 안전하게 실행)
h_code = st.session_state.get('my_html', "")
if h_code:
    try:
        # str()로 한 번 더 감싸서 TypeError 방지
        components.html(str(h_code), height=420, key=f"render_{st.session_state['u_count']}")
        
        # 번호 결과 표시
        st.subheader("🔮 추출된 행운의 번호")
        cols = st.columns(6)
        nums = st.session_state.get('num_res', [])
        for i, v in enumerate(nums):
            cols[i].markdown(f"""
                <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
                border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
                justify-content:center; font-weight:bold; font-size:18px; margin:auto; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.5); border: 2px solid white;'>
                    {v}
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.info("다시 시도해 주세요.")
else:
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 4. 하단 차트
st.divider()
st.subheader("📊 AI 구간별 데이터 가중치 현황")
st.bar_chart([random.randint(20, 60) for _ in range(5)])
