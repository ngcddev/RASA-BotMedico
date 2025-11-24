# RASA-BotMédico 🏥

Un chatbot inteligente basado en **RASA** para la gestión de citas médicas mediante procesamiento de lenguaje natural en español.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Guía de Funcionamiento](#guía-de-funcionamiento)
- [Componentes Principales](#componentes-principales)
- [Acciones Personalizadas](#acciones-personalizadas)
- [Intents y Entidades](#intents-y-entidades)
- [Ejecución](#ejecución)
- [Pruebas](#pruebas)
- [Troubleshooting](#troubleshooting)

---

## 📖 Descripción General

**RASA-BotMédico** es un asistente conversacional que utiliza el framework RASA para:

✅ Procesar solicitudes de citas médicas en lenguaje natural  
✅ Recopilar información (nombre, fecha, especialidad) a través de formularios  
✅ Reservar, cancelar y consultar citas  
✅ Mantener conversaciones naturales en español  
✅ Almacenar citas en memoria para gestión en tiempo real  

### Características Principales

- **NLU (Natural Language Understanding)**: Comprende intenciones y entidades en español
- **Diálogos Contextuales**: Maneja conversaciones complejas con formularios
- **Acciones Personalizadas**: Lógica de negocio para reserva y gestión de citas
- **Multilingüe**: Configurado específicamente para español
- **Politicas de IA**: Utiliza múltiples políticas de decisión (Memorización, Reglas, TED Policy)

---

## 📁 Estructura del Proyecto

```
RASA-BotMedico/
├── config.yml                 # Configuración del pipeline NLU y políticas
├── domain.yml                 # Definición de intents, entidades, slots y responses
├── credentials.yml            # Credenciales para conectar a canales
├── endpoints.yml              # Configuración de endpoints (acciones custom, etc)
├── actions/
│   ├── __init__.py           # Inicializador del módulo
│   ├── actions.py            # Acciones personalizadas del bot
│   └── __pycache__/          # Cache de Python
├── data/
│   ├── nlu.yml               # Datos de entrenamiento (intents y entidades)
│   ├── stories.yml           # Historias de conversación
│   ├── rules.yml             # Reglas de conversación
│   └── (otros archivos NLU)
├── models/                    # Modelos entrenados (.tar.gz)
├── tests/
│   └── test_stories.yml      # Historias de prueba
└── README.md                  # Este archivo

```

### Archivos Clave Explicados

| Archivo | Propósito |
|---------|-----------|
| **config.yml** | Define el pipeline de procesamiento de NLU y las políticas de diálogo |
| **domain.yml** | Vocabulario del bot: intents, entities, slots, acciones y respuestas |
| **data/nlu.yml** | Ejemplos de entrenamiento para reconocer intents y extraer entidades |
| **data/stories.yml** | Historias que definen flujos de conversación esperados |
| **actions/actions.py** | Código Python con lógica personalizada de acciones |

---

## 🔧 Requisitos

- **Python 3.8+** (recomendado 3.9 o 3.10)
- **RASA 3.x**
- **RASA SDK**
- Sistema operativo: Windows, macOS o Linux

---

## 📥 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ngcddev/RASA-BotMedico.git
cd RASA-BotMedico
```

### 2. Crear Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install rasa rasa-sdk
```

O instalar desde un archivo `requirements.txt` (si existe):

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

### config.yml - Pipeline de NLU

El pipeline define cómo RASA procesa el texto:

```yaml
pipeline:
  - WhitespaceTokenizer      # Divide el texto en palabras
  - RegexFeaturizer          # Extrae features con regex
  - LexicalSyntacticFeaturizer # Features sintácticas
  - CountVectorsFeaturizer   # Vectorización de palabras
  - CountVectorsFeaturizer   # Vectorización n-gramas de caracteres
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - DIETClassifier          # Clasificador dual-intent-entity
    epochs: 200
    entity_recognition: true
  - EntitySynonymMapper     # Mapea sinónimos de entidades
  - ResponseSelector        # Selecciona respuestas
  - FallbackClassifier      # Maneja confianza baja
```

### config.yml - Políticas de Diálogo

Las políticas determinan qué acción ejecuta el bot:

```yaml
policies:
  - MemoizationPolicy       # Memoriza historias exactas
  - RulePolicy              # Aplica reglas definidas
  - UnexpecTEDIntentPolicy  # Policy basada en intents
  - TEDPolicy               # Transformer Embedding Dialogue Policy
```

### domain.yml - Intents Definidos

```yaml
intents:
  - saludar              # Saludos iniciales
  - despedir             # Despedidas
  - afirmar              # Confirmaciones (sí, correcto)
  - negar                # Negaciones (no, para nada)
  - pedir_cita           # Solicitar cita
  - cancelar_cita        # Cancelar cita existente
  - consultar_citas      # Ver citas registradas
  - proporcionar_*       # Intents implícitos para slots
```

---

## 🗣️ Guía de Funcionamiento

### Flujo Básico de Conversación

```
Usuario: "Hola, necesito una cita médica"
    ↓
[Bot detecta intent: saludar + pedir_cita]
    ↓
[Bot activa formulario: cita_form]
    ↓
Bot: "¿Cuál es tu nombre?"
Usuario: "Juan García"
    ↓
[Bot extrae entity: nombre y llena slot "nombre"]
    ↓
Bot: "¿Qué fecha deseas? (ej: 2025-12-15)"
Usuario: "2025-12-20"
    ↓
[Bot extrae entity: fecha y llena slot "fecha"]
    ↓
Bot: "¿Qué especialidad necesitas?"
Usuario: "cardiología"
    ↓
[Bot extrae entity: especialidad y llena slot "especialidad"]
    ↓
[Todos los slots completos → Ejecuta action_reservar_cita]
    ↓
Bot: "Cita reservada exitosamente: ID 1, Paciente: Juan García..."
```

---

## 🔧 Componentes Principales

### 1. **NLU (Natural Language Understanding)**

#### Expresiones Regulares (Regex)

```yaml
- regex: nombre
  examples: |
    - [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+...

- regex: fecha
  examples: |
    - \d{4}-\d{2}-\d{2}        # Formato: 2025-12-20
    - (lunes|martes|miércoles) # Días de semana
    - (mañana|hoy)             # Referencias temporales
```

**Propósito**: Extraer entidades estructuradas del texto del usuario

#### Intents del NLU

| Intent | Ejemplo | Propósito |
|--------|---------|-----------|
| `saludar` | "Hola", "Buenos días" | Iniciar conversación |
| `pedir_cita` | "Necesito cita" | Solicitar nuevo turno |
| `cancelar_cita` | "Cancelar cita" | Eliminar cita existente |
| `consultar_citas` | "Ver mis citas" | Listar citas del usuario |
| `afirmar` | "Sí", "Correcto" | Confirmar |
| `negar` | "No", "Para nada" | Rechazar |

### 2. **Slots (Memoria Conversacional)**

Los slots almacenan información durante la conversación:

```yaml
slots:
  nombre:
    type: text
    influence_conversation: true
    mappings:
      - type: from_entity
        entity: nombre

  fecha:
    type: text
    influence_conversation: true
    mappings:
      - type: from_entity
        entity: fecha

  especialidad:
    type: text
    influence_conversation: true
    mappings:
      - type: from_entity
        entity: especialidad
```

**`influence_conversation: true`**: El valor del slot afecta futuras decisiones del bot

### 3. **Formularios (Forms)**

```yaml
forms:
  cita_form:
    required_slots:
      - nombre
      - fecha
      - especialidad
```

El formulario solicita cada slot requerido en orden hasta completarlos.

### 4. **Responses (Respuestas del Bot)**

```yaml
responses:
  utter_saludar:
    - text: "¡Hola! Soy el asistente de citas médicas. ¿En qué puedo ayudarte?"

  utter_preguntar_nombre:
    - text: "¿Cuál es tu nombre completo?"

  utter_cita_confirmada:
    - text: "Perfecto {nombre}, tu cita de {especialidad} ha sido reservada para el {fecha}."
```

Las variables `{nombre}`, `{fecha}`, etc., se rellena con valores de slots.

---

## 🎬 Acciones Personalizadas

Las acciones son función Python que ejecutan lógica de negocio:

### ActionReservarCita

```python
class ActionReservarCita(Action):
    def name(self) -> Text:
        return "action_reservar_cita"

    def run(self, dispatcher, tracker, domain):
        nombre = tracker.get_slot("nombre")
        fecha = tracker.get_slot("fecha")
        especialidad = tracker.get_slot("especialidad")
        
        if nombre and fecha and especialidad:
            cita = {
                "id": len(citas_reservadas) + 1,
                "nombre": nombre,
                "fecha": fecha,
                "especialidad": especialidad,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            citas_reservadas.append(cita)
            # Enviar confirmación...
```

**Responsabilidades**:
- ✅ Obtener datos de slots
- ✅ Validar información
- ✅ Guardar en memoria/BD
- ✅ Enviar confirmación al usuario

### ActionCancelarCita

```python
class ActionCancelarCita(Action):
    def name(self) -> Text:
        return "action_cancelar_cita"

    def run(self, dispatcher, tracker, domain):
        if citas_reservadas:
            cita_cancelada = citas_reservadas.pop()
            # Notificar cancelación...
```

### ActionConsultarCitas

```python
class ActionConsultarCitas(Action):
    def name(self) -> Text:
        return "action_consultar_citas"

    def run(self, dispatcher, tracker, domain):
        if citas_reservadas:
            # Listar todas las citas almacenadas
```

---

## 📚 Intents y Entidades

### Intents

Un intent es la **intención del usuario**:

```
Usuario: "Necesito una cita"      → Intent: pedir_cita
Usuario: "Quiero cancelar"         → Intent: cancelar_cita
Usuario: "¿Cuáles son mis citas?" → Intent: consultar_citas
```

### Entidades

Una entidad es **información específica** que extraemos:

```
Usuario: "Mi nombre es Juan García"
         ↓
         Entity: nombre = "Juan García"

Usuario: "Para el lunes próximo"
         ↓
         Entity: fecha = "lunes"

Usuario: "Necesito cardiología"
         ↓
         Entity: especialidad = "cardiología"
```

---

## 🚀 Ejecución

### 1. Entrenar el Modelo

```bash
rasa train
```

Esto crea un modelo en la carpeta `models/` basado en:
- NLU (intents, entidades)
- Diálogos (stories, rules)
- Políticas

### 2. Iniciar el Servidor de Acciones

En una **terminal separada**:

```bash
rasa run actions
```

El servidor se inicia en `http://localhost:5055`

### 3. Iniciar el Bot en Línea de Comandos

En otra **terminal**:

```bash
rasa shell
```

Ahora puedes chatear con el bot:

```
Your input -> hola
Hola! Soy el asistente de citas médicas. ¿En qué puedo ayudarte?

Your input -> necesito una cita
¿Cuál es tu nombre?

Your input -> Juan García
¿Para qué fecha deseas la cita?

Your input -> 2025-12-20
¿Qué especialidad necesitas?

Your input -> cardiología
Cita reservada exitosamente...
```

### 4. Iniciar con API REST

```bash
rasa run --enable-api --cors "*"
```

Luego haz requests a `http://localhost:5005/webhooks/rest/webhook`

---

## 🧪 Pruebas

### Ejecutar Test Stories

```bash
rasa test
```

Valida que las historias en `tests/test_stories.yml` se completen correctamente.

### Validar Datos de Entrenamiento

```bash
rasa data validate
```

Verifica:
- ✅ Intents consistentes
- ✅ Entidades bien anotadas
- ✅ Duplicados en NLU

---

## 📊 Flujos Conversacionales (Stories)

Los stories en `data/stories.yml` definen conversaciones válidas:

```yaml
- story: reservar cita con form
  steps:
  - intent: saludar
  - action: utter_saludar
  - intent: pedir_cita
  - action: cita_form          # Activa el formulario
  - active_loop: cita_form
  - active_loop: null          # Cierra el formulario
  - action: action_reservar_cita
```

---

## 🔌 Configuración de Endpoints

**endpoints.yml** define dónde se ejecutan las acciones:

```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

---

## 🐛 Troubleshooting

### Problema: "Action not found"

**Causa**: El servidor de acciones no está corriendo  
**Solución**:
```bash
rasa run actions  # En terminal separada
```

### Problema: "No intent matched"

**Causa**: El usuario escribió algo no reconocido  
**Solución**: Agregar más ejemplos al intent en `data/nlu.yml`:
```yaml
- intent: pedir_cita
  examples: |
    - necesito una cita
    - quiero reservar
    - solicito turno
    - dame una cita urgente
```

### Problema: Entidad no se extrae

**Causa**: La regex o ejemplos no son suficientes  
**Solución**:
```yaml
- regex: especialidad
  examples: |
    - (cardiología|cardiology|corazón|cardia)
```

### Problema: "Module 'rasa' has no attribute 'run'"

**Causa**: Versión incorrecta de RASA  
**Solución**:
```bash
pip install --upgrade rasa==3.4.0
```

### Limpiar Cache y Reentrenar

```bash
# Eliminar modelo antiguo
rmdir /s models

# Reentrenar
rasa train

# Usar nuevo modelo
rasa shell
```

---

## 💾 Almacenamiento de Datos

Actualmente, las citas se almacenan **en memoria** en la variable `citas_reservadas`:

```python
citas_reservadas = [
    {
        "id": 1,
        "nombre": "Juan García",
        "fecha": "2025-12-20",
        "especialidad": "cardiología",
        "timestamp": "2025-11-24 15:30:45"
    }
]
```

⚠️ **Nota**: Los datos se pierden al reiniciar el bot. Para persistencia:

### Opción A: Base de Datos SQLite

```python
import sqlite3

def guardar_cita(cita):
    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO citas (nombre, fecha, especialidad)
                      VALUES (?, ?, ?)''', 
                   (cita['nombre'], cita['fecha'], cita['especialidad']))
    conn.commit()
    conn.close()
```

### Opción B: Base de Datos PostgreSQL

```python
import psycopg2

conn = psycopg2.connect("dbname=medico user=postgres password=****")
cursor = conn.cursor()
cursor.execute("INSERT INTO citas VALUES (%s, %s, %s)", (nombre, fecha, especialidad))
conn.commit()
```

---

## 📝 Mejoras Futuras

- [ ] Integrar base de datos persistente
- [ ] Agregar notificaciones por email/SMS
- [ ] Conexión con calendario (Google Calendar, Outlook)
- [ ] Validación de fechas disponibles
- [ ] Autenticación de usuarios
- [ ] Integración con plataformas (Telegram, WhatsApp, Facebook)
- [ ] Análisis de sentimientos
- [ ] Generación de reportes

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'Agregar mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y disponible bajo la licencia MIT.

---

## 📞 Soporte

Para dudas o problemas, abre un issue en el repositorio de GitHub:  
[github.com/ngcddev/RASA-BotMedico/issues](https://github.com/ngcddev/RASA-BotMedico/issues)

---

## 🎯 Resumen Rápido

| Comando | Propósito |
|---------|-----------|
| `rasa train` | Entrenar modelo |
| `rasa shell` | Chat interactivo |
| `rasa run actions` | Iniciar servidor de acciones |
| `rasa test` | Ejecutar pruebas |
| `rasa data validate` | Validar datos NLU |
| `rasa run --enable-api` | Iniciar API REST |

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0  
**Estado**: En desarrollo activo 🚀

