# 🌐 Frontend Statico
Questo front-end è sviluppato in **HTML/CSS/JS** ed è completamente statico.  
Interagisce con il back-end tramite **fetch API** e viene servito tramite **Nginx**.
Non richiede Node.js, npm, React, Vue, framework vari: è leggero, portabile e facile da deployare.
E' possibile avviare le pagine anche in modalità *standalone*, ma alcune funzioni richiedono back-end e login quindi potrebbero non funzionare.
Ogni pagina usa infatti:
```js
fetch("http://localhost:8080/api/parcheggi")
fetch("http://localhost:8080/api/login", {...})
fetch("http://localhost:8080/api/simulazioni")
```
Le sessioni sono gestite tramite cookie nel back-end.