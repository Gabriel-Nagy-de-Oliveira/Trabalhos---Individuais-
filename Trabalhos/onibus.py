import os
import requests
import folium
import tempfile
import webbrowser
from dotenv import load_dotenv

# ==============================
# 1️⃣ Carregar token
# ==============================
load_dotenv(".env")
token = os.getenv("SPTRANS_TOKEN")

if not token:
    print("❌ ERRO: variável SPTRANS_TOKEN não encontrada no .env")
    exit()

# ==============================
# 2️⃣ Autenticação
# ==============================
s = requests.Session()
auth = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
)

if auth.text.lower() == "true":
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Falha ao autenticar. Verifique o token.")
    exit()

# ==============================
# 3️⃣ Digitar código CL da linha
# ==============================
codigo_linha = input("Digite o código CL da linha: ")

# ==============================
# 4️⃣ Buscar paradas da linha
# ==============================
url_paradas = f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
res = s.get(url_paradas)
paradas = res.json()

print(f"Total de paradas encontradas: {len(paradas)}")

if len(paradas) == 0:
    print("⚠ Esta linha não possui paradas ou está inativa agora.")
    exit()

# ==============================
# 5️⃣ Buscar ônibus em tempo real
# ==============================
url_posicao = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}"
resp = s.get(url_posicao)
dados_pos = resp.json()

onibus = dados_pos.get("vs", [])
print(f"Ônibus encontrados em tempo real: {len(onibus)}")

# ==============================
# 6️⃣ Criar mapa
# ==============================
m = folium.Map(location=[paradas[0]["py"], paradas[0]["px"]], zoom_start=14)

# ---- adicionar pins das paradas (azul)
for p in paradas:
    folium.Marker(
        location=[p["py"], p["px"]],
        popup=f"Parada: {p['np']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# ---- adicionar pins dos ônibus (vermelho)
for b in onibus:
    folium.Marker(
        location=[b["py"], b["px"]],
        popup=f"Ônibus: {b['p']}",
        icon=folium.Icon(color="red", icon="bus")
    ).add_to(m)

# ==============================
# 7️⃣ Abrir automaticamente NO NAVEGADOR sem cache
# ==============================
arquivo_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
m.save(arquivo_temp.name)
webbrowser.open("file://" + arquivo_temp.name)

print("\nMapa aberto em uma nova guia do navegador.\n")
