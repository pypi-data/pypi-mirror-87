# SAT WS

> Librería para usar el servicio web del SAT de Descarga Masiva

:us: The documentation of this project is in spanish as this is the natural language for intented audience.

:mexico: La documentación del proyecto está en español porque ese es el lenguaje principal de los usuarios.

Basada en gran parte del proyecto <https://github.com/phpcfdi/sat-ws-descarga-masiva>

Código fuente <https://gitlab.com/HomebrewSoft/sat_ws_api>

Esta librería contiene un cliente (consumidor) del servicio del SAT de
**Servicio Web de Descarga Masiva de CFDI y Retenciones**.

## Instalación

<!-- TODO -->

## Ejemplo básico de uso

<!-- TODO -->

## Acerca del Servicio Web de Descarga Masiva de CFDI y Retenciones

El servicio se compone de 4 partes:

1. Autenticación: Esto se hace con tu fiel y la libería oculta la lógica de obtener y usar el Token.
2. Solicitud: Presentar una solicitud incluyendo la fecha de inicio, fecha de fin, tipo de solicitud
   emitidas/recibidas y tipo de información solicitada (cfdi o metadata).
3. Verificación: pregunta al SAT si ya tiene disponible la solicitud.
4. Descargar los paquetes emitidos por la solicitud.

## Compatilibilidad

<!-- TODO -->

## Contribuciones

Las contribuciones con bienvenidas. Por favor lee [CONTRIBUTING][] para más detalles
y recuerda revisar el archivo de tareas pendientes [TODO][] y el [CHANGELOG][].

## Copyright and License

The `sat-ws` library is copyright © [HomebrewSoft](https://homebrewsoft.dev)
and licensed for use under the MIT License (MIT). Please see [LICENSE][] for more information.
