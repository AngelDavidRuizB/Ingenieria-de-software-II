# Ejercicio de patrones de diseño en Python

## Descripción extensa de la actividad

La actividad pide construir un ejemplo práctico en Python donde:

1. Se use el patrón `Singleton`.
2. Ese patrón se combine con otro patrón adicional.
3. Se intente cubrir los tres grandes grupos de patrones GOF:
- Creacionales.
- Estructurales.
- De comportamiento.
4. Además, dentro de lo creacional no quedarse solo con Singleton, sino incluir otro patrón de la misma categoría.

La solución se diseñó como un flujo de generación de reportes para que la integración sea realista:

- Primero se crea un reporte (creacional).
- Luego se añade auditoría al proceso (estructural).
- Finalmente se decide cómo exportar el resultado (comportamiento).

## Patrones implementados y rol de cada uno

### 1) Creacionales

- `Singleton` en [`singleton_logger.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/singleton_logger.py)
  - Clase principal: `Logger`.
  - Objetivo: asegurar una única instancia compartida para el registro de eventos.
  - Validación conceptual: dos variables distintas (`logger_a`, `logger_b`) apuntan al mismo objeto.

- `Factory Method` en [`factory_report.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/factory_report.py)
  - Clase principal: `ReportFactory`.
  - Objetivo: encapsular la creación de objetos de reporte (`TextReport`, `JsonReport`) sin acoplar el cliente a clases concretas.
  - Cumple con el requisito de usar otro patrón creacional además de Singleton.

### 2) Estructural

- `Decorator` en [`decorator_audit.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/decorator_audit.py)
  - Clase principal: `AuditDecorator`.
  - Objetivo: añadir comportamiento (auditoría antes/después) sin modificar la clase base `ReportService`.
  - Aporta flexibilidad porque permite extender responsabilidades por composición.

### 3) De comportamiento

- `Strategy` en [`strategy_export.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/strategy_export.py)
  - Clases principales: `ExportContext`, `ConsoleExport`, `UppercaseExport`.
  - Objetivo: cambiar el algoritmo de salida en tiempo de ejecución sin alterar el cliente.
  - Se demuestran dos estrategias distintas sobre el mismo contenido.

## Combinación solicitada: Singleton + otro patrón

La combinación se implementa en [`decorator_audit.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/decorator_audit.py):

- `AuditDecorator` (patrón estructural `Decorator`) envuelve un servicio de reportes.
- Durante `generate`, invoca `Logger()` para registrar inicio y fin.
- Como `Logger` es `Singleton`, toda auditoría usa la misma instancia compartida.

Con esto se cumple explícitamente la parte de “combinar Singleton con otro patrón”.

## Orquestación completa del ejercicio

El archivo [`main.py`](/Users/User/UNAL/Ingesoft2/patrones_diseño/main.py) integra todo el flujo:

1. Comprueba que `Logger` es único.
2. Crea un reporte usando `ReportFactory`.
3. Aplica `AuditDecorator` para registrar el proceso.
4. Ejecuta dos estrategias de exportación para mostrar variación de comportamiento.

## Cómo se comprueba (paso a paso)

En macOS (incluyendo MacBook Air), ejecutar:

```bash
cd /Users/User/UNAL/Ingesoft2/patrones_diseño
python3 main.py
```

Verificaciones esperadas en la salida:

1. `Logger único (singleton): True`
- Prueba directa de instancia única.

2. Mensajes:
- `[INFO] Inicia generación de reporte`
- `[INFO] Finaliza generación de reporte`
- Evidencia de que el `Decorator` añadió auditoría y usa el Singleton.

3. Dos bloques de salida distintos en Strategy:
- `ConsoleExport`: antepone texto descriptivo.
- `UppercaseExport`: transforma el contenido a mayúsculas.
- Evidencia de intercambio de algoritmo sin cambiar el cliente.

## Por qué sí es posible usar los tres tipos en este caso

Sí es posible porque el problema fue modelado en etapas con responsabilidades separadas:

1. Creación de objetos (`Singleton` + `Factory Method`).
2. Composición/extensión de comportamiento sobre objetos ya creados (`Decorator`).
3. Variación del algoritmo de ejecución según necesidad (`Strategy`).

Estas etapas son compatibles entre sí y no se excluyen. Por eso se pueden combinar en un mismo ejercicio sin forzar el diseño.

## Resumen final de cumplimiento

Se cumple todo lo solicitado:

1. `Singleton` implementado y comprobado.
2. `Singleton` combinado con `Decorator`.
3. Tres categorías cubiertas:
- Creacional: `Singleton` + `Factory Method`.
- Estructural: `Decorator`.
- Comportamiento: `Strategy`.
