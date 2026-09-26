## 📘 Ejercicio de Práctica: API de Reservas de Hotel (Booking System)

**Contexto:** Debes crear una API para administrar las reservas de habitaciones de un hotel boutique. Cada reserva tendrá un ID único autoincremental, el nombre del huésped, el número de habitación, el precio por noche y un campo opcional para solicitudes especiales.

### Requerimientos del código:

- **Base de Datos:** Un diccionario global llamado reservas: `Dict[int, dict] = {}`.

- **Modelos de Pydantic:**
  - **ReservaBase:** Con huesped (str), habitacion (int), precio_noche (float) y notas (str u opcional).
  - **ReservaCrear:** Hereda de ReservaBase.
  - **ReservaActualizar:** Todos los campos anteriores pero opcionales (None), para permitir cambios parciales (ej. si el cliente cambia de habitación o tarifa).
  - **ReservaRespuesta:** Hereda de ReservaBase e incluye el id (int).
