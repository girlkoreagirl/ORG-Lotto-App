import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import pandas as pd
import time

# --- [1. 최우선 세션 상태 초기화] ---
# 앱 시작 시 변수들이 없으면 빈 문자열("") 및 기본값으로 확실히 선언
if 'lotto_html' not in st.session_state:
    st.session_state['lotto_html'] = ""
if 'usage_count' not in st.session_state:
    st.session_state['usage_count'] = 0
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

# --- [2. 앱 설정 및 브랜딩] ---
st.set_page_config(page_title="Fortune AI: 프리미엄 데이터 로또", page_icon="💎", layout="centered")

# --- [3. 관리자 및 제한 설정 로드] ---
try:
    MAX_LIMIT = st.secrets.get("MAX_LIMIT", 5)
    ADMIN_KEY = st.secrets.get("ADMIN_KEY", "admin1234")
except:
    MAX_LIMIT = 5
    ADMIN_KEY = "admin1234"

# --- [4. 사이드바: 관리자 인증 및 상태 표시] ---
with st.sidebar:
    st.header("💎 HAN31 창작소")
    st.write(f"이용 한도: **{MAX_LIMIT}회**")
    st.write(f"현재 이용: **{st.session_state['usage_count']}회**")
    st.divider()
    
    st.subheader("🔐 관리자 인증")
    admin_input = st.text_input("인증키 입력", type="password")
    if admin_input == ADMIN_KEY:
        st.session_state['is_admin'] = True
        st.success("🔓 관리자 모드 활성화됨")
    elif admin_input:
        st.error("인증키가 일치하지 않습니다.")
        st.session_state['is_admin'] = False

    st.divider()
    if st.button("🔄 세션 초기화"):
        st.session_state['usage_count'] = 0
        st.session_state['lotto_html'] = ""
        st.rerun()

# --- [5. 실시간 데이터 가져오기] ---
@st.cache_data(ttl=3600)
def get_lotto_data():
    try:
        url = "https://www.dhlotto.co.kr/common.do?method=getLottoNumber&drwNo=1154" 
        r = requests.get(url, timeout=5).json()
        if r.get("returnValue") == "success":
            return r["drwNo"], [r[f"drwtNo{i}"] for i in range(1, 7)], r["bnusNo"]
    except: return None, None, None

drw_no, latest_nums, latest_bonus = get_lotto_data()

st.markdown("<style>.stApp { background-color: #050505; color: white; }</style>", unsafe_allow_html=True)
st.title("💎 Fortune AI: 프리미엄 분석")

if drw_no:
    st.markdown(f"""
    <div style="background:#111; padding:15px; border-radius:12px; border:1px solid #333; margin-bottom:20px; text-align:center;">
        <small style='color:#888;'>제 {drw_no}회 당첨 번호</small><br>
        <b style='font-size:20px; color:#ffd700;'>{' . '.join(map(str, latest_nums))} + {latest_bonus}</b>
    </div>
    """, unsafe_allow_html=True)

# --- [6. 추출 버튼 및 즉시 렌더링 로직] ---
is_allowed = st.session_state['is_admin'] or (st.session_state['usage_count'] < MAX_LIMIT)

if not is_allowed:
    st.error("🚫 이용 횟수가 소진되었습니다. 관리자 인증이 필요합니다.")
else:
    # [가장 중요] 버튼 클릭 시 즉시 HTML 생성 및 rerun 호출
    if st.button("✨ AI 프리미엄 번호 추출 START", use_container_width=True, type="primary"):
        st.session_state['usage_count'] += 1
        
        # 번호 생성
        res = random.sample(range(1, 46), 7)
        main_nums = sorted(res[:6])
        bonus_num = res[6]
        
        # HTML 코드를 세션에 즉시 저장
        st.session_state['lotto_html'] = f"""
        <div id='container' style='text-align:center; background:#000; padding:20px; border-radius:20px; border:1px solid #ffd70033;'>
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
        const res_main = {main_nums};
        const res_bonus = {bonus_num};

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
            res_main.forEach((n, i) => {{
                setTimeout(() => {{ mainTray.appendChild(createBall(n)); }}, i*600);
            }});
            setTimeout(() => {{
                plus.style.display="block";
                bonusTray.appendChild(createBall(res_bonus));
                setTimeout(() => {{ soundFinish.play(); }}, 300);
            }}, 3800);
        }}, 2000);
        </script>
        <style>@keyframes pop{{from{{transform:scale(0);}}to{{transform:scale(1);}}}}</style>
        """
        # 강제 리프레시를 통해 화면 최상단부터 다시 읽어 세션에 저장된 HTML을 렌더링하도록 함
        st.rerun()

# --- [7. 조건부 렌더링 및 유니크 Key 적용] ---
if st.session_state['lotto_html'] != "":
    # time.time()을 key로 사용하여 브라우저가 매번 새로운 컴포넌트로 인식하게 함 (멈춤 방지)
    components.html(
        st.session_state['lotto_html'], 
        height=480, 
        key=f"engine_{time.time()}"
    )
else:
    st.info("💡 위 버튼을 눌러 AI 분석을 시작하세요.")

# --- [8. 통계 차트] ---
st.subheader("📊 AI 구간별 분석 가중치")
chart_data = pd.DataFrame({
    '구간': ['1-10', '11-20', '21-30', '31-40', '41-45'],
    '가중치': [random.randint(20, 50) for _ in range(5)]
})
st.bar_chart(chart_data.set_index('구간'))
