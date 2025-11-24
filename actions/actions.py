
#================================================================================
#    RASA-BotMédico - Acciones Personalizadas
#================================================================================
#Módulo que contiene las acciones personalizadas del chatbot para gestionar
#citas médicas. Las acciones son funciones que se ejecutan cuando el bot
#necesita realizar lógica de negocio más allá de respuestas simples.

#Acciones disponibles:
#    - ActionReservarCita: Reserva una nueva cita médica
#    - ActionCancelarCita: Cancela la última cita reservada
#    - ActionConsultarCitas: Lista todas las citas registradas

#Autor: RASA-BotMédico Team
#Fecha: Noviembre 2025
#================================================================================


# ============================================================================
# IMPORTACIONES
# ============================================================================
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

# ============================================================================
# ALMACENAMIENTO TEMPORAL EN MEMORIA
# ============================================================================
# Lista global que almacena todas las citas reservadas
# NOTA: Los datos se pierden al reiniciar el bot. Para persistencia,
# integrar con una base de datos (SQLite, PostgreSQL, MongoDB, etc.)
citas_reservadas = []


# ============================================================================
# CLASE: ActionReservarCita
# ============================================================================
class ActionReservarCita(Action):
    
    #Acción para reservar una nueva cita médica.
    
    #Extrae los datos del usuario (nombre, fecha, especialidad) desde los slots
    #(memoria del bot), valida que estén completos, y los almacena en la lista
    #de citas reservadas.
    
    #Atributos:
    #    - citas_reservadas: Lista global donde se guardan las citas
        
    #Métodos:
    #    - name(): Retorna el identificador de la acción
    #    - run(): Ejecuta la lógica de reserva de cita
    

    def name(self) -> Text:
        
        #Retorna el nombre identificador de la acción.
        #ste nombre debe coincidir con el definido en domain.yml
        
        #Returns:
        #    str: "action_reservar_cita"
        
        return "action_reservar_cita"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Ejecuta la lógica de reserva de cita médica.
        
        #El flujo es:
        #1. Obtener datos del usuario desde los slots
        #2. Validar que todos los datos estén presentes
        #3. Crear objeto cita con ID único y timestamp
        #4. Guardar la cita en la lista global
        #5. Enviar confirmación al usuario
        
        #Args:
        #    dispatcher (CollectingDispatcher): Objeto para enviar mensajes al usuario
        #    tracker (Tracker): Contiene el estado de la conversación, slots y eventos
        #    domain (Dict): Definición de intents, entidades, acciones del bot
            
        #Returns:
        #    List[Dict]: Lista vacía (sin eventos adicionales que registrar)
        
        
        # ====================================================================
        # OBTENER DATOS DEL USUARIO DESDE LOS SLOTS
        # ====================================================================
        # Los slots son variables que almacenan información durante la 
        # conversación. Se llenan automáticamente cuando se detectan entidades
        # correspondientes.
        nombre = tracker.get_slot("nombre")
        fecha = tracker.get_slot("fecha")
        especialidad = tracker.get_slot("especialidad")
        
        # ====================================================================
        # VALIDAR QUE TODOS LOS DATOS ESTÉN DISPONIBLES
        # ====================================================================
        if nombre and fecha and especialidad:
            # Crear diccionario con toda la información de la cita
            cita = {
                "id": len(citas_reservadas) + 1,  # ID autoincremental
                "nombre": nombre,                  # Nombre del paciente
                "fecha": fecha,                    # Fecha de la cita
                "especialidad": especialidad,      # Especialidad médica
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha/hora de registro
            }
            
            # Agregar la cita a la lista global
            citas_reservadas.append(cita)
            
            # ================================================================
            # CONSTRUIR MENSAJE DE CONFIRMACIÓN
            # ================================================================
            # Crear un mensaje formateado con los detalles de la cita
            mensaje = f"Cita reservada exitosamente:\n" \
                     f"ID: {cita['id']}\n" \
                     f"Paciente: {nombre}\n" \
                     f"Especialidad: {especialidad}\n" \
                     f"Fecha: {fecha}"
            
            # Enviar el mensaje de confirmación al usuario
            dispatcher.utter_message(text=mensaje)
        else:
            # Si faltan datos, informar al usuario
            dispatcher.utter_message(text="Faltan datos para completar la reserva.")
        
        # Retornar lista vacía (RASA maneja los eventos internamente)
        return []


# ============================================================================
# CLASE: ActionCancelarCita
# ============================================================================
class ActionCancelarCita(Action):
    
    #Acción para cancelar la última cita médica registrada.
    
    #Verifica si hay citas disponibles y elimina la más reciente de la lista,
    #mostrando los detalles de la cita cancelada.
    
    #Atributos:
    #    - citas_reservadas: Lista global de donde se elimina la cita
        
    #Métodos:
    #    - name(): Retorna el identificador de la acción
    #    - run(): Ejecuta la lógica de cancelación
    

    def name(self) -> Text:
        ###
        #Retorna el nombre identificador de la acción.
        
        #Returns:
        #    str: "action_cancelar_cita"
        ###
        return "action_cancelar_cita"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Ejecuta la lógica de cancelación de la última cita.
        
        #El flujo es:
        #1. Verificar si hay citas disponibles
        #2. Eliminar la última cita usando pop()
        #3. Mostrar detalles de la cita cancelada
        #4. Si no hay citas, informar al usuario
        
        #Args:
        #    dispatcher (CollectingDispatcher): Objeto para enviar mensajes
        #    tracker (Tracker): Estado actual de la conversación
        #    domain (Dict): Definición del bot
            
        #Returns:
        #    List[Dict]: Lista vacía
        
        
        # ====================================================================
        # VERIFICAR SI HAY CITAS PARA CANCELAR
        # ====================================================================
        if citas_reservadas:
            # Eliminar la última cita de la lista (LIFO - Last In First Out)
            cita_cancelada = citas_reservadas.pop()
            
            # Construir mensaje con detalles de la cita cancelada
            mensaje = f"Cita cancelada:\n" \
                     f"ID: {cita_cancelada['id']}\n" \
                     f"Paciente: {cita_cancelada['nombre']}"
            
            # Enviar confirmación de cancelación
            dispatcher.utter_message(text=mensaje)
        else:
            # Informar si no hay citas para cancelar
            dispatcher.utter_message(text="No hay citas para cancelar.")
        
        return []


# ============================================================================
# CLASE: ActionConsultarCitas
# ============================================================================
class ActionConsultarCitas(Action):
    
    #Acción para listar todas las citas médicas registradas.
    
    #Recorre la lista de citas y presenta un resumen formateado de cada una,
    #incluyendo ID, paciente, especialidad, fecha y fecha de registro.
    
    #Atributos:
    #    - citas_reservadas: Lista global de donde se leen las citas
        
    #Métodos:
    #    - name(): Retorna el identificador de la acción
    #    - run(): Ejecuta la lógica de consulta
    

    def name(self) -> Text:
        
        #Retorna el nombre identificador de la acción.
        
        #Returns:
        #    str: "action_consultar_citas"
        
        return "action_consultar_citas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ###
        #Ejecuta la lógica de consulta de citas.
        
        #El flujo es:
        #1. Verificar si hay citas registradas
        #2. Construir tabla formateada con todas las citas
        #3. Iterar sobre cada cita y agregar sus detalles
        #4. Enviar la lista completa al usuario
        #5. Si no hay citas, informar al usuario
        
        #Args:
        #    dispatcher (CollectingDispatcher): Objeto para enviar mensajes
        #    tracker (Tracker): Estado actual de la conversación
        #    domain (Dict): Definición del bot
            
        #Returns:
        #    List[Dict]: Lista vacía
        ###
        
        # ====================================================================
        # VERIFICAR SI HAY CITAS REGISTRADAS
        # ====================================================================
        if citas_reservadas:
            # Inicializar mensaje con encabezado
            mensaje = "Citas registradas:\n\n"
            
            # ================================================================
            # ITERAR SOBRE TODAS LAS CITAS Y CONSTRUIR TABLA
            # ================================================================
            for cita in citas_reservadas:
                # Agregar detalles de cada cita al mensaje
                mensaje += f"ID: {cita['id']}\n" \
                          f"Paciente: {cita['nombre']}\n" \
                          f"Especialidad: {cita['especialidad']}\n" \
                          f"Fecha: {cita['fecha']}\n" \
                          f"Registrada: {cita['timestamp']}\n\n"
            
            # Enviar lista completa de citas
            dispatcher.utter_message(text=mensaje)
        else:
            # Informar si no hay citas registradas
            dispatcher.utter_message(text="No hay citas registradas actualmente.")
        
        return []