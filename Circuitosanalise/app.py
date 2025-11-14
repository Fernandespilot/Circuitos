import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="Analisador de Circuitos Elétricos Avançado",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# CSS personalizado para estilo moderno
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #17a2b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border-left-color: #17a2b8;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        display: flex;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        gap: 8px;
        padding: 12px 20px;
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f77b4 0%, #17a2b8 100%);
        color: white;
        border: 2px solid #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(31, 119, 180, 0.3);
    }
    
    /* Melhorar botões gerais */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Melhorar selectbox */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    /* Melhorar número inputs */
    .stNumberInput > div > div > input {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 0.5rem;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 2px rgba(31, 119, 180, 0.2);
    }
    
    /* Melhorar checkbox */
    .stCheckbox > label {
        font-weight: 500;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

class CircuitAnalyzer:
    def __init__(self):
        pass
    
    def calculate_rms_values(self, vm, im):
        """Calcula valores eficazes (RMS)"""
        vrms = vm / np.sqrt(2)
        irms = im / np.sqrt(2)
        return vrms, irms
    
    def calculate_period(self, f, nr_periods):
        """Calcula o período total baseado no número de ciclos"""
        return nr_periods * (1/f)
    
    def calculate_power_factor(self, theta_v_deg, theta_i_deg):
        """Calcula o fator de potência"""
        return np.cos(np.radians(abs(theta_v_deg - theta_i_deg)))
    
    def determine_circuit_type(self, theta_v_deg, theta_i_deg):
        """Determina o tipo de circuito baseado no defasamento"""
        # Normalizar ângulos para 0-360 graus
        theta_v_norm = theta_v_deg % 360
        theta_i_norm = theta_i_deg % 360
        
        phase_diff = theta_v_norm - theta_i_norm
        
        # Ajustar para o intervalo -180 a 180
        if phase_diff > 180:
            phase_diff -= 360
        elif phase_diff < -180:
            phase_diff += 360
        
        phase_diff_abs = abs(phase_diff)
        
        if phase_diff_abs < 1:  # Aproximadamente em fase
            return "Em fase (resistivo)", phase_diff_abs
        elif abs(phase_diff_abs - 90) < 1:  # Aproximadamente 90 graus
            if phase_diff < 0:
                return "Adiantado (puramente capacitivo)", phase_diff_abs
            else:
                return "Atrasado (puramente indutivo)", phase_diff_abs
        elif phase_diff < 0:
            return "Adiantado (capacitivo)", phase_diff_abs
        else:
            return "Atrasado (indutivo)", phase_diff_abs
    
    def calculate_instantaneous_values(self, vm, im, f, theta_v_rad, theta_i_rad, t_instant):
        """Calcula valores instantâneos de tensão e corrente"""
        v_instant = vm * np.sin(2 * np.pi * f * t_instant + theta_v_rad)
        i_instant = im * np.sin(2 * np.pi * f * t_instant + theta_i_rad)
        return v_instant, i_instant
    
    def calculate_power_correction(self, vrms, irms, theta_v_deg, theta_i_deg, fp, f, desired_fp=None):
        """Calcula a correção do fator de potência"""
        if desired_fp is None:
            return None
        
        # Conversão para radianos
        theta_v_rad = np.radians(theta_v_deg)
        theta_i_rad = np.radians(theta_i_deg)
        
        # Fasores
        v_phasor = vrms * np.exp(1j * theta_v_rad)
        i_phasor = irms * np.exp(1j * theta_i_rad)
        
        # Potência complexa
        s_complex = v_phasor * np.conj(i_phasor)
        p_active = s_complex.real
        q_reactive = s_complex.imag
        
        # Potência reativa necessária após correção
        q_after = p_active * np.tan(np.arccos(desired_fp))
        q_capacitor = q_reactive - q_after
        
        # Capacitância necessária
        capacitance = abs(q_capacitor / (vrms**2 * 2 * np.pi * f)) * 1e6  # em µF
        
        # Nova corrente
        xc = vrms**2 / q_capacitor if q_capacitor != 0 else float('inf')
        i_capacitor = vrms / abs(xc) if xc != float('inf') else 0
        
        return {
            'capacitance_uF': capacitance,
            'q_capacitor': q_capacitor,
            'i_capacitor': i_capacitor,
            'p_active': p_active,
            'q_after': q_after
        }
    
    def generate_waveforms(self, f, vm, im, theta_v_rad, theta_i_rad, periods):
        """Gera as formas de onda de tensão, corrente e potência"""
        t_total = periods / f
        t = np.linspace(-t_total, t_total, 2000)
        
        v = vm * np.sin(2 * np.pi * f * t + theta_v_rad)
        i = im * np.sin(2 * np.pi * f * t + theta_i_rad)
        p = v * i
        
        return t, v, i, p

def main():
    st.markdown('<h1 class="main-header">⚡ Analisador de Circuitos Elétricos Monofásicos</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">Contribuição FABLAB/IFMTMAKER - Interface Web Moderna</p>', unsafe_allow_html=True)
    
    analyzer = CircuitAnalyzer()
    
    # Sidebar para parâmetros de entrada
    with st.sidebar:
        st.markdown('<h2 style="color: #1f77b4;">📊 Parâmetros do Circuito</h2>', unsafe_allow_html=True)
        
        # Parâmetros básicos
        st.markdown("### 🔧 Parâmetros Básicos")
        f = st.number_input("Frequência (Hz)", min_value=1, max_value=1000, value=60, step=1)
        vm = st.number_input("Tensão Máxima - Vm (V)", min_value=0.1, max_value=1000.0, value=311.0, step=0.1)
        im = st.number_input("Corrente Máxima - Im (A)", min_value=0.01, max_value=100.0, value=14.14, step=0.01)
        nr_periods = st.number_input("Número de Ciclos", min_value=1, max_value=10, value=2, step=1)
        
        # Ângulos de fase
        st.markdown("### 📐 Ângulos de Fase")
        theta_v_deg = st.slider("Ângulo da Tensão (°)", -180, 180, 0)
        theta_i_deg = st.slider("Ângulo da Corrente (°)", -180, 180, -30)
        
        # Análise instantânea
        st.markdown("### ⏱️ Análise Instantânea")
        t_instant_ms = st.number_input("Instante de Análise (ms)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        
        # Correção do fator de potência
        st.markdown("### ⚙️ Correção do Fator de Potência")
        correct_pf = st.checkbox("Corrigir Fator de Potência")
        desired_pf = None
        if correct_pf:
            desired_pf = st.slider("Fator de Potência Desejado", 0.0, 1.0, 0.95, step=0.01)
    
    # Cálculos principais
    vrms, irms = analyzer.calculate_rms_values(vm, im)
    theta_v_rad = np.radians(theta_v_deg)
    theta_i_rad = np.radians(theta_i_deg)
    t_instant = t_instant_ms / 1000  # Converter para segundos
    
    fp = analyzer.calculate_power_factor(theta_v_deg, theta_i_deg)
    circuit_type, phase_diff = analyzer.determine_circuit_type(theta_v_deg, theta_i_deg)
    
    v_instant, i_instant = analyzer.calculate_instantaneous_values(
        vm, im, f, theta_v_rad, theta_i_rad, t_instant
    )
    
    # Gerar formas de onda
    t, v, i, p = analyzer.generate_waveforms(f, vm, im, theta_v_rad, theta_i_rad, nr_periods)
    
    # Layout principal com abas
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Análise Principal", "📊 Resultados Detalhados", "⚡ Correção FP", "📋 Relatório"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">📊 Valores Principais</div>', unsafe_allow_html=True)
            
            # Métricas principais
            st.metric("Frequência", f"{f} Hz", f"ω = {2*np.pi*f:.2f} rad/s")
            st.metric("Período", f"{1000/f:.2f} ms", f"T = 1/f")
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                st.metric("Tensão RMS", f"{vrms:.2f} V", f"Vm/√2")
                st.metric("V instantâneo", f"{v_instant:.2f} V", f"t = {t_instant_ms} ms")
            with col1_2:
                st.metric("Corrente RMS", f"{irms:.2f} A", f"Im/√2")
                st.metric("I instantâneo", f"{i_instant:.2f} A", f"t = {t_instant_ms} ms")
        
        with col2:
            st.markdown('<div class="sub-header">⚡ Análise de Potência</div>', unsafe_allow_html=True)
            
            p_avg = (vm * im / 2) * fp
            p_rms = vrms * irms * fp
            p_instant = v_instant * i_instant
            
            st.metric("Fator de Potência", f"{fp:.3f}", circuit_type)
            st.metric("Defasamento", f"{phase_diff:.2f}°", "θv - θi")
            st.metric("Potência Média", f"{p_avg:.2f} W", "P = VrmsIrmscosφ")
            st.metric("Potência Instantânea", f"{p_instant:.2f} W", f"t = {t_instant_ms} ms")
        
        # Gráfico principal
        st.markdown('<div class="sub-header">📈 Formas de Onda</div>', unsafe_allow_html=True)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Tensão e Corrente", "Potência"),
            vertical_spacing=0.1
        )
        
        # Tensão e Corrente
        fig.add_trace(
            go.Scatter(x=t*1000, y=v, name="v(t)", line=dict(color='red', width=2)),
            row=1, col=1
        )
        
        # Ajustar escala da corrente se necessário
        i_plot = i * 10 if vm/im > 11.454 else i
        i_label = "i(t) × 10" if vm/im > 11.454 else "i(t)"
        
        fig.add_trace(
            go.Scatter(x=t*1000, y=i_plot, name=i_label, line=dict(color='blue', width=2)),
            row=1, col=1
        )
        
        # Potência
        p_plot = p / 1000 if max(abs(p)) >= 1000 else p
        p_unit = "kW" if max(abs(p)) >= 1000 else "W"
        
        fig.add_trace(
            go.Scatter(x=t*1000, y=p_plot, name=f"p(t)", line=dict(color='magenta', width=2)),
            row=2, col=1
        )
        
        p_rms_array = np.full_like(t, p_rms/1000 if max(abs(p)) >= 1000 else p_rms)
        fig.add_trace(
            go.Scatter(x=t*1000, y=p_rms_array, name=f"Prms", line=dict(color='black', width=2, dash='dash')),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Tempo (ms)", row=1, col=1)
        fig.update_xaxes(title_text="Tempo (ms)", row=2, col=1)
        fig.update_yaxes(title_text="Tensão (V) / Corrente (A)", row=1, col=1)
        fig.update_yaxes(title_text=f"Potência ({p_unit})", row=2, col=1)
        
        fig.update_layout(height=600, title="Sinais Elétricos - Análise Temporal")
        st.plotly_chart(fig, width='stretch')
    
    with tab2:
        st.markdown('<div class="sub-header">🔍 Resultados Detalhados</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📐 Fasores")
            # Criar DataFrame para os fasores
            fasors_data = {
                "Grandeza": ["Tensão", "Corrente"],
                "Módulo": [f"{vrms:.3f} V", f"{irms:.3f} A"],
                "Ângulo": [f"{theta_v_deg:.1f}°", f"{theta_i_deg:.1f}°"],
                "Forma Polar": [f"{vrms:.3f}∠{theta_v_deg:.1f}°", f"{irms:.3f}∠{theta_i_deg:.1f}°"]
            }
            st.dataframe(pd.DataFrame(fasors_data), width='stretch')
            
            # Diagrama Fasorial
            st.markdown("#### 🧭 Diagrama Fasorial")
            
            # Criar o diagrama fasorial
            fig_fasor = go.Figure()
            
            # Fasor de tensão (referência)
            v_x = vrms * np.cos(theta_v_rad)
            v_y = vrms * np.sin(theta_v_rad)
            
            # Escalar a corrente para melhor visualização
            scale_factor = vrms / irms if irms > 0 else 1
            if scale_factor > 50:  # Se a diferença for muito grande, limitar o fator
                scale_factor = 50
            elif scale_factor < 2:  # Se for muito próxima, usar fator mínimo
                scale_factor = 2
                
            # Fasor de corrente (escalado)
            i_x_scaled = irms * scale_factor * np.cos(theta_i_rad)
            i_y_scaled = irms * scale_factor * np.sin(theta_i_rad)
            
            # Adicionar fasor de tensão
            fig_fasor.add_trace(go.Scatter(
                x=[0, v_x],
                y=[0, v_y],
                mode='lines+markers',
                name=f'Tensão: {vrms:.1f}∠{theta_v_deg:.1f}° V',
                line=dict(color='red', width=4),
                marker=dict(size=10, symbol='triangle-up')
            ))
            
            # Adicionar fasor de corrente
            fig_fasor.add_trace(go.Scatter(
                x=[0, i_x_scaled],
                y=[0, i_y_scaled],
                mode='lines+markers',
                name=f'Corrente: {irms:.2f}∠{theta_i_deg:.1f}° A (×{scale_factor:.0f})',
                line=dict(color='blue', width=4),
                marker=dict(size=10, symbol='circle')
            ))
            
            # Adicionar círculo de referência
            theta_circle = np.linspace(0, 2*np.pi, 100)
            max_mag = max(vrms, irms * scale_factor)  # Usar o fator de escala calculado
            circle_r = max_mag * 0.9
            
            fig_fasor.add_trace(go.Scatter(
                x=circle_r * np.cos(theta_circle),
                y=circle_r * np.sin(theta_circle),
                mode='lines',
                name='Referência',
                line=dict(color='lightgray', width=1, dash='dot'),
                showlegend=False
            ))
            
            # Adicionar linhas de referência dos eixos
            fig_fasor.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            fig_fasor.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Adicionar anotações com ângulos
            fig_fasor.add_annotation(
                x=v_x*0.7, y=v_y*0.7,
                text=f"V = {vrms:.1f}V",
                showarrow=False,
                font=dict(color="red", size=12)
            )
            
            fig_fasor.add_annotation(
                x=i_x_scaled*0.7, y=i_y_scaled*0.7,
                text=f"I = {irms:.2f}A",
                showarrow=False,
                font=dict(color="blue", size=12)
            )
            
            # Adicionar ângulo de defasagem
            phase_diff = theta_v_deg - theta_i_deg
            circuit_type, _ = analyzer.determine_circuit_type(theta_v_deg, theta_i_deg)
            
            fig_fasor.add_annotation(
                x=max_mag*0.3, y=-max_mag*0.15,
                text=f"φ = {phase_diff:.1f}°<br>FP = {fp:.3f}<br>{circuit_type.split('(')[0]}",
                showarrow=False,
                font=dict(color="purple", size=12, weight="bold"),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="purple",
                borderwidth=2,
                borderpad=4
            )
            
            fig_fasor.update_layout(
                title=f"Diagrama Fasorial - Tensão e Corrente<br><sub>Corrente escalada {scale_factor:.0f}x para melhor visualização</sub>",
                xaxis_title="Componente Real",
                yaxis_title="Componente Imaginária",
                height=450,
                xaxis=dict(scaleanchor="y", scaleratio=1, gridcolor="lightgray"),
                yaxis=dict(scaleanchor="x", scaleratio=1, gridcolor="lightgray"),
                showlegend=True,
                legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)", bordercolor="gray", borderwidth=1),
                plot_bgcolor="rgba(248,249,250,0.8)"
            )
            
            st.plotly_chart(fig_fasor, width='stretch')
            
            # Impedância equivalente
            z_complex = (vrms * np.exp(1j * theta_v_rad)) / (irms * np.exp(1j * theta_i_rad))
            z_mag = abs(z_complex)
            z_angle = np.degrees(np.angle(z_complex))
            
            st.markdown("#### ⚡ Impedância Equivalente")
            st.write(f"**Módulo:** {z_mag:.3f} Ω")
            st.write(f"**Ângulo:** {z_angle:.2f}°")
            st.write(f"**Forma Retangular:** {z_complex.real:.3f} + {z_complex.imag:.3f}j Ω")
        
        with col2:
            st.markdown("#### 🔺 Triângulo de Potências")
            
            # Cálculo das potências
            s_complex = vrms * irms * np.exp(1j * np.radians(theta_v_deg - theta_i_deg))
            s_apparent = abs(s_complex)
            p_active = s_complex.real
            q_reactive = s_complex.imag
            
            power_data = {
                "Tipo": ["Ativa (P)", "Reativa (Q)", "Aparente (S)"],
                "Valor": [f"{p_active:.3f} W", f"{abs(q_reactive):.3f} VAr", f"{s_apparent:.3f} VA"],
                "Unidade": ["W", "VAr", "VA"]
            }
            st.dataframe(pd.DataFrame(power_data), width='stretch')
            
            # Gráfico do triângulo de potências
            fig_power = go.Figure()
            
            # Triângulo de potência
            fig_power.add_trace(go.Scatter(
                x=[0, p_active, p_active, 0],
                y=[0, 0, q_reactive, 0],
                mode='lines+markers',
                name='Triângulo de Potência',
                line=dict(color='blue', width=3)
            ))
            
            fig_power.add_annotation(x=p_active/2, y=-20, text=f"P = {p_active:.1f} W", showarrow=False)
            fig_power.add_annotation(x=p_active+20, y=q_reactive/2, text=f"Q = {abs(q_reactive):.1f} VAr", showarrow=False)
            fig_power.add_annotation(x=p_active/2, y=q_reactive/2, text=f"S = {s_apparent:.1f} VA", showarrow=False)
            
            fig_power.update_layout(
                title="Triângulo de Potências",
                xaxis_title="Potência Ativa (W)",
                yaxis_title="Potência Reativa (VAr)",
                height=400
            )
            st.plotly_chart(fig_power, width='stretch')
    
    with tab3:
        if correct_pf and desired_pf is not None:
            st.markdown('<div class="sub-header">⚙️ Correção do Fator de Potência</div>', unsafe_allow_html=True)
            
            correction = analyzer.calculate_power_correction(
                vrms, irms, theta_v_deg, theta_i_deg, fp, f, desired_pf
            )
            
            if correction:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"✅ Fator de potência corrigido para: **{desired_pf:.3f}**")
                    
                    st.metric("Capacitância Necessária", f"{correction['capacitance_uF']:.2f} µF")
                    st.metric("Corrente no Capacitor", f"{correction['i_capacitor']:.3f} A")
                    
                    # Gerar formas de onda corrigidas
                    if correction['q_capacitor'] != 0:
                        # Nova corrente total (simplificado)
                        i_total_rms = np.sqrt(irms**2 + correction['i_capacitor']**2)
                        new_fp = correction['p_active'] / (vrms * i_total_rms)
                        
                        st.metric("Novo Fator de Potência", f"{new_fp:.3f}")
                        st.metric("Potência Ativa", f"{correction['p_active']:.2f} W")
                
                with col2:
                    # Gráfico comparativo do fator de potência
                    fp_data = {
                        'Condição': ['Original', 'Corrigido'],
                        'Fator de Potência': [fp, desired_pf],
                        'Cor': ['red', 'green']
                    }
                    
                    fig_fp = go.Figure()
                    fig_fp.add_trace(go.Bar(
                        x=fp_data['Condição'],
                        y=fp_data['Fator de Potência'],
                        marker_color=fp_data['Cor'],
                        text=[f'{fp:.3f}', f'{desired_pf:.3f}'],
                        textposition='auto'
                    ))
                    
                    fig_fp.update_layout(
                        title="Comparação do Fator de Potência",
                        yaxis_title="Fator de Potência",
                        yaxis=dict(range=[0, 1]),
                        height=400
                    )
                    st.plotly_chart(fig_fp, width='stretch')
        else:
            st.info("ℹ️ Marque a opção 'Corrigir Fator de Potência' na barra lateral para ver os cálculos de correção.")
    
    with tab4:
        st.markdown('<div class="sub-header">📋 Relatório Completo</div>', unsafe_allow_html=True)
        
        # Relatório em formato texto
        st.markdown("### 🔍 Parâmetros Elétricos dos Sinais")
        
        report_data = [
            f"**A)** Frequência (F) = {f} Hz",
            f"**B)** Velocidade Angular (ω = 2πF) = {2*np.pi*f:.3f} rad/s",
            f"**C)** Período (T = 1/F) = {1000/f:.3f} ms",
            f"**D)** Tensão Elétrica Máxima (Vm) = {vm:.3f} V",
            f"**E)** Tensão Elétrica Eficaz (Vrms = Vm/√2) = {vrms:.3f} V",
            f"**F)** Valor da Tensão no instante t = {t_instant_ms:.3f} ms = {v_instant:.2f} V",
            f"**G)** Corrente Elétrica Máxima (Im) = {im:.3f} A",
            f"**H)** Corrente Elétrica Eficaz (Irms = Im/√2) = {irms:.3f} A",
            f"**I)** Valor da Corrente no instante t = {t_instant_ms:.3f} ms = {i_instant:.2f} A",
            f"**J)** Potência Ativa Média = {(vm*im/2)*fp:.3f} W",
            f"**K)** Potência Ativa Eficaz (RMS) = {vrms*irms*fp:.3f} W",
            f"**L)** Ângulo de Fase da Tensão = {theta_v_deg:.3f}°",
            f"**M)** Ângulo de Fase da Corrente = {theta_i_deg:.3f}°",
            f"**N)** Defasamento entre Tensão e Corrente = {phase_diff:.3f}°",
            f"**O)** Fator de Potência = {fp:.3f} ({circuit_type})"
        ]
        
        for item in report_data:
            st.write(item)
        
        # Botão para download do relatório
        if st.button("📥 Gerar Relatório PDF"):
            st.success("Funcionalidade de geração de PDF será implementada em breve!")

if __name__ == "__main__":
    main()
