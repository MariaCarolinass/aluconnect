class ProgressStatus:
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    REVIEWED = 'REVIEWED'

    CHOICES = [
        (STARTED, "Iniciado"),
        (COMPLETED, "Concluído"),
        (REVIEWED, "Revisado"),
    ]