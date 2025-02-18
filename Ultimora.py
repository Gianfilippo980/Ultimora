#userò un display da 20x4 caratteri per mostrare l'ultimore dal televideo
import serial
import feedparser
from time import sleep

i=0
vfd=serial.Serial("/dev/ttyAMA1", baudrate=38400)

def comando (istruzione):
    ordine=[istruzione]
    binario=bytes(ordine)
    vfd.write(binario)

def Trasmissione (righe):
    for i in range(len(righe)):
        vfd.write (righe[i].encode('cp437','replace'))
        if isinstance(righe, list):
            sleep(0.1)
            
def filtra_link(testo : str) -> str:
    #Rimuove i link dal testo, alle volte presenti nel sommario sotto la forma di <a href="...">...</a>
    if "<a" in testo:
        inizio = testo.find("<a")
        fine = testo.find(">", inizio)
        testo = testo[:inizio] + testo[fine + 1:]
        inizio = testo.find("</a>")
        testo = testo[:inizio] + testo[inizio + 4:]
    return testo

while True:
    comando (12)
    ultimora=feedparser.parse('http://www.servizitelevideo.rai.it/televideo/pub/rss101.xml')
    j=0 
    if len(ultimora.entries)==0 :
        notizia="Errore di Rete"
    else:
        lancio = ultimora.entries[i].description.replace('\n', ' ')
        notizia = filtra_link(lancio)
    righe=[]
    while j < len (notizia):
        testo=notizia[j:j+20]
        j+=20
        l=len(testo)
        if l<20:
            for k in range(20-l):
                #questo ciclo serve a mantenere consisitente la lunghezza delle videate: 20 caratteri
                testo+=" "
        righe.append(testo)
        if len(righe)>4:
            righe.pop(0)
            Trasmissione(righe)
            sleep(2)
        else:
            Trasmissione(righe[-1])
            sleep(2)
    sleep(2)
    