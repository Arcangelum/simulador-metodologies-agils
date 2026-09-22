Markdown
# 🎯 Simulador de Metodologies Àgils

Aquest repositori conté un simulador interactiu desenvolupat en Python amb **Streamlit** per a la segona sessió de l'assignatura de Metodologies Àgils. 

L'objectiu d'aquesta eina és experimentar la causa i l'efecte de les decisions de gestió en **Scrum, Kanban, Lean i XP**.

---

## 🚀 Com executar el simulador al teu ordinador

Segueix aquests passos per instal·lar i executar l'aplicació localment:

### 1. Clonar o baixar aquest repositori
Obre la terminal i executa:
```bash
git clone [https://github.com/Arcangelum/simulador-metodologies-agils.git](https://github.com/Arcangelum/simulador-metodologies-agils.git)
cd simulador-metodologies-agils
(Si no utilitzes Git, pots baixar el codi fent clic al botó verd Code > Download ZIP de GitHub i descomprimir-lo).

2. Instal·lar les dependències
Assegura't de tenir Python 3.8+ instal·lat i executa:

Bash
pip install -r requirements.txt
3. Executar l'aplicació
Executa la següent comanda a la terminal:

Bash
streamlit run app.py
S'obrirà automàticament una pestanya al teu navegador web (normalment a http://localhost:8501) amb la interfície del simulador.

🎮 Què trobaràs al simulador?
Scrum: Observa la relació entre la sobrecàrrega del Sprint (Sprint Overcommit) i el Burnout mitjançant un Burndown Chart.

Kanban: Ajusta el límit de treball en curs (WIP) i comprova com afecta el Lead Time i els colls d'ampolla en un Diagrama de Flux Acumulat (CFD).

Lean: Compara l'estratègia d'un MVP ràpid enfront del desenvolupament llarg sense validació per mesurar el temps inútil (Waste/Muda).

XP: Visualitza com la manca de TDD i Refactoring augmenta el Deute Tècnic i redueix la velocitat de desenvolupament a zero.