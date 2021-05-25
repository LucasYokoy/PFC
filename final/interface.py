from tkinter import *
import nlp_pipeline as nlp

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

GREETING_MESSAGE = "Olá, sou o robô de perguntas e respostas. Em que posso ajudar?"
BOT_NAME = "BOT"

class ChatApplication:
    
    def __init__(self):
        self.dataset, self.pipeline = nlp.initialize_pipeline()
        self.window = Tk()
        self.answers = None
        self.chat_state = 'waiting_question'
        self._setup_main_window()
        
    def run(self):
        self._greeting_message()
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)    
    
    def _insert_user_message(self, msg):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f"Você: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
    def _insert_bot_message(self, msg):
        if not msg:
            return
        msg2 = f"{BOT_NAME}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)

    def _fetch_next_answer(self):
        try:
            answer = next(self.answers)
            self._insert_bot_message(answer)
            # the bot then asks if the user is happy with the given answer
            self._insert_bot_message("A resposta foi satisfatória?")
            # the state then changes to browsing answers
            self.chat_state = 'browsing_answers'
        except StopIteration:
        # if you run out of answers
            # display "desculpe, não consegui encontrar a resposta :\"
            self._insert_bot_message("Desculpe, não consegui encontrar a resposta :/")
            # display "Em que posso ajudar?"
            self._insert_bot_message("Em que posso ajudar?")
            # state changes to waiting question
            self.chat_state = 'waiting_question'
    
    def _chat_state_machine(self, msg):
        # defines what kind of answer is provided
        # 2 states: waiting question; browsing answers;
        # initial state: waiting question
        # waiting question:
        if self.chat_state == 'waiting_question':
            # the message must be passed on to the nlp_pipeline (which will return a generator of sorted answers)
            self.answers = self.pipeline(msg)
            self._fetch_next_answer()
        # browsing answers:
        elif self.chat_state == 'browsing_answers':
            # the only possible answers are yes or no, evaluating how useful the answer was
            if msg.lower() not in ['não','sim']:
                # if this is violated, display "não entendi"
                self._insert_bot_message("Não entendi.")
            # if the answer is 'yes', state changes to waiting question
            elif msg.lower() == 'sim':
                self._insert_bot_message("Obrigado! Posso ajudar em algo mais?")
                self.chat_state = 'waiting_question'
            # the only possibility left, is if the answer is 'no'
            else:
                # then the next answer is displayed
                self._fetch_next_answer()
                
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if msg:
            self._insert_user_message(msg)
            self._chat_state_machine(msg)
    
    def _greeting_message(self):
        msg = f"{BOT_NAME}: {GREETING_MESSAGE}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()