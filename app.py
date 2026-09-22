import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Simulador de Metodologies Àgils", page_icon="🎯", layout="wide")

# Estils visuals personalitzats
st.markdown("""
<style>
    .stMetric { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; }
    .card-todo { background-color: #e2e3e5; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 4px solid #6c757d; }
    .card-wip { background-color: #fff3cd; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 4px solid #ffc107; }
    .card-testing { background-color: #cff4fc; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 4px solid #0dcaf0; }
    .card-done { background-color: #d1e7dd; padding: 10px; border-radius: 6px; margin-bottom: 6px; font-size: 13px; border-left: 4px solid #198754; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# REINICI DE DADES
# -----------------------------------------------------------------------------
def reset():
    st.session_state.dia = 1
    # Scrum
    st.session_state.scrum_history = []
    # Kanban
    st.session_state.todo_k = 20
    st.session_state.wip_k = 0
    st.session_state.test_k = 0
    st.session_state.done_k = 0
    st.session_state.cfd_history = []
    # Lean
    st.session_state.lean_util = 0
    st.session_state.lean_waste = 0
    st.session_state.lean_history = []
    # XP
    st.session_state.xp_deute = 0
    st.session_state.xp_history = []

if 'dia' not in st.session_state:
    reset()

# -----------------------------------------------------------------------------
# BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.title("🎯 Simulador d'Impacte Àgil")
metodologia = st.sidebar.selectbox("Tria la metodologia a visualitzar:", 
    ["1. Scrum (Planificació vs Burnout)", 
     "2. Kanban (WIP vs Colls d'ampolla)", 
     "3. Lean (MVP vs Deixall/Waste)", 
     "4. XP (TDD vs Deute Tècnic)"])

if st.sidebar.button("🔄 Reiniciar Simulador"):
    reset()
    st.rerun()

st.title("Laboratori de Simulació de Metodologies Àgils")

# -----------------------------------------------------------------------------
# 1. SCRUM: BURNDOWN CHART & BURNOUT
# -----------------------------------------------------------------------------
if "Scrum" in metodologia:
    st.header("🏃 Mode Scrum: Planificació de Sprint i Burndown Chart")
    st.info("💡 **Objectiu:** Comprendre que per sobrecarregar el Sprint no s'obté millor resultat, sinó Burnout i bugs.")

    col_ctrl, col_graph = st.columns([1, 2])

    with col_ctrl:
        st.subheader("Configuració del Sprint")
        punts_compromesos = st.slider("Punts d'Història compromesos (Capacitat real equip: 12)", 5, 25, 12)
        
        if st.button("🚀 Executar Sprint (10 dies)"):
            diferencia = punts_compromesos - 12
            dies = list(range(0, 11))
            
            # Línia ideal
            ideal = [punts_compromesos - (punts_compromesos / 10) * d for d in dies]
            
            # Línia real
            real = [punts_compromesos]
            punts_restants = punts_compromesos
            
            for d in range(1, 11):
                if diferencia > 3:
                    # Sobrecàrrega: L'equip es cansa i la velocitat cau a la segona meitat
                    rendiment = random.choice([0, 1]) if d > 5 else random.choice([1, 2])
                else:
                    # Ritme sostenible
                    rendiment = random.choice([1, 2])
                
                punts_restants = max(0, punts_restants - rendiment)
                real.append(punts_restants)

            st.session_state.scrum_history.append({
                'Sprint': len(st.session_state.scrum_history) + 1,
                'Compromesos': punts_compromesos,
                'Completats': punts_compromesos - real[-1],
                'Dies': dies,
                'Ideal': ideal,
                'Real': real,
                'Sobrecàrrega': diferencia > 3
            })
            st.rerun()

    with col_graph:
        if st.session_state.scrum_history:
            últim_sprint = st.session_state.scrum_history[-1]
            st.subheader(f"📊 Burndown Chart - Sprint {últim_sprint['Sprint']}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=últim_sprint['Dies'], y=últim_sprint['Ideal'], name="Línia Ideal", line=dict(dash='dash', color='gray')))
            fig.add_trace(go.Scatter(x=últim_sprint['Dies'], y=últim_sprint['Real'], name="Línia Real", line=dict(color='red' if últim_sprint['Sobrecàrrega'] else 'green', width=3)))
            fig.update_layout(xaxis_title="Dies del Sprint", yaxis_title="Punts Restants", height=350)
            st.plotly_chart(fig, use_container_width=True)

            if últim_sprint['Sobrecàrrega']:
                st.error(f"❌ **Burnout detectat!** Us heu compromès a {últim_sprint['Compromesos']} punts però només n'heu completat {últim_sprint['Completats']}. La pressió ha provocat reducció de velocitat.")
            else:
                st.success(f"✅ **Sprint Completat!** Compromís sostenible de {últim_sprint['Compromesos']} punts i {últim_sprint['Completats']} punts lliurats.")

# -----------------------------------------------------------------------------
# 2. KANBAN: WORK IN PROGRESS (WIP) I COLLS D'AMPOLLA
# -----------------------------------------------------------------------------
elif "Kanban" in metodologia:
    st.header("📋 Mode Kanban: Control del WIP i Diagrama de Flux Acumulat (CFD)")
    st.info("💡 **Objectiu:** Observar com augmentar el límit de WIP crea colls d'ampolla i fa augmentar el Lead Time.")

    st.subheader("Configuració de Controls")
    wip_max = st.slider("Límit de WIP (Work In Progress) per a la columna 'Desenvolupament':", 1, 8, 3)

    if st.button("⏩ Simular 1 Dia de Treball"):
        st.session_state.dia += 1
        
        # Pull de Backlog a WIP segons el límit
        espai = wip_max - st.session_state.wip_k
        if espai > 0 and st.session_state.todo_k > 0:
            agafades = min(espai, st.session_state.todo_k)
            st.session_state.todo_k -= agafades
            st.session_state.wip_k += agafades

        # Rendiment afecta segons si hi ha multitassa excessiva
        if st.session_state.wip_k > 4:
            # Col·lapse per excessiu WIP
            fet_dev = 1
        else:
            fet_dev = min(st.session_state.wip_k, random.randint(1, 3))

        st.session_state.wip_k -= fet_dev
        st.session_state.test_k += fet_dev

        # Testing a Done
        fet_test = min(st.session_state.test_k, 2)
        st.session_state.test_k -= fet_test
        st.session_state.done_k += fet_test

        # Registrar historial per al CFD
        st.session_state.cfd_history.append({
            'Dia': st.session_state.dia,
            'Done': st.session_state.done_k,
            'Testing': st.session_state.test_k,
            'WIP': st.session_state.wip_k,
            'To Do': st.session_state.todo_k
        })
        st.rerun()

    # Visualització de columnes
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"### 📥 To Do ({st.session_state.todo_k})")
        for i in range(min(5, st.session_state.todo_k)):
            st.markdown(f"<div class='card-todo'>Tasca #{i+1}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"### ⚙️ WIP (Max {wip_max})")
        for i in range(st.session_state.wip_k):
            st.markdown(f"<div class='card-wip'>Tasca en procés</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"### 🧪 Testing ({st.session_state.test_k})")
        for i in range(st.session_state.test_k):
            st.markdown(f"<div class='card-testing'>Tasca en revisió</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"### ✅ Done ({st.session_state.done_k})")
        for i in range(min(5, st.session_state.done_k)):
            st.markdown(f"<div class='card-done'>Tasca Finalitzada</div>", unsafe_allow_html=True)

    # CFD Chart
    if st.session_state.cfd_history:
        st.subheader("📈 Diagrama de Flux Acumulat (CFD)")
        df_cfd = pd.DataFrame(st.session_state.cfd_history)
        fig_cfd = px.area(df_cfd, x='Dia', y=['Done', 'Testing', 'WIP', 'To Do'], 
                          title="Evolució de les Tasques (Si les franges d'InProgress creixen, el Lead Time augmenta)")
        fig_cfd.update_layout(height=300)
        st.plotly_chart(fig_cfd, use_container_width=True)

# -----------------------------------------------------------------------------
# 3. LEAN: MVP VS WASTE (DEIXALL)
# -----------------------------------------------------------------------------
elif "Lean" in metodologia:
    st.header("🌱 Mode Lean: Eliminació de Deixall (Muda) i Validació MVP")
    st.info("💡 **Objectiu:** Experimentar com fer un desenvolupament llarg sense validació genera feina inútil que el client rebutja.")

    col_dec, col_met = st.columns(2)

    with col_dec:
        st.subheader("Quina estratègia vols aplicar?")
        opcio = st.radio("Acció a executar:", [
            "Llançar un MVP ràpid (3 dies de desenvolupament)",
            "Desenvolupar el producte complet amb totes les opcions (20 dies sense feedback)",
            "Automatitzar processos i eliminar feina manual (2 dies)"
        ])

        if st.button("Executar Estratègia"):
            if "MVP" in opcio:
                st.session_state.lean_util += 10
                st.session_state.lean_history.append("MVP validat: 100% de la feina aprofitada.")
            elif "producte complet" in opcio:
                util = random.randint(3, 8)
                waste = 20 - util
                st.session_state.lean_util += util
                st.session_state.lean_waste += waste
                st.session_state.lean_history.append(f"Producte llarg llançat: {waste} dies de feina rebutjats pel client (Deixall)!")
            else:
                st.session_state.lean_history.append("Procés automatitzat: Es redueix el temps de lliurament futur.")
            st.rerun()

    with col_met:
        st.subheader("📊 Balanç de Temps Investit")
        df_lean = pd.DataFrame({
            'Tipus': ['Temps Útil (Valor Real)', 'Deixall / Waste (Sense Valor)'],
            'Dies': [st.session_state.lean_util, st.session_state.lean_waste]
        })
        fig_lean = px.pie(df_lean, values='Dies', names='Tipus', color='Tipus',
                          color_discrete_map={'Temps Útil (Valor Real)':'green', 'Deixall / Waste (Sense Valor)':'red'})
        fig_lean.update_layout(height=300)
        st.plotly_chart(fig_lean, use_container_width=True)

        for h in reversed(st.session_state.lean_history[-4:]):
            st.write(f"- {h}")

# -----------------------------------------------------------------------------
# 4. EXTREME PROGRAMMING (XP): TDD I DEUTE TÈCNIC
# -----------------------------------------------------------------------------
elif "XP" in metodologia:
    st.header("🛠️ Mode XP: Impacte del Deute Tècnic en la Velocitat")
    st.info("💡 **Objectiu:** Comprendre que no aplicar pràctiques d'enginyeria (TDD/Refactoring) permet anar ràpid al principi però atura el projecte a mitjà termini.")

    col_xp_ctrl, col_xp_graph = st.columns([1, 2])

    with col_xp_ctrl:
        st.subheader("Pràctiques Tècniques per a la setmana")
        usar_tdd = st.checkbox("🧪 Test-Driven Development (TDD)", value=True)
        usar_refactoring = st.checkbox("⚙️ Refactoring Continu", value=True)

        if st.button("💻 Executar Setmana de Desenvolupament"):
            # Lògica de simulació de deute
            if not usar_tdd:
                nou_deute = 15
            else:
                nou_deute = 0

            if not usar_refactoring:
                nou_deute += 10
            else:
                st.session_state.xp_deute = max(0, st.session_state.xp_deute - 10)

            st.session_state.xp_deute += nou_deute

            # Calcular la velocitat segons el deute acumulat
            velocitat_base = 12
            penalitzacio = (st.session_state.xp_deute / 100) * 10
            velocitat_real = max(1, int(velocitat_base - penalitzacio))

            st.session_state.xp_history.append({
                'Setmana': len(st.session_state.xp_history) + 1,
                'Deute': st.session_state.xp_deute,
                'Velocitat': velocitat_real
            })
            st.rerun()

    with col_xp_graph:
        if st.session_state.xp_history:
            st.subheader("📈 Velocitat vs. Deute Tècnic Acumulat")
            df_xp = pd.DataFrame(st.session_state.xp_history)

            fig_xp = go.Figure()
            fig_xp.add_trace(go.Scatter(x=df_xp['Setmana'], y=df_xp['Velocitat'], name="Velocitat de Lliurament", line=dict(color='blue', width=3)))
            fig_xp.add_trace(go.Scatter(x=df_xp['Setmana'], y=df_xp['Deute'], name="Deute Tècnic (%)", line=dict(color='red', dash='dash')))
            fig_xp.update_layout(xaxis_title="Setmanes", yaxis_title="Nivell", height=350)
            st.plotly_chart(fig_xp, use_container_width=True)

            if st.session_state.xp_deute > 40:
                st.warning("⚠️ **Deute Tècnic Elevat!** La manca de TDD o Refactoring fa que afegir noves funcions sigui cada vegada més lent i arriscat.")
            else:
                st.success("✨ **Codi Net!** Les pràctiques de qualitat mantenen la velocitat de l'equip sostinguda en el temps.")