# Reporte TDD — Módulo de Gestión de Reservas

## 1. Descripción del módulo

El módulo implementa la gestión de reservas de un restaurante, desarrollado aplicando TDD (Test-Driven Development) con el ciclo **RED → GREEN → REFACTOR**. En esta entrega se cubre el requerimiento funcional **RF01: Crear reserva**.

La solución se estructura en cuatro capas con responsabilidades bien definidas:

| Componente | Archivo | Responsabilidad |
|---|---|---|
| `Reservation` y `ReservationStatus` | `src/reservations/models/reservation.py` | Entidad de dominio (dataclass) con los datos de la reserva y su estado. |
| `ReservationService` | `src/reservations/services/reservation_service.py` | Lógica de negocio y casos de uso: validación de datos y generación de código. |
| `InMemoryReservationRepository` | `src/reservations/repositories/reservation_repository.py` | Abstracción de persistencia en memoria (`save`, `find`, `find_by_date`). |
| Excepciones de negocio | `src/reservations/exceptions/reservation_errors.py` | Jerarquía de errores (`MissingRequiredDataError`, `InvalidPartySizeError`). |

El flujo de creación es: `ReservationService.create_reservation()` valida los datos, genera un código único y persiste la reserva a través del repositorio.

> **Alcance:** este requerimiento se limita a crear la reserva. La verificación de disponibilidad/capacidad corresponde a otro requerimiento funcional y fue excluida de este alcance (ver sección 3).

## 2. Requerimientos implementados

**RF01 — Creación de una reserva**, con las siguientes reglas de negocio:

- El nombre del cliente es obligatorio: no se aceptan valores `None`, vacíos ni solo espacios.
- La fecha y la hora de la reserva son obligatorias.
- El tamaño del grupo (`party_size`) debe ser un entero mayor a cero.
- Se genera un código único autogenerado por reserva (`RES-0001`, `RES-0002`, …).
- La reserva se crea con estado `ACTIVE` por defecto.

## 3. Aplicación de TDD

El requerimiento se desarrolló siguiendo el ciclo completo RED → GREEN → REFACTOR, evidenciado en los commits de la rama `feature/rf01-create-reservation-refactor`:

| Fase | Commit | Descripción |
|---|---|---|
| RED | `295a5ce` test(red): Agrega tests de creación de reserva | Se escriben las pruebas antes de la implementación. |
| GREEN | `729f68e` test(green): Agrega codigo minimo funcional | Se implementa el código mínimo para pasar las pruebas. |
| REFACTOR | `e958391` test(refactor): Refactoriza codigo de reservas | Se mejora el diseño sin cambiar el comportamiento. |

Durante la fase GREEN se implementó además un método de verificación de disponibilidad (`_ensure_availability`) con sus pruebas, pero se determinó que ese comportamiento corresponde a la consulta de disponibilidad y no a la creación de la reserva en sí, por lo que fue retirado del alcance de RF01 junto con sus pruebas (4 casos) y su llamada en `create_reservation`.

Dentro de ese marco se distinguen **4 ciclos de comportamiento**, seleccionados como evidencia y descritos a continuación.

### Ciclo 1 — Creación de reserva con datos válidos

- **Comportamiento deseado:** `create_reservation` retorna una `Reservation` con los datos entregados y estado `ACTIVE`.
- **Prueba escrita inicialmente:** `test_creates_reservation_with_data_and_unique_code`.
- **Por qué falló (RED):** `create_reservation` lanzaba `NotImplementedError`, por lo que todas las pruebas de creación fallaban al ejecutarse.
- **Implementación que la hizo pasar (GREEN):** se construyó la `Reservation` (dataclass con estado por defecto `ACTIVE`), se asignó el código generado y se persistió con `repository.save()`.
- **Refactorización:** se renombraron los parámetros `date`/`time` a `reservation_date`/`reservation_time` y se usaron los alias `DateType`/`TimeType` para evitar el *shadowing* de los tipos de la librería estándar `datetime`.

### Ciclo 2 — Generación de códigos únicos

- **Comportamiento deseado:** cada reserva debe tener un código único e irrepetible.
- **Prueba escrita inicialmente:** `test_generates_unique_codes`, que crea dos reservas y verifica que sus códigos sean distintos.
- **Por qué falló (RED):** `create_reservation` lanzaba `NotImplementedError`.
- **Implementación que la hizo pasar (GREEN):** método privado `_generate_code` con un contador incremental que produce `RES-0001`, `RES-0002`, …; el contador se mantiene como estado interno del servicio.
- **Refactorización:** el flujo aplicó el mismo renombrado de parámetros y alias de tipos del Ciclo 1, manteniendo la unicidad verificada por la prueba.

### Ciclo 3 — Validación de datos obligatorios (nombre, fecha, hora)

- **Comportamiento deseado:** rechazar la reserva si falta el nombre del cliente, la fecha o la hora, lanzando `MissingRequiredDataError`.
- **Prueba escrita inicialmente:** `test_rejects_missing_customer_name` (parametrizada con `None`, `""` y `"   "`), `test_rejects_missing_date` y `test_rejects_missing_time`.
- **Por qué falló (RED):** la validación no existía; el método lanzaba `NotImplementedError` y la prueba esperaba la excepción de negocio.
- **Implementación que la hizo pasar (GREEN):** método privado `_validate`, que verifica nombre vacío con `strip()` y campos `None`, lanzando `MissingRequiredDataError`.
- **Refactorización:** en `_validate`, los parámetros se tiparon como opcionales (`DateType | None`, `TimeType | None`) para reflejar que se admiten valores nulos y se valida su presencia; se mejoró el formato multilínea de la firma.

### Ciclo 4 — Validación del tamaño del grupo

- **Comportamiento deseado:** el tamaño del grupo debe ser un entero mayor a cero; rechazar `0`, `-1`, `-10` con `InvalidPartySizeError`.
- **Prueba escrita inicialmente:** `test_rejects_non_positive_party_size`, parametrizada con `[0, -1, -10]`.
- **Por qué falló (RED):** no existía la validación; el método lanzaba `NotImplementedError`.
- **Implementación que la hizo pasar (GREEN):** dentro de `_validate`, se agregó la comprobación `not isinstance(party_size, int) or party_size <= 0` que lanza `InvalidPartySizeError`.
- **Refactorización:** se alineó el estilo de `_validate` (firmas y nombres consistentes con los del Ciclo 3); la regla en sí se mantuvo verificada por los mismos casos parametrizados.

## 4. Resultados de las pruebas

Al ejecutar la suite completa con `pytest` en el estado final (REFACTOR):

```
============================= test session starts ==============================
collected 11 items
tests/test_config.py::test_pytest_configuration PASSED                      [  9%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_creates_reservation_with_data_and_unique_code PASSED [ 18%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_generates_unique_codes PASSED [ 27%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_missing_customer_name[None] PASSED [ 36%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_missing_customer_name[] PASSED [ 45%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_missing_customer_name[   ] PASSED [ 54%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_missing_date PASSED [ 63%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_missing_time PASSED [ 72%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_non_positive_party_size[0] PASSED [ 81%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_non_positive_party_size[-1] PASSED [ 90%]
tests/unit/test_create_reservation.py::TestCreateReservation::test_rejects_non_positive_party_size[-10] PASSED [100%]

============================== 11 passed in 0.02s ==============================
```

**Resumen:**
- **Cantidad total de pruebas:** 11
- **Pruebas exitosas:** 11
- **Pruebas fallidas:** 0
- **Configuración:** 1 prueba de configuración de pytest (`tests/test_config.py`) + 10 pruebas del requerimiento RF01 (`tests/unit/test_create_reservation.py`).

**Evidencia de la fase RED:** al ejecutar la suite de creación (versión actual de `test_create_reservation.py`) sobre el commit `295a5ce` (fase RED), las 10 pruebas de creación fallaron (`10 failed, 1 passed`) porque `create_reservation` lanzaba `NotImplementedError`, lo que confirma que las pruebas se escribieron antes de la implementación.

## 5. Reflexión

- **Influencia de TDD en el diseño:** escribir las pruebas primero obligó a definir el contrato público de la solución antes de pensar en la implementación. Esto derivó en una arquitectura clara por capas (modelos, servicios, repositorios y excepciones), una interfaz limpia en `create_reservation` (nombre, cantidad de personas, fecha y hora) y reglas de negocio expresadas como excepciones específicas (`MissingRequiredDataError`, `InvalidPartySizeError`), evitando mensajes genéricos o lógica acoplada en una sola clase.
- **Cambios surgidos durante el desarrollo y las refactorizaciones:** se identificó que la verificación de disponibilidad/capacidad incorporada en la fase GREEN no correspondía al alcance de "crear reserva", por lo que se retiraron su método y sus 4 pruebas, dejando la creación con una responsabilidad única. En la refactorización se renombraron parámetros que ocultaban los tipos `date`/`time` de la librería estándar mediante los alias `DateType`/`TimeType` y se mejoró la legibilidad de `_validate`. Todo el tiempo, la suite permaneció en verde, garantizando que el refactor no alteró el comportamiento.
- **Dificultades al desarrollar primero las pruebas:** la principal fue definir el comportamiento esperado sin tener implementación alguna; en particular, fue necesario razonar casos límite (tamaño 0 y negativos, nombre solo con espacios) y decidir el contrato de errores (qué excepción lanzar y cuándo) antes de escribir la lógica, lo que resultó en pruebas más explícitas y en una implementación posterior más sencilla de validar. También apareció la dificultad de mantener el alcance enfocado: fue necesario discernir qué comportamientos congénitos a un caso de uso de creación (disponibilidad) debían separarse hacia otros requerimientos.