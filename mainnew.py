
import getpass
import pwinput
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
import os
import tkinter as tk
from tkinter import messagebox, simpledialog



#---------------------AREA DI DEFINIZIOEN METODI PER LE PASSWORD E VARIABILI--------------------------

HEADER = b"CRYPT:"
verde = "\033[32m"
giallo = "\033[33m"
reset = reset = "\033[0m"
global root

def carica_credenziali(percorso="CredenzialiNew.txt"):
    credenziali = {}
    with open(percorso, "r", encoding="utf-8-sig") as f:
        for line in f:
            if ":" in line:
                line = line.strip()  # Rimuove eventuali spazi extra e ritorni a capo
                nome, password = line.split(":", 1)
                credenziali[nome] = password
    return credenziali

#========== GENERAZIONE E LETTURA CHIAVE + FUNZIONI CHIAVE ==========
def genera_chiave():
    if not os.path.exists("chiave.key"):
        with open("chiave.key", "wb") as key_file:
            key_file.write(Fernet.generate_key())
        print("[+] Chiave generata.")
    else:
        print("[✓] Chiave già esistente.")

def carica_chiave():
    with open("chiave.key", "rb") as key_file:
        return key_file.read()
    
    # ========== CIFRA E DECIFRA FILE ==========

def cifra_file(nome_file):
    try:
        with open(nome_file, "rb") as file:
            contenuto = file.read()

        f = Fernet(carica_chiave())
        contenuto_cifrato = f.encrypt(contenuto)

        with open(nome_file, "wb") as file:
            file.write(contenuto_cifrato)

        print(f"[✓] {nome_file} cifrato.")
    except Exception as e:
        print(f"[x] Errore durante la cifratura di {nome_file}: {e}")

def decifra_file(nome_file):
    try:
        with open(nome_file, "rb") as file:
            contenuto = file.read()

        f = Fernet(carica_chiave())
        contenuto_decifrato = f.decrypt(contenuto)

        with open(nome_file, "wb") as file:
            file.write(contenuto_decifrato)

        print(f"[✓] {nome_file} decifrato.")
    except InvalidToken:
        print(f"[!] {nome_file} è già in chiaro o token non valido.")
    except Exception as e:
        print(f"[x] Errore durante la decifratura di {nome_file}: {e}")

#----------INIZIO GESTIONE NOME E PASSWORD, CON ANCHE GUI

'''sostituisco login con login_gui, già avevo sostituito gestione nome e gestione password con login che non mi utentica se non sono
entrambe verificate, poi da login a login_gui per non fare tutto da terminale'''

def login_gui():
    def verifica_login():
        nome = entry_nome.get()
        password = entry_password.get()
        credenziali = carica_credenziali()

        if nome in credenziali and password.strip() == credenziali[nome].strip():
            messagebox.showinfo("Accesso", f"Bentornato {nome}!")
            root.destroy()  # Chiudi finestra login
            menu_principale_gui()  # Apri il menu principale
        else:
            messagebox.showerror("Errore", "Credenziali errate")

    root = tk.Tk()
    root.title("Login Gestore Password")

    tk.Label(root, text="Nome utente:").pack()
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    tk.Label(root, text="Password:").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Accedi", command=verifica_login).pack()

    root.mainloop()

def menu_principale_gui():
    def inserisci_password():
        InserisciNewPassw()  # riuso della nostra funzione

    def visualizza_password():
        ViewAllPassw()

    def elimina_password():
        DeleteAPassw()

    def esci():
        cifra_file("CredenzialiNew.txt")
        cifra_file("psswGestorePssNew.txt")
        messagebox.showinfo("Uscita", "File criptati. Il programma verrà chiuso.")
        import sys
        sys.exit()  # Questo chiude completamente il programma

    app = tk.Tk()
    app.title("Gestore Password")

    tk.Button(app, text="Inserisci Nuova Password", command=inserisci_password).pack(pady=5)
    tk.Button(app, text="Visualizza Password", command=visualizza_password).pack(pady=5)
    tk.Button(app, text="Elimina Password", command=elimina_password).pack(pady=5)
    tk.Button(app, text="Esci e Cripta", command=esci).pack(pady=5)

    app.mainloop()


#---------------FUNZIONE CHE MI PERMETTE DI INSERIRE UNA NUOVA PASSOWRD, NEL FILE DEDICATO

def InserisciNewPassw():
    password = simpledialog.askstring("Inserisci Password", "Nuova password:", show='*')
    if password and not password.isspace():
        with open("psswGestorePssNew.txt", "a") as file:
            file.write(password.strip() + "\n")
        messagebox.showinfo("Successo", "Password aggiunta!")
    else:
        messagebox.showwarning("Errore", "Password non valida!")

def ViewAllPassw():
    try:
        with open("psswGestorePssNew.txt", "r") as f:
            contenuto = f.read()
        messagebox.showinfo("Le tue password", contenuto if contenuto else "Nessuna password trovata.")
    except FileNotFoundError:
        messagebox.showwarning("Errore", "File delle password non trovato.")

def DeleteAPassw():
    with open("psswGestorePssNew.txt", "r") as f:
        righe = [line.strip() for line in f]
    scelta = simpledialog.askstring("Elimina Password", "Quale password vuoi eliminare?\n" + "\n".join(righe))
    if scelta in righe:
        righe.remove(scelta)
        with open("psswGestorePssNew.txt", "w") as f:
            for riga in righe:
                f.write(riga + "\n")
        messagebox.showinfo("Successo", "Password eliminata!")
    else:
        messagebox.showwarning("Errore", "Password non trovata.")

def logout():
    cifra_file("psswGestorePssNew.txt")
    cifra_file("psswGestorePssNew.txt")
    root.destroy()


#--------------------------------------------------------------------
#MAIN

genera_chiave()  # Una sola volta per generare la chiave
decifra_file("CredenzialiNew.txt")
decifra_file("PsswGestorePssNew.txt")

login_gui()

print("1.per inserire una nuova password. \n" \
"2. per visualizzare le tue password. \n" \
"3. per eliminare una password esistente. \n" \
"4. per uscire senza effettuare operazioni \n ")
scelta = input("Quale Operazione Vuoi Svolgere?: ")
#scelta = int(scelta)    #altrimenti mi crea problemi di incompatib tra string e interi
while True:
    if scelta.isdigit():
        scelta = int(scelta)
        break
    else:
        print("Valore non valido. Inserisci un numero intero.\n")

while scelta < 5 :
    match scelta:
        case 1:
            print("Vuoi inserire una nuova password.")
            InserisciNewPassw()

        case 2:
            print("Vuoi visualizzare le tue password, eccole.")
            ViewAllPassw()

        case 3:
            print("Vuoi eliminare una password esistente.")
            DeleteAPassw()

        case 4:
            cifra_file("CredenzialiNew.txt")
            cifra_file("psswGestorePssNew.txt")
            print("Uscita dal programma in corso...\n")
            quit()
      
    print("1.per inserire una nuova password. \n" \
    "2. per visualizzare le tue password. \n" \
    "3. per eliminare una password esistente. \n" \
    "4. per uscire senza effettuare operazioni \n ")
    scelta = input("Quale Operazione Vuoi Svolgere?: ")
    scelta = int(scelta)

quit()
#Daniele Di Sarno