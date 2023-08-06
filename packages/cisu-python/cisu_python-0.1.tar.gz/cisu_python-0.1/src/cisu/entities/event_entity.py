from dataclasses import dataclass

from .commons import DateType, Severity, LocationType


@dataclass
class EventEntity:
    """
        Identifiant fonctionnel unique de l'affaire. Il doit pouvoir être généré de façon
            unique et décentralisée et ne présenter aucune ambiguïté.

        Attributes
        ----------
        eventId: str
        createdAt: DateType
            Groupe date heure de création de l'affaire. Il doit être renseigné à la fin du processus de la
                création
                de la première alerte. Lors de l'ajout d'alerte à une affaire ce champ ne doit pas être modifié.
                L'indicateur de fuseau horaire Z ne doit pas être utilisé. Le fuseau horaire pour UTC doit être
                représenté
                par '-00:00'.
        severity: Severity
        eventLocation: LocationType
            Localisation de l'affaire. Celle-ci est issue de la première alerte et ne doit pas être modifiée
                lors des nouvelles alertes associées à l'affaire en cours.

    """
    eventId: str
    createdAt: DateType
    severity: Severity
    eventLocation: LocationType
