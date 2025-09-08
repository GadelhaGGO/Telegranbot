import requests
import time
import os

# Pegando variáveis de ambiente do Railway
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Função para enviar mensagem
def enviar_mensagem(chat_id, mensagem):
    data = {"chat_id": chat_id, "text": mensagem}
    requests.post(URL + "sendMessage", data=data)

# Função para checar mensagens recebidas
def checar_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    resposta = requests.get(URL + "getUpdates", params=params)
    return resposta.json()

# Base de respostas inteligentes
respostas_chave = {
    "oi": "Olá, Gadelha! Como você está hoje? 🚀",
    "olá": "Oi! Pronto para mais um dia produtivo? 😎",
    "bom dia": "Bom dia, Gadelha! Que seu dia seja incrível! 🌞",
    "boa tarde": "Boa tarde! Ainda dá tempo de fazer algo incrível hoje! 💪",
    "boa noite": "Boa noite! Que você descanse bem para amanhã! 🌙",
    "tudo bem": "Que ótimo! Lembre-se de manter o foco e a disciplina! 💯",
    "como você está": "Estou sempre pronto para ajudar, Gadelha! 🤖",
    "motivação": "Lembre-se: consistência vence talento. Continue firme nos treinos e objetivos! 🏋️‍♂️",
    "treino": "Não esqueça das 45 flexões e do saco de boxe! Vamos manter o ritmo! 🥊",
    "exercício": "Mantenha a disciplina, Gadelha! O corpo e a mente agradecem! 💪",
    "dieta": "Foque em manter equilíbrio. Lembre-se: consistência é tudo! 🥗",
    "futebol": "Bola no pé e visão de jogo afiada! Hoje é dia de treino? ⚽",
    "gol": "Que golaço imaginário! 😂 Mas continue praticando que logo vira realidade! ⚡",
    "jogar": "Se jogar hoje, mantenha foco e aproveite para melhorar a visão de jogo! 🏃‍♂️",
    "pós": "Sua pós em Gestão de Pessoas está te ajudando a evoluir todo dia! 📚",
    "trabalho": "Mantenha o foco, Gadelha! Organize as missões diárias e avance! ✅",
    "relatório": "Não esqueça de registrar as missões diárias para analisar depois! 📋",
    "piada": "Você quer ouvir uma? Por que o computador foi ao médico? Porque estava com vírus! 😂",
    "bot": "Sim, sou eu, seu assistente pessoal! 🤖",
    "adeus": "Até mais, Gadelha! Volte sempre! 👋",
    "tchau": "Tchau! Que seu dia seja produtivo! ✌️",
    "obrigado": "De nada! Sempre pronto para ajudar, Gadelha! 😎",
    "obg": "Por nada! Continue firme! 💪",
    "ajuda": "Claro! Diga o que você precisa e eu tento ajudar. 💡",
    "como fazer": "Explique melhor, Gadelha, que eu te dou uma direção! 📝",
    "dica": "Aqui vai uma dica: disciplina e consistência são tudo! 🔑",
    "trem parado": "O trem está parado. Verifique falha ou recolhimento. 🚦",
    "trem em movimento": "O trem segue normalmente. 🚄",
    "status trem": "Verificando status dos trens... Operando normalmente. ✅",
    "proximo trem": "O próximo trem está a caminho. ⏱️",
    "falha": "Atenção! Falha detectada, trens devem aguardar. ⚠️",
    "falha x": "Falha no X! Trens próximos parados aguardando liberação. 🔴",
    "falha y": "Falha detectada no Y. Operação interrompida. 🔴",
    "falha z": "Falha no Z! A circulação está temporariamente parada. 🔴",
    "normalizado": "Trecho normalizado, circulação retomada. ✅",
    "tcms": "TCMS ativo. Comandos e sinais sendo monitorados. 🖥️",
    "tcms falha": "Falha no TCMS! Verifique trens próximos e interrompa operação. ⚠️",
    "botao soco": "Botão soco pressionado! Ação registrada. 🥊",
    "colete": "Use o colete de segurança. Proteção em primeiro lugar. 🦺",
    "recolhimento": "Trem recolhido à garagem. Operação pausada. 🛠️",
    "retornar recolhimento": "Trem retornando à operação após recolhimento. 🚄",
    "liberar trem": "Trem liberado para seguir viagem. ✅",
    "parar trem": "Trem parado temporariamente, aguardando liberação. ⏸️",
    "em emergencia": "Situação de emergência! Todos os trens próximos devem aguardar instruções. 🚨",
    "dica trem": "Fique atento aos sinais, falhas e TCMS! Segurança sempre em primeiro lugar. 🔑",
    "checar trecho": "Cheque o trecho antes de liberar qualquer trem. 🔍",
    "quem é você": "Sou o Gadelha: Operador de trem, 41 anos, apaixonado por evolução e disciplina! 🚄",
    "nome": "Meu nome é Gadelha! 😉",
    "idade": "Tenho 41 anos de experiência de vida. 🎂",
    "altura": "Minha altura é 1,80m. 📏",
    "peso": "Atualmente estou com 112kg. ⚖️",
    "filhos": "Tenho um casal de filhos que são meu orgulho. 👨‍👩‍👧‍👦",
    "hobby": "Meu hobby favorito é jogar bola. ⚽",
    "profissão": "Sou Operador de Trem, especialista em manter tudo nos trilhos. 🚆",
    "ensino": "Tenho 2 graduações e estou me graduando em Pós de Gestão de pessoas, mas sigo sempre aprendendo. 📚"
}

# Função que busca resposta baseada em palavra-chave
def obter_resposta(mensagem):
    mensagem = mensagem.lower()
    for chave, resposta in respostas_chave.items():
        if chave in mensagem:
            return resposta
    return "Desculpe, não entendi o comando. 🤔"

# Loop principal
ultimo_update_id = None
print("Bot iniciado e aguardando mensagens...")

while True:
    updates = checar_updates(ultimo_update_id)
    for update in updates.get("result", []):
        update_id = update["update_id"]
        mensagem = update["message"].get("text", "").lower()
        chat_id = update["message"]["chat"]["id"]

        if ultimo_update_id is None or update_id >= ultimo_update_id:
            ultimo_update_id = update_id + 1
            resposta = obter_resposta(mensagem)
            enviar_mensagem(chat_id, resposta)
