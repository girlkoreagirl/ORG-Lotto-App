import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import pandas as pd
import time

# --- [1. 앱 설정 및 브랜딩] ---
APP_TITLE = "Fortune AI: 프리미엄 데이터 로또"
APP_ICON = "💎"
DEVELOPER_NAME = "HAN31 창작소" 

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="centered")

# --- [2. 이용 횟수 제한 로직] ---
# Secrets에서 제한 수치 가져오기 (없을 경우 대비해 기본값 5 설정)
try:
    MAX_LIMIT = st.secrets["MAX_LIMIT"]
except:
    MAX_LIMIT = 5

# 세션 상태 초기화
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# --- [3. 실시간 데이터 및 디자인] ---
@st.cache_data(ttl=3600)
def get_lotto_data():
    try:
        # 최신 회차 정보 (예시 회차 1153)
        url = "https://www.dhlotto.co.kr/common.do?method=getLottoNumber&drwNo=1153" 
        r = requests.get(url, timeout=5).json()
        if r.get("returnValue") == "success":
            return r["drwNo"], [r[f"drwtNo{i}"] for i in range(1, 7)], r["bnusNo"]
    except: return None, None, None

drw_no, latest_nums, latest_bonus = get_lotto_data()

st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; }}
    .latest-box {{
        background: #111; padding: 15px; border-radius: 12px;
        border: 1px solid #333; margin-bottom: 20px; text-align: center;
    }}
    .limit-text {{
        color: #ffd700; text-align: center; font-size: 14px; margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title(f"{APP_ICON} {APP_TITLE}")
st.caption(f"Developed by {DEVELOPER_NAME}")

if drw_no:
    st.markdown(f"""
    <div class="latest-box">
        <small style='color: #888;'>공식 {drw_no}회 당첨 번호</small><br>
        <b style='font-size: 20px; color: #ffd700;'>{' . '.join(map(str, latest_nums))} <span style='color:white'>+</span> {latest_bonus}</b>
    </div>
    """, unsafe_allow_html=True)

# --- [4. 이용 횟수 안내 및 버튼 제어] ---
st.markdown(f"<div class='limit-text'>잔여 분석 횟수: {MAX_LIMIT - st.session_state.usage_count}회 / 총 {MAX_LIMIT}회</div>", unsafe_allow_html=True)

if st.session_state.usage_count < MAX_LIMIT:
    if st.button("✨ AI 분석 번호 추출 START", use_container_width=True):
        st.session_state.usage_count += 1
        st.session_state.show_analysis = True
        # 버튼을 누르면 즉시 화면을 갱신하여 애니메이션 실행
else:
    st.error("🚫 오늘의 분석이 종료되었습니다. (이용 횟수 초과)")
    st.info("이용 횟수는 접속 세션이 초기화되면 다시 부여됩니다.")

# --- [5. 로또 추첨 엔진 (애니메이션)] ---
# 사용자가 버튼을 눌렀을 때만 애니메이션 컴포넌트 출력
if st.session_state.show_analysis:
    lotto_html = """
    <div id='container' style='text-align:center; background:#000; padding:20px; border-radius:20px; border: 1px solid #ffd70033;'>
        <canvas id='lottoCanvas' width='400' height='380'></canvas>
        <div id="tray-wrapper" style="margin-top:10px;">
            <div id="tray" style="height:65px; background:linear-gradient(to bottom, #222, #000); border:1px solid #444; border-radius:10px; display:flex; align-items:center; justify-content:center; gap:8px;">
                <div id="main-nums" style="display:flex; gap:8px;"></div>
                <div id="plus" style="color:#ffd700; font-weight:bold; display:none;">+</div>
                <div id="bonus-num" style="display:flex;"></div>
            </div>
        </div>
    </div>

    <script>
    const soundPop = new Audio('https://www.soundjay.com/buttons/sounds/button-21.mp3');
    const soundFinish = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');
    
    const canvas=document.getElementById('lottoCanvas'), ctx=canvas.getContext('2d'),
          mainTray=document.getElementById('main-nums'), bonusTray=document.getElementById('bonus-num'), plus=document.getElementById('plus');

    let balls=[], mixing=true, centerX=200, centerY=190, radius=170;

    function getCol(id){
        if(id<=10) return "#fbc400"; if(id<=20) return "#69c8f2";
        if(id<=30) return "#ff7272"; if(id<=40) return "#aaaaaa"; return "#b0d840";
    }

    class Ball {
        constructor(id){
            this.id=id; this.r=13; this.x=centerX+(Math.random()-0.5)*100; this.y=centerY+(Math.random()-0.5)*100;
            this.vx=(Math.random()-0.5)*12; this.vy=(Math.random()-0.5)*12; this.color=getCol(id);
        }
        draw(){
            ctx.beginPath();
            let g=ctx.createRadialGradient(this.x-4,this.y-4,2,this.x,this.y,this.r);
            g.addColorStop(0,'#fff'); g.addColorStop(1,this.color);
            ctx.fillStyle=g; ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.fill();
            ctx.fillStyle="#000"; ctx.font="bold 11px Arial"; ctx.textAlign="center";
            ctx.fillText(this.id, this.x, this.y+4);
            ctx.closePath();
        }
        update(){
            if(mixing){
                this.vx += (Math.random()-0.5)*4; this.vy += (Math.random()-0.5)*4;
            }
            this.x+=this.vx; this.y+=this.vy; this.vx*=0.98; this.vy*=0.98;
            let dx=this.x-centerX, dy=this.y-centerY, d=Math.sqrt(dx*dx+dy*dy);
            if(d+this.r>radius){
                let nx=dx/d, ny=dy/d, dot=this.vx*nx+this.vy*ny;
                this.vx-=2*dot*nx; this.vy-=2*dot*ny;
                this.x=centerX+nx*(radius-this.r); this.y=centerY+ny*(radius-this.r);
            }
        }
    }

    for(let i=1;i<=45;i++) balls.push(new Ball(i));

    function animate(){
        ctx.clearRect(0,0,400,380);
        ctx.beginPath(); ctx.arc(centerX,centerY,radius,0,Math.PI*2);
        ctx.fillStyle="#111"; ctx.fill(); ctx.strokeStyle="#333"; ctx.lineWidth=5; ctx.stroke(); ctx.closePath();
        balls.forEach(b=>{b.update();b.draw();});
        requestAnimationFrame(animate);
    }

    function createBall(id){
        let d=document.createElement('div');
        d.style=`width:36px;height:36px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, ${getCol(id)});display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;color:black;box-shadow:2px 2px 5px rgba(0,0,0,0.5);animation:pop 0.4s ease-out;`;
        d.innerText=id; 
        soundPop.currentTime = 0; soundPop.play();
        return d;
    }

    animate();

    // 분석 실행 시뮬레이션
    setTimeout(()=>{
        mixing=false;
        let res=[]; while(res.length<7){
            let n=Math.floor(Math.random()*45)+1; if(!res.includes(n)) res.push(n);
        }
        let main = res.slice(0,6).sort((a,b)=>a-b);
        let bonus = res[6];

        main.forEach((n, i) => { 
            setTimeout(() => mainTray.appendChild(createBall(n)), i*500); 
        });
        setTimeout(() => { 
            plus.style.display="block"; 
            bonusTray.appendChild(createBall(bonus));
            setTimeout(() => { soundFinish.play(); }, 500);
        }, 3200);
    }, 1500);

    const s=document.createElement('style');
    s.innerHTML="@keyframes pop{from{transform:scale(0);}to{transform:scale(1);}}";
    document.head.appendChild(s);
    </script>
    """
    components.html(lotto_html, height=550)

# --- [6. 통계 분석 차트] ---
st.subheader("📊 번호 구간별 분석 가중치")
chart_data = pd.DataFrame({
    '구간': ['1-10', '11-20', '21-30', '31-40', '41-45'],
    'AI 추천 강도': [random.randint(20, 50) for _ in range(5)]
})
st.bar_chart(chart_data.set_index('구간'))

with st.sidebar:
    st.header("⚙️ HAN31 창작소")
    st.write(f"현재 설정된 제한: {MAX_LIMIT}회")
    st.write(f"나의 이용 횟수: {st.session_state.usage_count}회")
    st.divider()
    if st.button("초기화 (테스트용)"):
        st.session_state.usage_count = 0
        st.session_state.show_analysis = False
        st.rerun()
