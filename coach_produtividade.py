import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="COACH DE PRODUTIVIDADE", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_coach():
    return {"perfis": {}}

_cache = get_cache_coach()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_planos', 'biblioteca_planos',
    'meta_grande', 'area_foco', 'rotina_atual',
    'plano_ativo', 'checklist_hoje',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_plano(tipo: str, objetivo: str, conteudo: str):
    st.session_state.historico_planos.append({
        'data':     datetime.now().strftime('%d/%m %H:%M'),
        'tipo':     tipo,
        'objetivo': objetivo,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':            "Login",
    'usuario':          "",
    'api_key':          "",
    'pagina':           "Home",
    'historico_planos': [],
    'biblioteca_planos':[],
    'meta_grande':      "",
    'area_foco':        "",
    'rotina_atual':     "",
    'plano_ativo':      "",
    'checklist_hoje':   [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def coach_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um Coach de Produtividade e Metas de elite.
Usuário: {st.session_state.usuario}.
Filosofia: direto, prático, sem enrolação. Cada resposta deve ter 1 ação concreta imediata.
{system_extra}
Baseie-se em: GTD, Deep Work, Atomic Habits, Eisenhower Matrix, Time Blocking.
Escreva em português brasileiro natural. Seja humano, não robótico."""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_planos)
    bib   = len(st.session_state.biblioteca_planos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F0FDF4;border:1px solid #86EFAC;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} planos gerados · {bib} salvos na biblioteca</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"coach_produtividade_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="coachpro34"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'area_foco' not in st.session_state: st.session_state['area_foco'] = None
if 'biblioteca_planos' not in st.session_state: st.session_state['biblioteca_planos'] = []
if 'historico_planos' not in st.session_state: st.session_state['historico_planos'] = []
if 'meta_grande' not in st.session_state: st.session_state['meta_grande'] = None
if 'rotina_atual' not in st.session_state: st.session_state['rotina_atual'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 COACH DE PRODUTIVIDADE")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    (_tab_Home, _tab_Foco, _tab_Tarefas, _tab_Pomodoro, _tab_Habitos, _tab_Energia, _tab_Metas, _tab_Delegacao, _tab_Revisao) = st.tabs(['🏠 Painel', '🎯 Foco e Deep Work', '📋 Tarefas', '⏱️ Pomodoro', '🔄 Hábitos', '⚡ Energia', '🏆 Metas', '🤝 Delegar', '📊 Revisão'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_coachpro")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_coachpro", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🚀")
            st.markdown("<span class='badge'>Em evolução</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="coachpro3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        total_h = len(st.session_state.historico_planos)
        if total_h == 0 and len(st.session_state.biblioteca_planos) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        # CONFIGURAÇÃO DO PERFIL
        st.markdown("#### ⚙️ Seu perfil de produtividade")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.session_state.meta_grande  = st.text_input("Sua meta principal de vida:", value=st.session_state.meta_grande, placeholder="ex: ter renda própria, emagrecer 15kg...", key="coachpro4")
        with col_b:
            st.session_state.area_foco   = st.text_input("Área de maior foco agora:", value=st.session_state.area_foco, placeholder="ex: carreira, saúde, finanças...", key="coachpro5")
        with col_c:
            st.session_state.rotina_atual = st.text_input("Como está sua rotina hoje:", value=st.session_state.rotina_atual, placeholder="ex: trabalho das 8-18h, sem horário fixo...", key="coachpro6")


        # MÉTRICAS
        tipos = {}
        for p in st.session_state.historico_planos:
            tipos[p['tipo']] = tipos.get(p['tipo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_h}</div><div>Planos gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.biblioteca_planos)}</div><div>Na biblioteca</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Plano 90 dias',0)}</div><div>Planos 90 dias</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Rotina',0)}</div><div>Rotinas criadas</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Você não sobe ao nível das suas metas. Você cai ao nível dos seus sistemas.'</em> — James Clear</div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "🎯 Metas":       "Define metas SMART, prioriza objetivos e cria plano de ação",
            "📅 Plano 30/60/90": "Roteiro detalhado de 30, 60 ou 90 dias para qualquer objetivo",
            "🌅 Rotina":      "Cria sua rotina diária ideal — manhã, tarde e noite",
            "⏰ Gestão de Tempo": "Organiza suas tarefas com Matriz de Eisenhower e Time Blocking",
            "🧘 Modo Foco":   "Estratégias de Deep Work, Pomodoro e eliminação de distrações",
            "💪 Hábitos":     "Plano de construção ou eliminação de hábitos com gatilhos e recompensas",
            "📚 Biblioteca":  "Seus planos e rotinas salvos organizados",
            "📈 Progresso":   "Histórico completo de tudo que foi gerado",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_planos:
            st.markdown("### 🕐 Últimos Planos Gerados")
            for item in reversed(st.session_state.historico_planos[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<small style='color:#888'>{item['data']}</small><br>"
                    f"<small style='color:#555'>{item.get('objetivo', '')[:80]}</small></div>",
                    unsafe_allow_html=True
                )

        # ========================
        # METAS
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_coachpro")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_coachpro")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Foco:
        st.header("🧘 Modo Foco — Deep Work")
        st.markdown("Estratégias de foco profundo personalizadas para o seu contexto e suas distrações.")

        col1, col2 = st.columns(2)
        with col1:
            tarefa_foco   = st.text_input("Em que você precisa focar profundamente?",
                placeholder="ex: escrever meu e-book, estudar programação, criar conteúdo...", key="coachpro17_d2")
            distractores  = st.text_area("Suas maiores distrações:", height=80,
                placeholder="ex: celular, redes sociais, filhos em casa, barulho, pensamentos...", key="coachpro16_d2")
            ambiente      = st.text_input("Onde você vai trabalhar:",
                placeholder="ex: home office, café, trabalho, quarto...", key="coachpro15_d2")
        with col2:
            duracao_sessao= st.selectbox("Duração ideal de sessão de foco:", ["25 min (Pomodoro)","50 min","90 min (Ultradian)","2 horas","4 horas"], key="coachpro27_d2")
            historico_foco= st.radio("Sua relação atual com o foco:", ["Muito difícil focar","Consigo um pouco","Razoavelmente bom"], horizontal=True, key="coachpro28_d2")
            objetivo_foco = st.text_input("O que você quer completar nessa sessão de foco:",
                placeholder="ex: escrever 1.000 palavras, estudar 2 capítulos...", key="coachpro14_d2")

        if st.button("🧘 CRIAR MEU PROTOCOLO DE FOCO", key="coachpro29_d2"):
            if tarefa_foco.strip():
                with st.spinner("Montando seu protocolo de foco..."):
                    prompt = (
                        f"Crie um protocolo personalizado de foco profundo (Deep Work).\n"
                        f"Tarefa: {tarefa_foco}. Distrações: {distractores}. Ambiente: {ambiente}.\n"
                        f"Duração: {duracao_sessao}. Nível atual: {historico_foco}. Objetivo: {objetivo_foco}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🧘 PRÉ-SESSÃO (10 minutos antes):\n"
                        f"[Ritual de entrada no estado de foco — específico para esse contexto]\n\n"
                        f"📵 PROTOCOLO ANTI-DISTRAÇÃO:\n"
                        f"[Como neutralizar cada distração listada — soluções práticas e realistas]\n\n"
                        f"⏱️ ESTRUTURA DA SESSÃO DE {duracao_sessao}:\n"
                        f"[Minuto a minuto — o que fazer em cada fase da sessão]\n\n"
                        f"🔄 PROTOCOLO DE RETORNO (quando se distrair):\n"
                        f"[Como voltar ao foco sem se punir — em menos de 60 segundos]\n\n"
                        f"🏁 PÓS-SESSÃO (10 minutos depois):\n"
                        f"[Ritual de saída — para registrar o progresso e recarregar]\n\n"
                        f"📈 COMO AUMENTAR O FOCO PROGRESSIVAMENTE:\n"
                        f"[Plano de 4 semanas para treinar o músculo do foco]\n\n"
                        f"💡 INSIGHT PERSONALIZADO:\n"
                        f"[Uma observação específica sobre o padrão de distração dessa pessoa]"
                    )
                    res = coach_ia(prompt)
                    if res: st.session_state['res_foco_coachp1'] = str(res)
                    salvar_plano("Protocolo de Foco", tarefa_foco[:60], res)
                    st.session_state['foco_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Diga em que você precisa focar.")

        if st.session_state.get('foco_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['foco_temp'],
                    file_name="protocolo_foco.txt", mime="text/plain", use_container_width=True, key="coachpro13_d2")
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_foco", use_container_width=True):
                    st.session_state.biblioteca_planos.append({
                        'tipo': 'Protocolo de Foco', 'objetivo': tarefa_foco[:60],
                        'conteudo': st.session_state['foco_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

        # ========================
        # HÁBITOS
        # ========================

    with _tab_Tarefas:
        st.header("📋 Tarefas Inteligentes")
        st.markdown("*Gerencie suas tarefas com priorização inteligente da IA.*")
        _prompt_tarefas = st.text_area("Descreva sua situação ou dúvida:", height=120, key="coachp_tarefas_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="coachp_tarefas_btn", use_container_width=True):
            if _prompt_tarefas.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_tarefas}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Pomodoro:
        st.header("⏱️ Técnica Pomodoro")
        st.markdown("*Sessões de foco com intervalos estratégicos.*")
        _prompt_pomodoro = st.text_area("Descreva sua situação ou dúvida:", height=120, key="coachp_pomodoro_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="coachp_pomodoro_btn", use_container_width=True):
            if _prompt_pomodoro.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_pomodoro}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Habitos:
        st.header("💪 Construtor de Hábitos")
        st.markdown("Baseado em Atomic Habits — crie hábitos que grudam e elimine os que sabotam.")

        tab1, tab2 = st.tabs(["✅ Criar Novo Hábito", "❌ Eliminar Hábito Ruim"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                habito_novo   = st.text_input("Qual hábito você quer criar?",
                    placeholder="ex: exercitar 30min/dia, ler 20 páginas/dia, meditar 10min...", key="coachpro12_d2")
                motivacao_h   = st.text_input("Por que esse hábito importa para você?",
                    placeholder="ex: quero ter mais energia e saúde...", key="coachpro11_d2")
                tentativas_h  = st.text_input("Já tentou antes? O que aconteceu?",
                    placeholder="ex: sim, comecei 3 vezes e parei depois de 1 semana...", key="coachpro10_d2")
            with col2:
                frequencia_h  = st.selectbox("Frequência desejada:", ["Todo dia","5x por semana","3x por semana","2x por semana","1x por semana"], key="coachpro30_d2")
                horario_h     = st.text_input("Melhor horário:", placeholder="ex: manhã, após o almoço, à noite...", key="coachpro31_d2")
                habito_ancora = st.text_input("O que você já faz todo dia (hábito âncora)?",
                    placeholder="ex: tomar café, escovar os dentes, acordar...", key="coachpro9_d2")

            if st.button("✅ CRIAR PLANO DE HÁBITO", key="coachpro32_d2"):
                if habito_novo.strip():
                    with st.spinner("Criando seu plano de hábito..."):
                        prompt = (
                            f"Crie um plano completo para criar o hábito: '{habito_novo}'.\n"
                            f"Motivação: {motivacao_h}. Tentativas anteriores: {tentativas_h}.\n"
                            f"Frequência: {frequencia_h}. Horário: {horario_h}. Âncora: {habito_ancora}.\n\n"
                            f"Use a framework dos 4 passos de James Clear (Atomic Habits):\n\n"
                            f"🔔 1. GATILHO (Deixa óbvio):\n"
                            f"[Como tornar o gatilho do hábito impossível de ignorar — específico para essa rotina]\n\n"
                            f"😍 2. ANSEIO (Torna atraente):\n"
                            f"[Como fazer esse hábito parecer irresistível — técnica de empilhamento ou recompensa]\n\n"
                            f"⚡ 3. RESPOSTA (Facilita ao máximo):\n"
                            f"[Versão mínima do hábito para começar — regra dos 2 minutos adaptada]\n\n"
                            f"🏆 4. RECOMPENSA (Satisfação imediata):\n"
                            f"[Como celebrar imediatamente após o hábito para reforçar o circuito]\n\n"
                            f"📅 PLANO DE 66 DIAS (tempo médio para automatizar):\n"
                            f"Semana 1-2: [fase de início]\n"
                            f"Semana 3-4: [fase de consolidação]\n"
                            f"Semana 5-8: [fase de automatização]\n"
                            f"Semana 9+: [fase de manutenção]\n\n"
                            f"🚧 POR QUE VOCÊ FALHOU ANTES E COMO EVITAR:\n"
                            f"[Análise honesta das tentativas anteriores e solução específica]\n\n"
                            f"📏 COMO MEDIR:\n"
                            f"[Método simples de registro — máx 30 segundos por dia]"
                        )
                        res = coach_ia(prompt)
                        if res: st.session_state['res_habitos_coachp2'] = str(res)
                        salvar_plano("Hábito Novo", habito_novo[:60], res)
                        st.session_state['habito_novo_temp'] = res
                        st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Diga qual hábito quer criar.")

            if st.session_state.get('habito_novo_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar plano (.txt)", data=st.session_state['habito_novo_temp'],
                        file_name="habito_novo.txt", mime="text/plain", use_container_width=True, key="coachpro8_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_hab_novo", use_container_width=True):
                        st.session_state.biblioteca_planos.append({
                            'tipo': 'Hábito Novo', 'objetivo': habito_novo[:60],
                            'conteudo': st.session_state['habito_novo_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo!")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                habito_ruim  = st.text_input("Qual hábito você quer eliminar?",
                    placeholder="ex: rolar Instagram por horas, comer besteira à noite, procrastinar...", key="coachpro7_d2")
                gatilho_ruim = st.text_input("O que dispara esse hábito?",
                    placeholder="ex: entedio, estresse, ver o celular, após o jantar...", key="coachpro6_d2")
                tempo_habito = st.text_input("Há quanto tempo tem esse hábito?",
                    placeholder="ex: 3 anos, desde a pandemia...", key="coachpro5_d2")
            with col2:
                prejuizo     = st.text_input("Como ele prejudica sua vida?",
                    placeholder="ex: perco 2h por dia, fico culpado, não consigo dormir...", key="coachpro4_d2")
                tentativas_r = st.text_input("Já tentou parar? O que aconteceu?",
                    placeholder="ex: sim, durei 3 dias e voltei...", key="coachpro3_d2")

            if st.button("❌ CRIAR PLANO PARA ELIMINAR O HÁBITO", key="coachpro33_d2"):
                if habito_ruim.strip():
                    with st.spinner("Criando estratégia de eliminação..."):
                        prompt = (
                            f"Crie um plano para eliminar o hábito ruim: '{habito_ruim}'.\n"
                            f"Gatilho: {gatilho_ruim}. Tempo de hábito: {tempo_habito}.\n"
                            f"Prejuízo: {prejuizo}. Tentativas anteriores: {tentativas_r}.\n\n"
                            f"ESTRATÉGIA (baseada em Atomic Habits — inversão dos 4 passos):\n\n"
                            f"🙈 1. INVISÍVEL (Esconde o gatilho):\n"
                            f"[Como remover ou dificultar o acesso ao gatilho '{gatilho_ruim}']\n\n"
                            f"😐 2. POUCO ATRAENTE (Muda a mentalidade):\n"
                            f"[Como reprogramar a forma de ver esse hábito — associação negativa real]\n\n"
                            f"🧱 3. DIFICULTA (Aumenta o atrito):\n"
                            f"[Como tornar o hábito ruim fisicamente mais difícil de executar]\n\n"
                            f"😤 4. INSATISFATÓRIO (Consequência imediata):\n"
                            f"[Como criar uma punição ou consequência imediata que dói]\n\n"
                            f"🔄 SUBSTITUTO SAUDÁVEL:\n"
                            f"[Qual hábito positivo pode ocupar o mesmo horário/gatilho]\n\n"
                            f"📅 PLANO DE DESINTOXICAÇÃO (primeiros 21 dias):\n"
                            f"[O que esperar e como agir em cada fase]\n\n"
                            f"🚨 PLANO B (se recair):\n"
                            f"[Como voltar sem culpa e sem perder o progresso]"
                        )
                        res = coach_ia(prompt)
                        if res: st.session_state['res_habitos_coachp3'] = str(res)
                        salvar_plano("Eliminar Hábito", habito_ruim[:60], res)
                        st.session_state['habito_ruim_temp'] = res
                        st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Diga qual hábito quer eliminar.")

            if st.session_state.get('habito_ruim_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar estratégia (.txt)", data=st.session_state['habito_ruim_temp'],
                        file_name="eliminar_habito.txt", mime="text/plain", use_container_width=True, key="coachpro2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_hab_ruim", use_container_width=True):
                        st.session_state.biblioteca_planos.append({
                            'tipo': 'Eliminar Hábito', 'objetivo': habito_ruim[:60],
                            'conteudo': st.session_state['habito_ruim_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo!")

        # ========================
        # BIBLIOTECA
        # ========================

    with _tab_Energia:
        st.header("⚡ Gestão de Energia")
        st.markdown("*Gerencie seu nível de energia ao longo do dia.*")
        _prompt_energia = st.text_area("Descreva sua situação ou dúvida:", height=120, key="coachp_energia_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="coachp_energia_btn", use_container_width=True):
            if _prompt_energia.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_energia}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Metas:
        st.header("🎯 Definição e Priorização de Metas")
        st.markdown("Transforme desejos vagos em metas claras, mensuráveis e com plano de ação.")

        col1, col2 = st.columns(2)
        with col1:
            objetivo = st.text_area("O que você quer alcançar?", height=100,
                placeholder="ex: quero sair do emprego e ter minha própria renda online em 6 meses", key="coachpro33")
            prazo    = st.selectbox("Prazo:", ["1 mês","3 meses","6 meses","1 ano","2 anos","5 anos"], key="coachpro7")
            contexto = st.text_area("Sua situação atual:", height=80,
                placeholder="ex: trabalho CLT, ganho R$3.000, tenho 2h livres por dia...", key="coachpro32")
        with col2:
            area     = st.selectbox("Área da vida:", ["Carreira/Negócios","Finanças","Saúde/Corpo","Relacionamentos","Estudos","Espiritualidade/Propósito","Estilo de vida","Outro"], key="coachpro8")
            nivel    = st.radio("Nível de comprometimento:", ["Quero explorar","Estou decidido","Totalmente comprometido"], horizontal=True, key="coachpro9")
            obstaculos = st.text_input("Principal obstáculo:", placeholder="ex: falta de tempo, medo, sem dinheiro...", key="coachpro10")

        if st.button("🎯 CRIAR PLANO DE META SMART", key="coachpro11"):
            if objetivo.strip():
                with st.spinner("Estruturando sua meta..."):
                    prompt = (
                        f"Crie um plano completo de meta SMART para: '{objetivo}'.\n"
                        f"Área: {area}. Prazo: {prazo}. Contexto: {contexto}. "
                        f"Obstáculo: {obstaculos}. Comprometimento: {nivel}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🎯 META SMART REFORMULADA:\n"
                        f"[Reescreva a meta sendo: Específica, Mensurável, Atingível, Relevante, Temporal]\n\n"
                        f"📊 DIAGNÓSTICO HONESTO:\n"
                        f"[Avalie se a meta é realista no prazo e contexto dados — seja direto]\n\n"
                        f"🪜 MARCOS DO CAMINHO (milestones):\n"
                        f"[3-5 marcos intermediários com datas estimadas]\n\n"
                        f"⚡ AS 3 AÇÕES MAIS IMPORTANTES (as que movem o ponteiro de verdade):\n"
                        f"[Ação 1, Ação 2, Ação 3 — concretas e imediatas]\n\n"
                        f"🚧 COMO SUPERAR O OBSTÁCULO '{obstaculos}':\n"
                        f"[Estratégia prática específica para esse obstáculo]\n\n"
                        f"📅 PRÓXIMOS 7 DIAS — O QUE FAZER JÁ:\n"
                        f"[Plano dia a dia para a primeira semana]\n\n"
                        f"⚠️ ARMADILHAS A EVITAR:\n"
                        f"[Os 3 erros mais comuns de quem persegue essa meta e como fugir deles]"
                    )
                    res = coach_ia(prompt)
                    if res: st.session_state['res_metas_coachp4'] = str(res)
                    salvar_plano("Meta SMART", objetivo[:60], res)
                    st.session_state['meta_temp'] = res
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva o que você quer alcançar.")

        if st.session_state.get('meta_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano (.txt)", data=st.session_state['meta_temp'],
                    file_name="meta_smart.txt", mime="text/plain", use_container_width=True, key="coachpro31")
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", use_container_width=True, key="coachpro12"):
                    st.session_state.biblioteca_planos.append({
                        'tipo': 'Meta SMART', 'objetivo': objetivo[:60],
                        'conteudo': st.session_state['meta_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

        # ========================
        # PLANO 30/60/90 DIAS
        # ========================

    with _tab_Delegacao:
        st.header("🤝 O que Delegar?")
        st.markdown("*Descubra o que delegar para focar no que importa.*")
        _prompt_delegacao = st.text_area("Descreva sua situação ou dúvida:", height=120, key="coachp_delegacao_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="coachp_delegacao_btn", use_container_width=True):
            if _prompt_delegacao.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_delegacao}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Revisao:
        pass

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Coach de Produtividade — Metas, Rotina e Foco com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
