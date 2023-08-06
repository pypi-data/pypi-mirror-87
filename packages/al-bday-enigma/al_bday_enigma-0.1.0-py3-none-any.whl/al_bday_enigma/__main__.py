import fastapi as f
import random
import typing
import uvicorn

app = f.FastAPI(description="""
Questa è la documentazione di malbyx.gift.steffo.eu, che ti spiegherà come fare a ottenere il regalo.

Il sito è composto da [una singola pagina `/`](https://malbyx.gift.steffo.eu/), che esegue una piccola funzione ogni 
volta che viene aperta e restituisce una **risposta in 
[JSON](https://it.wikipedia.org/wiki/JavaScript_Object_Notation)**.

Il riquadro qui sotto contiene informazioni sul funzionamento della pagina `/`: cliccalo per espanderlo e leggere le 
informazioni contenute al suo interno.
""")


def generator():
    random.seed(12345)
    total = 1
    for seq in range(500):
        number = random.randint(1, 1000000)

        if seq == 0:
            response = {
                "ok": False,
                "help": "Hehe, non ti sembrava un po' troppo facile? Adesso, somma a 1 il numero contenuto nel campo "
                        "`number`.",
                "number": number,
                "remaining": 499 - seq,
            }

        elif seq == 499:
            response = {
                "ok": True,
                "help": "Ce l'hai fatta! Manda questa `password` a Steffo per ricevere il tuo regalino!",
                "teaser": "E chissà, magari quando avrai il computer nuovo potrebbe arrivare un regalo un po' più "
                          "grande... :)",
                "password": "TOWNSCAPER",
                "remaining": 0,
            }

        else:
            response = {
                "ok": False,
                "help": "Bravo! Ora continua a sommare `number` al tuo numero, e invia la tua nuova soluzione.",
                "number": number,
                "remaining": 499 - seq,
            }

        yield total, response
        total += number


responses = {number: response for number, response in iter(generator())}


@app.get("/", summary="Risolvi il problema per ricevere il tuo regalo!", tags=["Pagine"])
def gift(
       solution: typing.Optional[int] = f.Query(None, description="Inserisci qui la soluzione del problema."),
):
    """
    Se io ho due coppette di gelato, e me ne mangio una, quante coppette di gelato mi rimangono?

    -----

    Questa pagina dà risposte diverse in base al parametro `solution` che gli viene passato.

    Per passargli `solution`, basta aggiungere `?solution=` alla fine dell'url, seguito dal valore desiderato del
    parametro.

    > ```
    > https://malbyx.gift.steffo.eu/?solution=1234
    > ```

    È programmata in modo per resitituire una **password** qualora la soluzione inserita fosse giusta e un **errore**
    qualora la soluzione inserita fosse errata.

    -----

    Essendo una pagina di solo testo, [automatizzare l'invio e la ricezione di risposte è facile e veloce](
    https://requests.readthedocs.io/en/master/). _Potresti provare..._

    """

    if solution is None:
        return {
            "ok": False,
            "welcome": "Benvenuto a malbyx.gift.steffo.eu!",
            "info": "Visita https://malbyx.gift.steffo.eu/docs per capire come funziona questo sito.",
            "help": "Se io ho 2 pandori, e ne mangio 1, quanti pandori mi rimangono da mangiare?",
            "remaining": 500,
        }

    try:
        return responses[solution]
    except KeyError:
        return {
            "ok": False,
            "help": "La soluzione inviata non è valida.",
        }


if __name__ == "__main__":
    uvicorn.run(app, port=30013)
