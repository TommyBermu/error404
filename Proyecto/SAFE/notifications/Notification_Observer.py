from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class Subject(ABC):
    """
    Interfaz Subject para gestionar observadores (usuarios suscritos a notificaciones).
    """

    @abstractmethod
    def Suscribir(self, observer: Usuario) -> None:
        """Suscribir un usuario."""
        pass

    @abstractmethod
    def Desuscribir(self, observer: Usuario) -> None:
        """Desuscribir un usuario."""
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        """Notificar a todos los usuarios."""
        pass


class CourseNotificationSystem(Subject):
    """
    Sistema de notificaciones para cursos en SAFE.
    Notifica a estudiantes sobre: nuevas asignaciones, cambios de contenido,
    actualizaciones de progreso, etc.
    """

    def __init__(self, topic_name: str):
        self.topic_name = topic_name
        self.course_name = topic_name  # Consistent attribute for course name
        self._observers: List[Usuario] = []
        self._notification_history: List[dict] = []

    def Suscribir(self, observer: Usuario) -> None:
        """Estudiante se suscribe a notificaciones del tema."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"{observer.get_name()} se ha suscrito a notificaciones de '{self.topic_name}'")

    def Desuscribir(self, observer: Usuario) -> None:
        """Estudiante cancela suscripción a notificaciones."""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"{observer.get_name()} se ha desuscrito de '{self.topic_name}'")

    def notify(self, message: str, notification_type: str = "INFO") -> None:
        """
        Envía notificación a todos los estudiantes suscritos.
        
        Args:
            message: Contenido de la notificación
            notification_type: Tipo de notificación (INFO, ASSIGNMENT, GRADE, CONTENT)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        notification = {
            "course": self.course_name,
            "type": notification_type,
            "message": message,
            "timestamp": timestamp
        }
        
        self._notification_history.append(notification)

        print(f"\n[{notification_type}] Notificando sobre '{self.topic_name}'...")
        print(f"   Mensaje: {message}")
        print(f"   Hora: {timestamp}")
        
        for observer in self._observers:
            observer.update(notification)

    def new_assignment_published(self, assignment_name: str, due_date: str) -> None:
        """Profesor publica nueva asignación."""
        message = f"Nueva asignación disponible: '{assignment_name}'. Fecha límite: {due_date}"
        self.notify(message, "ASSIGNMENT")

    def content_updated(self, content_title: str) -> None:
        """Profesor actualiza contenido del curso."""
        message = f"Se ha actualizado el contenido: '{content_title}'"
        self.notify(message, "CONTENT")

    def grade_published(self, assignment_name: str) -> None:
        """Profesor publica calificaciones."""
        message = f"Calificaciones publicadas para: '{assignment_name}'"
        self.notify(message, "GRADE")


class Usuario(ABC):
    """
    Interfaz Usuario para usuarios que reciben notificaciones.
    """

    @abstractmethod
    def update(self, notification: dict) -> None:
        """Recibe actualización del sistema de notificaciones."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre del observador."""
        pass


class StudentObserver(Usuario):
    """
    Estudiante que recibe notificaciones sobre sus cursos.
    """

    def __init__(self, student_id: str, student_name: str, email: str):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.notifications: List[dict] = []

    def update(self, notification: dict) -> None:
        """Recibe y procesa notificación."""
        self.notifications.append(notification)
        
        # Simulación de envío de notificación
        print(f"   Notificación para {self.student_name}: {notification['message']}")
        
        # Aquí se integraría con sistema de envío real:
        # - Email
        # - Notificación push
        # - Almacenar en base de datos

    def get_name(self) -> str:
        return self.student_name

    def get_unread_notifications_count(self) -> int:
        """Retorna cantidad de notificaciones no leídas."""
        return len(self.notifications)




class InstructorObserver(Usuario):
    """
    Instructor que recibe notificaciones sobre actividad en sus cursos.
    Por ejemplo: entregas de asignaciones, preguntas de estudiantes, etc.
    """

    def __init__(self, instructor_id: str, instructor_name: str, email: str):
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.email = email
        self.notifications: List[dict] = []

    def update(self, notification: dict) -> None:
        """Recibe notificación sobre actividad en el curso."""
        self.notifications.append(notification)
        print(f"   👨‍🏫 → Instructor {self.instructor_name} notificado")

    def get_name(self) -> str:
        return f"Prof. {self.instructor_name}"


# ============================================
# DEMOSTRACIÓN DEL PATRÓN
# ============================================

if __name__ == "__main__":
 

    # Crear sistema de notificaciones para un curso (usa topic_name internamente)
    ingesoft_course = CourseNotificationSystem("Ingeniería de Software")
    # Ya no es necesario usar setattr, course_name se define en el constructor

    # Crear observadores
    alumno_a = StudentObserver("S001", "Juan Pérez", "juan.perez@univ.edu")
    alumno_b = StudentObserver("S002", "María González", "maria.gonzalez@univ.edu")
    profesor = InstructorObserver("I001", "Dr. Rodríguez", "rodriguez@univ.edu")

    # Suscribir (revisado: usar Suscribir / Desuscribir)
    ingesoft_course.Suscribir(alumno_a)
    ingesoft_course.Suscribir(alumno_b)
    ingesoft_course.Suscribir(profesor)

    # Publicar una asignación y una actualización de contenido
    ingesoft_course.new_assignment_published("Tarea 1: Ejemplos", "2025-01-15")
    ingesoft_course.content_updated("Apuntes - Capítulo 1")

    # Desuscribir a María
    ingesoft_course.Desuscribir(alumno_b)

    # Resumen simple de notificaciones (usar método del alumno y len() para el instructor)
    print("\nResumen:")
    print(f"{alumno_a.get_name()}: {alumno_a.get_unread_notifications_count()} notificaciones")
    print(f"{alumno_b.get_name()}: {alumno_b.get_unread_notifications_count()} notificaciones")
    print(f"{profesor.get_name()}: {len(profesor.notifications)} notificaciones")

    
