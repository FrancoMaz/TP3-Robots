# Backend-robots

---

### Instalar dependencias

```
pip3 install -r requirements.txt
``` 

---

### Levantar localmente el proyecto

``` 
python3 app.py
``` 

---
Una vez levantado el proyecto de python ya escucha requests 
entrantes, por lo que cuando la app Android realiza el request 
con la imagen va a realizar todo el proceso para devolver el link 
y la imagen del resultado más similar.

Los pasos que ejecuta el backend internamente son:
1) Guarda la imagen que se envía desde Android en la carpeta images/uploads.
2) Con dicha imagen se ejecuta el script de Yolo dos veces. Primero lo ejecuta con el archivo de pesos de los materiales de los mates. La imagen resultante con los labels detectados se almacena en yolo/runs/detect/exp. Si esta red no detectó ningún mate, se corre nuevamente yolo con el archivo de pesos de coco128, y la imagen con los labels resultante se almacena en yolo/runs/detect/exp2.
3) Si Yolo no detectó ningún objeto con ninguna de las dos corridas, entonces devuelve 404 y se finaliza la ejecución.
4) Si, en cambio, alguna de las dos redes arrojó resultados, entonces se procede a hacer un request a la api de MercadoLibre, donde el query de búsqueda es el label de Yolo traducido.
5) De los primeros 20 resultados devueltos por dicha API, se almacenan las imagenes en images/results. Si no hubo resultados, se devuelve 404 a la app de Android.
6) Luego, se procede a ejecutar la red de similitudes entre imagenes, donde la master image es la imagen almacenada en images/uploads, y las imagenes a comparar son las que se encuentran en images/results. Los vectores que se utilizan para comparar se almacenan en feature-vectors, y las similitudes con sus respectivos puntajes se escriben en nearest_neighbors.json.
7) Luego de este procesamiento, se devuelve la imagen y el link del resultado más similar a la app de Android
    
