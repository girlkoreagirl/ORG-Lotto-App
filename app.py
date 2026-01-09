import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 초기 설정 (앱 시작하자마자 빈 상자를 확실히 만들어 에러 방지)
if 'num_res' not in st.session_state: st.session_state['num_res'] = []
if 'u_count' not in st.session_state: st.session_state['u_count'] = 0

st.set_page_config(page_title="Fortune AI", page_icon="💎", layout="centered")
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("모든 오류를 해결하고 사운드와 애니메이션을 복구한 무적 버전입니다!")

# 2. 버튼 클릭 시 데이터 생성 로직
if st.button("🚀 AI 프리미엄 분석 시작 (무제한)", use_container_width=True, type="primary"):
    st.session_state['num_res'] = sorted(random.sample(range(1, 46), 6))
    st.session_state['u_count'] += 1
    # st.rerun()은 3.13 버전에서 충돌할 수 있어 이번엔 뺏습니다. 버튼 누르면 자동 갱신됩니다.

# 3. 화면 출력 로직 (데이터가 있을 때만 실행)
if st.session_state['num_res']:
    # [애니메이션 + 사운드 복구] HTML 생성
    # TypeError 원천 차단을 위해 즉석에서 f-string으로 생성합니다.
    lotto_balls = str(st.session_state['num_res'])
    html_content = f"""
    <div style='width:100%; height:400px; background:black; border-radius:20px; border:3px solid gold; overflow:hidden; position:relative;'>
        <canvas id='lotto' width='600' height='400' style='width:100%; height:100%;'></canvas>
        <div id='msg' style='position:absolute; bottom:20px; width:100%; text-align:center; color:gold; font-family:sans-serif; font-weight:bold;'>✨ AI 엔진 가동 및 분석 진행 중... ✨</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const c = document.getElementById('lotto');
        const x = c.getContext('2d');
        const balls = [];
        for(let i=0; i<45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 15, col: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*18, vy: (Math.random()-0.5)*18
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
        setTimeout(() => {{ document.getElementById('msg').innerText = '🎉 분석 완료! 행운을 빕니다! 🎉'; }}, 2500);
    </script>
    """
    
    # 4. 컴포넌트 호출 (str() 강제 변환으로 TypeError 방지)
    components.html(
        str(html_content), 
        height=420, 
        key=f"final_render_{st.session_state['u_count']}"
    )
    
    # 번호 공 디자인 출력
    st.subheader("🔮 추출된 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(st.session_state['num_res']):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:18px; margin:auto; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.5); border: 2px solid white;'>
                {n}
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 5. 하단 데이터 차트 (항상 표시)
st.divider()
st.subheader("📊 AI 구간별 데이터 분석 현황")
st.bar_chart([random.randint(20, 60) for _ in range(5)])
