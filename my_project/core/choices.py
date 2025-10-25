from django.db import models

#Choices para Users
class EstadoRoles(models.TextChoices):
    STUDENT = 'student', 'Estudiante'
    TEACHER = 'teacher', 'Docente'
    ADMIN = 'admin', 'Administrador'

#Choices para Study
class EstadoModes(models.TextChoices):
    CARDS = 'cards', 'Tarjetas'
    CRAM = 'cram', 'Repaso rápido'
    
class EstadoQuality(models.IntegerChoices):
    AGAIN = 0, 'Otra vez'
    HARD = 1, 'Difícil'
    GOOD = 2, 'Bien'
    EASY = 3, 'Fácil'

#Choices para Decks
class EstadoVisibility(models.TextChoices):
    PRIVATE = 'private', 'Privada'    
    PUBLIC = 'public', 'Pública'

class EstadoTypes(models.TextChoices):
    BASIC = 'basic', 'Básica'
    CLOZE = 'cloze', 'Cloze'
    IMAGE = 'image', 'Imagen'
    AUDIO = 'audio', 'Audio'
    
#Choices para Users - Idiomas
class EstadoIdiomas(models.TextChoices):
    ES = 'es', 'Español'
    EN = 'en', 'Inglés'
    FR = 'fr', 'Francés'
    DE = 'de', 'Alemán'
    IT = 'it', 'Italiano'
    PT = 'pt', 'Portugués'
    ZH = 'zh', 'Chino'
    JA = 'ja', 'Japonés'
    RU = 'ru', 'Ruso'
    AR = 'ar', 'Árabe'
    
#Choices para clases
class EstadoNivel(models.TextChoices):
    BEGINNER = 'beginner', 'Principiante'
    INTERMEDIATE = 'intermediate', 'Intermedio'
    ADVANCED = 'advanced', 'Avanzado'   