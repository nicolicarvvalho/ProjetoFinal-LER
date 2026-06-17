from datetime import datetime

estacionamento = {}  
vagas_totais = 20

# Gararante que o histórico comece totalmente zerado
historico_pagamentos = []

def calcular_valor(minutos):
    # Se o cliente ficou menos ou igual a 15 minutos, não paga nada (Carência)
    if minutos <= 15:
        return 0.0
    
    # Se ficou entre 16 e 60 minutos, cobra a taxa fixa de R$ 10.00
    if minutos <= 60:
        return 10.0
    
    # Se passou de 1 hora, calcula as horas adicionais
    minutos_adicionais = minutos - 60
    horas_adicionais = minutos_adicionais // 60
    if minutos_adicionais % 60 > 0:
        horas_adicionais += 1
        
    return 10.0 + (horas_adicionais * 5.0)

while True:
    vagas_restantes = vagas_totais - len(estacionamento)
    
    print("\n" + "="*45)
    print(f" ⛐ QUICKPARKING CLI | Vagas Restantes: {vagas_restantes}/{vagas_totais}")
    
    if vagas_restantes <= 0:
        print(" 🚨   ESTACIONAMENTO LOTADO!")
        print("Registrar Entrada Desabilitado")
    print("="*45)
    
    print("1. Registrar Entrada")
    print("2. Registrar Saída e Pagamento")
    print("3. Excluir Registro (Correção de Erro)")
    print("4. Relatório de Faturamento Total")
    print("5. Sair")
    print("-"*45)
    
    opcao = input("Digite uma opção: ").strip()
    
    if opcao == "1":
        if vagas_restantes <= 0:
            print("\n ERRO: Ação bloqueada. O estacionamento está lotado!")
            continue
            
        placa = input("Digite a placa: ").upper().strip()
        
        if placa in estacionamento:
            print("\n ERRO: Esta placa já está dentro do estacionamento!")
            continue
            
        print("\n Seleção de Tipo:")
        print("C. Carro")
        print("M. Moto")
        botao_tipo = input("Selecione o tipo (C ou M): ").strip().upper()
        
        if botao_tipo in ["C", "CARRO"]:
            tipo_veiculo = "CARRO"
        elif botao_tipo in ["M", "MOTO"]:
            tipo_veiculo = "MOTO"
        else:
            print("\n Seleção inválida. Operação cancelada.")
            continue
            
        estacionamento[placa] = {
            "hora_entrada": datetime.now(),
            "tipo": tipo_veiculo
        }
        print(f"\n Gravado com sucesso! Veículo [{tipo_veiculo}] Placa [{placa}] registrado.")
        
    elif opcao == "2":
        placa = input("Buscar Placa Ativa - Digite a placa: ").upper().strip()
        
        if placa not in estacionamento:
            print("\n Placa não encontrada ou não está ativa no sistema!")
            continue
            
        info_veiculo = estacionamento[placa]
        hora_entrada = info_veiculo["hora_entrada"]
        
        hora_saida = datetime.now()
        diferenca = hora_saida - hora_entrada
        
        segundos_totais = diferenca.total_seconds()
        minutos_decorridos = int(segundos_totais // 60)
        if segundos_totais % 60 > 0:
            minutos_decorridos += 1
            
        valor_pagar = calcular_valor(minutos_decorridos)
        
        print("\n" + "-"*40)
        print(f"🧾 TELA DE SAÍDA - VEÍCULO: {placa}")
        print(f"⏱ Tempo de permanência: {minutos_decorridos} minuto(s).")
        print(f"💰 VALOR NA TELA: R$ {valor_pagar:.2f}")
        print("-"*40)
        
        if valor_pagar > 0:
            print("Selecione a forma de pagamento:")
            print("1. Dinheiro")
            print("2. Cartão")
            print("3. Pix")
            botao_pagamento = input("Forma escolhida: ").strip()
            
            if botao_pagamento == "1" or botao_pagamento.upper() == "DINHEIRO":
                forma_salva = "Dinheiro"
            elif botao_pagamento in ["2", "CARTAO", "CARTÃO"]:
                forma_salva = "Cartão"
            elif botao_pagamento == "3" or botao_pagamento.upper() == "PIX":
                forma_salva = "Pix"
            else:
                print("\n Opção inválida. Definindo automaticamente como Pix para concluir.")
                forma_salva = "Pix"
                
            # O valor só entra no histórico AQUI, após a saída ser confirmada
            historico_pagamentos.append(valor_pagar)
            print(f"\n Pagamento registrado via [{forma_salva}].")
        else:
            print("\n Saída liberada! Sem cobrança (Tempo de carência).")
            
        del estacionamento[placa]
        print(f" Vaga correspondente à placa {placa} agora está LIVRE.")

    elif opcao == "3":
        print("\n--- LISTA DE PLACAS ATIVAS NO PÁTIO ---")
        if not estacionamento:
            print("Nenhum veículo estacionado no momento.")
            continue
            
        for p in estacionamento.keys():
            print(f" Placa: {p} -> Excluir Registro disponível]")
            
        placa_excluir = input("\n Digite a placa que deseja EXCLUIR (correção de erro): ").upper().strip()
        
        if placa_excluir in estacionamento:
            del estacionamento[placa_excluir]
            print(f"\n Registro da placa {placa_excluir} foi EXCLUÍDO e a vaga foi liberada sem cobranças.")
        else:
            print("\n Esta placa não foi encontrada na lista.")

    elif opcao == "4":
        total_faturado = sum(historico_pagamentos)
        
        print("\n" + "#"*40)
        print(" 🗃️ TELA DE FATURAMENTO TOTAL")
        print("#"*40)
        print(f" Atendimentos pagos realizados: {len(historico_pagamentos)}")
        print(f" TOTAL FATURADO EXIBIDO: R$ {total_faturado:.2f}")
        print("#"*40)
        
    elif opcao in ["5", "SAIR"]:
        print("\nSistema encerrado. Até logo!")
        break
    else:
        print("\n Comando inválido!")