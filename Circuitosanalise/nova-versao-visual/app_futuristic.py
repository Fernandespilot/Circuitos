import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import math
import cmath

# Configuração da página
st.set_page_config(
    page_title="🚀 Circuit Nexus - Análise Futurística",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Futurístico Ultra Moderno
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Cores Futurísticas */
    :root {
        --neon-cyan: #00ffff;
        --neon-purple: #ff00ff;
        --neon-blue: #0080ff;
        --electric-green: #00ff80;
        --plasma-orange: #ff8000;
        --dark-space: #0a0a0f;
        --dark-blue: #0f1629;
        --mid-blue: #1a2332;
        --light-blue: #243447;
    }
    
    /* Background principal com efeito space */
    .main {
        background: linear-gradient(135deg, 
            #0a0a0f 0%, 
            #1a0f1a 25%, 
            #0f1629 50%, 
            #1a2332 75%, 
            #0a0a0f 100%);
        background-attachment: fixed;
    }
    
    /* Animação de partículas futurísticas */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(0, 128, 255, 0.05) 0%, transparent 50%);
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes particleFloat {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(360deg); }
    }
    
    /* Header Futurístico */
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, 
            var(--neon-cyan), 
            var(--neon-purple), 
            var(--neon-blue), 
            var(--electric-green));
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        margin-bottom: 1rem;
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--neon-cyan), 
            var(--neon-purple), 
            transparent);
        box-shadow: 0 0 15px var(--neon-cyan);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        text-align: center;
        color: var(--neon-cyan);
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        letter-spacing: 2px;
    }
    
    /* Sidebar Futurística */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(15, 22, 41, 0.95) 0%, 
            rgba(26, 35, 50, 0.95) 100%);
        border-right: 2px solid var(--neon-cyan);
        box-shadow: 5px 0 20px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Inputs Futurísticos */
    .stNumberInput > div > div > input,
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, 
            rgba(15, 22, 41, 0.8) 0%, 
            rgba(26, 35, 50, 0.8) 100%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 12px;
        color: var(--neon-cyan);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.1);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        transform: scale(1.02);
    }
    
    /* Labels Futurísticas */
    .stMarkdown h3, .stMarkdown h2 {
        font-family: 'Orbitron', monospace;
        color: var(--electric-green);
        text-shadow: 0 0 10px rgba(0, 255, 128, 0.5);
        border-bottom: 1px solid rgba(0, 255, 128, 0.3);
        padding-bottom: 5px;
    }
    
    /* Tabs Futurísticas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        display: flex;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        padding: 15px 25px;
        background: linear-gradient(135deg, 
            rgba(15, 22, 41, 0.8) 0%, 
            rgba(26, 35, 50, 0.8) 100%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.9rem;
        color: var(--neon-cyan);
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 255, 255, 0.2), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
        transform: translateY(-3px) scale(1.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.2) 0%, 
            rgba(255, 0, 255, 0.2) 100%);
        border-color: var(--neon-purple);
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.8);
        color: white;
        transform: translateY(-2px);
    }
    
    /* Métricas Futurísticas */
    .metric-container {
        background: linear-gradient(135deg, 
            rgba(15, 22, 41, 0.9) 0%, 
            rgba(26, 35, 50, 0.9) 100%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            var(--neon-cyan), 
            var(--electric-green), 
            var(--neon-purple));
        background-size: 200% 100%;
        animation: borderGlow 2s linear infinite;
    }
    
    @keyframes borderGlow {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 255, 255, 0.4);
        border-color: var(--electric-green);
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--electric-green);
        text-shadow: 0 0 15px rgba(0, 255, 128, 0.6);
    }
    
    .metric-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--neon-cyan);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Botões Futurísticos */
    .stButton > button {
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.1) 0%, 
            rgba(255, 0, 255, 0.1) 100%);
        border: 2px solid var(--neon-cyan);
        border-radius: 15px;
        color: white;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1rem;
        padding: 12px 25px;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.3) 0%, 
            rgba(255, 0, 255, 0.3) 100%);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.6);
        transform: translateY(-2px) scale(1.05);
        border-color: var(--electric-green);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Checkboxes Futurísticos */
    .stCheckbox > label {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        color: var(--neon-cyan);
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
    }
    
    /* Selectbox Futurística */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, 
            rgba(15, 22, 41, 0.8) 0%, 
            rgba(26, 35, 50, 0.8) 100%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 12px;
        color: var(--neon-cyan);
    }
    
    /* Alertas e Mensagens Futurísticas */
    .stSuccess {
        background: linear-gradient(135deg, 
            rgba(0, 255, 128, 0.1) 0%, 
            rgba(0, 255, 255, 0.1) 100%);
        border: 2px solid var(--electric-green);
        border-radius: 15px;
        color: var(--electric-green);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, 
            rgba(255, 0, 0, 0.1) 0%, 
            rgba(255, 0, 255, 0.1) 100%);
        border: 2px solid var(--neon-purple);
        border-radius: 15px;
        color: var(--neon-purple);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    .stInfo {
        background: linear-gradient(135deg, 
            rgba(0, 128, 255, 0.1) 0%, 
            rgba(0, 255, 255, 0.1) 100%);
        border: 2px solid var(--neon-blue);
        border-radius: 15px;
        color: var(--neon-blue);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    /* Dataframes Futurísticos */
    .stDataFrame {
        background: rgba(15, 22, 41, 0.8);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Scrollbars customizadas */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 22, 41, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--electric-green), var(--neon-cyan));
    }
    
    /* Efeito de pulsação para elementos ativos */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0); }
    }
    
    .pulse-element {
        animation: pulse 2s infinite;
    }
    
    /* Efeito holográfico */
    .holographic {
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.1) 0%, 
            rgba(255, 0, 255, 0.1) 25%, 
            rgba(0, 255, 128, 0.1) 50%, 
            rgba(255, 128, 0, 0.1) 75%, 
            rgba(0, 255, 255, 0.1) 100%);
        background-size: 400% 400%;
        animation: hologram 4s ease-in-out infinite;
    }
    
    @keyframes hologram {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

class FuturisticCircuitAnalyzer:
    def __init__(self):
        pass
    
    def calculate_rms_values(self, vm, im):
        """Calcula valores eficazes (RMS)"""
        return vm / np.sqrt(2), im / np.sqrt(2)
    
    def calculate_power_factor(self, theta_v_deg, theta_i_deg):
        """Calcula o fator de potência"""
        return np.cos(np.radians(abs(theta_v_deg - theta_i_deg)))
    
    def determine_circuit_type(self, theta_v_deg, theta_i_deg):
        """Determina o tipo de circuito"""
        phase_diff = theta_v_deg - theta_i_deg
        
        if phase_diff > 180:
            phase_diff -= 360
        elif phase_diff < -180:
            phase_diff += 360
        
        phase_diff_abs = abs(phase_diff)
        
        if phase_diff_abs < 1:
            return "🔄 Em fase (resistivo)", phase_diff_abs, "#00ff80"
        elif abs(phase_diff_abs - 90) < 1:
            if phase_diff < 0:
                return "⚡ Adiantado (capacitivo)", phase_diff_abs, "#00ffff"
            else:
                return "🔋 Atrasado (indutivo)", phase_diff_abs, "#ff8000"
        elif phase_diff < 0:
            return "💫 Adiantado (capacitivo)", phase_diff_abs, "#00ffff"
        else:
            return "⚡ Atrasado (indutivo)", phase_diff_abs, "#ff8000"
    
    def calculate_impedance(self, vrms, irms, theta_v_rad, theta_i_rad):
        """Calcula impedância complexa"""
        v_phasor = vrms * np.exp(1j * theta_v_rad)
        i_phasor = irms * np.exp(1j * theta_i_rad)
        return v_phasor / i_phasor
    
    def generate_futuristic_waveforms(self, f, vm, im, theta_v_rad, theta_i_rad, periods=3):
        """Gera formas de onda com mais pontos para visualização suave"""
        t_total = periods / f
        t = np.linspace(0, t_total, 2000)
        
        omega = 2 * np.pi * f
        v = vm * np.sin(omega * t + theta_v_rad)
        i = im * np.sin(omega * t + theta_i_rad)
        p = v * i
        
        return t, v, i, p

def create_futuristic_metric(label, value, unit="", delta=None, color="#00ffff"):
    """Cria métrica com design futurístico"""
    delta_html = f'<div style="color: {color}; font-size: 0.9rem;">Δ {delta}</div>' if delta else ''
    
    html = f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value} <span style="font-size: 1.2rem; color: {color};">{unit}</span></div>
        {delta_html}
    </div>
    """
    return html

def create_holographic_chart(fig):
    """Aplica tema futurístico aos gráficos Plotly"""
    fig.update_layout(
        plot_bgcolor='rgba(10, 10, 15, 0.8)',
        paper_bgcolor='rgba(15, 22, 41, 0.9)',
        font=dict(
            family="Orbitron, monospace",
            size=12,
            color="#00ffff"
        ),
        title=dict(
            font=dict(size=16, color="#00ff80"),
            x=0.5
        ),
        xaxis=dict(
            gridcolor="rgba(0, 255, 255, 0.2)",
            zerolinecolor="rgba(0, 255, 255, 0.4)",
            color="#00ffff"
        ),
        yaxis=dict(
            gridcolor="rgba(0, 255, 255, 0.2)",
            zerolinecolor="rgba(0, 255, 255, 0.4)",
            color="#00ffff"
        ),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(15, 22, 41, 0.8)",
            bordercolor="#00ffff",
            borderwidth=2,
            font=dict(color="#00ffff")
        )
    )
    return fig

def main():
    # Header futurístico
    st.markdown('<h1 class="main-header">⚡ CIRCUIT NEXUS ⚡</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🚀 INTERFACE FUTURÍSTICA PARA ANÁLISE DE CIRCUITOS ELÉTRICOS 🚀</p>', unsafe_allow_html=True)
    
    analyzer = FuturisticCircuitAnalyzer()
    
    # Sidebar futurística
    with st.sidebar:
        st.markdown('## 🎛️ PAINEL DE CONTROLE')
        
        st.markdown('### ⚡ PARÂMETROS ELÉTRICOS')
        col1, col2 = st.columns(2)
        
        with col1:
            f = st.number_input("🌊 Frequência", min_value=1, max_value=1000, value=60, step=1)
            vm = st.number_input("📈 Tensão Máx", min_value=0.1, max_value=1000.0, value=311.0, step=0.1)
            
        with col2:
            im = st.number_input("⚡ Corrente Máx", min_value=0.01, max_value=100.0, value=14.14, step=0.01)
            periods = st.number_input("🔄 Períodos", min_value=1, max_value=5, value=3, step=1)
        
        st.markdown('### 🎯 ÂNGULOS DE FASE')
        theta_v_deg = st.slider("📐 Ângulo Tensão (°)", -180, 180, 0)
        theta_i_deg = st.slider("📐 Ângulo Corrente (°)", -180, 180, -30)
        
        st.markdown('### 🔧 OPÇÕES AVANÇADAS')
        show_harmonics = st.checkbox("🌈 Análise Harmônica", value=True)
        show_3d = st.checkbox("🎮 Visualização 3D", value=False)
        real_time = st.checkbox("⏱️ Tempo Real", value=False)
    
    # Cálculos principais
    vrms, irms = analyzer.calculate_rms_values(vm, im)
    theta_v_rad = np.radians(theta_v_deg)
    theta_i_rad = np.radians(theta_i_deg)
    
    fp = analyzer.calculate_power_factor(theta_v_deg, theta_i_deg)
    circuit_type, phase_diff, type_color = analyzer.determine_circuit_type(theta_v_deg, theta_i_deg)
    
    z_complex = analyzer.calculate_impedance(vrms, irms, theta_v_rad, theta_i_rad)
    z_mag = abs(z_complex)
    z_angle = np.degrees(np.angle(z_complex))
    
    # Potências
    s_complex = vrms * irms * np.exp(1j * np.radians(theta_v_deg - theta_i_deg))
    p_active = s_complex.real
    q_reactive = s_complex.imag
    s_apparent = abs(s_complex)
    
    # Tabs futurísticas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 ANÁLISE PRINCIPAL", 
        "📊 FASORES 3D", 
        "🌊 ESPECTRO", 
        "⚡ POTÊNCIA", 
        "📱 RELATÓRIO"
    ])
    
    with tab1:
        # Métricas principais em layout futurístico
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_futuristic_metric(
                "FREQUÊNCIA", f"{f}", "Hz", 
                f"ω = {2*np.pi*f:.1f} rad/s", "#00ffff"
            ), unsafe_allow_html=True)
            
        with col2:
            st.markdown(create_futuristic_metric(
                "TENSÃO RMS", f"{vrms:.2f}", "V", 
                f"Pico: {vm:.1f}V", "#00ff80"
            ), unsafe_allow_html=True)
            
        with col3:
            st.markdown(create_futuristic_metric(
                "CORRENTE RMS", f"{irms:.3f}", "A", 
                f"Pico: {im:.2f}A", "#ff8000"
            ), unsafe_allow_html=True)
            
        with col4:
            st.markdown(create_futuristic_metric(
                "FATOR POTÊNCIA", f"{fp:.3f}", "", 
                circuit_type, type_color
            ), unsafe_allow_html=True)
        
        # Gráfico principal de formas de onda
        t, v, i, p = analyzer.generate_futuristic_waveforms(f, vm, im, theta_v_rad, theta_i_rad, periods)
        
        fig_waves = make_subplots(
            rows=2, cols=1,
            subplot_titles=("🌊 Sinais Elétricos v(t) e i(t)", "⚡ Potência Instantânea p(t)"),
            vertical_spacing=0.1
        )
        
        # Tensão com gradiente futurístico
        fig_waves.add_trace(
            go.Scatter(
                x=t*1000, y=v, 
                name="v(t)", 
                line=dict(color="#00ffff", width=3),
                hovertemplate="<b>Tensão</b><br>Tempo: %{x:.2f} ms<br>Valor: %{y:.2f} V<extra></extra>"
            ), row=1, col=1
        )
        
        # Corrente
        scale_factor = vm/im if im > 0 else 1
        i_display = i * (10 if scale_factor > 10 else 1)
        i_label = f"i(t) ×{10 if scale_factor > 10 else 1}"
        
        fig_waves.add_trace(
            go.Scatter(
                x=t*1000, y=i_display, 
                name=i_label, 
                line=dict(color="#ff8000", width=3),
                hovertemplate="<b>Corrente</b><br>Tempo: %{x:.2f} ms<br>Valor: %{y:.2f} A<extra></extra>"
            ), row=1, col=1
        )
        
        # Potência com efeito neon
        p_display = p/1000 if max(abs(p)) > 1000 else p
        p_unit = "kW" if max(abs(p)) > 1000 else "W"
        
        fig_waves.add_trace(
            go.Scatter(
                x=t*1000, y=p_display, 
                name=f"p(t)", 
                line=dict(color="#ff00ff", width=4),
                fill='tozeroy',
                fillcolor="rgba(255, 0, 255, 0.1)",
                hovertemplate=f"<b>Potência</b><br>Tempo: %{{x:.2f}} ms<br>Valor: %{{y:.2f}} {p_unit}<extra></extra>"
            ), row=2, col=1
        )
        
        # Linha de potência RMS
        p_rms_display = (p_active/1000 if max(abs(p)) > 1000 else p_active)
        fig_waves.add_trace(
            go.Scatter(
                x=t*1000, y=np.full_like(t, p_rms_display),
                name="P_rms", 
                line=dict(color="#00ff80", width=3, dash='dash'),
                hovertemplate=f"<b>Potência RMS</b><br>Valor: {p_active:.2f} W<extra></extra>"
            ), row=2, col=1
        )
        
        fig_waves.update_xaxes(title_text="Tempo [ms]", row=1, col=1)
        fig_waves.update_xaxes(title_text="Tempo [ms]", row=2, col=1)
        fig_waves.update_yaxes(title_text="Amplitude [V/A]", row=1, col=1)
        fig_waves.update_yaxes(title_text=f"Potência [{p_unit}]", row=2, col=1)
        
        fig_waves = create_holographic_chart(fig_waves)
        fig_waves.update_layout(height=700, title="🌊 ANÁLISE TEMPORAL DOS SINAIS")
        
        st.plotly_chart(fig_waves, use_container_width=True)
    
    with tab2:
        st.markdown("## 🎯 DIAGRAMA FASORIAL FUTURÍSTICO")
        
        # Criar diagrama fasorial em 3D se habilitado
        if show_3d:
            fig_3d = go.Figure()
            
            # Fasor de tensão
            fig_3d.add_trace(go.Scatter3d(
                x=[0, vrms * np.cos(theta_v_rad)],
                y=[0, vrms * np.sin(theta_v_rad)],
                z=[0, 0],
                mode='lines+markers',
                line=dict(color='#00ffff', width=8),
                marker=dict(size=[5, 12], color='#00ffff'),
                name=f'V: {vrms:.1f}∠{theta_v_deg:.1f}°',
                hovertemplate="<b>Tensão</b><br>Módulo: %{text}<extra></extra>",
                text=[f"{vrms:.2f}V"]
            ))
            
            # Fasor de corrente (escalado)
            i_scale = vrms / irms * 0.7
            fig_3d.add_trace(go.Scatter3d(
                x=[0, irms * i_scale * np.cos(theta_i_rad)],
                y=[0, irms * i_scale * np.sin(theta_i_rad)],
                z=[0, 0],
                mode='lines+markers',
                line=dict(color='#ff8000', width=8),
                marker=dict(size=[5, 12], color='#ff8000'),
                name=f'I: {irms:.3f}∠{theta_i_deg:.1f}°',
                hovertemplate="<b>Corrente</b><br>Módulo: %{text}<extra></extra>",
                text=[f"{irms:.3f}A"]
            ))
            
            fig_3d = create_holographic_chart(fig_3d)
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title="Componente Real",
                    yaxis_title="Componente Imaginária", 
                    zaxis_title="Fase",
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                ),
                title="🎮 FASORES 3D INTERATIVOS",
                height=600
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            # Diagrama fasorial 2D melhorado
            fig_phasor = go.Figure()
            
            # Círculo de referência
            theta_circle = np.linspace(0, 2*np.pi, 100)
            max_val = max(vrms, irms * (vrms/irms * 0.7))
            circle_r = max_val * 0.9
            
            fig_phasor.add_trace(go.Scatter(
                x=circle_r * np.cos(theta_circle),
                y=circle_r * np.sin(theta_circle),
                mode='lines',
                line=dict(color='rgba(0, 255, 255, 0.3)', width=2, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Fasor de tensão
            fig_phasor.add_trace(go.Scatter(
                x=[0, vrms * np.cos(theta_v_rad)],
                y=[0, vrms * np.sin(theta_v_rad)],
                mode='lines+markers',
                line=dict(color='#00ffff', width=6),
                marker=dict(size=[8, 15], color='#00ffff', symbol=['circle', 'triangle-up']),
                name=f'🔹 V: {vrms:.1f}∠{theta_v_deg:.1f}°',
                hovertemplate="<b>Tensão</b><br>Módulo: %{text}<br>Ângulo: " + f"{theta_v_deg:.1f}°<extra></extra>",
                text=[f"{vrms:.2f}V", f"{vrms:.2f}V"]
            ))
            
            # Fasor de corrente
            i_scale = vrms / irms * 0.7
            fig_phasor.add_trace(go.Scatter(
                x=[0, irms * i_scale * np.cos(theta_i_rad)],
                y=[0, irms * i_scale * np.sin(theta_i_rad)],
                mode='lines+markers',
                line=dict(color='#ff8000', width=6),
                marker=dict(size=[8, 15], color='#ff8000', symbol=['circle', 'triangle-up']),
                name=f'🔸 I: {irms:.3f}∠{theta_i_deg:.1f}° (×{i_scale:.1f})',
                hovertemplate="<b>Corrente</b><br>Módulo: %{text}<br>Ângulo: " + f"{theta_i_deg:.1f}°<extra></extra>",
                text=[f"{irms:.3f}A", f"{irms:.3f}A"]
            ))
            
            # Adicionar anotações com ângulos
            fig_phasor.add_annotation(
                x=vrms * np.cos(theta_v_rad) * 0.6,
                y=vrms * np.sin(theta_v_rad) * 0.6,
                text=f"V<br>{vrms:.1f}V",
                showarrow=False,
                font=dict(color="#00ffff", size=12, family="Orbitron"),
                bgcolor="rgba(15, 22, 41, 0.8)",
                bordercolor="#00ffff",
                borderwidth=2
            )
            
            fig_phasor.add_annotation(
                x=irms * i_scale * np.cos(theta_i_rad) * 0.6,
                y=irms * i_scale * np.sin(theta_i_rad) * 0.6,
                text=f"I<br>{irms:.3f}A",
                showarrow=False,
                font=dict(color="#ff8000", size=12, family="Orbitron"),
                bgcolor="rgba(15, 22, 41, 0.8)",
                bordercolor="#ff8000",
                borderwidth=2
            )
            
            fig_phasor = create_holographic_chart(fig_phasor)
            fig_phasor.update_layout(
                title="🎯 DIAGRAMA FASORIAL INTERATIVO",
                xaxis=dict(scaleanchor="y", scaleratio=1, title="Componente Real"),
                yaxis=dict(scaleanchor="x", scaleratio=1, title="Componente Imaginária"),
                height=600
            )
            
            st.plotly_chart(fig_phasor, use_container_width=True)
        
        # Informações da impedância
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_futuristic_metric(
                "IMPEDÂNCIA", f"{z_mag:.2f}", "Ω", 
                f"∠{z_angle:.1f}°", "#ff00ff"
            ), unsafe_allow_html=True)
            
        with col2:
            st.markdown(create_futuristic_metric(
                "DEFASAGEM", f"{phase_diff:.1f}", "°", 
                f"θ_v - θ_i", type_color
            ), unsafe_allow_html=True)
    
    with tab3:
        st.markdown("## 🌈 ANÁLISE ESPECTRAL")
        
        if show_harmonics:
            # Simular análise harmônica
            freqs = np.array([f, 3*f, 5*f, 7*f, 9*f])  # Harmônicos ímpares
            mags = np.array([1.0, 0.33, 0.2, 0.14, 0.11]) * vrms  # Magnitudes típicas
            
            fig_spectrum = go.Figure()
            
            # Espectro de frequência
            fig_spectrum.add_trace(go.Bar(
                x=freqs,
                y=mags,
                name="Espectro de Tensão",
                marker=dict(
                    color=['#00ffff', '#ff8000', '#ff00ff', '#00ff80', '#ffff00'],
                    line=dict(color='rgba(0, 255, 255, 0.8)', width=2)
                ),
                hovertemplate="<b>Freq:</b> %{x:.0f} Hz<br><b>Mag:</b> %{y:.2f} V<extra></extra>"
            ))
            
            fig_spectrum = create_holographic_chart(fig_spectrum)
            fig_spectrum.update_layout(
                title="🌈 ESPECTRO DE FREQUÊNCIAS",
                xaxis_title="Frequência [Hz]",
                yaxis_title="Magnitude [V]",
                height=500
            )
            
            st.plotly_chart(fig_spectrum, use_container_width=True)
            
            # THD (Total Harmonic Distortion)
            thd = np.sqrt(sum(mags[1:]**2)) / mags[0] * 100
            
            st.markdown(create_futuristic_metric(
                "THD TOTAL", f"{thd:.2f}", "%", 
                "Distorção Harmônica", "#ff00ff"
            ), unsafe_allow_html=True)
    
    with tab4:
        st.markdown("## ⚡ ANÁLISE DE POTÊNCIA AVANÇADA")
        
        # Triângulo de potências em 3D
        fig_power = go.Figure()
        
        # Triângulo de potência
        fig_power.add_trace(go.Scatter(
            x=[0, p_active, p_active, 0],
            y=[0, 0, q_reactive, 0],
            mode='lines+markers',
            fill='tonexty',
            fillcolor='rgba(255, 0, 255, 0.2)',
            line=dict(color='#ff00ff', width=4),
            marker=dict(size=10, color='#ff00ff'),
            name='Triângulo de Potência',
            hovertemplate="<b>Potência</b><br>P: %{x:.1f} W<br>Q: %{y:.1f} VAr<extra></extra>"
        ))
        
        # Vetores individuais
        fig_power.add_trace(go.Scatter(
            x=[0, p_active],
            y=[0, 0],
            mode='lines+text',
            line=dict(color='#00ff80', width=6),
            text=['', f'P = {p_active:.1f} W'],
            textposition='middle center',
            textfont=dict(color='#00ff80', size=12, family="Orbitron"),
            name='Potência Ativa',
            showlegend=False
        ))
        
        if abs(q_reactive) > 0.1:
            fig_power.add_trace(go.Scatter(
                x=[p_active, p_active],
                y=[0, q_reactive],
                mode='lines+text',
                line=dict(color='#ff8000', width=6),
                text=['', f'Q = {q_reactive:.1f} VAr'],
                textposition='middle left',
                textfont=dict(color='#ff8000', size=12, family="Orbitron"),
                name='Potência Reativa',
                showlegend=False
            ))
        
        fig_power = create_holographic_chart(fig_power)
        fig_power.update_layout(
            title="🔺 TRIÂNGULO DE POTÊNCIAS FUTURÍSTICO",
            xaxis_title="Potência Ativa [W]",
            yaxis_title="Potência Reativa [VAr]",
            height=500
        )
        
        st.plotly_chart(fig_power, use_container_width=True)
        
        # Métricas de potência
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_futuristic_metric(
                "POTÊNCIA ATIVA", f"{p_active:.1f}", "W", 
                "Energia Útil", "#00ff80"
            ), unsafe_allow_html=True)
            
        with col2:
            st.markdown(create_futuristic_metric(
                "POTÊNCIA REATIVA", f"{abs(q_reactive):.1f}", "VAr", 
                "Energia Reativa", "#ff8000"
            ), unsafe_allow_html=True)
            
        with col3:
            st.markdown(create_futuristic_metric(
                "POTÊNCIA APARENTE", f"{s_apparent:.1f}", "VA", 
                "Potência Total", "#ff00ff"
            ), unsafe_allow_html=True)
    
    with tab5:
        st.markdown("## 📱 RELATÓRIO FUTURÍSTICO COMPLETO")
        
        # Dados para tabela
        data = {
            "PARÂMETRO": [
                "🌊 Frequência", "📈 Tensão Máxima", "📈 Tensão RMS", 
                "⚡ Corrente Máxima", "⚡ Corrente RMS", "📐 Ângulo Tensão",
                "📐 Ângulo Corrente", "🎯 Defasagem", "🔌 Impedância",
                "💪 Fator de Potência", "⚡ Potência Ativa", "🔋 Potência Reativa",
                "💫 Potência Aparente", "🏷️ Tipo de Circuito"
            ],
            "VALOR": [
                f"{f} Hz", f"{vm:.1f} V", f"{vrms:.2f} V",
                f"{im:.2f} A", f"{irms:.3f} A", f"{theta_v_deg:.1f}°",
                f"{theta_i_deg:.1f}°", f"{phase_diff:.1f}°", f"{z_mag:.2f} Ω",
                f"{fp:.3f}", f"{p_active:.1f} W", f"{abs(q_reactive):.1f} VAr",
                f"{s_apparent:.1f} VA", circuit_type
            ],
            "OBSERVAÇÃO": [
                f"ω = {2*np.pi*f:.1f} rad/s", "Amplitude máxima", "Valor eficaz",
                "Amplitude máxima", "Valor eficaz", "Fase inicial",
                "Fase inicial", "θ_v - θ_i", f"∠{z_angle:.1f}°",
                "cos(φ)", "Energia útil", "Energia reativa",
                "Energia total", "Classificação"
            ]
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, height=500)
        
        # Botão de download futurístico
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 DOWNLOAD RELATÓRIO.CSV",
            data=csv,
            file_name=f"circuit_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
