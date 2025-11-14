# Módulo de interface e visualizações
# Componentes reutilizáveis para a interface Streamlit

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import io
import base64

class UIComponents:
    """Componentes de interface reutilizáveis"""
    
    @staticmethod
    def create_metric_card(title: str, value: str, delta: str = None, 
                          help_text: str = None) -> None:
        """Cria card de métrica personalizado"""
        with st.container():
            st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                border-left: 5px solid #1f77b4;
                margin: 0.5rem 0;
            ">
                <h4 style="margin: 0; color: #2c3e50;">{title}</h4>
                <h2 style="margin: 0.5rem 0; color: #1f77b4;">{value}</h2>
                {f'<p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">{delta}</p>' if delta else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if help_text:
                st.info(help_text)
    
    @staticmethod
    def create_parameter_section(title: str, icon: str = "🔧") -> None:
        """Cria seção de parâmetros com estilo"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #1f77b4, #17a2b8);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin: 1rem 0 0.5rem 0;
        ">
            <h3 style="margin: 0;">{icon} {title}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_alert(message: str, alert_type: str = "info") -> None:
        """Cria alertas coloridos"""
        colors = {
            "info": "#17a2b8",
            "success": "#28a745", 
            "warning": "#ffc107",
            "error": "#dc3545"
        }
        
        st.markdown(f"""
        <div style="
            background-color: {colors.get(alert_type, colors['info'])}15;
            border: 1px solid {colors.get(alert_type, colors['info'])};
            color: {colors.get(alert_type, colors['info'])};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        ">
            {message}
        </div>
        """, unsafe_allow_html=True)

class ChartGenerator:
    """Gerador de gráficos interativos"""
    
    @staticmethod
    def create_waveform_chart(t: np.ndarray, v: np.ndarray, i: np.ndarray, 
                            p: np.ndarray, vm: float, im: float) -> go.Figure:
        """Cria gráfico de formas de onda melhorado"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("📈 Tensão e Corrente vs Tempo", "⚡ Potência vs Tempo"),
            vertical_spacing=0.12,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Ajustar escala da corrente se necessário
        scale_factor = 10 if vm/im > 11.454 else 1
        i_plot = i * scale_factor
        i_label = f"i(t) × {scale_factor}" if scale_factor > 1 else "i(t)"
        
        # Tensão e Corrente
        fig.add_trace(
            go.Scatter(
                x=t*1000, y=v, 
                name="v(t)", 
                line=dict(color='#e74c3c', width=2.5),
                hovertemplate="Tempo: %{x:.2f} ms<br>Tensão: %{y:.2f} V<extra></extra>"
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=t*1000, y=i_plot, 
                name=i_label, 
                line=dict(color='#3498db', width=2.5),
                hovertemplate=f"Tempo: %{{x:.2f}} ms<br>Corrente: %{{y:.2f}} A<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Potência
        p_plot = p / 1000 if max(abs(p)) >= 1000 else p
        p_unit = "kW" if max(abs(p)) >= 1000 else "W"
        
        fig.add_trace(
            go.Scatter(
                x=t*1000, y=p_plot, 
                name=f"p(t)", 
                line=dict(color='#9b59b6', width=2.5),
                hovertemplate=f"Tempo: %{{x:.2f}} ms<br>Potência: %{{y:.2f}} {p_unit}<extra></extra>"
            ),
            row=2, col=1
        )
        
        # Linha de potência média
        p_avg = np.mean(p_plot)
        fig.add_hline(
            y=p_avg, 
            line=dict(color='#2c3e50', width=2, dash='dash'),
            annotation_text=f"P médio = {p_avg:.2f} {p_unit}",
            row=2, col=1
        )
        
        # Configurações dos eixos
        fig.update_xaxes(title_text="Tempo (ms)", showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(title_text="Tensão (V) / Corrente (A)", showgrid=True, gridwidth=1, gridcolor='lightgray', row=1)
        fig.update_yaxes(title_text=f"Potência ({p_unit})", showgrid=True, gridwidth=1, gridcolor='lightgray', row=2)
        
        fig.update_layout(
            height=700,
            title="📊 Análise Temporal dos Sinais Elétricos",
            title_font_size=16,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_power_triangle(p_active: float, q_reactive: float) -> go.Figure:
        """Cria triângulo de potências interativo"""
        s_apparent = np.sqrt(p_active**2 + q_reactive**2)
        
        fig = go.Figure()
        
        # Triângulo
        fig.add_trace(go.Scatter(
            x=[0, p_active, p_active, 0],
            y=[0, 0, q_reactive, 0],
            mode='lines+markers',
            name='Triângulo de Potência',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8, color='#e74c3c'),
            hovertemplate="<extra></extra>"
        ))
        
        # Hipotenusa (potência aparente)
        fig.add_trace(go.Scatter(
            x=[0, p_active],
            y=[0, q_reactive],
            mode='lines',
            name='Potência Aparente',
            line=dict(color='#e74c3c', width=3, dash='dash'),
            hovertemplate="<extra></extra>"
        ))
        
        # Anotações
        fig.add_annotation(x=p_active/2, y=-s_apparent*0.1, 
                          text=f"P = {p_active:.1f} W", showarrow=False, font_size=12)
        fig.add_annotation(x=p_active+s_apparent*0.05, y=q_reactive/2, 
                          text=f"Q = {abs(q_reactive):.1f} VAr", showarrow=False, font_size=12)
        fig.add_annotation(x=p_active/2-s_apparent*0.1, y=q_reactive/2+s_apparent*0.05, 
                          text=f"S = {s_apparent:.1f} VA", showarrow=False, font_size=12)
        
        fig.update_layout(
            title="🔺 Triângulo de Potências",
            xaxis_title="Potência Ativa (W)",
            yaxis_title="Potência Reativa (VAr)",
            height=450,
            showlegend=False,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
        )
        
        return fig
    
    @staticmethod
    def create_phasor_diagram(vrms: float, irms: float, theta_v: float, theta_i: float) -> go.Figure:
        """Cria diagrama fasorial"""
        fig = go.Figure()
        
        # Conversão para coordenadas cartesianas
        v_x = vrms * np.cos(np.radians(theta_v))
        v_y = vrms * np.sin(np.radians(theta_v))
        i_x = irms * np.cos(np.radians(theta_i))
        i_y = irms * np.sin(np.radians(theta_i))
        
        # Fasor tensão
        fig.add_trace(go.Scatter(
            x=[0, v_x], y=[0, v_y],
            mode='lines+markers',
            name=f'V = {vrms:.1f}V ∠ {theta_v:.1f}°',
            line=dict(color='#e74c3c', width=4),
            marker=dict(size=[0, 12], symbol=['circle', 'arrow'], 
                       color='#e74c3c', line=dict(width=2))
        ))
        
        # Fasor corrente (escalado para visualização)
        scale = vrms / irms if irms > 0 else 1
        fig.add_trace(go.Scatter(
            x=[0, i_x*scale], y=[0, i_y*scale],
            mode='lines+markers',
            name=f'I = {irms:.1f}A ∠ {theta_i:.1f}° (escala {scale:.1f}×)',
            line=dict(color='#3498db', width=4),
            marker=dict(size=[0, 12], symbol=['circle', 'arrow'], 
                       color='#3498db', line=dict(width=2))
        ))
        
        # Círculo de referência
        theta_circle = np.linspace(0, 2*np.pi, 100)
        max_radius = max(vrms, irms*scale)
        fig.add_trace(go.Scatter(
            x=max_radius * np.cos(theta_circle),
            y=max_radius * np.sin(theta_circle),
            mode='lines',
            name='Referência',
            line=dict(color='lightgray', width=1, dash='dot'),
            showlegend=False
        ))
        
        fig.update_layout(
            title="📐 Diagrama Fasorial",
            xaxis_title="Componente Real",
            yaxis_title="Componente Imaginária",
            height=450,
            xaxis=dict(scaleanchor="y", scaleratio=1, showgrid=True),
            yaxis=dict(showgrid=True),
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_harmonic_spectrum(frequencies: np.ndarray, amplitudes: np.ndarray) -> go.Figure:
        """Cria espectro de harmônicos"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=frequencies,
            y=amplitudes,
            name='Espectro de Frequências',
            marker_color='#9b59b6',
            hovertemplate="Frequência: %{x:.1f} Hz<br>Amplitude: %{y:.3f}<extra></extra>"
        ))
        
        fig.update_layout(
            title="🌊 Análise de Harmônicos (FFT)",
            xaxis_title="Frequência (Hz)",
            yaxis_title="Amplitude",
            height=400,
            showlegend=False
        )
        
        return fig

class DataExporter:
    """Classe para exportação de dados"""
    
    @staticmethod
    def create_report_dataframe(params: Dict, results: Dict) -> pd.DataFrame:
        """Cria DataFrame para relatório"""
        data = {
            "Parâmetro": [
                "Frequência", "Tensão Máxima", "Corrente Máxima", "Ângulo Tensão", 
                "Ângulo Corrente", "Tensão RMS", "Corrente RMS", "Fator de Potência",
                "Potência Ativa", "Potência Reativa", "Potência Aparente",
                "Impedância", "Tipo de Circuito"
            ],
            "Valor": [
                f"{params.get('frequency', 0)} Hz",
                f"{params.get('voltage_max', 0):.2f} V",
                f"{params.get('current_max', 0):.2f} A", 
                f"{params.get('voltage_angle', 0):.1f}°",
                f"{params.get('current_angle', 0):.1f}°",
                f"{results.get('voltage_rms', 0):.2f} V",
                f"{results.get('current_rms', 0):.2f} A",
                f"{results.get('power_factor', 0):.3f}",
                f"{results.get('power_active', 0):.2f} W",
                f"{results.get('power_reactive', 0):.2f} VAr",
                f"{results.get('power_apparent', 0):.2f} VA",
                f"{results.get('impedance_magnitude', 0):.2f} Ω",
                f"{results.get('circuit_type', 'N/A')}"
            ]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_csv_download(df: pd.DataFrame, filename: str = "relatorio_circuito.csv") -> str:
        """Gera link de download para CSV"""
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Baixar CSV</a>'
    
    @staticmethod
    def generate_waveform_csv(t: np.ndarray, v: np.ndarray, i: np.ndarray, p: np.ndarray) -> str:
        """Gera CSV das formas de onda"""
        df = pd.DataFrame({
            'Tempo_ms': t * 1000,
            'Tensao_V': v,
            'Corrente_A': i,
            'Potencia_W': p
        })
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="formas_onda.csv">📥 Baixar Formas de Onda</a>'

class PresetManager:
    """Gerenciador de presets de circuitos"""
    
    PRESETS = {
        "Residencial 220V": {
            "frequency": 60,
            "voltage_max": 311.13,  # 220V RMS * √2
            "current_max": 14.14,   # 10A RMS * √2
            "voltage_angle": 0,
            "current_angle": 0,
            "description": "Circuito residencial padrão brasileiro"
        },
        "Industrial 380V": {
            "frequency": 60,
            "voltage_max": 537.4,   # 380V RMS * √2
            "current_max": 70.7,    # 50A RMS * √2
            "voltage_angle": 0,
            "current_angle": -30,
            "description": "Circuito industrial trifásico (uma fase)"
        },
        "Motor Indutivo": {
            "frequency": 60,
            "voltage_max": 311.13,
            "current_max": 28.28,   # 20A RMS * √2
            "voltage_angle": 0,
            "current_angle": -25,   # Atraso típico de motor
            "description": "Motor de indução monofásico"
        },
        "Capacitor Banco": {
            "frequency": 60,
            "voltage_max": 311.13,
            "current_max": 7.07,    # 5A RMS * √2
            "voltage_angle": 0,
            "current_angle": 90,    # Corrente adiantada
            "description": "Banco de capacitores"
        }
    }
    
    @classmethod
    def get_preset_names(cls) -> List[str]:
        """Retorna nomes dos presets disponíveis"""
        return list(cls.PRESETS.keys())
    
    @classmethod
    def get_preset(cls, name: str) -> Dict:
        """Retorna preset pelo nome"""
        return cls.PRESETS.get(name, {})
    
    @classmethod
    def apply_preset(cls, name: str) -> None:
        """Aplica preset aos controles da interface"""
        preset = cls.get_preset(name)
        if preset:
            for key, value in preset.items():
                if key != "description" and f"preset_{key}" not in st.session_state:
                    st.session_state[f"preset_{key}"] = value
