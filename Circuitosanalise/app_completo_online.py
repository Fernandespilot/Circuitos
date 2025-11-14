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

# Configuração da página
st.set_page_config(
    page_title="⚡ Circuit Analyzer PRO - Versão Completa",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e293b 0%, #334155 50%, #475569 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background: #1e293b;
        border-radius: 5px 5px 0px 0px;
        color: #94a3b8;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1 style="color: #00d4ff; margin: 0;">⚡ CIRCUIT ANALYZER PRO</h1>
    <h3 style="color: #a78bfa; margin: 0;">Versão Completa - Análise Profissional de Circuitos RLC</h3>
    <p style="color: #94a3b8; margin: 0;">🚀 Deploy Online - Todas as Funcionalidades Avançadas</p>
</div>
""", unsafe_allow_html=True)

class CircuitAnalyzerPro:
    def __init__(self):
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.results_history = []
    
    def sidebar_controls(self):
        st.sidebar.markdown("## 🎛️ Painel de Controle")
        
        # Parâmetros básicos
        st.sidebar.markdown("### ⚙️ Parâmetros do Circuito")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            f = st.number_input("Frequência (Hz)", value=60.0, min_value=0.1, max_value=10000.0, step=0.1)
            vm = st.number_input("Tensão máx (V)", value=311.0, min_value=0.1, max_value=1000.0, step=0.1)
            theta_v = st.number_input("Ângulo V (°)", value=0.0, min_value=-180.0, max_value=180.0, step=0.1)
        
        with col2:
            im = st.number_input("Corrente máx (A)", value=10.0, min_value=0.1, max_value=100.0, step=0.1)
            theta_i = st.number_input("Ângulo I (°)", value=-30.0, min_value=-180.0, max_value=180.0, step=0.1)
        
        st.sidebar.markdown("### 🔧 Componentes")
        
        col3, col4 = st.sidebar.columns(2)
        
        with col3:
            r = st.number_input("Resistência (Ω)", value=10.0, min_value=0.1, max_value=1000.0, step=0.1)
            l = st.number_input("Indutância (H)", value=0.01, min_value=0.001, max_value=10.0, step=0.001, format="%.6f")
        
        with col4:
            c = st.number_input("Capacitância (F)", value=100e-6, min_value=1e-9, max_value=1e-3, step=1e-6, format="%.9f")
        
        # Presets rápidos
        st.sidebar.markdown("### 🚀 Presets Rápidos")
        
        if st.sidebar.button("🏠 Circuito Residencial (60Hz)"):
            st.session_state.preset = "residencial"
            
        if st.sidebar.button("🏭 Circuito Industrial (50Hz)"):
            st.session_state.preset = "industrial"
            
        if st.sidebar.button("📻 Circuito RF (1MHz)"):
            st.session_state.preset = "rf"
        
        return f, vm, im, theta_v, theta_i, r, l, c
    
    def calculate_circuit_parameters(self, f, vm, im, theta_v, theta_i, r, l, c):
        """Calcula todos os parâmetros do circuito"""
        # Conversões
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
        
        # Impedância
        z_total = complex(r, x_total)
        z_mag = abs(z_total)
        z_angle = math.degrees(cmath.phase(z_total))
        
        # Potências
        phase_diff = theta_v_rad - theta_i_rad
        fp = math.cos(phase_diff)
        p_active = vrms * irms * fp
        q_reactive = vrms * irms * math.sin(phase_diff)
        s_apparent = vrms * irms
        
        # Frequência de ressonância
        f_res = 1 / (2 * math.pi * math.sqrt(l * c))
        
        return {
            'omega': omega,
            'vrms': vrms,
            'irms': irms,
            'xl': xl,
            'xc': xc,
            'x_total': x_total,
            'z_total': z_total,
            'z_mag': z_mag,
            'z_angle': z_angle,
            'phase_diff': phase_diff,
            'fp': fp,
            'p_active': p_active,
            'q_reactive': q_reactive,
            's_apparent': s_apparent,
            'f_res': f_res
        }
    
    def plot_signals(self, f, vm, im, theta_v, theta_i):
        """Plota sinais temporais"""
        t_final = 3 / f
        t = np.linspace(0, t_final, 1000)
        omega = 2 * math.pi * f
        
        # Sinais
        v = vm * np.sin(omega * t + math.radians(theta_v))
        i = im * np.sin(omega * t + math.radians(theta_i))
        p = v * i
        
        # Criar subplot
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Tensão v(t)', 'Corrente i(t)', 'Potência p(t)'),
            vertical_spacing=0.08
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
        
        # Potência
        fig.add_trace(
            go.Scatter(x=t*1000, y=p, name='p(t)', line=dict(color='#10b981', width=3)),
            row=3, col=1
        )
        
        # Potência média
        fig.add_trace(
            go.Scatter(x=t*1000, y=[np.mean(p)]*len(t), name=f'P médio = {np.mean(p):.1f} W', 
                      line=dict(color='#f59e0b', width=2, dash='dash')),
            row=3, col=1
        )
        
        # Layout
        fig.update_layout(
            height=600,
            template='plotly_dark',
            title_text="📊 Sinais Elétricos Temporais"
        )
        
        fig.update_xaxes(title_text="Tempo [ms]", row=3, col=1)
        fig.update_yaxes(title_text="Tensão [V]", row=1, col=1)
        fig.update_yaxes(title_text="Corrente [A]", row=2, col=1)
        fig.update_yaxes(title_text="Potência [W]", row=3, col=1)
        
        return fig
    
    def plot_phasors(self, vm, im, theta_v, theta_i):
        """Plota diagramas fasoriais"""
        # Componentes dos fasores
        v_real = vm * math.cos(math.radians(theta_v))
        v_imag = vm * math.sin(math.radians(theta_v))
        i_real = im * math.cos(math.radians(theta_i))
        i_imag = im * math.sin(math.radians(theta_i))
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Fasor Tensão', 'Fasor Corrente'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Fasor tensão
        fig.add_trace(
            go.Scatter(x=[0, v_real], y=[0, v_imag], mode='lines+markers',
                      line=dict(color='#ef4444', width=4),
                      marker=dict(size=[0, 12], color='#ef4444'),
                      name=f'V = {vm:.1f}∠{theta_v:.1f}°'),
            row=1, col=1
        )
        
        # Círculo de referência tensão
        theta_circle = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(
            go.Scatter(x=vm*np.cos(theta_circle), y=vm*np.sin(theta_circle),
                      mode='lines', line=dict(color='#4ade80', width=1, dash='dash'),
                      name='Referência V', showlegend=False),
            row=1, col=1
        )
        
        # Fasor corrente
        fig.add_trace(
            go.Scatter(x=[0, i_real], y=[0, i_imag], mode='lines+markers',
                      line=dict(color='#3b82f6', width=4),
                      marker=dict(size=[0, 12], color='#3b82f6'),
                      name=f'I = {im:.1f}∠{theta_i:.1f}°'),
            row=1, col=2
        )
        
        # Círculo de referência corrente
        fig.add_trace(
            go.Scatter(x=im*np.cos(theta_circle), y=im*np.sin(theta_circle),
                      mode='lines', line=dict(color='#4ade80', width=1, dash='dash'),
                      name='Referência I', showlegend=False),
            row=1, col=2
        )
        
        # Layout
        fig.update_layout(
            height=400,
            template='plotly_dark',
            title_text="⚡ Diagramas Fasoriais"
        )
        
        # Eixos iguais
        max_v = vm * 1.2
        max_i = im * 1.2
        
        fig.update_xaxes(range=[-max_v, max_v], title="Real [V]", row=1, col=1)
        fig.update_yaxes(range=[-max_v, max_v], title="Imaginário [V]", row=1, col=1)
        fig.update_xaxes(range=[-max_i, max_i], title="Real [A]", row=1, col=2)
        fig.update_yaxes(range=[-max_i, max_i], title="Imaginário [A]", row=1, col=2)
        
        return fig
    
    def plot_frequency_response(self, r, l, c):
        """Plota resposta em frequência (Bode)"""
        # Faixa de frequências (1 Hz a 100 kHz)
        frequencies = np.logspace(0, 5, 1000)  # 1 Hz to 100 kHz
        omega = 2 * np.pi * frequencies
        
        # Função de transferência do circuito RLC
        s = 1j * omega
        
        # Impedância total
        Z = r + s * l + 1 / (s * c)
        H = 1 / Z  # Admitância (ou outra função de transferência desejada)
        
        # Magnitude e fase
        magnitude_db = 20 * np.log10(np.abs(H))
        phase_deg = np.angle(H) * 180 / np.pi
        
        # Criar subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Magnitude', 'Fase'),
            vertical_spacing=0.1,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Magnitude
        fig.add_trace(
            go.Scatter(x=frequencies, y=magnitude_db, name='|H(jω)|',
                      line=dict(color='#ef4444', width=3)),
            row=1, col=1
        )
        
        # Fase
        fig.add_trace(
            go.Scatter(x=frequencies, y=phase_deg, name='∠H(jω)',
                      line=dict(color='#3b82f6', width=3)),
            row=2, col=1
        )
        
        # Frequência de ressonância
        f_res = 1 / (2 * np.pi * np.sqrt(l * c))
        fig.add_vline(x=f_res, line_dash="dash", line_color="orange", 
                     annotation_text=f"f₀ = {f_res:.1f} Hz")
        
        # Layout
        fig.update_layout(
            height=500,
            template='plotly_dark',
            title_text="📊 Diagrama de Bode"
        )
        
        fig.update_xaxes(type="log", title="Frequência [Hz]")
        fig.update_yaxes(title="Magnitude [dB]", row=1, col=1)
        fig.update_yaxes(title="Fase [°]", row=2, col=1)
        
        return fig
    
    def plot_transient_response(self, r, l, c):
        """Plota resposta transitória"""
        # Parâmetros do sistema
        # Para circuito RLC série: s² + (R/L)s + 1/(LC) = 0
        
        # Coeficientes da equação característica
        a = 1
        b = r / l
        c_coef = 1 / (l * c)
        
        # Criar sistema em espaço de estados
        # Para um sistema de segunda ordem
        num = [1/(l*c)]  # Numerador
        den = [1, r/l, 1/(l*c)]  # Denominador
        
        system = signal.TransferFunction(num, den)
        
        # Tempo de simulação
        t = np.linspace(0, 0.1, 1000)  # 100ms
        
        # Resposta ao degrau
        t_step, y_step = signal.step_response(system, T=t)
        
        # Resposta ao impulso
        t_impulse, y_impulse = signal.impulse_response(system, T=t)
        
        # Criar subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Resposta ao Degrau', 'Resposta ao Impulso'),
            vertical_spacing=0.1
        )
        
        # Resposta ao degrau
        fig.add_trace(
            go.Scatter(x=t_step*1000, y=y_step, name='Degrau',
                      line=dict(color='#10b981', width=3)),
            row=1, col=1
        )
        
        # Resposta ao impulso
        fig.add_trace(
            go.Scatter(x=t_impulse*1000, y=y_impulse, name='Impulso',
                      line=dict(color='#8b5cf6', width=3)),
            row=2, col=1
        )
        
        # Layout
        fig.update_layout(
            height=500,
            template='plotly_dark',
            title_text="🚀 Análise Transitória"
        )
        
        fig.update_xaxes(title="Tempo [ms]")
        fig.update_yaxes(title="Amplitude", row=1, col=1)
        fig.update_yaxes(title="Amplitude", row=2, col=1)
        
        return fig
    
    def plot_nyquist(self, r, l, c):
        """Plota diagrama de Nyquist"""
        # Faixa de frequências
        frequencies = np.logspace(0, 5, 1000)
        omega = 2 * np.pi * frequencies
        s = 1j * omega
        
        # Função de transferência
        H = 1 / (r + s * l + 1 / (s * c))
        
        real_part = np.real(H)
        imag_part = np.imag(H)
        
        fig = go.Figure()
        
        # Diagrama de Nyquist
        fig.add_trace(
            go.Scatter(x=real_part, y=imag_part, mode='lines',
                      name='Nyquist', line=dict(color='#f59e0b', width=3))
        )
        
        # Ponto crítico (-1, 0)
        fig.add_trace(
            go.Scatter(x=[-1], y=[0], mode='markers',
                      marker=dict(color='red', size=10, symbol='x'),
                      name='Ponto Crítico (-1,0)')
        )
        
        fig.update_layout(
            title="📊 Diagrama de Nyquist",
            xaxis_title="Parte Real",
            yaxis_title="Parte Imaginária",
            template='plotly_dark',
            height=500
        )
        
        return fig
    
    def run(self):
        # Sidebar com controles
        f, vm, im, theta_v, theta_i, r, l, c = self.sidebar_controls()
        
        # Calcular parâmetros
        params = self.calculate_circuit_parameters(f, vm, im, theta_v, theta_i, r, l, c)
        
        # Abas principais
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Sinais Elétricos", 
            "⚡ Diagrama Fasorial", 
            "🔧 Designer de Circuitos",
            "🚀 Análise Transitória",
            "📊 Resposta em Frequência", 
            "📋 Relatórios"
        ])
        
        with tab1:
            st.markdown("### 📊 Análise de Sinais Temporais")
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔋 Tensão RMS", f"{params['vrms']:.1f} V")
            with col2:
                st.metric("⚡ Corrente RMS", f"{params['irms']:.1f} A")
            with col3:
                st.metric("📊 Potência Ativa", f"{params['p_active']:.1f} W")
            with col4:
                st.metric("🎯 Fator de Potência", f"{params['fp']:.3f}")
            
            # Gráfico de sinais
            fig_signals = self.plot_signals(f, vm, im, theta_v, theta_i)
            st.plotly_chart(fig_signals, use_container_width=True)
        
        with tab2:
            st.markdown("### ⚡ Análise Fasorial")
            
            # Métricas fasoriais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📐 Defasagem V-I", f"{math.degrees(params['phase_diff']):.1f}°")
            with col2:
                st.metric("🔄 Impedância |Z|", f"{params['z_mag']:.1f} Ω")
            with col3:
                st.metric("📊 Ângulo Z", f"{params['z_angle']:.1f}°")
            with col4:
                st.metric("🎯 Freq. Ressonância", f"{params['f_res']:.1f} Hz")
            
            # Gráfico fasorial
            fig_phasor = self.plot_phasors(vm, im, theta_v, theta_i)
            st.plotly_chart(fig_phasor, use_container_width=True)
        
        with tab3:
            st.markdown("### 🔧 Designer de Circuitos")
            
            circuit_type = st.selectbox(
                "Tipo de Circuito:",
                ["RLC Série", "RLC Paralelo", "Filtro Passa-Baixa", "Filtro Passa-Alta"]
            )
            
            # Análise de componentes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🔴 Resistor")
                st.write(f"R = {r:.1f} Ω")
                st.write(f"P_R = {params['irms']**2 * r:.1f} W")
            
            with col2:
                st.markdown("#### 🔵 Indutor")
                st.write(f"L = {l:.6f} H")
                st.write(f"X_L = {params['xl']:.1f} Ω")
            
            with col3:
                st.markdown("#### ⚪ Capacitor")
                st.write(f"C = {c:.9f} F")
                st.write(f"X_C = {params['xc']:.1f} Ω")
        
        with tab4:
            st.markdown("### 🚀 Análise Transitória")
            
            # Parâmetros do sistema
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Frequência natural
                wn = 1 / math.sqrt(l * c)
                st.metric("🌊 Freq. Natural", f"{wn/(2*np.pi):.1f} Hz")
            
            with col2:
                # Fator de amortecimento
                zeta = r / (2 * math.sqrt(l / c))
                st.metric("🎯 Amortecimento ζ", f"{zeta:.3f}")
            
            with col3:
                # Tipo de resposta
                if zeta < 1:
                    response_type = "Sub-amortecida"
                elif zeta == 1:
                    response_type = "Criticamente amortecida"
                else:
                    response_type = "Super-amortecida"
                st.metric("📊 Tipo de Resposta", response_type)
            
            # Gráfico transitório
            fig_transient = self.plot_transient_response(r, l, c)
            st.plotly_chart(fig_transient, use_container_width=True)
        
        with tab5:
            st.markdown("### 📊 Análise de Frequência")
            
            # Seletor de tipo de análise
            analysis_type = st.selectbox(
                "Tipo de Análise:",
                ["Diagrama de Bode", "Diagrama de Nyquist", "Ambos"]
            )
            
            if analysis_type in ["Diagrama de Bode", "Ambos"]:
                fig_bode = self.plot_frequency_response(r, l, c)
                st.plotly_chart(fig_bode, use_container_width=True)
            
            if analysis_type in ["Diagrama de Nyquist", "Ambos"]:
                fig_nyquist = self.plot_nyquist(r, l, c)
                st.plotly_chart(fig_nyquist, use_container_width=True)
        
        with tab6:
            st.markdown("### 📋 Relatório Completo")
            
            # Dados para download
            report_data = {
                'Parâmetro': [
                    'Frequência [Hz]', 'Tensão RMS [V]', 'Corrente RMS [A]',
                    'Resistência [Ω]', 'Indutância [H]', 'Capacitância [F]',
                    'Reatância Indutiva [Ω]', 'Reatância Capacitiva [Ω]',
                    'Impedância Total [Ω]', 'Ângulo da Impedância [°]',
                    'Potência Ativa [W]', 'Potência Reativa [VAr]',
                    'Potência Aparente [VA]', 'Fator de Potência',
                    'Frequência de Ressonância [Hz]'
                ],
                'Valor': [
                    f, params['vrms'], params['irms'],
                    r, l, c,
                    params['xl'], params['xc'],
                    params['z_mag'], params['z_angle'],
                    params['p_active'], params['q_reactive'],
                    params['s_apparent'], params['fp'],
                    params['f_res']
                ]
            }
            
            df_report = pd.DataFrame(report_data)
            
            # Exibir tabela
            st.dataframe(df_report, use_container_width=True)
            
            # Download do relatório
            csv = df_report.to_csv(index=False)
            st.download_button(
                label="📥 Download Relatório CSV",
                data=csv,
                file_name=f"relatorio_circuito_{f}Hz.csv",
                mime="text/csv"
            )

# Executar aplicação
if __name__ == "__main__":
    analyzer = CircuitAnalyzerPro()
    analyzer.run()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b;">
    <p>⚡ Circuit Analyzer PRO - Versão Completa Online</p>
    <p>🚀 Desenvolvido para análises profissionais de circuitos elétricos</p>
    <p>📊 Todas as funcionalidades: Sinais • Fasores • Transitória • Frequência • Bode • Nyquist</p>
</div>
""", unsafe_allow_html=True)
