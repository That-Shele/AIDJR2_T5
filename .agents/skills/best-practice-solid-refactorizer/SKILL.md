---
name: best-practice-solid-refactorizer
description: Guía para refactorizar monolitos en Python aplicando Clean Architecture, buenas prácticas y debugging. Útil para modernizar y desacoplar bases de código heredadas.
---
# Refactorización de Monolitos Python

## Resumen
Esta guía proporciona un flujo estructurado para descomponer y refactorizar un monolito en Python hacia una arquitectura limpia (Clean Architecture). Incorpora principios SOLID, prácticas de testing rigurosas y técnicas de debugging avanzado.

## Cuándo usar
- Para modernizar, limpiar o refactorizar un monolito de Python.
- Para desacoplar bases de código heredadas (legacy code) o extraer módulos progresivamente.
- Para implementar Clean Architecture de forma progresiva.

## Pasos para la Refactorización

1. **Análisis y Preparación (Descubrimiento)**
   - Mapea el código actual en la raiz y comprende sus flujos. Herramientas como `pydeps` pueden ayudar a visualizar el acoplamiento.
   

2. **Debugging y Red de Seguridad (Testing)**
   - Escribe pruebas de caracterización ("caja negra") antes de tocar la lógica interna. Asegura que el comportamiento esperado no cambia (Test-Driven Refactoring).
   - Utiliza herramientas de debugging nativas como `pdb` o robustece la configuración de `logging` para capturar el estado interno acoplado.
 

3. **Implementación de Clean Architecture**
   Separa el código en anillos de responsabilidad:
   - **Entities (Dominio):** Objetos de dominio puros (ej. con `dataclasses` o `Pydantic`) sin dependencias externas.
   - **Use Cases (Casos de uso):** Lógica de negocio específica de la aplicación.
   - **Interface Adapters:** Controladores web, presentadores y abstracción de la base de datos (Patrón Repository).
   - **Infrastructure:** Framework web (FastAPI/Django/Flask), ORM (SQLAlchemy), y librerías de terceros.


4. **Desacoplamiento Progresivo (Patrón Strangler Fig)**
   - Evita reescrituras tipo "Big Bang". Identifica un flujo, aíslalo y extrae sus dependencias progresivamente.
 

5. **Buenas Prácticas (Clean Code)**
   - **Inyección de Dependencias:** Úsala para inyectar repositorios de infraestructura a los Use Cases, haciendo el código fácilmente testeable con _mocks_.
   - **Tipado Estático:** Agrega _Type Hints_ y utiliza `mypy` en el CI/CD.
   - **Linter/Formatter:** Estandariza la calidad del código mediante `black`, `ruff`, o `flake8`.

## Gotchas y Consideraciones
- **Sobrediseño (Over-engineering):** Clean Architecture requiere interfaces y abstracciones extras. Cuidado con crear capas que solo pasen datos sin añadir valor (passthrough).
- **Acoplamiento Oculto:** Presta atención a variables globales o singletons informales en Python que rompan los límites de las capas.
- **Tests Acoplados a la Implementación:** Los tests deben evaluar entradas y salidas de la lógica de negocio, no si llamaste a una función interna de forma específica.