# ⚡ Analisador de Circuitos Elétricos - Interface Web Moderna

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Status](https://img.shields.io/badge/Status-Produção-green.svg)

Uma aplicação web moderna e interativa para análise de circuitos elétricos monofásicos, convertida de código Scilab original com funcionalidades avançadas e interface profissional.

## 🚀 Aplicações Disponíveis

### 1. **� Analisador Avançado** ⭐ RECOMENDADO
- 🎛️ **25+ funcionalidades** profissionais
- 📈 **Análise harmônica** completa
- 🎯 **Presets inteligentes** (Residencial, Industrial, Motor)
- 💾 **Export múltiplos formatos** (CSV, JSON, PDF)
- 🧮 **Calculadoras auxiliares** integradas
- 📊 **Visualizações avançadas** e interativas

### 2. **⚡ Analisador Original**
- ✅ **Conversão direta** do código Scilab
- 📊 **Interface básica** e funcional
- 🔢 **Cálculos fundamentais** de circuitos AC
- 🎨 **Interface limpa** e intuitiva

## 🚀 Funcionalidades Principais

### � **Análise Completa de Circuitos**
- ✅ Análise de sinais elétricos v(t), i(t) e p(t)
- ✅ Cálculo de valores eficazes (RMS)
- ✅ Análise de fator de potência e defasagem
- ✅ Correção do fator de potência com dimensionamento
- ✅ Análise de potências ativa, reativa e aparente

### � **Interface Moderna**
- 🎯 Design responsivo com Streamlit
- 📱 Layout otimizado para desktop e mobile
- 🎨 Temas personalizados e gradientes
- ⚡ Interações fluidas e animações suaves

### � **Visualizações Avançadas**
- 📊 Gráficos interativos com Plotly
- 🌊 Formas de onda em tempo real
- 🔺 Triângulo de potências
- 📐 Diagrama fasorial
- 📊 Análise harmônica

## 🔧 Instalação e Execução

### Pré-requisitos
```bash
Python 3.8+
```

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/circuitos-analise.git
cd circuitos-analise
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute as aplicações

#### **� Analisador Avançado (RECOMENDADO)**
```bash
streamlit run app_advanced.py --server.port 8502
```
🌐 Acesse: `http://localhost:8502`

#### **⚡ Analisador Original**
```bash
streamlit run app.py
```
🌐 Acesse: `http://localhost:8501`

## 💻 Como Usar

### 1. **Configuração de Parâmetros**
   - 📊 Defina frequência (Hz)
   - ⚡ Configure tensão máxima (V)
   - 🔌 Ajuste corrente máxima (A)  
   - 📐 Defina ângulos de fase (graus)

### 2. **Análise Automática**
   - ✅ Valores RMS calculados automaticamente
   - 📈 Gráficos gerados em tempo real
   - 🔢 Métricas exibidas em cards interativos

### 3. **Correção do Fator de Potência**
   - 🎯 Defina fator de potência desejado
   - 📊 Visualize dimensionamento do capacitor
   - 💰 Analise economia de energia

### 4. **Exportação de Resultados**
   - 📁 Baixe dados em CSV
   - 📋 Gere relatórios profissionais
   - 💾 Salve configurações para reuso

## 🧩 Arquitetura do Projeto

```
📁 circuitos-analise/
├── 📄 app.py                      # Analisador original
├── 📄 app_advanced.py             # Analisador avançado ⭐  
├── 📄 circuit_calculator.py       # Classes de cálculo
├── 📄 ui_components.py            # Componentes de UI
├── 📄 requirements.txt            # Dependências
├── 📄 README.md                   # Esta documentação
└── 📄 MELHORIAS.md                # Histórico de melhorias
```

### 🏗️ **Módulos Principais**

#### `circuit_calculator.py`
```python
@dataclass
class CircuitParameters:
    """Parâmetros validados do circuito"""
    frequency: float
    voltage_max: float
    current_max: float
    voltage_phase: float
    current_phase: float

class ElectricalCalculator:
    """Calculadora especializada para circuitos elétricos"""
    
class AdvancedCircuitAnalyzer:
    """Análise avançada com cache e otimizações"""
```

#### `ui_components.py`
```python
def create_metric_cards():
    """Cards de métricas com hover effects"""

def create_advanced_charts():
    """Gráficos interativos Plotly"""

def export_data():
    """Sistema de exportação multi-formato"""
```

## 🎯 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.8+ | 🐍 Backend e lógica |
| **Streamlit** | 1.28+ | 🌐 Interface web |
| **NumPy** | 1.24+ | 🔢 Cálculos numéricos |
| **Pandas** | 2.0+ | 📊 Manipulação de dados |
| **Plotly** | 5.15+ | 📈 Visualizações interativas |
| **SciPy** | 1.10+ | 🧮 Funções científicas |
| **Dataclasses** | 3.8+ | 🏗️ Estruturas de dados |
| **Enum** | 3.8+ | 🎯 Tipos seguros |
| **UUID** | 3.8+ | 🔑 Identificação única |

## 📊 Comparativo das Versões

| Funcionalidade | Original | Avançada |
|---|:---:|:---:|
| Análise básica | ✅ | ✅ |
| Interface moderna | ✅ | ✅ |
| Gráficos interativos | ✅ | ✅ |
| Análise harmônica | ❌ | ✅ |
| Presets de circuitos | ❌ | ✅ |
| Export de dados | ❌ | ✅ |
| Calculadoras extras | ❌ | ✅ |
| Relatórios PDF | ❌ | ✅ |
| Cache otimizado | ❌ | ✅ |
| Métricas avançadas | ❌ | ✅ |

## 🔍 Exemplos de Uso

### 📋 **Circuito Residencial**
```python
# Configuração típica residencial 220V
frequency = 60.0        # Hz
voltage_max = 311.0     # V (220V RMS)
current_max = 10.0      # A
voltage_phase = 0.0     # graus
current_phase = -30.0   # graus (carga indutiva)
```

### 🏭 **Motor Industrial**
```python
# Configuração automática com preset "Motor Indutivo"
frequency = 60.0        # Hz
voltage_max = 537.0     # V (380V RMS)  
current_max = 50.0      # A
voltage_phase = 0.0     # graus
current_phase = -45.0   # graus
```

## 🤝 Contribuindo

Contribuições são bem-vindas! 

### 📋 **Como Contribuir**
1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Add: Nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/NovaFuncionalidade`)
5. **Abra** um Pull Request

## 📈 Próximos Passos

1. **🔌 Integração SPICE**: Simulação profissional de circuitos
2. **🤖 IA Integrada**: Sugestões automáticas de configuração
3. **📱 Versão Mobile**: Interface responsiva completa
4. **☁️ Cloud Sync**: Sincronização de configurações na nuvem
5. **👥 Colaboração**: Compartilhamento de análises
6. **🎓 Tutoriais**: Sistema de ensino interativo integrado

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Agradecimentos

- 🎓 **Comunidade Scilab** - Código original de inspiração
- 🚀 **Streamlit Team** - Framework web fantástico  
- 📊 **Plotly Developers** - Visualizações incríveis
- 🐍 **Python Community** - Ecossistema científico robusto

---

<div align="center">

**⚡ Analise e Simule Circuitos Elétricos com Tecnologia Moderna! ⚡**

![Electrical Engineering](https://img.shields.io/badge/Electrical-Engineering-orange.svg)
![Circuit Analysis](https://img.shields.io/badge/Circuit-Analysis-blue.svg)
![Modern Interface](https://img.shields.io/badge/Modern-Interface-green.svg)

</div>
