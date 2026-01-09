import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="Fortune AI 로또", page_icon="💎", layout="centered")

# 2. 세션 상태 초기화 (데이터 보관함)
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []
if 'update_count' not in st.session_state:
    st.session_state['update_count'] = 0

# 3. 디자인 및 타이틀
st.title("💎 Fortune AI: 프리미엄 로또")
st.write("모든 에러를 해결한 무제한 버전입니다. 행운을 빕니다!")

# 4. 분석 시작 버튼
if st.button("🚀 AI 프리미엄 분석 시작 (무제한)", use_container_width=True, type="primary"):
    # 행운의 번호 생성
    st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
    st.session_state['update_count'] += 1
    # st.rerun() 없이도 아래에서 바로 렌더링되도록 구성

# 5. 결과 화면 출력 (번호가 있을 때만 실행)
if st.session_state['numbers']:
    nums = st.session_state['numbers']
    count = st.session_state['update_count']
    
    # [애니메이션 + 사운드] 통합 HTML
    # 사운드는 브라우저 보안상 클릭 후에만 재생되므로 버튼 클릭 시점에 자동 재생 시도
    lotto_html = f"""
    <div style='width:100%; height:400px; background:#000; border-radius:20px; border:3px solid #ffd700; position:relative; overflow:hidden;'>
        <canvas id='canvas' style='width:100%; height:100%;'></canvas>
        <div id='txt' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-size:18px; font-weight:bold;'>💎 AI 가중치 분석 및 추첨 중...</div>
        <audio autoplay><source src="https://www.soundjay.com/misc/sounds/bell-ringing-04.mp3" type="audio/mp3"></audio>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 400;
        const balls = [];
        for(let i=0; i<45; i++) {{
            balls.push({{
                x: Math.random()*560+20, y: Math.random()*360+20,
                r: 14, color: 'hsl('+(i*8)+', 80%, 60%)',
                vx: (Math.random()-0.5)*16, vy: (Math.random()-0.5)*16
            }});
        }}
        function draw() {{
            ctx.clearRect(0,0,600,400);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<14 || b.x>586) b.vx *= -1;
                if(b.y<14 || b.y>386) b.vy *= -1;
                ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
                let g = ctx.createRadialGradient(b.x-4, b.y-4, 2, b.x, b.y, b.r);
                g.addColorStop(0, '#fff'); g.addColorStop(1, b.color);
                ctx.fillStyle = g; ctx.fill();
            }});
            requestAnimationFrame(draw);
        }}
        draw();
        setTimeout(() => {{ document.getElementById('txt').innerText = '✨ 분석 완료! 행운을 빕니다 ✨'; }}, 2500);
    </script>
    """
    
    # 애니메이션 표시 (매번 새로운 key를 주어 무조건 다시 그리게 함)
    components.html(lotto_html, height=420, key=f"final_lotto_{count}")
    
    # 번호 공 표시
    st.subheader("🔮 추출된 행운의 번호")
    cols = st.columns(6)
    for i, n in enumerate(nums):
        cols[i].markdown(f"""
            <div style='background:radial-gradient(circle at 30% 30%, #f1c40f, #f39c12); color:black; 
            border-radius:50%; width:50px; height:50px; display:flex; align-items:center; 
            justify-content:center; font-weight:bold; font-size:18px; margin:auto; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.4); border: 2px solid #fff;'>
                {n}
            </div>
        """, unsafe_allow_html=True)
else:
    # 데이터가 없을 때만 안내 문구 표시
    st.info("💡 위 버튼을 눌러 AI 프리미엄 분석을 시작하세요!")

# 6. 하단 통계 그래프 (항상 표시)
st.divider()
st.subheader("📊 AI 구간별 분석 가중치 현황")
st.bar_chart([random.randint(20, 60) for _ in range(5)])
