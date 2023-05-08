# Prospettiva e geometria proiettiva
La geometria proiettiva è un'estensione della geometria euclidea.
Mentre la geometria euclidea studia la forma degli oggetti planari e solidi che rimangono immutate da traslazioni, rotazioni e riflessioni, la geometria proiettiva studia il modo in cui gli oggetti sono visti in prospettiva e rappresentati su un piano (schermo).
Un modello geometrico per lo studio della prospettiva (lineare) è quello che include l'occhio (o centro di proiezione), il piano immagine (schermo) e l'oggetto da osservare.
I punti proiettati sul piano vengono trovati tracciando una retta dall'occhio ad un punto sull'oggetto e calcolando l'intersezione con il piano.
Possiamo rappresentare questo modello nello spazio \(\mathbb{E}^{3}\), chiamando gli assi \(X, Y\) e \(U\). Poniamo il centro di proiezione all'origine \(O\). Il piano immagine sarà il piano affine di equazione \(U = 1\). Prendiamo \(P\) come punto sull'oggetto osservato e chiamiamo \(P'\) il punto proiettato.
Tutti i punti nello spazio, eccetto quelli appartenenti al piano \(U = 0\), hanno un unico corrispondente sul piano affine che funge da schermo.
Questi saranno i punti "propri" del nostro piano proiettivo.
Ogni retta passante per O e giacente sul piano \(U=0\) individuerà una ed una sola direzione sul piano schermo. Tali direzioni saranno i punti "impropri" del nostro piano proeittivo e costituiscono la chiusura proiettiva del piano immagine.

<img src="img/chiusura_proiettiva.jpg" width="300" >

I punti impropri costituisco una sola retta (detta "impropria") del piano proiettivo. Ogni suo punto individua una direzione nel piano affine di cui il piano proiettivo è chiusura.

I punti propri, ovvero quelli con coordinata \(U \not = 0\) possono essere individuati con le loro coordinate proiettive, con la seguente notazione: \((X:Y:U)\).

Le coordinate affini \((x,y)\) di \(P'\) si determinano con le seguenti formule:

$$
  \begin{cases}
    \begin{aligned}
      x &= \frac{X}{U} \\
      y &= \frac{Y}{U}
    \end{aligned},\quad U\neq 0
  \end{cases}
$$

Dato che punti sulla stessa retta individuano lo stesso punto proiettato, coordinate proiettive uguali a meno di un fattore di proporzionalità indicano lo stesso punto \(P'\).
                                
$$
    (X:Y:U) \equiv \rho (X:Y:U) \quad con \quad \rho \in \mathbb{R}
$$

L'estensione della geometria proiettiva rispetto alla geometria affine del piano è costituita dai punti impropri sopra definiti.
Tali punti, che hanno la terza coordinata nulla, consentono di rappresentare sullo schermo quei punti dove rette parallele nello spazio vengono viste incidenti (si pensi ad es. all'immagine di due rotaie).


# Chiusura proiettiva su disco
Per visualizzare questi punti impropri (o punti ideali) possiamo immaginare una corrispondenza tra il piano proiettivo e l'interno di un disco circolare.
In questo modo i punti ideali si troveranno sul bordo del disco, disposti in modo tale che punti agli antipodi individueranno lo stesso punto ideale.

Per mappare i punti propri del nostro piano proiettivo \(\pi\) (escludendo quindi i punti con coodinata \(U = 0\)), nello spazio interno al disco, faremo le seguenti operazioni per ciascun punto \(P \in \mathbb{E}^{2}\):
- Proiettare \(P\) su una semisfera di raggio unitario, trovando \(P'\)
- Proiettare \(P'\) sul piano passante per il centro della semisfera e parallelo a \(\pi\), trovando \(P''\)

<img src="img/proiezione_semisfera.jpg" width="300" >

Usando la trigonometria è possibile ricavare direttamente le coordinate \((x'',y'')\) di \(P''\) a partire dalle coordinate \((x,y)\) di \(P\), nel seguente modo:

$$
  \begin{cases}
    \begin{aligned}
      x'' &= \sin \arctan x \\
      y'' &= \sin \arctan y
    \end{aligned}
  \end{cases}
$$

Dove la formula per \(x\) è stata ricavata dalle seguenti osservazioni:

<img src="img/sezione_proiezione_semisfera.jpg" width="300" >


# Curve cubiche

Le curve cubiche che consideriamo in questo progetto sono curve algebriche piane affini di grado tre, e hanno la forma:

$$
Ax^3 + Bx^2y + Cxy^2 + Dy^3 + Ex^2 + Fxy + Gy^2 + Hx + Iy + J = 0
$$

Tali curve possono essere spezzate in componenti aventi grado minore: due per le coniche ed uno per le rette.
Qui non prenderemo in considerazione le cubiche spezzate, limitandoci alle altre, dette irriducibili.
Per ciascuna di tali curve, nell'applicativo, andremo a tracciare un grafico qualitativo nel piano affine e poi la sua immagine corrispondente nel modello proiettivo del disco introdotto sopra.

## Classificazione affine
Sono presenti diverse possibili classificazioni di queste curve, ciascuna prende in considerazione gli invarianti rispetto a diverse trasformazioni. La classificazione che andremo a considerare è quella affine, ovvero quella che raggruppa le curve uguali a meno di una trasformazione affine nel piano.
Si intende il piano affine di cui consideriamo la chiusura  proiettiva come detto prima.
Secondo questa classificazione sono presenti le seguenti curve non riducibili:

- $x^3 + xy^2 + x^2 + Hx + Iy + J = 0 \\ -∞ < H < ∞,\qquad 0 \leq I < ∞,\qquad -∞ < J < ∞$
- $x^3 + xy^2 + y + Hx + J = 0 \\ -∞ < H < ∞,\qquad -∞ < J < ∞$
- $x^3 + xy^2 + x + J = 0 \\ 0 \leq J < ∞$
- $x^3 + xy^2 + 1 = 0$
- $x^3 - xy^2 - x^2 + Hx + Iy + J = 0 \\ -∞ < H < ∞,\qquad -∞ < I \leq 0 ,\qquad -∞ < J < ∞$
- $x^3 - xy^2 + 1 = 0$
- $x^2y + y^2 - x + y + J = 0 \\ -∞ < J < ∞$
- $x^2y + y^2 + y + J = 0 \\ -∞ < J < ∞$
- $x^2y + y^2 - 1 = 0$
- $x^2y + y^2= 0$
- $x^2y - x + y + J = 0 \\ 0 \leq J < ∞$
- $x^2y - x = 0$
- $x^2y - x + 1 = 0$
- $x^2y + y + 1 = 0$
- $x^2y + 1= 0$
- $x^3 - y^2 + x + J = 0\\ -∞ \lt J \lt ∞$
- $x^3 - y^2 - x + J = 0\\ -∞ \lt J \lt ∞$
- $x^3 - y^2 + 1 = 0$
- $x^3 - y^2 = 0$
- $x^3 - y = 0$
- $x^3 - xy + 1 = 0$

> Weinberg, David A. "The topological classification of cubic curves." The Rocky Mountain Journal of Mathematics (1988): 655-664.


## Classificazione topologica
Un'altra classificazione interessante è quella topologica, ovvero quella che raggruppa le curve cubiche a meno di un omeomforismo del piano affine, pensato come spazio topologico \(\mathbb{R}^2\), dotato della topologia euclidea.
In matematica, e più precisamente in topologia, un omeomorfismo è una particolare funzione fra spazi topologici che modella l'idea intuitiva di "deformazione senza strappi".
Andremo a tracciare la chiusura proiettiva delle curve non riducibili distinte secondo questa classificazione nell'applicativo.
Le curve riducibili, topologicamente distinte disegnate qua sotto, corrisponderebbero a combinazioni di curve algebriche piane di primo e secondo grado e pertanto non sono di nostro interesse.

<img src="img/curve_riducibili.jpg" width="300" >

> Weinberg, David A. "The topological classification of cubic curves." The Rocky Mountain Journal of Mathematics (1988): 665-679.