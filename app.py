
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import base64

# --- CONFIGURATION ---
st.set_page_config(
    page_title="THE STRAT ARCADE",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- NEON ARCADE CSS ---
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

    /* GLOBAL THEME */
    .stApp {
        background-color: #050510;
        color: #e0e0e0;
        font-family: 'VT323', monospace;
    }

    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        color: #ff00ff;
        text-shadow: 4px 4px 0px #000, -2px -2px 0px #00ffff;
        margin-bottom: 20px;
    }
    
    .big-text {
        font-size: 24px;
        color: #00ffff;
    }

    /* BUTTONS */
    .stButton > button {
        background-color: #000000;
        color: #00ff00;
        border: 2px solid #00ff00;
        font-family: 'Press Start 2P', cursive;
        font-size: 14px;
        text-transform: uppercase;
        padding: 10px 20px;
        transition: all 0.1s;
        box-shadow: 0 0 10px #00ff00;
    }

    .stButton > button:hover {
        background-color: #00ff00;
        color: #000000;
        box-shadow: 0 0 20px #00ff00, inset 0 0 10px #000;
    }

    .stButton > button:active {
        transform: translateY(2px);
    }
    
    /* CRT EFFECT OVERLAY */
    .crt::before {
        content: " ";
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }
    
    /* UTILS */
    .neon-box {
        border: 2px solid #ff00ff;
        box-shadow: 0 0 15px #ff00ff;
        padding: 20px;
        background: #111;
        margin-bottom: 20px;
    }
    
    .status-bar {
        font-family: 'Press Start 2P';
        font-size: 12px;
        color: #ffff00;
        padding: 10px;
        border-bottom: 2px solid #ffff00;
        margin-bottom: 20px;
    }

</style>
<div class="crt"></div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'state' not in st.session_state:
    st.session_state.state = 'SPLASH' # SPLASH, TUTORIAL, GAME
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'tutorial_step' not in st.session_state:
    st.session_state.tutorial_step = 0

# --- SOUND ENGINE (Simple HTML Audio) ---
def play_sound(type):
    # Base64 encoded simple beeps (placeholders)
    # Ideally, we would generate these or load small mp3s. 
    # For MVP, using short silent placeholders or minimal data URIs if possible.
    # To properly work without external files, we skip actual binary data here 
    # and just show a visual indicator or use a very short beep if available.
    pass 

# --- CHART ENGINE ---
def generate_candle_data(n=5):
    # Generate random walk
    time_arr = np.arange(n)
    open_p = 100 + np.cumsum(np.random.randn(n) * 2)
    close_p = open_p + np.random.randn(n) * 2
    high_p = np.maximum(open_p, close_p) + np.abs(np.random.randn(n))
    low_p = np.minimum(open_p, close_p) - np.abs(np.random.randn(n))
    
    # Enforce last candle type for learning
    # Example: Force an Inside Bar (1)
    prev_h = high_p[-2]
    prev_l = low_p[-2]
    
    # Force Inside
    high_p[-1] = prev_h - 0.5
    low_p[-1] = prev_l + 0.5
    if open_p[-1] > high_p[-1]: open_p[-1] = high_p[-1]
    if close_p[-1] > high_p[-1]: close_p[-1] = high_p[-1]
    if open_p[-1] < low_p[-1]: open_p[-1] = low_p[-1]
    if close_p[-1] < low_p[-1]: close_p[-1] = low_p[-1]
    
    df = pd.DataFrame({
        'time': time_arr,
        'open': open_p,
        'high': high_p,
        'low': low_p,
        'close': close_p
    })
    return df

def plot_candles(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#ff00ff', # Neon Pink
        decreasing_line_color='#39ff14', # Neon Green
        line_width=2
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='#222', zeroline=False, showticklabels=True)
    )
    return fig

# --- SCREENS ---

def splash_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>THE STRAT<br>ARCADE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00ffff;' class='big-text'>Train your eyes. Level up.<br>Become Inevitable.</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("PRESS START", use_container_width=True):
            st.session_state.state = 'TUTORIAL'
            st.rerun()

def tutorial_screen():
    st.markdown("<div class='status-bar'>TUTORIAL MODE | STEP 1/3</div>", unsafe_allow_html=True)
    
    st.markdown("## TOPIC: THE INSIDE BAR (1)")
    
    # Persist tutorial chart
    if 'tutorial_chart' not in st.session_state:
        st.session_state.tutorial_chart = generate_candle_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='neon-box'>", unsafe_allow_html=True)
        st.plotly_chart(plot_candles(st.session_state.tutorial_chart), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.info("An Inside Bar (1) stays completely within the range of the previous candle.")
        st.markdown("Does the last candle break the high or low of the previous one?")
        
        if st.button("NO - It's Inside (1)", key="ans1"):
            st.balloons()
            st.success("CORRECT! That is a 1 Bar.")
            time.sleep(1.5)
            st.session_state.state = 'GAME'
            # Clear tutorial chart for next time
            del st.session_state.tutorial_chart
            st.rerun()
            
        if st.button("YES - It broke out (2/3)", key="ans2"):
            st.error("Look closer! The high is lower, and the low is higher.")

def game_screen():
    # HUD
    st.markdown(f"""
    <div class='status-bar'>
        LEVEL {st.session_state.level} | XP {st.session_state.xp} | STREAK 🔥 {st.session_state.get('streak', 0)}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## IDENTIFY THE PATTERN")
    
    # Persist game chart
    if 'game_chart' not in st.session_state:
        st.session_state.game_chart = generate_candle_data(6)
    
    st.plotly_chart(plot_candles(st.session_state.game_chart), use_container_width=True)
    
    cols = st.columns(4)
    # Correct Answer (Logic is simplified for MVP - hardcoded to Inside Bar for now as per generator)
    if cols[0].button("1 (Inside)"):
        st.session_state.xp += 10
        st.session_state.streak = st.session_state.get('streak', 0) + 1
        st.success("CORRECT! +10 XP")
        time.sleep(1.0)
        # Clear chart to force regeneration
        del st.session_state.game_chart
        st.rerun()
        
    if cols[1].button("2U (Up)"):
        st.error("WRONG! Try again.")
        st.session_state.streak = 0
        
    if cols[2].button("2D (Down)"):
        st.error("WRONG! Try again.")
        st.session_state.streak = 0
        
    if cols[3].button("3 (Outside)"):
        st.error("WRONG! Try again.")
        st.session_state.streak = 0

# --- MAIN LOOP ---
if st.session_state.state == 'SPLASH':
    splash_screen()
elif st.session_state.state == 'TUTORIAL':
    tutorial_screen()
elif st.session_state.state == 'GAME':
    game_screen()
