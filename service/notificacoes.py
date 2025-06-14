def notificar_equipamento_offline(equipamento_id: int):
    print(f"⚠️ NOTIFICAÇÃO: Equipamento ID {equipamento_id} ficou offline!")

def notificar_alocacao(recurso_id: int, equipamento_id: int, tipo_recurso: str):
    print(f"ℹ️ NOTIFICAÇÃO: Recurso {tipo_recurso} (ID {recurso_id}) foi alocado para o equipamento ID {equipamento_id}")

def notificar_desalocacao(recurso_id: int):
    print(f"ℹ️ NOTIFICAÇÃO: Recurso ID {recurso_id} foi desalocado e está disponível")
