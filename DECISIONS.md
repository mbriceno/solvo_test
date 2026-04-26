# Decisiones Arquitectónicas del Proyecto

## 1. Decisiones de Diseño

### Arquitectura de Identidad: Aislamiento por Plataforma

Se implementó un modelo de identidad donde la entidad "Usuario" está vinculada estrictamente a una "Plataforma", utilizando un índice único compuesto por `(email, platform_id)`.

* **Alternativa considerada:** Identidad Unificada (Global Account). Un único registro de usuario global vinculado a múltiples plataformas.
* **Por qué se descartó:**
    1. Para este MVP un modelo unificado comprometería todo el ecosistema si una cuenta es vulnerada. El aislamiento garantiza que una brecha en una plataforma no afecte a las demás.
    2. Las plataformas pueden requerir ciclos de vida distintos (MFA, políticas de password, etc.). Un modelo global forzaría un single point of failure.
    3. Pensando en una posible baja por parte de los usuarios se bería afectado el cumplimiento de normativas (GDPR). El borrado de cuenta no sería atomico y sería más complejo modelar el borrado de cuentas por plataformas.

### Gestión de Reglas Dinámicas: Master Template + Overrides con Redis

Se diseñó un sistema de resolución de reglas que combina una configuración global (`GlobalConfig`) con sobreescrituras por plataforma vía `JSONField`. El uso de `JSONField` permite una extensibilidad infinita sin migraciones. Para mitigar el costo de procesamiento, se integró **Redis** como capa de caché, asegurando validaciones de baja latencia.

* **Alternativa considerada:** implementar tablas relacionales con columnas fijas.
* **Por qué se descartó:** Las tablas fijas requieren migraciones de base de datos para cada regla nueva, restando agilidad operativa.

### Arquitectura de Módulos Aislados y Patrón Service-Repository

El proyecto se organizó en cuatro módulos independientes (`authentication`, `platforms`, `users`, `notifications`) siguiendo una estructura de capas limpia. El patrón **Service-Repository** asegura que el repositorio maneje el acceso a datos y el servicio la lógica de negocio. Esto garantiza un sistema desacoplado, testeable y preparado para una transición transparente hacia microservicios.

* **Alternativa considerada:** Fat Views/Serializers (colocar la lógica en la capa de transporte).
* **Por qué se descartó:** Genera código difícil de testear y con alta deuda técnica. Dificulta el crecimiento hacia microservicios y duplica lógica si se añaden otros puntos de entrada (CLI, Tareas Celery).

### Adopción de IA y GitHub Spec Kit como Aceleradores de Ingeniería

Se integró el uso de IA y el framework **GitHub Spec Kit** como piezas centrales, incluyendo los scripts de automatización en el repositorio.

* **Alternativa considerada:** Desarrollo manual tradicional ("Code-First").
* **Por qué se descartó:** Para este caso un MVP entregable en un plazo corto de tiempo. El desarrollo manual de *boilerplate* consume tiempo que pude invertir de otra forma en el proyecto.
* **Decisión final:** Adoptar **"Specification-First Development"**.
    1. **Documentación como Código:** Los scripts del Spec Kit hacen que el proceso sea transparente y reproducible.
    2. **Garantía de Estándares:** La IA actuó como motor de cumplimiento normativo (PEP8, Ruff, Type Hints).
    3. **Eficiencia Operativa:** Permitió maximizar el *Time-to-Market* sin sacrificar la calidad técnica ni generar deuda técnica innecesaria.

## 2. Implementación de Reglas Configurables por Plataforma

### Problema: Rigidez vs. Mantenibilidad

Este sistemas, exige límites o comportamientos distintos por plataforma (ej. la Plataforma A permite 5 dispositivos, la Plataforma B permite 10). Hardcodear estas reglas o crear columnas en la base de datos para cada una genera un sistema rígido, costoso de mantener y difícil de escalar.

### Solución
Se implementó un motor de reglas basado en dos capas de precedencia, gestionado por un servicio especializado (`RuleResolver`):

1. **Platform Override (Alta Prioridad):** Se consulta el campo `JSONField` en el modelo de la Plataforma. Si la regla existe (ej. `{"max_devices": 10}`), se toma este valor.
2. **Global Template (Prioridad Media):** Si la regla no está definida para la plataforma, el sistema consulta la tabla `GlobalConfig`. Esto permite cambiar un valor por defecto para todo el ecosistema en tiempo de ejecución sin tocar una sola línea de código.

### Justificación del Approach: ¿Por qué este diseño?

* **Principio de Abierto/Cerrado (Solid OCP):** El sistema está "cerrado" para modificación (no hay que editar código para añadir una regla como `session_timeout`) pero "abierto" para extensión (basta con agregar la clave al JSON o a la tabla global).
* **Eficiencia con Redis:** Consultar un `JSONField` y realizar un "fallback" jerárquico en cada request de validación es costoso a nivel de CPU y DB. Por ello, se implementó una **capa de caché en Redis** que almacena el resultado final de la resolución de reglas para cada plataforma. Esto garantiza que la validación sea una operación de **O(1)** en memoria.
* **Agilidad del Negocio:** Permite al equipo de soporte o administradores ajustar límites de usuarios en tiempo real desde un panel administrativo, eliminando la dependencia de ciclos de despliegue (CI/CD) para cambios paramétricos.
* **Por Mejorar:** Cabe destacar que la implementación fue desarrollada tomando en cuenta la generalidad, con una mejor definición del sistema de reglas y su utlidad futura, se podrían aplicar mejoras.

## 3. Diseño del Sistema de Notificaciones y Extensibilidad

### Problema: Acoplamiento y Bloqueo de Procesos

En arquitecturas básicas, las notificaciones suelen enviarse de forma síncrona dentro de la misma función que genera el evento (ej. enviar un email justo después de guardar un usuario). Esto aumenta el tiempo de respuesta del API, acopla el dominio de negocio con proveedores externos y hace que el sistema falle si el proveedor de correos está caído.

### Solución

Se diseñó un módulo independiente (`notifications`) que actúa como un sistema de despacho persistente, basado en las siguientes premisas:

1. **Persistencia Primero:** Antes de intentar un envío, la notificación se guarda en la base de datos con su estado (`is_read`), el usuario destino y, fundamentalmente, un `template_context` (JSONField). Esto garantiza que el evento no se pierda y permite auditoría.
2. **Abstracción de Canales (Flags de Despacho):** El modelo incluye campos booleanos (`send_email`, `send_sms`, `send_socket`). El `NotificationService` no decide arbitrariamente cómo enviar; consulta al `RuleResolver` de la plataforma para activar los canales según la configuración del cliente.
3. **Contexto Dinámico:** El uso de un `JSONField` para el contexto permite que el sistema de notificaciones sea agnóstico al contenido. Puede recibir desde un nombre de usuario hasta una IP de origen o un código de verificación, sin cambiar el esquema de la base de datos.

### Consideraciones para la Extensibilidad

* **Preparación para Microservicios:** Al ser un módulo aislado con su propio Service y Repository, el sistema está listo para ser extraído a un microservicio independiente o un proceso worker (Celery) que procese la cola de notificaciones en segundo plano sin afectar la experiencia del usuario.
* **Patrón de Estrategia para Proveedores:** El diseño permite integrar nuevos canales (ej. Push Notifications, WhatsApp) simplemente añadiendo un nuevo flag en el modelo y un "handler" en el servicio de despacho, sin necesidad de modificar los módulos de `authentication` o `users`.
* **Independencia de Disparo:** Los otros módulos del sistema solo necesitan saber que deben "emitir" una notificación; no necesitan conocer la lógica de si se enviará por SMS o si requiere un template específico. Esto mantiene el núcleo del sistema limpio y enfocado en su responsabilidad única.

## 4. Estrategia de Escalabilidad: Hacia el Millón de Usuarios

Si el sistema proyectara un crecimiento hacia un millón de usuarios activos, la arquitectura actual debería evolucionar para mitigar cuellos de botella en la base de datos y la latencia de red. Estas son las acciones clave:

### Migración a Microservicios y Bases de Datos Especializadas

* El módulo de `notifications` y el de `platforms` (específicamente el Rule Resolver) se moverían a microservicios independientes.
* La base de datos relacional (PostgreSQL) se mantendría para datos transaccionales, pero las notificaciones con alta tasa de escritura podrían ser migradas a una base de datos NoSQL (como MongoDB o DynamoDB) para manejar el volumen sin degradar el rendimiento del core.

### Implementación de una Arquitectura Event-Driven

* En lugar de llamadas directas entre servicios, utilizaría un **Message Broker** (como RabbitMQ o Kafka).
* **Ejemplo:** Cuando un usuario registra un dispositivo, el `UserService` emitiría un evento `DeviceRegistered`. El sistema de notificaciones, suscrito a este evento, procesaría el envío de forma asíncrona, eliminando cualquier latencia en el API principal.

### Caché Avanzada y Sharding

* Ampliaría el uso de Redis no solo para reglas, sino para sesiones y perfiles de usuario frecuentes, implementando estrategias de *Write-through* para mantener la consistencia.
* Segmentaría la base de datos de usuarios por `platform_id`. Dado que nuestro diseño ya aisla a los usuarios por plataforma, el *sharding* sería natural y permitiría distribuir la carga en múltiples nodos de base de datos.

## 5. Transición a Microservicios con FastAPI

Si tuviera que extraer el primer componente hacia un microservicio, el candidato sería el **módulo de Notifications (y específicamente su Dispatcher)**.

### ¿Por qué el sistema de Notificaciones?

1. Las notificaciones dependen casi exclusivamente de llamadas a red (APIs externas de Email, SMS, WebSockets). FastAPI, al estar construido sobre **Starlette** y soportar `async/await` de forma nativa, maneja estas operaciones de Entrada/Salida de manera mucho más eficiente que el modelo síncrono tradicional de Django, permitiendo procesar miles de notificaciones concurrentes con un consumo de memoria mínimo.
2. El volumen de notificaciones suele ser órdenes de magnitud mayor que el de registros o logins. Al moverlo a FastAPI, podemos escalar este servicio horizontalmente (más pods en K8s) durante picos de tráfico sin necesidad de escalar toda la lógica de negocio de la plataforma o la gestión de usuarios.
3. Si un proveedor de SMS tarda 30 segundos en responder o falla, el microservicio de FastAPI puede manejar los reintentos y la presión sin bloquear los hilos de ejecución de la API principal, garantizando que el usuario siempre pueda navegar por la plataforma aunque las notificaciones lleven retraso.
