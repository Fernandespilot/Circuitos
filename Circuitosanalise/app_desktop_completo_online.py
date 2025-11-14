import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
import pandas as pd
from matplotlib.patches import Circle, Rectangle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.signal as signal
from matplotlib.patches import Circle as MPLCircle
import matplotlib.patches as patches

# Configuração da página
st.set_page_config(
    page_title="⚡ Circuit Analyzer PRO - Versão Completa Professional",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado futurístico
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0a0e27 0%, #161b3a 50%, #2d3561 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        border: 2px solid #00d4ff;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0px 20px;
        background: linear-gradient(135deg, #1a1f3e 0%, #2d3561 100%);
        border-radius: 10px 10px 0px 0px;
        color: #a78bfa;
        font-weight: bold;
        font-size: 14px;
        border: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
        color: white !important;
        border: 2px solid #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
    }
    .advanced-card {
        background: linear-gradient(135deg, #1a1f3e 0%, #2d3561 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #6366f1;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.3);
    }
    .sidebar .stSelectbox label {
        color: #00d4ff !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Header principal futurístico
st.markdown("""
<div class="main-header">
    <h1 style="color: #00d4ff; margin: 0; font-size: 2.5rem;">⚡ CIRCUIT ANALYZER PRO</h1>
    <h2 style="color: #a78bfa; margin: 0.5rem 0;">Versão Profissional Completa - Análise Avançada de Circuitos RLC</h2>
    <p style="color: #94a3b8; margin: 0; font-size: 1.2rem;">🚀 Deploy Online | 🔬 Análises Profissionais | 📊 6 Módulos Avançados</p>
    <p style="color: #6366f1; margin: 0.5rem 0; font-size: 1rem;">
        🎯 Transitória • 📊 Bode • 🌐 Nyquist • ⚡ Fasores • 🔧 Designer • 📋 Relatórios
    </p>
</div>
""", unsafe_allow_html=True)

class CircuitAnalyzerProfessional:
    def __init__(self):
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.results_history = []
            st.session_state.current_preset = "custom"
    
    def sidebar_controls(self):
        st.sidebar.markdown("## 🎛️ PAINEL DE CONTROLE PROFISSIONAL")
        
        # Presets avançados
        st.sidebar.markdown("### 🚀 Presets Profissionais")
        preset = st.sidebar.selectbox(
            "Configurações Rápidas:",
            ["Custom", "Residencial 60Hz", "Industrial 50Hz", "RF 1MHz", "Audio 1kHz", "Power 50/60Hz"],
            key="preset_selector"
        )
        
        # Aplicar presets
        if preset == "Residencial 60Hz":
            f, vm, im, theta_v, theta_i, r, l, c = 60.0, 311.0, 10.0, 0.0, -30.0, 10.0, 0.01, 100e-6
        elif preset == "Industrial 50Hz":
            f, vm, im, theta_v, theta_i, r, l, c = 50.0, 380.0, 20.0, 0.0, -25.0, 5.0, 0.05, 200e-6
        elif preset == "RF 1MHz":
            f, vm, im, theta_v, theta_i, r, l, c = 1000000.0, 5.0, 0.1, 0.0, -45.0, 50.0, 1e-6, 100e-12
        elif preset == "Audio 1kHz":
            f, vm, im, theta_v, theta_i, r, l, c = 1000.0, 10.0, 1.0, 0.0, -60.0, 100.0, 0.001, 10e-6
        elif preset == "Power 50/60Hz":
            f, vm, im, theta_v, theta_i, r, l, c = 60.0, 220.0, 15.0, 0.0, -20.0, 8.0, 0.02, 150e-6
        else:
            # Parâmetros customizáveis
            st.sidebar.markdown("### ⚙️ Parâmetros do Circuito")
            
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                f = st.number_input("Frequência (Hz)", value=60.0, min_value=0.1, max_value=10e6, step=0.1, format="%.2f")
                vm = st.number_input("Tensão máx (V)", value=311.0, min_value=0.1, max_value=10000.0, step=0.1)
                theta_v = st.number_input("Ângulo V (°)", value=0.0, min_value=-180.0, max_value=180.0, step=0.1)
            
            with col2:
                im = st.number_input("Corrente máx (A)", value=10.0, min_value=0.1, max_value=1000.0, step=0.1)
                theta_i = st.number_input("Ângulo I (°)", value=-30.0, min_value=-180.0, max_value=180.0, step=0.1)
            
            st.sidebar.markdown("### 🔧 Componentes")
            
            col3, col4 = st.sidebar.columns(2)
            
            with col3:
                r = st.number_input("Resistência (Ω)", value=10.0, min_value=0.1, max_value=10000.0, step=0.1)
                l = st.number_input("Indutância (H)", value=0.01, min_value=1e-9, max_value=10.0, step=0.001, format="%.6f")
            
            with col4:
                c = st.number_input("Capacitância (F)", value=100e-6, min_value=1e-12, max_value=1e-3, step=1e-9, format="%.9f")
        
        # Configurações avançadas
        st.sidebar.markdown("### 🔬 Configurações Avançadas")
        
        # Faixa de frequência para análise
        freq_range = st.sidebar.slider(
            "Faixa de Frequência (log10 Hz)",
            min_value=-2, max_value=7, value=(0, 5), step=1
        )
        
        # Tempo de simulação transitória
        sim_time = st.sidebar.slider(
            "Tempo de Simulação (s)",
            min_value=0.01, max_value=1.0, value=0.1, step=0.01
        )
        
        return f, vm, im, theta_v, theta_i, r, l, c, freq_range, sim_time
    
    def calculate_all_parameters(self, f, vm, im, theta_v, theta_i, r, l, c):
        """Calcula todos os parâmetros avançados do circuito"""
        # Conversões básicas
        omega = 2 * math.pi * f
        theta_v_rad = math.radians(theta_v)
        theta_i_rad = math.radians(theta_i)
        
        # Valores RMS
        vrms = vm / math.sqrt(2)
        irms = im / math.sqrt(2)
        
        # Reatâncias
        xl = omega * l
        xc = 1 / (omega * c)
        x_total = xl - xc
        
        # Impedância complexa
        z_total = complex(r, x_total)
        z_mag = abs(z_total)
        z_angle = math.degrees(cmath.phase(z_total))
        
        # Admitância
        y_total = 1 / z_total
        y_mag = abs(y_total)
        y_angle = math.degrees(cmath.phase(y_total))
        
        # Potências
        phase_diff = theta_v_rad - theta_i_rad
        fp = math.cos(phase_diff)
        p_active = vrms * irms * fp
        q_reactive = vrms * irms * math.sin(phase_diff)
        s_apparent = vrms * irms
        
        # Frequência de ressonância
        f_res = 1 / (2 * math.pi * math.sqrt(l * c))
        
        # Parâmetros transitórios
        wn = 1 / math.sqrt(l * c)  # Frequência natural
        zeta = r / (2 * math.sqrt(l / c))  # Fator de amortecimento
        
        # Tipo de resposta
        if zeta < 1:
            response_type = "Sub-amortecida"
            wd = wn * math.sqrt(1 - zeta**2)  # Frequência amortecida
        elif zeta == 1:
            response_type = "Criticamente amortecida"
            wd = 0
        else:
            response_type = "Super-amortecida"
            wd = 0
        
        # Constantes de tempo
        if zeta != 1:
            tau = 1 / (zeta * wn)
        else:
            tau = 1 / wn
        
        return {
            'omega': omega, 'vrms': vrms, 'irms': irms,
            'xl': xl, 'xc': xc, 'x_total': x_total,
            'z_total': z_total, 'z_mag': z_mag, 'z_angle': z_angle,
            'y_total': y_total, 'y_mag': y_mag, 'y_angle': y_angle,
            'phase_diff': phase_diff, 'fp': fp,
            'p_active': p_active, 'q_reactive': q_reactive, 's_apparent': s_apparent,
            'f_res': f_res, 'wn': wn, 'zeta': zeta, 'wd': wd,
            'response_type': response_type, 'tau': tau
        }
    
    def plot_signals_advanced(self, f, vm, im, theta_v, theta_i, params):
        """Plota sinais temporais com análises avançadas"""
        t_final = 3 / f
        t = np.linspace(0, t_final, 2000)  # Mais pontos para melhor resolução
        omega = 2 * math.pi * f
        
        # Sinais principais
        v = vm * np.sin(omega * t + math.radians(theta_v))
        i = im * np.sin(omega * t + math.radians(theta_i))
        p = v * i
        
        # Componentes de potência
        p_avg = params['p_active']
        p_reactive = params['q_reactive']
        
        # Criar subplot com 4 gráficos
        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=('Tensão v(t)', 'Corrente i(t)', 'Potência Instantânea p(t)', 'Análise de Potência'),
            vertical_spacing=0.06,
            specs=[[{"secondary_y": False}]] * 4
        )
        
        # Tensão
        fig.add_trace(
            go.Scatter(x=t*1000, y=v, name='v(t)', line=dict(color='#ef4444', width=3)),
            row=1, col=1
        )
        
        # Corrente
        fig.add_trace(
            go.Scatter(x=t*1000, y=i, name='i(t)', line=dict(color='#3b82f6', width=3)),
            row=2, col=1
        )
        
        # Potência instantânea
        fig.add_trace(
            go.Scatter(x=t*1000, y=p, name='p(t) instantânea', line=dict(color='#10b981', width=3)),
            row=3, col=1
        )
        
        # Potência média
        fig.add_trace(
            go.Scatter(x=t*1000, y=[p_avg]*len(t), name=f'P ativa = {p_avg:.1f} W', 
                      line=dict(color='#f59e0b', width=2, dash='dash')),
            row=3, col=1
        )
        
        # Análise de potência (barras)
        power_types = ['Ativa (P)', 'Reativa (Q)', 'Aparente (S)']
        power_values = [params['p_active'], abs(params['q_reactive']), params['s_apparent']]
        colors = ['#10b981', '#8b5cf6', '#f59e0b']
        
        fig.add_trace(
            go.Bar(x=power_types, y=power_values, name='Potências',
                   marker=dict(color=colors)),
            row=4, col=1
        )
        
        # Layout
        fig.update_layout(
            height=800,
            template='plotly_dark',
            title_text="📊 Análise Completa de Sinais Temporais",
            showlegend=True
        )
        
        # Atualizações dos eixos
        fig.update_xaxes(title_text="Tempo [ms]", row=3, col=1)
        fig.update_xaxes(title_text="Tipo de Potência", row=4, col=1)
        fig.update_yaxes(title_text="Tensão [V]", row=1, col=1)
        fig.update_yaxes(title_text="Corrente [A]", row=2, col=1)
        fig.update_yaxes(title_text="Potência [W]", row=3, col=1)
        fig.update_yaxes(title_text="Potência [W/VAr/VA]", row=4, col=1)
        
        return fig
    
    def plot_phasors_advanced(self, vm, im, theta_v, theta_i, params):
        """Plota diagramas fasoriais avançados"""
        # Componentes dos fasores
        v_real = vm * math.cos(math.radians(theta_v))
        v_imag = vm * math.sin(math.radians(theta_v))
        i_real = im * math.cos(math.radians(theta_i))
        i_imag = im * math.sin(math.radians(theta_i))
        
        # Impedância
        z_real = params['z_total'].real
        z_imag = params['z_total'].imag
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Fasor Tensão', 'Fasor Corrente', 'Impedância Z', 'Potência Complexa'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Fasor tensão
        fig.add_trace(
            go.Scatter(x=[0, v_real], y=[0, v_imag], mode='lines+markers',
                      line=dict(color='#ef4444', width=4),
                      marker=dict(size=[0, 15], color='#ef4444'),
                      name=f'V = {vm:.1f}∠{theta_v:.1f}°'),
            row=1, col=1
        )
        
        # Círculo de referência tensão
        theta_circle = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(
            go.Scatter(x=vm*np.cos(theta_circle), y=vm*np.sin(theta_circle),
                      mode='lines', line=dict(color='#4ade80', width=1, dash='dash'),
                      name='Ref V', showlegend=False),
            row=1, col=1
        )
        
        # Fasor corrente
        fig.add_trace(
            go.Scatter(x=[0, i_real], y=[0, i_imag], mode='lines+markers',
                      line=dict(color='#3b82f6', width=4),
                      marker=dict(size=[0, 15], color='#3b82f6'),
                      name=f'I = {im:.1f}∠{theta_i:.1f}°'),
            row=1, col=2
        )
        
        # Círculo de referência corrente
        fig.add_trace(
            go.Scatter(x=im*np.cos(theta_circle), y=im*np.sin(theta_circle),
                      mode='lines', line=dict(color='#4ade80', width=1, dash='dash'),
                      name='Ref I', showlegend=False),
            row=1, col=2
        )
        
        # Impedância
        z_max = max(abs(z_real), abs(z_imag), 1) * 1.2
        fig.add_trace(
            go.Scatter(x=[0, z_real], y=[0, z_imag], mode='lines+markers',
                      line=dict(color='#f59e0b', width=4),
                      marker=dict(size=[0, 15], color='#f59e0b'),
                      name=f'Z = {params["z_mag"]:.1f}∠{params["z_angle"]:.1f}°'),
            row=2, col=1
        )
        
        # Potência complexa
        s_real = params['p_active']
        s_imag = params['q_reactive']
        s_max = max(abs(s_real), abs(s_imag), 1) * 1.2
        
        fig.add_trace(
            go.Scatter(x=[0, s_real], y=[0, s_imag], mode='lines+markers',
                      line=dict(color='#8b5cf6', width=4),
                      marker=dict(size=[0, 15], color='#8b5cf6'),
                      name=f'S = {s_real:.1f} + j{s_imag:.1f}'),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            height=600,
            template='plotly_dark',
            title_text="⚡ Análise Fasorial Completa"
        )
        
        # Eixos iguais
        max_v, max_i = vm * 1.2, im * 1.2
        
        fig.update_xaxes(range=[-max_v, max_v], title="Real [V]", row=1, col=1)
        fig.update_yaxes(range=[-max_v, max_v], title="Imag [V]", row=1, col=1)
        fig.update_xaxes(range=[-max_i, max_i], title="Real [A]", row=1, col=2)
        fig.update_yaxes(range=[-max_i, max_i], title="Imag [A]", row=1, col=2)
        fig.update_xaxes(range=[-z_max, z_max], title="Real [Ω]", row=2, col=1)
        fig.update_yaxes(range=[-z_max, z_max], title="Imag [Ω]", row=2, col=1)
        fig.update_xaxes(range=[-s_max, s_max], title="P [W]", row=2, col=2)
        fig.update_yaxes(range=[-s_max, s_max], title="Q [VAr]", row=2, col=2)
        
        return fig
    
    def plot_frequency_response_advanced(self, r, l, c, freq_range):
        """Plota resposta em frequência completa com Bode e Nyquist"""
        # Faixa de frequências
        f_start, f_end = 10**freq_range[0], 10**freq_range[1]
        frequencies = np.logspace(freq_range[0], freq_range[1], 2000)
        omega = 2 * np.pi * frequencies
        
        # Função de transferência - Impedância do circuito
        s = 1j * omega
        Z = r + s * l + 1 / (s * c)
        H = 1 / Z  # Admitância como função de transferência
        
        # Magnitude e fase
        magnitude_db = 20 * np.log10(np.abs(H))
        phase_deg = np.angle(H) * 180 / np.pi
        
        # Criar subplot para Bode
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Magnitude (Bode)', 'Fase (Bode)', 'Nyquist', 'Polo-Zero'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Magnitude Bode
        fig.add_trace(
            go.Scatter(x=frequencies, y=magnitude_db, name='|H(jω)| [dB]',
                      line=dict(color='#ef4444', width=3)),
            row=1, col=1
        )
        
        # Fase Bode
        fig.add_trace(
            go.Scatter(x=frequencies, y=phase_deg, name='∠H(jω) [°]',
                      line=dict(color='#3b82f6', width=3)),
            row=2, col=1
        )
        
        # Nyquist
        real_part = np.real(H)
        imag_part = np.imag(H)
        
        fig.add_trace(
            go.Scatter(x=real_part, y=imag_part, mode='lines',
                      name='Nyquist', line=dict(color='#10b981', width=3)),
            row=1, col=2
        )
        
        # Ponto crítico (-1, 0) no Nyquist
        fig.add_trace(
            go.Scatter(x=[-1], y=[0], mode='markers',
                      marker=dict(color='red', size=12, symbol='x'),
                      name='Ponto Crítico', showlegend=False),
            row=1, col=2
        )
        
        # Frequência de ressonância
        f_res = 1 / (2 * np.pi * np.sqrt(l * c))
        if f_start <= f_res <= f_end:
            fig.add_vline(x=f_res, line_dash="dash", line_color="orange", 
                         annotation_text=f"f₀ = {f_res:.2f} Hz",
                         row=1, col=1)
            fig.add_vline(x=f_res, line_dash="dash", line_color="orange", 
                         row=2, col=1)
        
        # Análise de polos e zeros (simplified)
        wn = 1 / np.sqrt(l * c)
        zeta = r / (2 * np.sqrt(l / c))
        
        if zeta < 1:
            # Polos complexos conjugados
            sigma = -zeta * wn
            wd = wn * np.sqrt(1 - zeta**2)
            pole1 = complex(sigma, wd)
            pole2 = complex(sigma, -wd)
        else:
            # Polos reais
            pole1 = -wn * (zeta + np.sqrt(zeta**2 - 1))
            pole2 = -wn * (zeta - np.sqrt(zeta**2 - 1))
        
        # Plot polos no plano s
        if isinstance(pole1, complex):
            fig.add_trace(
                go.Scatter(x=[pole1.real, pole2.real], y=[pole1.imag, pole2.imag],
                          mode='markers', marker=dict(color='red', size=12, symbol='x'),
                          name='Polos'),
                row=2, col=2
            )
        else:
            fig.add_trace(
                go.Scatter(x=[pole1, pole2], y=[0, 0],
                          mode='markers', marker=dict(color='red', size=12, symbol='x'),
                          name='Polos'),
                row=2, col=2
            )
        
        # Layout
        fig.update_layout(
            height=700,
            template='plotly_dark',
            title_text="📊 Análise Completa de Frequência"
        )
        
        # Atualizações dos eixos
        fig.update_xaxes(type="log", title="Frequência [Hz]", row=1, col=1)
        fig.update_xaxes(type="log", title="Frequência [Hz]", row=2, col=1)
        fig.update_yaxes(title="Magnitude [dB]", row=1, col=1)
        fig.update_yaxes(title="Fase [°]", row=2, col=1)
        fig.update_xaxes(title="Parte Real", row=1, col=2)
        fig.update_yaxes(title="Parte Imaginária", row=1, col=2)
        fig.update_xaxes(title="σ (Parte Real)", row=2, col=2)
        fig.update_yaxes(title="jω (Parte Imaginária)", row=2, col=2)
        
        return fig
    
    def plot_transient_response_advanced(self, r, l, c, sim_time):
        """Plota resposta transitória completa"""
        # Parâmetros do sistema
        wn = 1 / math.sqrt(l * c)
        zeta = r / (2 * math.sqrt(l / c))
        
        # Coeficientes da equação diferencial
        # s² + (R/L)s + 1/(LC) = 0
        num = [1/(l*c)]  # Numerador
        den = [1, r/l, 1/(l*c)]  # Denominador
        
        system = signal.TransferFunction(num, den)
        
        # Tempo de simulação
        t = np.linspace(0, sim_time, 2000)
        
        # Respostas
        t_step, y_step = signal.step_response(system, T=t)
        t_impulse, y_impulse = signal.impulse_response(system, T=t)
        
        # Resposta natural (condições iniciais)
        if zeta < 1:
            # Sub-amortecida
            wd = wn * math.sqrt(1 - zeta**2)
            y_natural = np.exp(-zeta * wn * t) * np.cos(wd * t)
        elif zeta == 1:
            # Criticamente amortecida
            y_natural = (1 + wn * t) * np.exp(-wn * t)
        else:
            # Super-amortecida
            r1 = -wn * (zeta + math.sqrt(zeta**2 - 1))
            r2 = -wn * (zeta - math.sqrt(zeta**2 - 1))
            y_natural = 0.5 * (np.exp(r1 * t) + np.exp(r2 * t))
        
        # Criar subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Resposta ao Degrau', 'Resposta ao Impulso', 
                          'Resposta Natural', 'Características do Sistema'),
            vertical_spacing=0.1
        )
        
        # Resposta ao degrau
        fig.add_trace(
            go.Scatter(x=t_step*1000, y=y_step, name='Degrau Unitário',
                      line=dict(color='#10b981', width=3)),
            row=1, col=1
        )
        
        # Resposta ao impulso
        fig.add_trace(
            go.Scatter(x=t_impulse*1000, y=y_impulse, name='Impulso Unitário',
                      line=dict(color='#8b5cf6', width=3)),
            row=1, col=2
        )
        
        # Resposta natural
        fig.add_trace(
            go.Scatter(x=t*1000, y=y_natural, name='Resposta Natural',
                      line=dict(color='#f59e0b', width=3)),
            row=2, col=1
        )
        
        # Envelope (para sub-amortecida)
        if zeta < 1:
            envelope = np.exp(-zeta * wn * t)
            fig.add_trace(
                go.Scatter(x=t*1000, y=envelope, name='Envelope Superior',
                          line=dict(color='#ef4444', width=2, dash='dash')),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=t*1000, y=-envelope, name='Envelope Inferior',
                          line=dict(color='#ef4444', width=2, dash='dash')),
                row=2, col=1
            )
        
        # Características do sistema (barras)
        characteristics = ['ωₙ [rad/s]', 'ζ', 'τ [ms]', 'f₀ [Hz]']
        tau = 1 / (zeta * wn) if zeta > 0 else float('inf')
        f0 = wn / (2 * np.pi)
        values = [wn, zeta, tau*1000, f0]
        
        fig.add_trace(
            go.Bar(x=characteristics, y=values, name='Parâmetros do Sistema',
                   marker=dict(color=['#ef4444', '#3b82f6', '#10b981', '#f59e0b'])),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            height=700,
            template='plotly_dark',
            title_text=f"🚀 Análise Transitória Completa - {params['response_type']}"
        )
        
        # Atualizações dos eixos
        fig.update_xaxes(title="Tempo [ms]")
        fig.update_yaxes(title="Amplitude")
        
        return fig
    
    def create_circuit_diagram(self, circuit_type, r, l, c):
        """Cria diagrama do circuito"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.set_facecolor('#1e293b')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        
        if circuit_type == "RLC Série":
            # Fonte de tensão
            circle = patches.Circle((1, 3), 0.5, linewidth=3, edgecolor='#10b981', facecolor='none')
            ax.add_patch(circle)
            ax.text(1, 3, 'V', ha='center', va='center', color='#10b981', fontsize=14, fontweight='bold')
            
            # Resistor
            rect = patches.Rectangle((3, 2.5), 1.5, 1, linewidth=3, edgecolor='#ef4444', facecolor='none')
            ax.add_patch(rect)
            ax.text(3.75, 3, f'R\n{r}Ω', ha='center', va='center', color='#ef4444', fontsize=10, fontweight='bold')
            
            # Indutor
            for i in range(4):
                circle = patches.Circle((5.5 + i*0.3, 3), 0.15, linewidth=2, edgecolor='#3b82f6', facecolor='none')
                ax.add_patch(circle)
            ax.text(6, 2.2, f'L\n{l:.3f}H', ha='center', va='center', color='#3b82f6', fontsize=10, fontweight='bold')
            
            # Capacitor
            ax.plot([8, 8], [2.3, 3.7], color='white', linewidth=4)
            ax.plot([8.3, 8.3], [2.3, 3.7], color='white', linewidth=4)
            ax.text(8.15, 2, f'C\n{c*1e6:.0f}μF', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
            
            # Fios conectores
            connections = [
                ([1.5, 3], [3, 3]),  # V to R
                ([4.5, 5.2], [3, 3]),  # R to L
                ([6.8, 8], [3, 3]),  # L to C
                ([8.3, 9.5], [3, 3]),  # C to down
                ([9.5, 9.5], [3, 1]),  # Right vertical
                ([9.5, 1], [1, 1]),  # Bottom
                ([1, 1], [1, 2.5])  # Left vertical
            ]
            
            for (x, y) in connections:
                ax.plot(x, y, color='white', linewidth=2)
        
        ax.set_title(f'Circuito {circuit_type}', color='#00d4ff', fontsize=16, fontweight='bold')
        ax.axis('off')
        
        return fig
    
    def run(self):
        # Sidebar com controles
        f, vm, im, theta_v, theta_i, r, l, c, freq_range, sim_time = self.sidebar_controls()
        
        # Calcular todos os parâmetros
        params = self.calculate_all_parameters(f, vm, im, theta_v, theta_i, r, l, c)
        
        # Abas principais
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Sinais Elétricos", 
            "⚡ Diagrama Fasorial", 
            "🔧 Designer de Circuitos",
            "🚀 Análise Transitória",
            "📊 Resposta em Frequência", 
            "📋 Relatórios Profissionais"
        ])
        
        with tab1:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Análise Avançada de Sinais Temporais")
            
            # Métricas principais em cards
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("🔋 Tensão RMS", f"{params['vrms']:.2f} V", f"Max: {vm:.1f} V")
            with col2:
                st.metric("⚡ Corrente RMS", f"{params['irms']:.2f} A", f"Max: {im:.1f} A")
            with col3:
                st.metric("📊 Potência Ativa", f"{params['p_active']:.1f} W", f"FP: {params['fp']:.3f}")
            with col4:
                st.metric("🔄 Potência Reativa", f"{abs(params['q_reactive']):.1f} VAr", 
                         f"{'Indutiva' if params['q_reactive'] > 0 else 'Capacitiva'}")
            with col5:
                st.metric("⚡ Potência Aparente", f"{params['s_apparent']:.1f} VA", 
                         f"η: {(params['p_active']/params['s_apparent']*100):.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico de sinais avançado
            fig_signals = self.plot_signals_advanced(f, vm, im, theta_v, theta_i, params)
            st.plotly_chart(fig_signals, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### ⚡ Análise Fasorial e Impedância Completa")
            
            # Métricas fasoriais avançadas
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("📐 Defasagem V-I", f"{math.degrees(params['phase_diff']):.1f}°")
            with col2:
                st.metric("🔄 Impedância |Z|", f"{params['z_mag']:.2f} Ω", f"∠{params['z_angle']:.1f}°")
            with col3:
                st.metric("⚡ Admitância |Y|", f"{params['y_mag']:.4f} S", f"∠{params['y_angle']:.1f}°")
            with col4:
                st.metric("🎯 Freq. Ressonância", f"{params['f_res']:.1f} Hz")
            with col5:
                st.metric("📊 Reatância Total", f"{params['x_total']:.2f} Ω", 
                         f"XL-XC: {params['xl']:.1f}-{params['xc']:.1f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico fasorial avançado
            fig_phasor = self.plot_phasors_advanced(vm, im, theta_v, theta_i, params)
            st.plotly_chart(fig_phasor, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### 🔧 Designer de Circuitos e Análise de Componentes")
            
            circuit_type = st.selectbox(
                "Tipo de Circuito:",
                ["RLC Série", "RLC Paralelo", "Filtro Passa-Baixa", "Filtro Passa-Alta", "Filtro Passa-Faixa"]
            )
            
            # Análise detalhada de componentes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🔴 Resistor")
                st.write(f"**Valor:** {r:.2f} Ω")
                st.write(f"**Potência:** {params['irms']**2 * r:.2f} W")
                st.write(f"**Energia (1s):** {params['irms']**2 * r:.2f} J")
                
            with col2:
                st.markdown("#### 🔵 Indutor")
                st.write(f"**Valor:** {l:.6f} H ({l*1000:.3f} mH)")
                st.write(f"**Reatância:** {params['xl']:.2f} Ω")
                st.write(f"**Energia:** {0.5 * l * params['irms']**2:.4f} J")
                
            with col3:
                st.markdown("#### ⚪ Capacitor")
                st.write(f"**Valor:** {c:.9f} F ({c*1e6:.1f} μF)")
                st.write(f"**Reatância:** {params['xc']:.2f} Ω")
                st.write(f"**Energia:** {0.5 * c * params['vrms']**2:.4f} J")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Diagrama do circuito
            try:
                fig_circuit = self.create_circuit_diagram(circuit_type, r, l, c)
                st.pyplot(fig_circuit, use_container_width=True)
                plt.close(fig_circuit)
            except:
                st.info("Diagrama do circuito será exibido aqui")
        
        with tab4:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### 🚀 Análise Transitória Avançada")
            
            # Parâmetros do sistema
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌊 Freq. Natural", f"{params['wn']/(2*np.pi):.2f} Hz", f"ωₙ: {params['wn']:.1f} rad/s")
            with col2:
                st.metric("🎯 Amortecimento ζ", f"{params['zeta']:.3f}")
            with col3:
                st.metric("📊 Tipo de Resposta", params['response_type'])
            with col4:
                st.metric("⏱️ Constante de Tempo", f"{params['tau']*1000:.1f} ms")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico transitório
            fig_transient = self.plot_transient_response_advanced(r, l, c, sim_time)
            st.plotly_chart(fig_transient, use_container_width=True)
        
        with tab5:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Análise Completa de Frequência")
            
            # Seletor de tipo de análise
            col1, col2 = st.columns(2)
            with col1:
                analysis_type = st.selectbox(
                    "Tipo de Análise:",
                    ["Bode + Nyquist", "Bode Apenas", "Nyquist Apenas", "Análise Completa"]
                )
            with col2:
                show_margins = st.checkbox("Mostrar Margens de Estabilidade", value=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Gráfico de frequência
            fig_freq = self.plot_frequency_response_advanced(r, l, c, freq_range)
            st.plotly_chart(fig_freq, use_container_width=True)
        
        with tab6:
            st.markdown('<div class="advanced-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Relatório Profissional Completo")
            
            # Dados completos para download
            report_data = {
                'Parâmetro': [
                    'Frequência [Hz]', 'Tensão RMS [V]', 'Corrente RMS [A]',
                    'Resistência [Ω]', 'Indutância [H]', 'Capacitância [F]',
                    'Reatância Indutiva [Ω]', 'Reatância Capacitiva [Ω]', 'Reatância Total [Ω]',
                    'Impedância Magnitude [Ω]', 'Impedância Ângulo [°]',
                    'Admitância Magnitude [S]', 'Admitância Ângulo [°]',
                    'Potência Ativa [W]', 'Potência Reativa [VAr]', 'Potência Aparente [VA]',
                    'Fator de Potência', 'Eficiência [%]',
                    'Frequência de Ressonância [Hz]', 'Frequência Natural [Hz]',
                    'Fator de Amortecimento', 'Tipo de Resposta', 'Constante de Tempo [ms]'
                ],
                'Valor': [
                    f"{f:.2f}", f"{params['vrms']:.3f}", f"{params['irms']:.3f}",
                    f"{r:.3f}", f"{l:.6f}", f"{c:.9f}",
                    f"{params['xl']:.3f}", f"{params['xc']:.3f}", f"{params['x_total']:.3f}",
                    f"{params['z_mag']:.3f}", f"{params['z_angle']:.2f}",
                    f"{params['y_mag']:.6f}", f"{params['y_angle']:.2f}",
                    f"{params['p_active']:.3f}", f"{params['q_reactive']:.3f}", f"{params['s_apparent']:.3f}",
                    f"{params['fp']:.4f}", f"{(params['p_active']/params['s_apparent']*100):.2f}",
                    f"{params['f_res']:.2f}", f"{params['wn']/(2*np.pi):.2f}",
                    f"{params['zeta']:.4f}", params['response_type'], f"{params['tau']*1000:.2f}"
                ]
            }
            
            df_report = pd.DataFrame(report_data)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Exibir tabela
            st.dataframe(df_report, use_container_width=True)
            
            # Botões de download
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"relatorio_circuito_completo_{f}Hz.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Relatório em texto
                report_text = f"""
RELATÓRIO TÉCNICO - CIRCUIT ANALYZER PRO
==========================================

CONFIGURAÇÃO DO CIRCUITO:
• Frequência: {f:.2f} Hz
• Resistência: {r:.3f} Ω
• Indutância: {l:.6f} H ({l*1000:.3f} mH)
• Capacitância: {c:.9f} F ({c*1e6:.1f} μF)

ANÁLISE DE SINAIS:
• Tensão RMS: {params['vrms']:.3f} V (Max: {vm:.1f} V)
• Corrente RMS: {params['irms']:.3f} A (Max: {im:.1f} A)
• Defasagem V-I: {math.degrees(params['phase_diff']):.2f}°

ANÁLISE DE IMPEDÂNCIA:
• Reatância XL: {params['xl']:.3f} Ω
• Reatância XC: {params['xc']:.3f} Ω
• Impedância |Z|: {params['z_mag']:.3f} Ω ∠{params['z_angle']:.2f}°
• Admitância |Y|: {params['y_mag']:.6f} S ∠{params['y_angle']:.2f}°

ANÁLISE DE POTÊNCIA:
• Potência Ativa: {params['p_active']:.3f} W
• Potência Reativa: {params['q_reactive']:.3f} VAr
• Potência Aparente: {params['s_apparent']:.3f} VA
• Fator de Potência: {params['fp']:.4f}
• Eficiência: {(params['p_active']/params['s_apparent']*100):.2f}%

ANÁLISE TRANSITÓRIA:
• Frequência Natural: {params['wn']/(2*np.pi):.2f} Hz
• Fator de Amortecimento: {params['zeta']:.4f}
• Tipo de Resposta: {params['response_type']}
• Constante de Tempo: {params['tau']*1000:.2f} ms
• Frequência de Ressonância: {params['f_res']:.2f} Hz

==========================================
Gerado por Circuit Analyzer PRO v2.0
Data: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
                st.download_button(
                    label="📄 Download Relatório TXT",
                    data=report_text,
                    file_name=f"relatorio_tecnico_{f}Hz.txt",
                    mime="text/plain"
                )
            
            with col3:
                # JSON para análises posteriores
                import json
                json_data = json.dumps(params, default=str, indent=2)
                st.download_button(
                    label="🔧 Download JSON",
                    data=json_data,
                    file_name=f"dados_circuito_{f}Hz.json",
                    mime="application/json"
                )

# Executar aplicação
if __name__ == "__main__":
    analyzer = CircuitAnalyzerProfessional()
    analyzer.run()

# Footer profissional
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
    <h4 style="color: #00d4ff;">⚡ CIRCUIT ANALYZER PRO - Versão Profissional Completa</h4>
    <p style="margin: 0.5rem 0;">🚀 Desenvolvido para análises profissionais e educação avançada em engenharia elétrica</p>
    <p style="margin: 0.5rem 0;">📊 <strong>Funcionalidades:</strong> Sinais Temporais • Análise Fasorial • Resposta Transitória • Bode & Nyquist • Designer de Circuitos • Relatórios Profissionais</p>
    <p style="margin: 0.5rem 0; color: #a78bfa;">🎓 <strong>Ideal para:</strong> Universidades • Escolas Técnicas • Engenheiros • Pesquisa • Demonstrações Profissionais</p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem;">© 2024 Circuit Analyzer PRO | Versão 2.0 Professional | Deploy Online Ready</p>
</div>
""", unsafe_allow_html=True)
