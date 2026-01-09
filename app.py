import streamlit as st
import streamlit.components.v1 as components
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="Fortune AI: 프리미엄 데이터 로또", page_icon="💎", layout="centered")

# 2. 세션 상태(주머니) 초기화 - 앱 시작 시 에러 방지
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'last_updated' not in st.session_state:
    st.session_state['last_updated'] = 0.0
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'numbers' not in st.session_state:
    st.session_state['numbers'] = []

# 3. 설정값 불러오기 (Secrets 리모컨)
# 관리자 암호와 제한 횟수가 설정되어 있지 않을 때를 대비한 기본값 설정
ADMIN_PASSWORD = st.secrets.get("ADMIN_KEY", "owner123")
MAX_LIMIT = st.secrets.get("MAX_LIMIT", 5)

# 4. 사이드바 - 관리자 모드 및 정보
with st.sidebar:
    st.header("💎 HAN31 창작소")
    st.write("본 앱은 엔터테인먼트 목적으로 제작되었습니다.")
    st.divider()
    
    st.subheader("⚙️ 관리자 설정")
    admin_input = st.text_input("관리자 암호를 입력하세요", type="password")
    is_admin = (admin_input == ADMIN_PASSWORD)
    
    if is_admin:
        st.success("🔓 관리자 모드 활성화됨 (무제한)")
    else:
        st.info(f"📊 나의 분석 현황: {st.session_state['usage_count']} / {MAX_LIMIT}회")

# 5. 메인 화면 타이틀
st.title("💎 Fortune AI: 프리미엄 데이터 로또")
st.write("Powered by Advanced Physics Engine | Developed by HAN31 창작소")

# 6. 추첨 로직 함수
def generate_lotto_animation(numbers):
    # 공 애니메이션 HTML 코드 (2회차 실행 시에도 다시 돌도록 key값 최적화)
    balls_json = str(numbers)
    html_code = f"""
    <div id='lotto-container' style='width:100%; height:450px; background:#000; border-radius:20px; position:relative; overflow:hidden; border:2px solid #333;'>
        <canvas id='lottoCanvas'></canvas>
        <div id='status' style='position:absolute; bottom:20px; width:100%; text-align:center; color:#ffd700; font-family:sans-serif; font-weight:bold;'>ANALYZING DATA...</div>
    </div>
    <script>
        const canvas = document.getElementById('lottoCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 600; canvas.height = 400;
        const balls = [];
        const targetNumbers = {balls_json};
        
        // 공 생성 및 물리 엔진 로직 (간략화된 버전)
        for(let i=0; i<45; i++) {{
            balls.push({{
                x: Math.random()*500+50, y: Math.random()*300+50,
                radius: 15, color: 'hsl('+(i*8)+', 70%, 60%)',
                vx: (Math.random()-0.5)*10, vy: (Math.random()-0.5)*10
            }});
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            balls.forEach(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.x<15 || b.x>585) b.vx *= -1;
                if(b.y<15 || b.y>385) b.vy *= -1;
                ctx.beginPath(); ctx.arc(b.x, b.y, b.radius, 0, Math.PI*2);
                ctx.fillStyle = b.color; ctx.fill();
            }});
            requestAnimationFrame(animate);
        }}
        animate();
        setTimeout(() => {{ document.getElementById('status').innerText = 'EXTRACTION COMPLETE'; }}, 3000);
    </script>
    """
    return html_code

# 7. 사운드 재생 함수 (HTML 이용)
def play_sound(sound_url):
    sound_html = f"""
    <audio autoplay>
        <source src="{sound_url}" type="audio/mp3">
    </audio>
    """
    components.html(sound_html, height=0)

# 8. 메인 실행 버튼 섹션
can_use = is_admin or (st.session_state['usage_count'] < MAX_LIMIT)

if can_use:
    if st.button("✨ AI 프리미엄 분석 시작", use_container_width=True, type="primary"):
        # 사운드 재생 (무료 효과음 URL)
        play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
        
        # 번호 생성 및 상태 업데이트
        st.session_state['numbers'] = sorted(random.sample(range(1, 46), 6))
        st.session_state['lotto_html'] = generate_lotto_animation(st.session_state['numbers'])
        st.session_state['last_updated'] = time.time()
        st.session_state['usage_count'] += 1
        st.rerun() # 화면 즉시 갱신
else:
    st.error("🚫 오늘의 분석이 종료되었습니다.")
    st.warning("한정된 AI 자원 보호를 위해 세션당 이용 횟수를 제한하고 있습니다.")

# 9. 애니메이션 및 결과 출력 (데이터가 있을 때만)
if st.session_state['lotto_html']:
    try:
        # 공 애니메이션 표시
        components.html(
            st.session_state['lotto_html'], 
            height=480, 
            key=f"lotto_engine_{st.session_state['last_updated']}"
        )
        
        # 결과 번호 표시
        nums = st.session_state['numbers']
        st.subheader("🔮 분석된 행운의 번호")
        cols = st.columns(6)
        for i, n in enumerate(nums):
            cols[i].markdown(f"<div style='background:#f1c40f; color:black; border-radius:50%; width:50px; height:50px; display:flex; align-items:center; justify-content:center; font-weight:bold; margin:auto;'>{n}</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error("애니메이션 로드 중 오류가 발생했습니다. 다시 시도해 주세요.")

# 10. 통계 그래프 (항상 표시)
st.divider()
st.subheader("📊 AI 구간별 분석 데이터")
chart_data = {
    "1-10": random.randint(20, 50),
    "11-20": random.randint(20, 50),
    "21-30": random.randint(20, 50),
    "31-40": random.randint(20, 50),
    "41-45": random.randint(20, 50)
}
st.bar_chart(chart_data)
