# Módulo de cálculos de circuitos elétricos
# Separação de responsabilidades para melhor manutenibilidade

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, List
import streamlit as st

@dataclass
class CircuitParameters:
    """Classe para armazenar parâmetros do circuito"""
    frequency: float
    voltage_max: float
    current_max: float
    voltage_angle: float
    current_angle: float
    periods: int = 2

@dataclass
class CalculationResults:
    """Classe para armazenar resultados dos cálculos"""
    voltage_rms: float
    current_rms: float
    power_factor: float
    power_active: float
    power_reactive: float
    power_apparent: float
    impedance_magnitude: float
    impedance_angle: float
    circuit_type: str
    phase_difference: float

class ElectricalCalculator:
    """Calculadora principal para análise de circuitos elétricos"""
    
    def __init__(self):
        self.tolerance = 1e-6
    
    @staticmethod
    @st.cache_data
    def calculate_rms_values(vm: float, im: float) -> Tuple[float, float]:
        """Calcula valores eficazes (RMS) com cache para performance"""
        return vm / np.sqrt(2), im / np.sqrt(2)
    
    @staticmethod
    def validate_parameters(params: CircuitParameters) -> List[str]:
        """Valida parâmetros de entrada"""
        errors = []
        
        if params.frequency <= 0:
            errors.append("Frequência deve ser positiva")
        if params.voltage_max <= 0:
            errors.append("Tensão máxima deve ser positiva")
        if params.current_max <= 0:
            errors.append("Corrente máxima deve ser positiva")
        if not (1 <= params.periods <= 20):
            errors.append("Número de períodos deve estar entre 1 e 20")
            
        return errors
    
    def calculate_power_factor(self, theta_v_deg: float, theta_i_deg: float) -> float:
        """Calcula fator de potência com tratamento de erros"""
        try:
            return np.cos(np.radians(abs(theta_v_deg - theta_i_deg)))
        except Exception:
            return 0.0
    
    def determine_circuit_type(self, theta_v_deg: float, theta_i_deg: float) -> Tuple[str, float]:
        """Determina tipo de circuito com lógica melhorada"""
        # Normalizar ângulos
        theta_v_norm = self._normalize_angle(theta_v_deg)
        theta_i_norm = self._normalize_angle(theta_i_deg)
        
        phase_diff = theta_v_norm - theta_i_norm
        phase_diff = self._normalize_phase_difference(phase_diff)
        phase_diff_abs = abs(phase_diff)
        
        # Classificação com tolerância
        if phase_diff_abs < self.tolerance:
            return "Em fase (resistivo)", phase_diff_abs
        elif abs(phase_diff_abs - 90) < 1.0:
            if phase_diff < 0:
                return "Adiantado (puramente capacitivo)", phase_diff_abs
            else:
                return "Atrasado (puramente indutivo)", phase_diff_abs
        elif phase_diff < 0:
            return "Adiantado (capacitivo)", phase_diff_abs
        else:
            return "Atrasado (indutivo)", phase_diff_abs
    
    def _normalize_angle(self, angle: float) -> float:
        """Normaliza ângulo para 0-360 graus"""
        return angle % 360
    
    def _normalize_phase_difference(self, phase_diff: float) -> float:
        """Normaliza diferença de fase para -180 a 180 graus"""
        if phase_diff > 180:
            phase_diff -= 360
        elif phase_diff < -180:
            phase_diff += 360
        return phase_diff
    
    def calculate_impedance(self, vrms: float, irms: float, 
                          theta_v_rad: float, theta_i_rad: float) -> Tuple[complex, float, float]:
        """Calcula impedância complexa"""
        v_phasor = vrms * np.exp(1j * theta_v_rad)
        i_phasor = irms * np.exp(1j * theta_i_rad)
        
        if abs(i_phasor) < self.tolerance:
            return complex(float('inf'), 0), float('inf'), 0
            
        z_complex = v_phasor / i_phasor
        z_magnitude = abs(z_complex)
        z_angle = np.degrees(np.angle(z_complex))
        
        return z_complex, z_magnitude, z_angle
    
    def calculate_powers(self, vrms: float, irms: float, 
                        theta_v_deg: float, theta_i_deg: float) -> Dict[str, float]:
        """Calcula todas as potências"""
        phase_diff_rad = np.radians(theta_v_deg - theta_i_deg)
        
        s_apparent = vrms * irms
        p_active = s_apparent * np.cos(phase_diff_rad)
        q_reactive = s_apparent * np.sin(phase_diff_rad)
        
        return {
            'apparent': s_apparent,
            'active': p_active,
            'reactive': q_reactive,
            'reactive_abs': abs(q_reactive)
        }
    
    def calculate_instantaneous_values(self, vm: float, im: float, f: float,
                                     theta_v_rad: float, theta_i_rad: float, 
                                     t_instant: float) -> Tuple[float, float, float]:
        """Calcula valores instantâneos de v, i e p"""
        v_instant = vm * np.sin(2 * np.pi * f * t_instant + theta_v_rad)
        i_instant = im * np.sin(2 * np.pi * f * t_instant + theta_i_rad)
        p_instant = v_instant * i_instant
        
        return v_instant, i_instant, p_instant
    
    def find_time_for_value(self, amplitude: float, target_value: float, 
                           frequency: float, phase_rad: float) -> Optional[float]:
        """Encontra o primeiro instante onde a grandeza atinge um valor específico"""
        if abs(target_value) > abs(amplitude):
            return None
            
        # Considera o semiciclo apropriado
        if target_value >= 0:
            t = (np.arcsin(target_value / amplitude) - phase_rad) / (2 * np.pi * frequency)
        else:
            t = (np.arcsin(abs(target_value) / amplitude) - phase_rad) / (2 * np.pi * frequency) + 1 / (2 * frequency)
        
        # Garantir tempo positivo
        while t < 0:
            t += 1 / frequency
            
        return t
    
    @staticmethod
    @st.cache_data
    def generate_waveforms(f: float, vm: float, im: float, 
                          theta_v_rad: float, theta_i_rad: float, 
                          periods: int, points: int = 2000) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Gera formas de onda com cache para performance"""
        t_total = periods / f
        t = np.linspace(-t_total, t_total, points)
        
        v = vm * np.sin(2 * np.pi * f * t + theta_v_rad)
        i = im * np.sin(2 * np.pi * f * t + theta_i_rad)
        p = v * i
        
        return t, v, i, p
    
    def perform_complete_analysis(self, params: CircuitParameters) -> CalculationResults:
        """Executa análise completa do circuito"""
        # Validação
        errors = self.validate_parameters(params)
        if errors:
            raise ValueError(f"Parâmetros inválidos: {', '.join(errors)}")
        
        # Conversões
        theta_v_rad = np.radians(params.voltage_angle)
        theta_i_rad = np.radians(params.current_angle)
        
        # Cálculos RMS
        vrms, irms = self.calculate_rms_values(params.voltage_max, params.current_max)
        
        # Fator de potência e tipo de circuito
        fp = self.calculate_power_factor(params.voltage_angle, params.current_angle)
        circuit_type, phase_diff = self.determine_circuit_type(params.voltage_angle, params.current_angle)
        
        # Impedância
        z_complex, z_magnitude, z_angle = self.calculate_impedance(
            vrms, irms, theta_v_rad, theta_i_rad
        )
        
        # Potências
        powers = self.calculate_powers(vrms, irms, params.voltage_angle, params.current_angle)
        
        return CalculationResults(
            voltage_rms=vrms,
            current_rms=irms,
            power_factor=fp,
            power_active=powers['active'],
            power_reactive=powers['reactive'],
            power_apparent=powers['apparent'],
            impedance_magnitude=z_magnitude,
            impedance_angle=z_angle,
            circuit_type=circuit_type,
            phase_difference=phase_diff
        )

class PowerFactorCorrector:
    """Classe especializada para correção do fator de potência"""
    
    def __init__(self):
        pass
    
    def calculate_correction(self, results: CalculationResults, vrms: float, 
                           frequency: float, desired_fp: float) -> Optional[Dict]:
        """Calcula correção do fator de potência"""
        if not (0 < desired_fp <= 1):
            return None
            
        try:
            # Potência reativa necessária após correção
            q_after = results.power_active * np.tan(np.arccos(desired_fp))
            q_capacitor = results.power_reactive - q_after
            
            if abs(q_capacitor) < 1e-6:
                return None
                
            # Capacitância em µF
            capacitance = abs(q_capacitor / (vrms**2 * 2 * np.pi * frequency)) * 1e6
            
            # Reatância e corrente do capacitor
            xc = vrms**2 / q_capacitor if q_capacitor != 0 else float('inf')
            i_capacitor = vrms / abs(xc) if abs(xc) != float('inf') else 0
            
            # Nova corrente total (aproximação)
            i_total_rms = np.sqrt(results.current_rms**2 + i_capacitor**2)
            new_fp = results.power_active / (vrms * i_total_rms) if i_total_rms > 0 else 0
            
            return {
                'capacitance_uF': capacitance,
                'q_capacitor': q_capacitor,
                'i_capacitor': i_capacitor,
                'new_power_factor': new_fp,
                'new_current_total': i_total_rms,
                'reduction_current': ((results.current_rms - i_total_rms) / results.current_rms) * 100,
                'energy_savings': self._calculate_energy_savings(results.power_active, results.current_rms, i_total_rms)
            }
            
        except Exception:
            return None
    
    def _calculate_energy_savings(self, p_active: float, i_old: float, i_new: float) -> float:
        """Calcula economia de energia percentual"""
        if i_old <= 0:
            return 0
        reduction = (i_old - i_new) / i_old
        return reduction * 100

class HarmonicAnalyzer:
    """Classe para análise de harmônicos (FFT)"""
    
    @staticmethod
    @st.cache_data
    def analyze_harmonics(signal: np.ndarray, frequency: float, 
                         max_harmonics: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """Análise FFT para detectar harmônicos"""
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/(frequency * len(signal)))
        
        # Pegar apenas frequências positivas
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft[:len(fft)//2])
        
        # Normalizar
        positive_fft = positive_fft / len(signal) * 2
        
        # Limitar número de harmônicos
        limit = min(max_harmonics, len(positive_freqs))
        
        return positive_freqs[:limit], positive_fft[:limit]
