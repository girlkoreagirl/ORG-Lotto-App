import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Fortune AI", layout="centered")

st.markdown("""<style>
    .main { background-color: #0e1117; }
    .stButton>button { background: linear-gradient(#f1c40f, #d4ac0d); color: black; font-weight: bold; border-radius: 30px; width: 100%; height: 50px; border: none; }
</style>""", unsafe_allow_html=True)

if "nums" not in st.session_state: st.session_state.nums, st.session_state.bonus, st.session_state.rid = [6,12,15,19,30,39], 33, 0

st.markdown("<h1 style='text-align:center; color:white;'>💎 Fortune AI: 프리미엄 로또</h1>", unsafe_allow_html=True)

res_h = "".join([f"<div style='width:35px;height:35px;border-radius:50%;background:white;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;margin:2px;'>{n}</div>" for n in st.session_state.nums])
html_c = f"""
<div style='background:#111;border-radius:20px;padding:20px;display:flex;flex-direction:column;align-items:center;'>
    <canvas id='l' width='400' height='300'></canvas>
    <div style='margin-top:20px;background:#000;padding:10px 20px;border-radius:50px;display:flex;gap:10px;align-items:center;border:1px solid #444;'>
        {res_h} <span style='color:white;'>+</span> <div style='width:35px;height:35px;border-radius:50%;background:#3498db;color:black;display:flex;align-items:center;justify-content:center;font-weight:bold;'>{st.session_state.bonus}</div>
    </div>
</div>
<script>
    const c=document.getElementById('l'),x=c.getContext('2d'),balls=[];
    for(let i=1;i<=45;i++) balls.push({{x:200,y:150,vx:(Math.random()-0.5)*12,vy:(Math.random()-0.5)*12,r:10,col:'hsl('+(i*8)+',70%,60%)'}});
    function d(){{
        x.clearRect(0,0,400,300);x.beginPath();x.arc(200,150,140,0,Math.PI*2);x.fillStyle='#050505';x.fill();
        balls.forEach(b=>{{
            b.x+=b.vx;b.y+=b.vy;const dist=Math.sqrt((b.x-200)**2+(b.y-150)**2);
            if(dist+b.r>140){{const nx=(b.x-200)/dist,ny=(b.y-150)/dist,dot=b.vx*nx+b.vy*ny;b.vx-=2*dot*nx;b.vy-=2*dot*ny;b.x=200+nx*(140-b.r);b.y=150+ny*(140-b.r);}}
            x.beginPath();x.arc(b.x,b.y,b.r,0,Math.PI*2);x.fillStyle=b.col;x.fill();
        }});requestAnimationFrame(d);
    }}d();
</script>"""

components.html(html_c, height=480, key=f"v_{st.session_state.rid}")

if st.button("✨ 다시 분석하기"):
    r = random.sample(range(1, 46), 7)
    st.session_state.nums, st.session_state.bonus, st.session_state.rid = sorted(r[:6]), r[6], st.session_state.rid+1
    st.rerun()
