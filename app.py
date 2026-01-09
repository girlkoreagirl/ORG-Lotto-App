import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import pandas as pd

# --- [1. 앱 설정 및 초기화] ---
APP_TITLE = "Fortune AI: 프리미엄 데이터 로또"
APP_ICON = "💎"
DEVELOPER_NAME = "HAN31 창작소" 

# lotto_html 변수 초기화 (코드 시작 시점)
lotto_html = ""

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="centered")

# --- [2. 세션 상태 관리] ---
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0  # 애니메이션 강제 갱신용 ID

# --- [3. 설정값 로드 및 예외 처리] ---
try:
    MAX_LIMIT = st.secrets.get("MAX_LIMIT", 5)
    ADMIN_KEY = st.secrets.get("ADMIN_KEY", "admin1234")
except Exception as e:
    MAX_LIMIT = 5
    ADMIN_KEY = "admin1234"
    st.warning("설정 파일을 불러오지 못해 기본값으로 작동합니다.")

# --- [4. 관리자 인증 시스템 (사이드바 맨 아래)] ---
with st.sidebar:
    st.header(f"{APP_ICON} {DEVELOPER_NAME}")
    st.write(f"일반 이용 한도: **{MAX_LIMIT}회**")
    st.write(f"현재 이용 횟수: **{st.session_state.usage_count}회**")
    st.divider()
    
    # 관리자 인증 칸
    st.subheader("🔐 시스템 제어")
    input_key = st.text_input("관리자 인증키 입력", type="password", placeholder="비밀번호를 입력하세요")
    
    if input_key == ADMIN_KEY:
        st.session_state.is_admin = True
        st.success("🔓 관리자 모드 활성화됨")
        st.caption("이용 제한 없이 무제한으로 분석이 가능합니다.")
    elif input_key:
        st.error("암호가 일치하지 않습니다.")
        st.session_state.is_admin = False

    st.divider()
    if st.button("🔄 세션 초기화"):
        st.session_state.usage_count = 0
        st.session_state.run_id = 0
        st.rerun()

# --- [5. 실시간 데이터 가져오기 (예외 처리 포함)] ---
@st.cache_data(ttl=3600)
def get_lotto_data():
    try:
        # 최신 회차 API 호출
        url = "https://www.dhlotto.co.kr/common.do?method=getLottoNumber&drwNo=1153" 
        r = requests.get(url, timeout=5).json()
        if r.get("returnValue") == "success":
            return r["drwNo"], [r[f"drwtNo{i}"] for i in range(1, 7)], r["bnusNo"]
    except Exception as e:
        # 에러 발생 시 로그만 남기고 None 반환하여 앱 멈춤 방지
        print(f"Data Fetch Error: {e}")
    return None, None, None

try:
    drw_no, latest_nums, latest_bonus = get_lotto_data()
except:
    drw_no, latest_nums, latest_bonus = None, None, None

# --- [6. UI 스타일링 및 헤더] ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .latest-box {
        background: #111; padding: 15px; border-radius: 12px;
        border: 1px solid #333; margin-bottom: 20px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title(f"{APP_ICON} {APP_TITLE}")

if drw_no:
    st.markdown(f"""
    <div class="latest-box">
        <small style='color: #888;'>공식 {drw_no}회 당첨 번호</small><br>
        <b style='font-size: 20px; color: #ffd700;'>{' . '.join(map(str, latest_nums))} <span style='color:white'>+</span> {latest_bonus}</b>
    </div>
    """, unsafe_allow_html=True)

# --- [7. 분석 시작 로직 및 애니메이션 제어] ---
# 제한 확인 (관리자라면 무조건 통과)
is_allowed = st.session_state.is_admin or (st.session_state.usage_count < MAX_LIMIT)

if not is_allowed:
    st.error("🚫 오늘의 분석 이용 횟수가 모두 소진되었습니다.")
    st.info("관리자 인증을 하거나 세션을 초기화해주세요.")
else:
    # 이용 가능한 경우에만 버튼 활성화
    if st.button("✨ AI 프리미엄 번호 추출 START", use_container_width=True, type="primary"):
        try:
            st.session_state.usage_count += 1
            st.session_state.run_id += 1  # Key를 변경하여 애니메이션 재생 유도
        except Exception as e:
            st.error("분석 엔진 작동 중 오류가 발생했습니다.")

# 이용 제한에 걸리지 않았고, 실행 버튼이 한 번이라도 눌렸을 때만 컴포넌트 호출
if is_allowed and st.session_state.run_id > 0:
    try:
        # 번호 생성 로직
        nums = random.sample(range(1, 46), 7)
        main_nums = sorted(nums[:6])
        bonus_num = nums[6]

        # lotto_html 문자열 구성
        lotto_html = f"""
        <div id='container' style='text-align:center; background:#000; padding:20px; border-radius:20px; border: 1px solid #ffd70033;'>
            <canvas id='lottoCanvas' width='400' height='350'></canvas>
            <div id="tray" style="height:70px; background:linear-gradient(to bottom, #111, #000); border:1px solid #444; border-radius:12px; display:flex; align-items:center; justify-content:center; gap:8px;">
                <div id="main-nums" style="display:flex; gap:8px;"></div>
                <div id="plus" style="color:#ffd700; font-weight:bold; display:none;">+</div>
                <div id="bonus-num" style="display:flex;"></div>
            </div>
        </div>

        <script>
        const soundPop = new Audio('https://www.soundjay.com/buttons/sounds/button-21.mp3');
        const soundFinish = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

        const canvas=document.getElementById('lottoCanvas'), ctx=canvas.getContext('2d'),
              mainTray=document.getElementById('main-nums'), bonusTray=document.getElementById('bonus-num'), plus=document.getElementById('plus');

        let balls=[], mixing=true, centerX=200, centerY=175, radius=150;
        const result_main = {main_nums};
        const result_bonus = {bonus_num};

        function getCol(id){{
            if(id<=10) return "#fbc400"; if(id<=20) return "#69c8f2";
            if(id<=30) return "#ff7272"; if(id<=40) return "#aaaaaa"; return "#b0d840";
        }}

        class Ball {{
            constructor(id){{
                this.id=id; this.r=12; this.x=centerX+(Math.random()-0.5)*100; this.y=centerY+(Math.random()-0.5)*100;
                this.vx=(Math.random()-0.5)*15; this.vy=(Math.random()-0.5)*15; this.color=getCol(id);
            }}
            draw(){{
                ctx.beginPath();
                let g=ctx.createRadialGradient(this.x-4,this.y-4,2,this.x,this.y,this.r);
                g.addColorStop(0,'#fff'); g.addColorStop(1,this.color);
                ctx.fillStyle=g; ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.fill();
                ctx.fillStyle="#000"; ctx.font="bold 10px Arial"; ctx.textAlign="center"; ctx.fillText(this.id, this.x, this.y+4);
                ctx.closePath();
            }}
            update(){{
                if(mixing) {{ this.vx += (Math.random()-0.5)*5; this.vy += (Math.random()-0.5)*5; }}
                this.x+=this.vx; this.y+=this.vy; this.vx*=0.99; this.vy*=0.99;
                let dx=this.x-centerX, dy=this.y-centerY, d=Math.sqrt(dx*dx+dy*dy);
                if(d+this.r>radius){{
                    let nx=dx/d, ny=dy/d, dot=this.vx*nx+this.vy*ny;
                    this.vx-=2*dot*nx; this.vy-=2*dot*ny;
                    this.x=centerX+nx*(radius-this.r); this.y=centerY+ny*(radius-this.r);
                }}
            }}
        }}

        for(let i=1;i<=45;i++) balls.push(new Ball(i));

        function animate(){{
            ctx.clearRect(0,0,400,350);
            ctx.beginPath(); ctx.arc(centerX,centerY,radius,0,Math.PI*2);
            ctx.fillStyle="#0a0a0a"; ctx.fill(); ctx.strokeStyle="#333"; ctx.lineWidth=5; ctx.stroke(); ctx.closePath();
            balls.forEach(b=>{{b.update();b.draw();}});
            requestAnimationFrame(animate);
        }}

        function createBall(id){{
            let d=document.createElement('div');
            d.style=`width:36px;height:36px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, ${{getCol(id)}});display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;color:black;animation:pop 0.5s ease-out;`;
            d.innerText=id; soundPop.currentTime=0; soundPop.play(); return d;
        }}

        animate();

        setTimeout(()=>{{
            mixing=false;
            result_main.forEach((n, i) => {{
                setTimeout(() => {{ mainTray.appendChild(createBall(n)); }}, i*600);
            }});
            setTimeout(() => {{
                plus.style.display="block";
                bonusTray.appendChild(createBall(result_bonus));
                setTimeout(() => {{ soundFinish.play(); }}, 300);
            }}, 3800);
        }}, 2000);
        </script>
        <style>@keyframes pop{{from{{transform:scale(0);}}to{{transform:scale(1);}}}}</style>
        """
        
        # [핵심] key 파라미터에 run_id를 넣어 매 실행 시 컴포넌트를 강제 재생성함 (버그 수정)
        components.html(lotto_html, height=480, key=f"lotto_engine_{st.session_state.run_id}")

    except Exception as e:
        st.error("애니메이션 렌더링 중 오류가 발생했습니다.")

# --- [8. 통계 섹션 (예외 처리 포함)] ---
try:
    st.subheader("📊 AI 분석 가중치 현황")
    chart_data = pd.DataFrame({
        '구간': ['1-10', '11-20', '21-30', '31-40', '41-45'],
        '가중치': [random.randint(20, 50) for _ in range(5)]
    })
    st.bar_chart(chart_data.set_index('구간'))
except:
    st.write("통계 데이터를 표시할 수 없습니다.")
