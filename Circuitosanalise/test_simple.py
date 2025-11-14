print("🔧 Iniciando teste simples...")

try:
    print("📦 Importando módulos...")
    from circuit_editor import CircuitBuilder, ComponentType
    print("✅ Import OK!")
    
    print("🏗️ Criando builder...")
    builder = CircuitBuilder()
    print("✅ Builder criado!")
    
    print("📊 Testando parâmetros...")
    params = builder.calculate_circuit_parameters()
    print(f"✅ Parâmetros: {params}")
    
    print("🎉 Teste concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
