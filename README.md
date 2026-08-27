# Restaurant Reservation

## 1. Descripción
Módulo de gestión de reservas para un restaurante, desarrollado como actividad académica para aplicar TDD (Test-Driven Development).

## 2. Objetivo
El objetivo principal de este proyecto es aplicar explícitamente el ciclo de desarrollo guiado por pruebas:

**RED → GREEN → REFACTOR**

## 3. Tecnologías
* Python 3.12+
* pytest
* Git
* GitHub

## 4. Arquitectura inicial
El diseño inicial del proyecto está estructurado con las siguientes responsabilidades, las cuales podrán evolucionar durante los ciclos de refactorización de TDD:

* `models`: Entidades de dominio y estructuras de datos (ej. Reservation).
* `services`: Lógica de negocio y casos de uso.
* `repositories`: Abstracción para el almacenamiento y persistencia en memoria.
* `exceptions`: Excepciones de negocio personalizadas.
* `tests`: Pruebas automatizadas (unitarias, integración, etc.).

> **IMPORTANTE**: Estas responsabilidades representan el diseño inicial para comenzar el desarrollo mediante TDD.

## 5. Instalación

Sigue estos pasos para preparar el entorno de desarrollo local:

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd restaurant-reservation
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual**:
   - En Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 6. Ejecutar pruebas

Para ejecutar la suite de pruebas automatizadas:

```bash
pytest
```

## 7. Estado del proyecto
**Proyecto base. La implementación de la lógica de negocio se realizará posteriormente mediante TDD.**

