import tkinter as tk
from tkinter import messagebox
import re
import csv
class CNPInvalidError(Exception):
    def __init__(self, message="CNP-ul trebuie să aiba exact 13 cifre."):
        self.message=message
        super().__init__(self.message)

class NumeInvalidError(Exception):
    def __init__(self, message="Caractere interzise in nume si prenume!Numele si prenumele trebuie sa contina doar litere,spatiu/cratima intre prenume."):
        self.message=message
        super().__init__(self.message)
def majuscula(cuv):
    return cuv.capitalize()
def validare_nume(nume_prenume):
    if not re.match(r'^[a-zA-Z\-]+$',nume_prenume):
        raise NumeInvalidError()
    return True
def validare_cnp(CNP):
    if not re.match(r'^\d{13}$',CNP):
        raise CNPInvalidError()
    v_ultima_cifra=[2,7,9,1,4,6,3,5,8,2,7,9]
    s=sum(int(CNP[i]) * v_ultima_cifra[i] for i in range(len(v_ultima_cifra)))
    x=s%11
    if x == 10:
        x=1
    else:
        x=x
    return x == int(CNP[-1])

def validare_elemente(nume_prenume_cnp):
    match_cnp=re.search(r'\b\d{13}\b',nume_prenume_cnp)
    if not match_cnp:
        raise CNPInvalidError()
    CNP=match_cnp.group(0).strip()
    nume_prenume_part=nume_prenume_cnp[:match_cnp.start()].strip()
    parts=re.split(r'\s|-', nume_prenume_part)
    if len(parts)<2:
        raise NumeInvalidError()
    nume=majuscula(parts[0])
    prenume1=majuscula(parts[1])
    prenume2=majuscula(parts[2]) if len(parts)>2 else ""
    if not validare_nume(nume) or not validare_nume(prenume1) or (prenume2 and not validare_nume(prenume2)):
        raise NumeInvalidError()
    if not validare_cnp(CNP):
        return None
    return {'nume': nume, 'prenume1': prenume1, 'prenume2': prenume2, 'CNP': CNP}

def salvare_in_fisier(lista_cursanti,tip_fisier='csv'):
    if tip_fisier == 'csv':
        filename = 'cursanti.csv'
        with open(filename, mode='wt', newline='', encoding='utf-8') as fisier:
            fieldnames=['nume','prenume1','prenume2','CNP']
            writer=csv.DictWriter(fisier,fieldnames=fieldnames)
            writer.writeheader()
            for cursant in lista_cursanti:
                writer.writerow(cursant)
    elif tip_fisier == 'txt':
        filename='cursanti.txt'
        with open(filename,mode='wt',encoding='utf-8') as fisier:
            for cursant in lista_cursanti:
                fisier.write(f"Nume: {cursant['nume']}, Prenume1: {cursant['prenume1']},"f" Prenume2: {cursant['prenume2']}, CNP: {cursant['CNP']}\n")
    else:
        print("Tipul fisierului introdus nu este valid.")
        return
    print(f"Datele au fost salvate în '{filename}'")

def adauga_cursant():
    nume_prenume_cnp=entry_cursant.get().strip()
    try:
        date_valide=validare_elemente(nume_prenume_cnp)
        if date_valide:
            lista_cursanti.append(date_valide)
            messagebox.showinfo("Succes!","Datele sunt valide si au fost adaugate in lista.")
    except (CNPInvalidError, NumeInvalidError) as e:
        messagebox.showerror("Eroare", str(e))
def salvare_date():
    if lista_cursanti:
        salvare_in_fisier(lista_cursanti)
    else:
        messagebox.showwarning("Nu exista date de salvat.")
root=tk.Tk()
root.title("Gestionarea si validarea datelor despre cursanti")
root.configure(bg="#F1A6F4")

frame_cursant=tk.Frame(root,padx=10,pady=10,bg="#F1A6F4")
frame_cursant.pack(padx=10,pady=10)

label_introducere=tk.Label(frame_cursant,text="Introduceți datele: ",bg="#F1A6F4",fg="black")
label_introducere.grid(row=0,column=0,padx=5,pady=5)

entry_cursant=tk.Entry(frame_cursant,width=50)
entry_cursant.grid(row=0,column=1,padx=5,pady=5)

btn_adauga=tk.Button(frame_cursant,text="Adauga",command=adauga_cursant,bg="#A8CFF1",fg="black")
btn_adauga.grid(row=1, column=0, columnspan=2, pady=10)

frame_actiuni=tk.Frame(root, padx=10, pady=10, bg="#F1A6F4")
frame_actiuni.pack(padx=10, pady=10)

btn_salveaza=tk.Button(frame_actiuni, text="Salveaza", command=salvare_date, bg="green", fg="black")
btn_salveaza.grid(row=0, column=0, padx=0, pady=0, sticky="ew")#ew ca sa ocupe spatiul pe oriz

btn_iesire=tk.Button(frame_actiuni, text="Iesire", command=root.quit, bg="red", fg="black")
btn_iesire.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

lista_cursanti=[]

root.mainloop()
