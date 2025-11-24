from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

# Almacenamiento temporal en memoria
citas_reservadas = []

class ActionReservarCita(Action):
    def name(self) -> Text:
        return "action_reservar_cita"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
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
            
            mensaje = f"✅ Cita reservada exitosamente:\n" \
                     f"ID: {cita['id']}\n" \
                     f"Paciente: {nombre}\n" \
                     f"Especialidad: {especialidad}\n" \
                     f"Fecha: {fecha}"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text="Faltan datos para completar la reserva.")
        
        return []

class ActionCancelarCita(Action):
    def name(self) -> Text:
        return "action_cancelar_cita"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if citas_reservadas:
            cita_cancelada = citas_reservadas.pop()
            mensaje = f"❌ Cita cancelada:\n" \
                     f"ID: {cita_cancelada['id']}\n" \
                     f"Paciente: {cita_cancelada['nombre']}"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text="No hay citas para cancelar.")
        
        return []

class ActionConsultarCitas(Action):
    def name(self) -> Text:
        return "action_consultar_citas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if citas_reservadas:
            mensaje = "📋 Citas registradas:\n\n"
            for cita in citas_reservadas:
                mensaje += f"ID: {cita['id']}\n" \
                          f"Paciente: {cita['nombre']}\n" \
                          f"Especialidad: {cita['especialidad']}\n" \
                          f"Fecha: {cita['fecha']}\n" \
                          f"Registrada: {cita['timestamp']}\n\n"
            dispatcher.utter_message(text=mensaje)
        else:
            dispatcher.utter_message(text="No hay citas registradas actualmente.")
        
        return []