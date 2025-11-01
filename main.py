import tkinter as tk
from tkinter import messagebox
import random
import time
import math


class AuroraGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Luzes de Aurora")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0a0a1e')

        self.karma = 0
        self.score = 0
        self.phase = 1
        self.path = 1
        self.choices = []
        self.minigame_active = False
        self.current_minigame_score = 0
        self.target_score = 0
        self.anim_offset = 0

        self.setup_ui()
        self.animate_bg()
        self.show_start_screen()
        self.root.bind('<Escape>', lambda e: self.quit_game())
        self.root.mainloop()

    def setup_ui(self):
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0, bg='#0a0a1e')
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tk.Frame(self.root, bg='')
        self.main_frame.place(x=50, y=30, relwidth=1, relheight=1, width=-100, height=-60)

        self.hud_frame = tk.Frame(self.main_frame, bg='#16213e')
        self.hud_frame.pack(fill='x', pady=(0, 10))

        self.karma_label = tk.Label(self.hud_frame, text=f"Karma: {self.karma}",
                                    font=('Arial', 12), bg='#16213e', fg='white')
        self.karma_label.pack(side='left', padx=10)

        self.phase_label = tk.Label(self.hud_frame, text=f"Fase: {self.phase}/3",
                                    font=('Arial', 12), bg='#16213e', fg='white')
        self.phase_label.pack(side='left', padx=10)

        self.score_label = tk.Label(self.hud_frame, text=f"Score: {self.score}",
                                    font=('Arial', 12), bg='#16213e', fg='white')
        self.score_label.pack(side='right', padx=10)

        self.content_frame = tk.Frame(self.main_frame, bg='#0f3460')
        self.content_frame.pack(fill='both', expand=True)

        # Canvas da personagem Aria em pixel art no canto inferior direito
        self.char_canvas = tk.Canvas(self.content_frame, width=160, height=210, bg='#0f3460', highlightthickness=0)
        self.char_canvas.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

    def animate_bg(self):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w < 100:
                self.root.after(50, self.animate_bg)
                return

            self.bg_canvas.delete("all")
            self.anim_offset += 0.015

            for i in range(4):
                pts = []
                offset = self.anim_offset + i * 0.6
                color_val = (math.sin(offset + i) + 1) / 2
                r = int(20 + color_val * 80)
                g = int(40 + color_val * 120)
                b = int(140 - color_val * 40)
                color = f"#{r:02x}{g:02x}{b:02x}"

                for x in range(0, w + 40, 40):
                    y = h * (0.25 + i * 0.18) + math.sin(x / 80 + offset) * 60
                    pts.extend([x, y])

                if len(pts) >= 4:
                    pts.extend([w, h, 0, h])
                    self.bg_canvas.create_polygon(pts, fill=color, outline="", stipple="gray50")

            if random.random() > 0.8:
                self.bg_canvas.create_oval(random.randint(0, w), random.randint(0, int(h * 0.5)),
                                           random.randint(0, w) + 2, random.randint(0, int(h * 0.5)) + 2, fill='white',
                                           outline='')

            self.root.after(40, self.animate_bg)
        except:
            self.root.after(100, self.animate_bg)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            if widget != self.char_canvas:
                widget.destroy()

    def update_hud(self):
        self.karma_label.config(text=f"Karma: {self.karma}")
        self.phase_label.config(text=f"Fase: {self.phase}/3")
        self.score_label.config(text=f"Score: {self.score}")

    def show_start_screen(self):
        self.clear_content()
        tk.Label(self.content_frame, text="🌟 Luzes de Aurora 🌟",
                 font=('Arial', 36, 'bold'), bg='#0f3460', fg='#e94560').pack(pady=30)

        # Introdução detalhada
        intro_text = (
            "Você é Aria, uma jovem mensageira da vila de Kiri.\n\n"
            "Ultimamente, luzes misteriosas dançam no horizonte, sinais ancestrais que dizem respeito ao destino do mundo.\n"
            "Sua missão é seguir essas luzes, tomar decisões cruciais e proteger sua vila de perigos desconhecidos.\n"
            "Prepare-se para desvendar segredos antigos e enfrentar desafios que moldarão o futuro.\n\n"
            "No crepúsculo do mundo conhecido, quando as estrelas se alinham e o véu entre os mundos se afina,\n"
            "uma mensageira da vila de Kiri testemunha um fenômeno que mudará para sempre o destino de todos.\n\n"
            "As Luzes de Aurora não são meros fogos no céu - são portais para reinos esquecidos,\n"
            "mensagens de deuses antigos, e provas para aqueles que ousam desafiar o desconhecido.\n\n"
            "3 Fases × 3 Caminhos = 9 Destinos Únicos!\n\n"
            "Pressione ESC para sair • Suas escolhas ecoarão pela eternidade."
        )
        tk.Label(self.content_frame, text=intro_text, font=('Arial', 14), bg='#0f3460',
                 fg='white', wraplength=900, justify='center').pack(pady=20)

        tk.Button(self.content_frame, text="🚀 INICIAR JORNADA", font=('Arial', 18),
                  bg='#e94560', fg='white', command=self.start_phase1, width=20, height=2).pack(pady=20)
        self.draw_character(neutral=True)

    def start_phase1(self):
        self.phase = 1
        self.update_hud()
        self.show_phase_decision()

    def show_phase_decision(self):
        self.clear_content()
        phase_titles = {1: "🌌 FASE 1: O PRIMEIRO SINAL", 2: "📜 FASE 2: O PORTAL ANCESTRAL",
                        3: "⚡ FASE 3: O DESTINO FINAL"}
        tk.Label(self.content_frame, text=phase_titles[self.phase],
                 font=('Arial', 20, 'bold'), bg='#0f3460', fg='#e94560').pack(pady=20)
        descriptions = {
            1: "Três caminhos se abrem diante das luzes misteriosas. Cada escolha levará a uma jornada única...",
            2: "O portal ancestral revela múltiplas estratégias. Sua decisão moldará o destino de todos...",
            3: "O momento decisivo chegou! O universo aguarda sua escolha final..."}
        tk.Label(self.content_frame, text=descriptions[self.phase],
                 font=('Arial', 14), bg='#0f3460', fg='white', wraplength=1000).pack(pady=10)
        btn_frame = tk.Frame(self.content_frame, bg='#0f3460')
        btn_frame.pack(pady=20)

        if self.phase == 1:
            choices = [("🔍 CAMINHO DA CORAGEM\nInvestigar sozinho as luzes", lambda: self.choose_path(1)),
                       ("🏘️ CAMINHO DA COMUNIDADE\nAlertar o vilarejo", lambda: self.choose_path(2)),
                       ("📦 CAMINHO DO DEVER\nCumprir a missão original", lambda: self.choose_path(3))]
        elif self.phase == 2:
            choices = [("📚 CAMINHO DO CONHECIMENTO\nEstudar os pergaminhos antigos", lambda: self.choose_path(1)),
                       ("🛡️ CAMINHO DA PROTEÇÃO\nPreparar defesas para a vila", lambda: self.choose_path(2)),
                       ("🤝 CAMINHO DA ALIANÇA\nBuscar aliados entre tribos", lambda: self.choose_path(3))]
        else:
            choices = [("⚖️ CAMINHO DO EQUILÍBRIO\nUsar rituais de harmonia", lambda: self.choose_path(1)),
                       ("🚫 CAMINHO DA SEGURANÇA\nFechar o portal permanentemente", lambda: self.choose_path(2)),
                       ("💥 CAMINHO DA OUSADIA\nAbrir completamente o portal", lambda: self.choose_path(3))]

        for text, command in choices:
            tk.Button(btn_frame, text=text, font=('Arial', 12), bg='#1a1a2e', fg='white',
                      width=40, height=3, command=command).pack(pady=8)

        self.draw_character(neutral=True)

    def choose_path(self, path):
        self.path = path
        karma_values = {1: {1: 2, 2: 1, 3: 0}, 2: {1: 2, 2: 1, 3: 1}, 3: {1: 3, 2: 0, 3: -2}}
        self.karma += karma_values[self.phase][path]
        path_names = {1: {1: "Coragem Solitária", 2: "Sabedoria Coletiva", 3: "Dever Inquebrável"},
                      2: {1: "Conhecimento Arcano", 2: "Fortificação Épica", 3: "Alianças Eternas"},
                      3: {1: "Equilíbrio Perfeito", 2: "Preservação Absoluta", 3: "Evolução Radical"}}
        self.choices.append(f"Fase {self.phase}: {path_names[self.phase][path]}")
        self.show_path_story()

    def show_path_story(self):
        self.clear_content()
        stories = {
            (1,
             1): "🌌 CAMINHO DA CORAGEM SOLITÁRIA 🌌\n\nVocê segue corajosamente as luzes na floresta escura. Após horas de caminhada sob árvores ancestrais, encontra um CÍRCULO DE PEDRAS pulsando com energia cósmica. No centro, um VIAJANTE TEMPORAL ferido revela a verdade chocante: você é a última descendente dos GUARDIÕES DAS AURORA!\n\nEle entrega um artefato ancestral que permite ver além do véu dimensional. Sua coragem é recompensada com conhecimento proibido sobre a verdadeira natureza das luzes.\n\n💫 Recompensa: +2 Karma e Visão Dimensional",
            (1,
             2): "🏘️ CAMINHO DA SABEDORIA COLETIVA 🏘️\n\nVocê alerta toda a vila, convocando uma reunião de emergência no Grande Salão. Inicialmente céticos, os anciões ficam pasmos quando as luzes intensificam-se exatamente como você predisse.\n\nO HISTORIADOR-CHEFE revela pergaminhos secretos: as Luzes ocorrem a cada 500 anos, sempre precedendo grandes mudanças cósmicas. A vila se une, combinando sabedoria ancestral com preparativos modernos.\n\n🤝 Recompensa: +1 Karma e União Comunitária",
            (1,
             3): "📦 CAMINHO DO DEVER INQUEBRÁVEL 📦\n\nSua disciplina é lendária. Enquanto outros se distraem com as luzes, você cumpre sua missão com precisão absoluta. Para seu espanto, a mensagem contém referências codificadas às Aurora!\n\nO destinatário revela-se um MEMBRO DA SOCIEDADE SECRETA DA AURORA, que aguardava este momento há gerações. Sua confiabilidade prova que é digna de segredos maiores.\n\n⚖️ Recompensa: +0 Karma e Confiança dos Líderes",
            (2,
             1): "📚 CAMINHO DO CONHECIMENTO ARCANO 📚\n\nVocê mergulha na BIBLIOTECA PROIBIDA, decifrando textos na LINGUAGEM ESTELAR dos construtores do portal. Sua descoberta é revolucionária: o portal é uma PONTE DE APRENDIZADO interestelar!\n\nAprende RITUAIS DE ESTABILIZAÇÃO que podem salvar o mundo e descobre como comunicar-se com as inteligências do outro lado. O conhecimento se torna sua maior arma.\n\n🎓 Recompensa: +2 Karma e Sabedoria Ancestral",
            (2,
             2): "🛡️ CAMINHO DA FORTIFICAÇÃO ÉPICA 🛡️\n\nVocê lidera a construção de MURALHAS DE ENERGIA que brilham com luz estelar. Cada cidadão contribui, criando a maior obra defensiva da história de Kiri.\n\nUsando técnicas dos CONSTRUTORES ANCESTRAIS, a vila se transforma em fortaleza imponente. Sua liderança prova que a vontade coletiva pode desafiar forças cósmicas.\n\n🏰 Recompensa: +1 Karma e Vila Impenetrável",
            (2,
             3): "🤝 CAMINHO DAS ALIANÇAS ETERNAS 🤝\n\nSua jornada diplomática une TRIBOS ESQUECIDAS. XAMANIS DAS MONTANHAS revelam profecias sobre sua chegada, enquanto ARQUEIROS DO VALE oferecem precisão lendária.\n\nUma ALIANÇA CÓSMICA nasce, combinando magias ancestrais com tecnologias perdidas. Pela primeira vez em milênios, todas as raças se unem sob uma bandeira.\n\n🌍 Recompensa: +1 Karma e Exército Multicultural",
            (3,
             1): "⚖️ CAMINHO DO EQUILÍBRIO PERFEITO ⚖️\n\nVocê realiza o RITUAL DA HARMONIA CÓSMICA, canalizando energias não usadas desde a criação do mundo. Seres de luz e sombra encontram paz sob sua mediação.\n\nO portal se estabiliza como UNIVERSIDADE INTERDIMENSIONAL, onde conhecimentos de mil mundos são compartilhados. Kiri torna-se farol cultural da galáxia.\n\n🌈 Recompensa: +3 Karma e Era Dourada",
            (3,
             2): "🚫 CAMINHO DA PRESERVAÇÃO ABSOLUTA 🚫\n\nUsando ARTEFATOS DO SELAMENTO ANCESTRAL, você realiza o fechamento permanente. A ameaça some, mas com ela oportunidades cósmicas infinitas.\n\nÀ noite, você sonha com MUNDOS PERDIDOS e ALIANÇAS que poderiam ter sido. A segurança tem preço, e você carrega esse peso.\n\n🔒 Recompensa: +0 Karma e Segurança Imediata",
            (3,
             3): "💥 CAMINHO DA EVOLUÇÃO RADICAL 💥\n\nVocê amplifica o portal além dos limites, desencadeando TORMENTA DE TRANSFORMAÇÃO. Alguns ganham poderes telepáticos, outros tornam-se seres de energia pura.\n\nA realidade é redefinida. O mundo nunca mais será o mesmo - para o bem e para o mal. Sua ousadia cria paraíso para alguns, inferno para outros.\n\n⚡ Consequência: -2 Karma e Mundo Transformado"
        }

        story_frame = tk.Frame(self.content_frame, bg='#0f3460')
        story_frame.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(story_frame, bg='#0f3460', highlightthickness=0)
        scrollbar = tk.Scrollbar(story_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#0f3460')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        title_colors = {1: '#27ae60', 2: '#3498db', 3: '#e67e22'}
        tk.Label(scrollable_frame, text=f"CAMINHO {self.path}",
                 font=('Arial', 18, 'bold'), bg='#0f3460', fg=title_colors[self.path]).pack(pady=10)
        tk.Label(scrollable_frame, text=stories[(self.phase, self.path)], font=('Arial', 11),
                 bg='#0f3460', fg='white', wraplength=900, justify='left').pack(pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        tk.Button(self.content_frame, text="🎮 INICIAR DESAFIO DA FASE", font=('Arial', 14, 'bold'),
                  bg='#e94560', fg='white', command=self.start_minigame, width=30, height=2).pack(pady=20)
        self.update_hud()
        self.draw_character()

    def draw_character(self, neutral=False):
        self.char_canvas.delete("all")

        # Cores melhoradas para a Aria
        skin_color = "#FFDBAC"  # Pele mais natural
        hair_color = "#8B4513"  # Castanho mais rico
        eye_color = "#2E8B57"  # Verde esmeralda
        cloak_color = "#4A235A"  # Roxo escuro elegante
        dress_color = "#6C3483"  # Roxo médio
        details_color = "#F7DC6F"  # Dourado para detalhes

        # Determinar expressão baseada nas escolhas
        if neutral:
            mouth_style = "neutral"
            eye_style = "neutral"
        else:
            if self.phase == 1:
                if self.path == 1:
                    mouth_style = "happy"
                    eye_style = "determined"
                elif self.path == 2:
                    mouth_style = "neutral"
                    eye_style = "wise"
                else:
                    mouth_style = "serious"
                    eye_style = "focused"
            elif self.phase == 2:
                if self.path == 1:
                    mouth_style = "happy"
                    eye_style = "curious"
                elif self.path == 2:
                    mouth_style = "determined"
                    eye_style = "strong"
                else:
                    mouth_style = "neutral"
                    eye_style = "diplomatic"
            else:
                if self.path == 1:
                    mouth_style = "happy"
                    eye_style = "peaceful"
                elif self.path == 2:
                    mouth_style = "neutral"
                    eye_style = "cautious"
                else:
                    mouth_style = "serious"
                    eye_style = "intense"

        # Desenhar a Aria - versão muito melhorada
        # Cabelo (longo e elegante)
        self.char_canvas.create_oval(45, 45, 115, 115, fill=hair_color, outline="")
        self.char_canvas.create_rectangle(50, 85, 110, 160, fill=hair_color, outline="")

        # Rosto
        self.char_canvas.create_oval(55, 60, 105, 100, fill=skin_color, outline="")

        # Olhos
        if eye_style == "determined":
            # Olhos determinados
            self.char_canvas.create_oval(65, 75, 75, 85, fill="white", outline="")
            self.char_canvas.create_oval(85, 75, 95, 85, fill="white", outline="")
            self.char_canvas.create_oval(69, 78, 73, 82, fill=eye_color, outline="")
            self.char_canvas.create_oval(89, 78, 93, 82, fill=eye_color, outline="")
            # Sobrancelhas determinadas
            self.char_canvas.create_line(63, 70, 73, 68, width=3, fill=hair_color)
            self.char_canvas.create_line(87, 68, 97, 70, width=3, fill=hair_color)
        elif eye_style == "wise":
            # Olhos sábios
            self.char_canvas.create_oval(65, 75, 75, 85, fill="white", outline="")
            self.char_canvas.create_oval(85, 75, 95, 85, fill="white", outline="")
            self.char_canvas.create_oval(70, 80, 74, 84, fill=eye_color, outline="")
            self.char_canvas.create_oval(90, 80, 94, 84, fill=eye_color, outline="")
            # Sobrancelhas suaves
            self.char_canvas.create_line(63, 72, 73, 70, width=2, fill=hair_color)
            self.char_canvas.create_line(87, 70, 97, 72, width=2, fill=hair_color)
        elif eye_style == "curious":
            # Olhos curiosos
            self.char_canvas.create_oval(65, 75, 75, 85, fill="white", outline="")
            self.char_canvas.create_oval(85, 75, 95, 85, fill="white", outline="")
            self.char_canvas.create_oval(68, 78, 72, 82, fill=eye_color, outline="")
            self.char_canvas.create_oval(88, 78, 92, 82, fill=eye_color, outline="")
            # Sobrancelhas arqueadas
            self.char_canvas.create_line(63, 68, 73, 65, width=2, fill=hair_color)
            self.char_canvas.create_line(87, 65, 97, 68, width=2, fill=hair_color)
        else:
            # Olhos neutros (padrão)
            self.char_canvas.create_oval(65, 75, 75, 85, fill="white", outline="")
            self.char_canvas.create_oval(85, 75, 95, 85, fill="white", outline="")
            self.char_canvas.create_oval(70, 79, 74, 83, fill=eye_color, outline="")
            self.char_canvas.create_oval(90, 79, 94, 83, fill=eye_color, outline="")
            # Sobrancelhas neutras
            self.char_canvas.create_line(63, 70, 73, 70, width=2, fill=hair_color)
            self.char_canvas.create_line(87, 70, 97, 70, width=2, fill=hair_color)

        # Boca
        if mouth_style == "happy":
            self.char_canvas.create_arc(70, 85, 90, 95, start=0, extent=-180, style='arc', width=2, outline="black")
        elif mouth_style == "determined":
            self.char_canvas.create_line(70, 90, 90, 90, width=2, fill="black")
        elif mouth_style == "serious":
            self.char_canvas.create_arc(70, 92, 90, 97, start=0, extent=180, style='arc', width=2, outline="black")
        else:  # neutral
            self.char_canvas.create_line(72, 90, 88, 90, width=2, fill="black")

        # Corpo e vestes
        self.char_canvas.create_rectangle(60, 100, 100, 160, fill=dress_color, outline="")

        # Capa/capa de mensageira
        self.char_canvas.create_arc(40, 90, 120, 200, start=0, extent=180, fill=cloak_color, outline="")

        # Detalhes dourados na roupa
        self.char_canvas.create_line(60, 110, 100, 110, fill=details_color, width=2)
        self.char_canvas.create_line(60, 125, 100, 125, fill=details_color, width=2)
        self.char_canvas.create_line(60, 140, 100, 140, fill=details_color, width=2)

        # Colar/amuleto
        self.char_canvas.create_oval(77, 105, 83, 111, fill=details_color, outline="")

        # Mãos
        self.char_canvas.create_oval(50, 130, 60, 140, fill=skin_color, outline="")
        self.char_canvas.create_oval(100, 130, 110, 140, fill=skin_color, outline="")

    def start_minigame(self):
        self.clear_content()
        difficulties = {
            1: {"time": 12, "target": 8,
                "fail_message": "FASE 1 FALHADA: Você não coletou recursos suficientes!\nAs luzes desaparecem e a oportunidade foi perdida."},
            2: {"time": 10, "target": 10,
                "fail_message": "FASE 2 FALHADA: O portal ficou instável!\nA energia cósmica consome a vila."},
            3: {"time": 10, "target": 10,
                "fail_message": "FASE 3 FALHADA: O equilíbrio foi rompido!\nO mundo sucumbe ao caos dimensional."}
        }
        config = difficulties[self.phase]
        game_time = config["time"]
        self.target_score = config["target"]
        self.fail_message = config["fail_message"]
        self.current_minigame_score = 0

        themes = {1: "Coletar Cristais de Energia Cósmica", 2: "Estabilizar o Portal Ancestral",
                  3: "Controlar as Energias Dimensionais"}
        tk.Label(self.content_frame, text=f"🎯 {themes[self.phase]}", font=('Arial', 20, 'bold'), bg='#0f3460',
                 fg='#e94560').pack(pady=10)
        tk.Label(self.content_frame, text=f"Meta: {self.target_score} pontos em {game_time} segundos",
                 font=('Arial', 14), bg='#0f3460', fg='white').pack(pady=5)
        self.time_label = tk.Label(self.content_frame, text=f"Tempo: {game_time}s", font=('Arial', 16), bg='#0f3460',
                                   fg='white')
        self.time_label.pack()
        self.minigame_score_label = tk.Label(self.content_frame, text=f"Pontuação: 0", font=('Arial', 16), bg='#0f3460',
                                             fg='white')
        self.minigame_score_label.pack()
        self.game_canvas = tk.Canvas(self.content_frame, width=800, height=400, bg='#1a1a2e')
        self.game_canvas.pack(pady=20)

        self.target_btn = tk.Button(self.game_canvas, text="🎯", font=('Arial', 16), bg='#e94560', fg='white',
                                    state='disabled')
        tk.Button(self.content_frame, text="INICIAR DESAFIO", font=('Arial', 14), bg='#e94560', fg='white',
                  command=lambda: self.run_minigame(game_time), width=20).pack(pady=10)

    def run_minigame(self, game_time):
        self.minigame_active = True
        self.current_minigame_score = 0
        self.end_time = time.time() + game_time
        self.minigame_score_label.config(text=f"Pontuação: 0")

        def update():
            if not self.minigame_active:
                return
            remaining = max(0, self.end_time - time.time())
            self.time_label.config(text=f"Tempo: {remaining:.1f}s")
            if remaining <= 0:
                self.end_minigame()
                return
            self.root.after(100, update)

        def spawn():
            if not self.minigame_active:
                return
            self.game_canvas.delete("target")
            x, y = random.randint(50, 750), random.randint(50, 350)
            self.target_btn.config(state='normal')
            self.target_btn.place_forget()
            self.target_btn.config(command=self.collect_point)
            self.game_canvas.create_window(x, y, window=self.target_btn, tags="target")
            self.root.after(random.randint(500, 1200), spawn)

        update()
        spawn()

    def collect_point(self):
        if self.minigame_active:
            self.current_minigame_score += 1
            self.score += 1
            self.minigame_score_label.config(text=f"Pontuação: {self.current_minigame_score}")
            self.game_canvas.delete("target")
            self.target_btn.config(state='disabled')

    def end_minigame(self):
        self.minigame_active = False
        self.game_canvas.delete("target")
        if self.current_minigame_score >= self.target_score:
            self.show_victory()
        else:
            self.show_defeat()

    def show_victory(self):
        self.clear_content()
        victory_messages = {
            1: "🎉 FASE 1 COMPLETADA!\nVocê dominou as energias iniciais!",
            2: "✨ FASE 2 SUPERADA!\nO portal está sob controle!",
            3: "🌟 FASE 3 CONCLUÍDA!\nVocê alcançou o ápice do poder!"
        }
        tk.Label(self.content_frame, text="✅ VITÓRIA!", font=('Arial', 24, 'bold'),
                 bg='#0f3460', fg='#27ae60').pack(pady=20)
        tk.Label(self.content_frame, text=victory_messages[self.phase], font=('Arial', 14),
                 bg='#0f3460', fg='white', wraplength=900).pack(pady=10)
        tk.Label(self.content_frame, text=f"Pontuação: {self.current_minigame_score}/{self.target_score}",
                 font=('Arial', 12, 'bold'), bg='#0f3460', fg='#27ae60').pack(pady=5)
        karma_bonus = {1: 1, 2: 2, 3: 3}
        self.karma += karma_bonus[self.phase]
        tk.Label(self.content_frame, text=f"+{karma_bonus[self.phase]} Karma!",
                 font=('Arial', 12), bg='#0f3460', fg='#f1c40f').pack(pady=5)
        self.update_hud()
        if self.phase < 3:
            tk.Button(self.content_frame, text=f"➡️ AVANÇAR PARA FASE {self.phase + 1}",
                      font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                      command=self.next_phase, width=30, height=2).pack(pady=20)
        else:
            tk.Button(self.content_frame, text="🏁 VER FINAL DA JORNADA", font=('Arial', 14, 'bold'),
                      bg='#e94560', fg='white', command=self.show_ending, width=25, height=2).pack(pady=20)

    def show_defeat(self):
        self.clear_content()
        tk.Label(self.content_frame, text="💀 DERROTA", font=('Arial', 24, 'bold'),
                 bg='#0f3460', fg='#e74c3c').pack(pady=20)
        tk.Label(self.content_frame, text=self.fail_message, font=('Arial', 14),
                 bg='#0f3460', fg='white', wraplength=900).pack(pady=10)
        tk.Label(self.content_frame, text=f"Pontuação: {self.current_minigame_score}/{self.target_score}",
                 font=('Arial', 12, 'bold'), bg='#0f3460', fg='#e74c3c').pack(pady=5)
        karma_penalty = {1: -1, 2: -2, 3: -3}
        self.karma += karma_penalty[self.phase]
        self.update_hud()
        tk.Button(self.content_frame, text="🔄 TENTAR NOVAMENTE", font=('Arial', 14),
                  bg='#e67e22', fg='white', command=self.retry_phase, width=25, height=2).pack(pady=10)
        tk.Button(self.content_frame, text="🚪 SAIR", font=('Arial', 12), bg='#34495e',
                  fg='white', command=self.quit_game, width=20, height=2).pack(pady=10)

    def next_phase(self):
        self.phase += 1
        self.update_hud()
        self.show_phase_decision()

    def retry_phase(self):
        self.show_phase_decision()

    def show_ending(self):
        self.clear_content()
        if self.karma >= 8:
            final_text = "🏆 FINAL LENDÁRIO\nSua jornada se tornou lenda eterna!"
            color = '#f1c40f'
        elif self.karma >= 5:
            final_text = "✨ FINAL HERÓICO\nSua liderança salvou o mundo!"
            color = '#27ae60'
        elif self.karma >= 2:
            final_text = "⚖️ FINAL DO EQUILÍBRIO\nSua sabedoria prevaleceu!"
            color = '#3498db'
        else:
            final_text = "💀 FINAL DA LIÇÃO\nO preço da ousadia foi alto..."
            color = '#e74c3c'

        tk.Label(self.content_frame, text="FIM DA JORNADA", font=('Arial', 24, 'bold'),
                 bg='#0f3460', fg=color).pack(pady=20)
        tk.Label(self.content_frame, text=final_text, font=('Arial', 14), bg='#0f3460',
                 fg='white', wraplength=900).pack(pady=15)
        choices_text = "\n".join(self.choices)
        tk.Label(self.content_frame, text="📜 SUA JORNADA:\n" + choices_text,
                 font=('Arial', 11), bg='#0f3460', fg='#cccccc').pack(pady=10)
        tk.Label(self.content_frame, text=f"⭐ Karma Final: {self.karma} | 🎯 Score Final: {self.score}",
                 font=('Arial', 14, 'bold'), bg='#0f3460', fg='white').pack(pady=10)
        btn_frame = tk.Frame(self.content_frame, bg='#0f3460')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="🔄 JOGAR NOVAMENTE", font=('Arial', 12), bg='#e94560',
                  fg='white', command=self.restart, width=18, height=2).pack(side='left', padx=10)
        tk.Button(btn_frame, text="🚪 SAIR", font=('Arial', 12), bg='#34495e', fg='white',
                  command=self.quit_game, width=18, height=2).pack(side='left', padx=10)

    def restart(self):
        self.karma = 0
        self.score = 0
        self.phase = 1
        self.path = 1
        self.choices = []
        self.update_hud()
        self.show_start_screen()

    def quit_game(self):
        if messagebox.askokcancel("Sair", "Deseja sair do jogo?"):
            self.root.destroy()


if __name__ == "__main__":
    AuroraGame()











