import streamlit as st
import polars as pl
import altair as alt

# utility scripts
from data.preprocessing import *

def main():
    st.title("Una dieta sana migliora la vita?",
             help='Fonti: [OurWorldInData](https://ourworldindata.org/data/) e'
             ' [Gapminder](https://www.gapminder.org/data/).'
             ' Maggiori dettagli [in fondo](/#fonti).')
    "## Un'analisi sul consumo di verdura nel mondo"
    table1 = veg_vs_lifeexp()
    logscale = st.checkbox('Scala logaritmica',
                           help="Attiva/disattiva la trasformazione logaritmica sull'asse x")
    st.altair_chart(
        alt.Chart(table1.filter(pl.col('Year') == st.slider('Anno',1975,2016,2016,1))) # 1961,2021,2021,1)))
        .mark_circle()
        .encode(
            alt.X('Vegetables consumption').scale(type = 'log' if logscale else 'linear'),
            alt.Y('Life expectancy', scale=alt.Scale(domain=[None,90], clamp=True)),
            alt.Size('Population'),
            alt.Color('Obesity', scale=alt.Scale(domain=[0,70], range=['blue','red','darkred'], clamp=True)),
            alt.Tooltip(['Country/area','Vegetables consumption','Life expectancy','Obesity','Population'])
        )
        ,use_container_width=True
    )
    '''In questo grafico si cerca di valutare se il consumo di verdura abbia una qualche influenza 
    sull'aspettativa di vita.
    I dati riportano l'aspettativa di vita alla nascita in anni rispetto alla quantità annuale 
    di verdura consumata pro capite (in Kg, asse x) e alla percentuale di popolazione considerata 
    obesa (BMI>=30, colorazione dei punti). Inoltre la dimensione dei punti è proporzionata 
    al numero di abitanti del paese in considerazione.'''
    
    '''Il grafico, nonostante mostri una leggera tendenza dei punti a posizionarsi su una retta 
    (quando viene applicata la trasformata logaritmica all'asse delle x), dimostra 
    l'inadeguatezza delle variabili prese in considerazione per questa analisi.
    L'aspettativa di vita in particolare è influenzata da molti fattori, quali guerre e epidemie,
    molto più di quanto possa mai essere determinante una variazione nella dieta. Questo si può 
    notare in particolare osservando durante gli anni '70 l'outlier in basso, corrispondente alla 
    Cambogia durante il tragico periodo dei Khmer rossi (l'aspettativa di vita scende a 11/12 anni). 
    Inoltre la quantità di verdura consumata non considera il resto dell'alimentazione, e 
    l'obesità sembra correlata negativamente, al contrario di quello che si poteva ipotizzare 
    (un fattore nascosto legato sia all'aspettativa di vita che all'obesità potrebbe essere la 
    ricchezza del paese, misurato attraverso il PIL).'''
    
    "Tutto questo ci spinge ad analizzare i dati in modo diverso."
    
    "## Uno sguardo sulla dieta nel mondo"

    '''Se dall'analisi precedente non risulta molto sensata la correlazione tra obesità e aspettativa 
    di vita, dall'altra parte si nota molto chiaramente un aumento generale dell'obesità nel mondo 
    negli anni, soprattutto dagli anni '90 in poi.'''

    st.line_chart(obesity.filter(pl.col('Country/area').str.contains(r'\(WHO\)')),
                  x='Year', y='Obesity', color='Country/area')
    
    "Nello specifico dunque, __cos'è cambiato nell'alimentazione delle persone?__"
    "_Sono responsabili gli zuccheri? E i grassi?_"

    st.altair_chart(
        alt.Chart(diet2.filter(pl.col('Country/area') == 'World'))
        .mark_area()
        .encode(
            x=alt.X('Year'),
            y=alt.Y('Food available for consumption'),
            color=alt.Color('Food type')
        )
        .properties(title='Kilocalories per day per capita over time, world data'),
        use_container_width=True
    )

    '''Questo grafico contiene molte informazioni, ma tra tutti i valori quello più evidente è 
    l'aumento nel consumo di olii vegetali, il cambiamento in assoluto più visibile tra i dati 
    a livello mondiale.'''

    "## Conclusioni"

    '''Da questa piccola analisi si può sicuramente concludere poco, essendo stata svolta senza 
    nessun fine educativo ma solo come esercizio personale. Da qui però sarebbe sicuramente 
    interessante continuare l'analisi provando ad analizzare la relazione che ha il consumo di 
    olio vegetale in relazione con l'obesità, in paesi dove l'obesità è notoriamente un problema 
    come gli Stati Uniti o addirittura l'isola di 
    [Nauru](https://it.wikipedia.org/wiki/Obesit%C3%A0_a_Nauru). O ancora si potrebbe confrontare 
    la differenza tra la dieta occidentale e quella orientale, nello specifico per capire come 
    paesi come il Giappone non abbiano praticamente subito negli anni il problema della 
    crescente obesità, e dunque capire quali sono gli errori nella dieta che ci portano a 
    ingrassare.'''

    '''In questo piccolo progetto sono partito un po' a caso, _anche sbagliando_, ma ho voluto 
    tenere anche le prime considerazioni, probabilmente sbagliate, perché possano essere 
    in qualche modo d'insegnamento.'''

    "## Fonti"
    '''
    1. vegetable-consumption-per-capita, da [OurWorldInData](https://ourworldindata.org/data/) ([data](https://ourworldindata.org/grapher/vegetable-consumption-per-capita))
    2. life-expectancy-hmd-unwpp, da [OurWorldInData](https://ourworldindata.org/data/) ([data](https://ourworldindata.org/grapher/life-expectancy))
    3. pop (population data), da WORLD BANK via [Gapminder](https://www.gapminder.org/data/)
    4. share-of-adults-defined-as-obese, da [OurWorldInData](https://ourworldindata.org/data/ ([data](https://ourworldindata.org/grapher/share-of-adults-defined-as-obese))
    5. dietary-composition-by-country, da [OurWorldInData](https://ourworldindata.org/data/ ([data](https://ourworldindata.org/grapher/dietary-composition-by-country))
    '''


if __name__ == "__main__":
    main()
