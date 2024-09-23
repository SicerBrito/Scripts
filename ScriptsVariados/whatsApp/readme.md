# Documentación: Script de WhatsApp para enviar el guión de Shrek

Autor: Sicer Andres Brito Gutierrez

## Archivo de referencia
`whatsappMovieSherk.js`

## Descripción
Este script automatiza el envío del guión inicial de la película Shrek a través de WhatsApp Web. Utiliza JavaScript para interactuar con la interfaz de WhatsApp Web, enviando el texto línea por línea. El script solo se puede ejecutar desde WhatsApp Web debido a que se ejecuta desde la consola para desarrolladores del navegador.

## Requisitos
- Acceso a WhatsApp Web
- Navegador web con herramientas de desarrollador (DevTools)
- Una conversación abierta en WhatsApp Web donde enviar el mensaje

## Funcionalidades principales

### 1. Función `enviarScript(scriptText)`
Esta función asíncrona es el núcleo del script. Toma el texto del guión como entrada y lo envía línea por línea.

#### Parámetros
- `scriptText` (string): El texto completo del guión a enviar.

#### Funcionamiento
1. Divide el texto en líneas, eliminando espacios en blanco y líneas vacías.
2. Localiza el área de texto en la interfaz de WhatsApp Web.
3. Para cada línea:
   - Inserta el texto en el área de mensaje.
   - Simula el evento de cambio.
   - Hace clic en el botón de enviar.
   - Espera 250ms entre mensajes (excepto para el último).

#### Retorno
- Promesa que resuelve con el número de líneas enviadas.

### 2. Contenido del guión
El script incluye las primeras líneas del guión de Shrek, incluyendo la narración inicial y una nota sobre la canción "Allstar" de Smashmouth.

## Instrucciones de uso

1. Copia todo el contenido del archivo `whatsappMovieSherk.js`.
2. Abre WhatsApp Web en tu navegador.
3. Abre cualquier conversación en WhatsApp Web donde desees enviar el guión.
4. Presiona la tecla `F12` para abrir las herramientas de desarrollador (DevTools).
5. Navega a la pestaña "Consola" dentro de las herramientas de desarrollador.
6. Pega el código en la consola de DevTools.
7. Presiona Enter para ejecutar el script.

### Solución de problemas
Si encuentras un error o una denegación de ejecución, podrías ver un mensaje similar a este:

![Mensaje de error](https://miro.medium.com/v2/resize:fit:640/format:webp/0*JNDnh4igkY6JhnCi)

Para resolver este problema:
1. Escribe `allow pasting` en la consola.
2. Presiona `Enter`.
3. Intenta pegar y ejecutar el script nuevamente.

Si encuentras el error "Não há uma conversa aberta" (No hay una conversación abierta), asegúrate de tener una conversación de WhatsApp Web activa antes de ejecutar el script.

## Advertencias y consideraciones
- Este script envía múltiples mensajes rápidamente, lo que podría ser considerado spam.
- El uso de scripts automatizados en WhatsApp puede violar los términos de servicio.
- Asegúrate de tener permiso del destinatario antes de enviar una gran cantidad de mensajes.
- Utiliza este script con responsabilidad y respetando la privacidad de los demás usuarios de WhatsApp.

## Soporte
Para preguntas o problemas relacionados con este script, contacta al autor: Sicer Andres Brito Gutierrez.

---
