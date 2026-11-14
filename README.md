## Integrantes

- Julián Giraldo Chica - Julian-GC
- Joan Sebastian Herrera Montes - JoansebHM
- Juan José Henao Aristizábal (**Propietario**) - Juanjoseh99

## Evidencias
https://github.com/Juanjoseh99/entregable-2-cicd/pull/1
https://github.com/Juanjoseh99/entregable-2-cicd/actions/runs/43615847645

## Preguntas

### I. ¿Qué ventajas le proporciona a un proyecto el uso de un pipeline de CI? Menciona al menos tres ventajas específicas y explica por qué son importantes.

Detecta errores temprano. Cada push o PR ejecuta pruebas, Black y la cobertura (≥ 80 %). Si algo falla, el pipeline se detiene. Corregir un bug al momento de escribirlo es más barato que hacerlo en producción.

Calidad consistente. Linters, cobertura y el Quality Gate de SonarCloud se aplican igual a todos los cambios, sin depender de la memoria de cada persona.

main siempre estable. Con la rama protegida, solo entran PRs con el pipeline en verde. Así hay menos conflictos y el equipo puede trabajar en paralelo.

Artefacto reproducible. La imagen Docker se construye una vez, se prueba y se publica tal cual. Lo que se despliega es lo que se validó.

---

### II. ¿Cuál es la diferencia entre una prueba unitaria, una prueba de componente y una prueba de aceptación? Da un ejemplo de algo que probarías con cada una (en el contexto de cualquier aplicación que conozcas, descríbela primero).
 
Aplicación: calculadora web en Flask. Tiene un formulario con dos números y una operación, y muestra el resultado.
Unitaria: prueba una función aislada. Ejemplo: dividir(1, 0) lanza ZeroDivisionError.
De componente: prueba rutas, lógica y plantilla juntas con el cliente de pruebas de Flask, sin servidor ni navegador. Ejemplo: un POST con 5, 3 y sumar devuelve HTML con 8.
De aceptación: prueba la app en ejecución como lo haría un usuario, con Selenium contra el contenedor Docker. Ejemplo: el navegador escribe 10 y 2, elige "dividir" y ve 5 en pantalla.
La unitaria verifica que el cálculo sea correcto. La de componente verifica que las piezas de la app funcionen juntas. La de aceptación verifica que el usuario pueda hacer lo que necesita en la aplicación real.

---

### III. Describe brevemente qué hace cada uno de los steps principales de tu workflow de GitHub Actions (desde el checkout hasta el push de Docker). Explica el propósito de cada uno (qué hace y para qué se hace).

Checkout: descarga el código del repositorio para que el pipeline pueda trabajar con él.
Set up Python: instala Python 3.13 para ejecutar las herramientas y las pruebas.
Install dependencies: instala las librerías necesarias para el proyecto.
Black: verifica que el código tenga un formato uniforme.
Pylint y Flake8: detectan errores y malas prácticas en el código.
Unit and Component Tests: prueban la lógica y exigen al menos un 80% de cobertura.
Build Docker image: empaqueta la aplicación en una imagen.
Start container: ejecuta la imagen para probarla como en producción.
Acceptance Tests: prueban la aplicación desde el navegador, como lo haría un usuario.
Show container logs: si algo falla, muestra los logs para diagnosticar.
Upload Reports: guarda los reportes de pruebas y calidad para revisarlos.
SonarCloud Scan: analiza la calidad y seguridad del código y bloquea el pipeline si no se cumplen los criterios.
Login to Docker Hub: se autentica en Docker Hub, solo en main.
Push Docker image: publica la imagen validada en Docker Hub.

---

### IV. ¿Qué problemas o dificultades encontraron al implementar este taller? ¿Cómo los solucionaron? Cada integrante describe al menos un problema o aprendizaje propio, identificándose con su nombre.

Juan Jose: Como vengo de la ciencia de datos, al principio me costó ver cómo encajaba todo esto en mi trabajo. En software lo que cambia es el código, pero en datos también cambian los datos y los modelos, y eso hace que todo sea menos directo. Lo que me ayudó fue ir paso por paso, buscando el equivalente de cada parte del pipeline en mi día a día: las pruebas, para validar las funciones de limpieza y transformación

Sebastian Herrera: En mi día a día estoy acostumbrado a trabajar con automatizaciones y con el CI mas que todo del proyecto. El único reto que encontré fue entender bien el manejo de credenciales en el yaml porque nunca había trabajado con secretos ni con las propiedades del repositorio.

Julian Giraldo: Por mi trabajo como analista de datos conozco bien la idea de controlar qué información llega a un reporte o dashboard final. Antes de publicar un dato hay que validarlo, revisarlo y asegurarse de que no dañe lo que ya funciona. En GitHub aprendí que esa misma lógica se aplica al código, aunque la herramienta era nueva para mí. Entendí que el pipeline en verde no es un trámite. Es la garantía de que nadie, incluido yo, rompe la versión oficial por un descuido.

---

### V. ¿Qué ventajas ofrece construir la imagen Docker, ejecutar las pruebas de aceptación sobre ella y publicar exactamente esa misma imagen, en lugar de simplemente validar el código?

Al construir la imagen Docker, ejecutar las pruebas de aceptación sobre ella y publicar exactamente esa misma imagen, se valida el artefacto real que se despliega (con su Dockerfile, dependencias, versión de Python y configuración), no solo el código fuente. Esto garantiza que lo que pasó las pruebas es idéntico a lo que llega a producción, evita diferencias entre el entorno de desarrollo y el de ejecución, y detecta a tiempo fallos que el código por sí solo no revelaría, como un Dockerfile mal armado, una dependencia faltante o un error de arranque del contenedor. Por otro lado, si se reconstruyera la imagen después de las pruebas, podría cambiar algo como una librería actualizada o una capa distinta y lo publicado ya no sería lo probado.

---

### VI. Sobre el Pull Request de la sección 9: ¿qué pruebas agregaron y qué error de la calculadora detectaría cada una? Con el error intencional, ¿en qué paso falló el pipeline, qué pasos no se ejecutaron y cómo impidieron la protección de main y el pipeline que ese error llegara a main y a Docker Hub?

En el Pull Request agregaron dos pruebas. La primera, `test_operaciones_con_decimales`, revisa que sumar, restar, multiplicar y dividir funcionen bien con decimales, y detectaría errores como redondeos o conversiones a entero. La segunda, `test_operaciones_con_dos_negativos`, revisa que los signos se manejen bien cuando ambos números son negativos, y detectaría, por ejemplo, que `restar(-2, -3)` no dé 1 o que `multiplicar(-2, -3)` no dé 6.

Después se introdujo a propósito el error de que `restar` se cambia `a - b` por `a + b`. El pipeline falló en el paso "Run Unit and Component Tests", porque las pruebas de resta esperaban un resultado y recibieron otro. Como GitHub Actions se detiene en el primer fallo, no se ejecutaron la construcción de la imagen Docker, el arranque del contenedor, las pruebas de aceptación, el análisis de SonarCloud, el login en Docker Hub ni el push de la imagen.

Con eso el error quedó contenido en dos niveles. La protección de main exige que el job `build-and-test` termine en verde, así que con el check en rojo el PR no se podía fusionar y el código malo nunca llegó a main. Además, el pipeline solo publica en Docker Hub cuando hay un push a main y después de que todas las pruebas pasen. Al fallar antes, no se construye la imagen, y nada defectuoso llegó a Docker Hub.
