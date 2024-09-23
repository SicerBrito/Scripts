# Documentación del Script de Envío de Mensajes en WhatsApp Web

## Autor
Sicer Andrés Brito Gutiérrez

## Referencia
[Enlace al archivo con el script](https://example.com/script.js)

## Descripción
Este script automatiza el envío de múltiples mensajes en WhatsApp Web, dividiendo un texto largo en mensajes individuales y enviándolos secuencialmente.

## Funcionamiento
El script consta de dos partes principales:

1. La función `enviarScript(scriptText)`
2. La llamada a la función con el texto a enviar

### Función `enviarScript(scriptText)`

Esta función asíncrona realiza las siguientes tareas:

1. Divide el texto de entrada en líneas, eliminando espacios en blanco y líneas vacías.
2. Localiza el área de chat principal y el campo de texto en la interfaz de WhatsApp Web.
3. Para cada línea del texto:
   - Inserta la línea en el campo de texto.
   - Simula el evento de cambio en el campo de texto.
   - Hace clic en el botón de envío.
   - Espera un breve periodo entre mensajes.
4. Retorna el número total de mensajes enviados.

### Llamada a la función

La función se llama con un template string que contiene el texto a enviar. Después de la ejecución, se muestra en la consola el número de mensajes enviados o cualquier error ocurrido.

## Uso
Para utilizar este script:

1. Abra WhatsApp Web en su navegador.
2. Abra la conversación donde desea enviar los mensajes.
3. Abra la consola del navegador.
4. Copie y pegue el script completo en la consola.
5. Presione Enter para ejecutar.

## Solución de problemas
Si encuentras un error o una denegación de ejecución, podrías ver un mensaje similar a este:

![Mensaje de error](https://miro.medium.com/v2/resize:fit:640/format:webp/0*JNDnh4igkY6JhnCi)

Para resolver este problema:
1. Escribe `allow pasting` en la consola.
2. Presiona `Enter`.
3. Intenta pegar y ejecutar el script nuevamente.

Si encuentras el error "Não há uma conversa aberta" (No hay una conversación abierta), asegúrate de tener una conversación de WhatsApp Web activa antes de ejecutar el script.

## Soporte
Para soporte o consultas, contacte al autor:
Discord: SicerBrito#1610

## Nota de Responsabilidad
Este script debe utilizarse con responsabilidad y ética. El autor no se hace responsable de cualquier daño causado por el uso malintencionado o inadecuado de este script.