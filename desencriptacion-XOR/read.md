## Explicación del pensamiento y búsqueda de la solución:

1. **Entender el problema:** El problema consistía en descifrar un mensaje cifrado utilizando un algoritmo XOR con una llave de longitud 4, donde la llave consiste en caracteres alfabéticos minúsculos ('a' a 'z') y el mensaje cifrado se compone de números.
2. **Desarrollo de la solución:**
   - Se implementaron tres funciones principales:
     - `xor_desencriptar`: Esta función realiza el proceso de desencriptar un mensaje utilizando el algoritmo XOR con una llave dada.
     - `verificar_legibilidad`: Verifica si un mensaje desencriptado es legible según ciertos criterios definidos por una expresión regular.
     - `fuerza_bruta_desencriptar`: Realiza un ataque de fuerza bruta para descifrar el mensaje cifrado probando todas las posibles combinaciones de llaves de longitud 4.
   - Se utilizó la biblioteca `re` para trabajar con expresiones regulares y definir un patrón para verificar la legibilidad del mensaje desencriptado.
   - Se utilizó un enfoque de fuerza bruta para probar todas las combinaciones posibles de llaves alfabéticas minúsculas.
   - Se realizó la desencriptación del mensaje cifrado utilizando el algoritmo XOR con cada una de las llaves generadas.
   - Se verificó la legibilidad del mensaje desencriptado utilizando la función `verificar_legibilidad`.
   - Si se encontraba un mensaje desencriptado legible, se imprimía la llave y el mensaje desencriptado.
3. **Refinamiento y optimización:** No se realizaron optimizaciones adicionales ya que el problema era factible de resolver mediante fuerza bruta debido a la longitud relativamente corta de la llave (4 caracteres). Se utilizaron bucles anidados para generar todas las posibles combinaciones de llaves.
4. **Pruebas y verificación:** Se ejecutó el código y se verificó que el mensaje desencriptado resultante fuera legible y coherente. En caso de encontrar un mensaje desencriptado legible, se detuvo el proceso de fuerza bruta y se imprimió el resultado.
 