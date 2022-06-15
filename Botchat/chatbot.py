import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


#Creating tkinter GUI

from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk

class Chatbot:

    def __init__(self,root):
        self.root=root
        self.root.title("Ruang Pintar")
        self.root.geometry("730x620+0+0")
        self.root.bind('<Return>',self.enter_func)

        main_frame=Frame(self.root,bd=4,bg='powder blue',width=610)
        main_frame.pack()

        img_chat=Image.open('chat.jpg')
        img_chat=img_chat.resize((200,70),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img_chat)

        Title_label=Label(main_frame,bd=3,relief=RAISED,anchor='nw',width=730,compound=LEFT,image=self.photoimg,text='RUANG PINTAR',font=('Algerian',35,'bold'),fg='Deep Sky Blue',bg='white')
        Title_label.pack(side=TOP)
        
        self.scroll_y=ttk.Scrollbar(main_frame,orient=VERTICAL)
        self.text=Text(main_frame,width=65,height=20,bd=3,relief=RAISED,font=('arial',14),yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side=RIGHT,fill=Y)
        self.text.pack()


        btn_frame=Frame(self.root,bd=4,bg='white',width=730)
        btn_frame.pack()

        label_1=Label(btn_frame,text="Tuliskan Sesuatu",font=('arial',14,'bold'),fg='black',bg='white')
        label_1.grid(row=0,column=0,padx=5,sticky=W)

        self.entry=StringVar()
        self.entry1=ttk.Entry(btn_frame,textvariable=self.entry,width=40,font=('times new roman',16,'bold'))
        self.entry1.grid(row=0,column=1,padx=5,sticky=W)

        self.send=Button(btn_frame,text="Send>>",command=self.send,font=('arial',15,'bold'),width=8,bg='Deep Sky Blue',)
        self.send.grid(row=0,column=2,padx=5,sticky=W)

        self.clare=Button(btn_frame,text="Clear Data",command=self.clear,font=('arial',15,'bold'),width=8,bg='red',fg='white')
        self.clare.grid(row=1,column=0,padx=5,sticky=W)
        
        self.dan=''
        self.label_11=Label(btn_frame,text=self.dan,font=('arial',14,'bold'),fg='blue',bg='white')
        self.label_11.grid(row=1,column=1,padx=5,sticky=W)



    # =======================function Declaration=============================
    def enter_func(self,event):
        self.send.invoke()
        self.entry.set('')
       
    def clear(self):
        self.text.delete ('1.0',END)
        self.entry.set('')
    def send(self):
        self.msg = self.entry.get().strip()
        

       
        if self.msg != '':
           self.text.config(state=NORMAL)
           self.text.insert(END, "You: " + self.msg + '\n\n')
           self.text.config(foreground="#446665", font=("Verdana", 12 ))
     
           ints = predict_class(self.msg)
           res = getResponse(ints, intents)
        
           self.text.insert(END, "Bot: " + res + '\n\n')
            
           self.text.config(state=DISABLED)
           self.text.yview(END)
        
        if (self.entry.get()==''):
            self.dan='tolong isi sesuatu didalam'
            self.label_11.config(text=self.dan,fg='red')


       

if __name__ =='__main__':
    root=Tk()
    obj=Chatbot(root)
    root.mainloop()