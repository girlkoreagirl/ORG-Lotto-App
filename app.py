import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import pandas as pd
from datetime import datetime

# --- [기본 설정 생략 (기존과 동일)] ---
st.set_page_config(page_title="Fortune AI: 프리미엄 데이터 로또", page_icon="💎", layout="centered")

# --- [디자인 스타일링 (기존과 동일)] ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: white; }}
    .latest-box {{
        background: linear-gradient(145deg, #111, #1a1a1a);
        padding: 20px; border-radius: 15px;
        border: 1px solid #333; margin-bottom: 25px; text-align: center;
    }}
    .ball-mini {{
        display: inline-block; width: 28px; height: 28px; line-height: 28px;
        border-radius: 50%; margin: 2px; font-weight: bold; font-size: 13px; color: black; text-align: center;
    }}
    .c1 {{ background: #fbc400; }} .c2 {{ background: #69c8f2; }}
    .c3 {{ background: #ff7272; }} .c4 {{ background: #aaaaaa; }} .c5 {{ background: #b0d840; }}
    </style>
""", unsafe_allow_html=True)

st.title("💎 Fortune AI: 프리미엄 데이터 로또")

# --- [로또 추첨 엔진 + 사운드 추가] ---
lotto_html = """
<div id='container' style='text-align:center; background:#000; padding:20px; border-radius:20px; border: 1px solid #ffd70033;'>
    <canvas id='lottoCanvas' width='400' height='380'></canvas>
    <div id="tray-wrapper" style="margin-top:10px;">
        <div id="status-text" style="font-size:11px; color:#ffd700; margin-bottom:8px; height:15px;">READY</div>
        <div id="tray" style="height:70px; background:linear-gradient(to bottom, #111, #000); border:1px solid #444; border-radius:12px; display:flex; align-items:center; justify-content:center; gap:8px;">
            <div id="main-nums" style="display:flex; gap:8px;"></div>
            <div id="plus" style="color:#ffd700; font-weight:bold; display:none;">+</div>
            <div id="bonus-num" style="display:flex;"></div>
        </div>
    </div>
    <button id='btn' style='margin-top:20px; width:100%; padding:18px; background:linear-gradient(135deg, #ffd700, #b8860b); border:none; border-radius:50px; font-weight:bold; font-size:18px; cursor:pointer; color:#000;'>✨ AI 분석 번호 추출 START</button>
</div>

<script>
// --- [사운드 리소스 설정] ---
const soundStart = new Audio('https://www.soundjay.com/buttons/sounds/button-19.mp3'); // 시작/클릭음
const soundPop = new Audio('https://www.soundjay.com/buttons/sounds/button-21.mp3');   // 공 나올 때
const soundFinish = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3'); // 최종 완료음 (짧은 종소리)

const canvas=document.getElementById('lottoCanvas'), ctx=canvas.getContext('2d'), btn=document.getElementById('btn'), 
      mainTray=document.getElementById('main-nums'), bonusTray=document.getElementById('bonus-num'), 
      plus=document.getElementById('plus'), statusText=document.getElementById('status-text');

let balls=[], mixing=false, centerX=200, centerY=190, radius=170;

function getCol(id){
    if(id<=10) return "#fbc400"; if(id<=20) return "#69c8f2";
    if(id<=30) return "#ff7272"; if(id<=40) return "#aaaaaa"; return "#b0d840";
}

class Ball {
    constructor(id){
        this.id=id; this.r=13; this.x=centerX+(Math.random()-0.5)*100; this.y=centerY+(Math.random()-0.5)*100;
        this.vx=(Math.random()-0.5)*10; this.vy=(Math.random()-0.5)*10; this.color=getCol(id);
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
            let a = Math.atan2(this.y-centerY, this.x-centerX);
            this.vx += Math.cos(a+Math.PI/2)*3 + (Math.random()-0.5)*10;
            this.vy += Math.sin(a+Math.PI/2)*3 + (Math.random()-0.5)*10;
        }
        this.x+=this.vx; this.y+=this.vy; this.vx*=0.99; this.vy*=0.99;
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
    ctx.fillStyle="#0a0a0a"; ctx.fill(); ctx.strokeStyle="#333"; ctx.lineWidth=8; ctx.stroke(); ctx.closePath();
    balls.forEach(b=>{b.update();b.draw();});
    requestAnimationFrame(animate);
}

function createBall(id){
    let d=document.createElement('div');
    d.style=`width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff, ${getCol(id)});display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:bold;color:black;box-shadow:2px 4px 8px rgba(0,0,0,0.5);animation:pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);`;
    d.innerText=id; 
    
    // 공이 생성될 때 톡! 소리 재생
    soundPop.currentTime = 0; 
    soundPop.play();
    
    return d;
}

btn.onclick=()=>{
    if(mixing) return;
    
    // 시작 사운드 재생
    soundStart.play();
    
    mixing=true; mainTray.innerHTML=""; bonusTray.innerHTML=""; plus.style.display="none";
    statusText.innerText="ANALYZING DATA PATTERNS...";
    btn.innerText="🌪️ AI 엔진 분석 중...";
    btn.style.opacity="0.5";
    
    setTimeout(()=>{
        mixing=false;
        statusText.innerText="EXTRACTION COMPLETE";
        btn.innerText="✨ 다시 분석하기";
        btn.style.opacity="1";
        
        let res=[]; while(res.length<7){
            let n=Math.floor(Math.random()*45)+1; if(!res.includes(n)) res.push(n);
        }
        let main = res.slice(0,6).sort((a,b)=>a-b);
        let bonus = res[6];

        main.forEach((n, i) => { 
            setTimeout(() => {
                mainTray.appendChild(createBall(n));
            }, i*600); 
        });
        
        setTimeout(() => { 
            plus.style.display="block"; 
            bonusTray.appendChild(createBall(bonus));
            
            // 마지막 보너스 번호까지 나오면 성공 사운드!
            setTimeout(() => { soundFinish.play(); }, 500);
            
        }, 3800);
    }, 2500);
};

const s=document.createElement('style');
s.innerHTML="@keyframes pop{from{transform:scale(0) rotate(-180deg);}to{transform:scale(1) rotate(0);}}";
document.head.appendChild(s);
animate();
</script>
"""

components.html(lotto_html, height=660)

# --- [하단 통계 부분 생략 (기존과 동일)] ---
st.info("💡 버튼을 누르면 물리 엔진 시뮬레이션과 함께 분석 사운드가 재생됩니다.")
