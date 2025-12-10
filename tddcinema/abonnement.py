"""Gestion des abonnements UGC pour le TD TDDCinema.

Les réponses aux questions du sujet sont indiquées dans les commentaires
numérotés Q1 à Q11.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, Tuple


class Formula(Enum):
    """Référentiel des formules d'abonnement."""

    ILLIMITE_26_PLUS = "UGC Illimité 26+"
    ILLIMITE_26_MINUS = "UGC Illimité -26"
    ILLIMITE_2_PERS = "UGC Illimité 2 personnes"
    FAMILLE = "UGC Illimité Famille"
    ILLIMITE_WEEKEND = "UGC Illimité Week-end"
    ILLIMITE_SEMAINE = "UGC Illimité Semaine"
    ILLIMITE_3D = "UGC Illimité + 1er film 3D inclus"
    CINE_PLUS_CANAL = "CINE+ / 1 Canal+"
    CINE_DAY = "UGC Illimité CINE DAY"


@dataclass(frozen=True)
class TariffPlan:
    monthly_fee: Decimal
    first_payment_brackets: Tuple[Decimal, Decimal, Decimal, Decimal]

    def first_payment_for_day(self, start_day: int) -> Decimal:
        """Retourne le montant du premier paiement en fonction du jour du mois."""

        if not 1 <= start_day <= 31:
            raise ValueError("Le jour de début doit être compris entre 1 et 31")
        if start_day <= 8:
            return self.first_payment_brackets[0]
        if start_day <= 16:
            return self.first_payment_brackets[1]
        if start_day <= 22:
            return self.first_payment_brackets[2]
        return self.first_payment_brackets[3]


# Q1 - Calculs théoriques : on compare les mensualités 1 mois avec 6/12 mois.
# Le total annuel de référence est mensualité * 12. Pour vérifier la cohérence des
# formules 6 mois, on calcule (mensualité x 6) et on applique le premier paiement
# spécifique deux fois pour simuler deux périodes de 6 mois ; on retient l'offre la
# moins chère. Les optimisations favorables au consommateur incluent l'alignement
# du premier paiement sur la mensualité à partir du 17 du mois ou l'ajout d'un mois
# offert lors d'un engagement 12 mois.


# Tarifs mensuels (tableau 1)
TABLE_1: Dict[Formula, TariffPlan] = {
    Formula.ILLIMITE_26_PLUS: TariffPlan(
        monthly_fee=Decimal("22.90"),
        first_payment_brackets=(
            Decimal("45.80"),
            Decimal("30.53"),
            Decimal("30.60"),
            Decimal("22.90"),
        ),
    ),
    Formula.ILLIMITE_26_MINUS: TariffPlan(
        monthly_fee=Decimal("17.90"),
        first_payment_brackets=(
            Decimal("35.80"),
            Decimal("24.79"),
            Decimal("23.87"),
            Decimal("17.90"),
        ),
    ),
    Formula.ILLIMITE_2_PERS: TariffPlan(
        monthly_fee=Decimal("36.80"),
        first_payment_brackets=(
            Decimal("73.60"),
            Decimal("49.32"),
            Decimal("49.26"),
            Decimal("36.80"),
        ),
    ),
    Formula.FAMILLE: TariffPlan(
        monthly_fee=Decimal("37.90"),
        first_payment_brackets=(
            Decimal("75.80"),
            Decimal("50.59"),
            Decimal("50.56"),
            Decimal("37.90"),
        ),
    ),
    Formula.ILLIMITE_WEEKEND: TariffPlan(
        monthly_fee=Decimal("16.90"),
        first_payment_brackets=(
            Decimal("33.80"),
            Decimal("22.43"),
            Decimal("22.53"),
            Decimal("16.90"),
        ),
    ),
    Formula.ILLIMITE_SEMAINE: TariffPlan(
        monthly_fee=Decimal("19.90"),
        first_payment_brackets=(
            Decimal("39.80"),
            Decimal("27.46"),
            Decimal("26.53"),
            Decimal("19.90"),
        ),
    ),
}

# Tarifs 6 ou 12 mois (tableau 2)
TABLE_2: Dict[Formula, TariffPlan] = {
    Formula.ILLIMITE_26_PLUS: TariffPlan(
        monthly_fee=Decimal("22.90"),
        first_payment_brackets=(
            Decimal("29.59"),
            Decimal("22.90"),
            Decimal("22.90"),
            Decimal("22.90"),
        ),
    ),
    Formula.ILLIMITE_26_MINUS: TariffPlan(
        monthly_fee=Decimal("17.90"),
        first_payment_brackets=(
            Decimal("20.84"),
            Decimal("17.90"),
            Decimal("17.90"),
            Decimal("17.90"),
        ),
    ),
    Formula.ILLIMITE_2_PERS: TariffPlan(
        monthly_fee=Decimal("36.80"),
        first_payment_brackets=(
            Decimal("42.93"),
            Decimal("36.80"),
            Decimal("36.80"),
            Decimal("36.80"),
        ),
    ),
    Formula.FAMILLE: TariffPlan(
        monthly_fee=Decimal("37.90"),
        first_payment_brackets=(
            Decimal("44.24"),
            Decimal("37.90"),
            Decimal("37.90"),
            Decimal("37.90"),
        ),
    ),
    Formula.ILLIMITE_3D: TariffPlan(
        monthly_fee=Decimal("30.90"),
        first_payment_brackets=(
            Decimal("30.90"),
            Decimal("30.90"),
            Decimal("30.90"),
            Decimal("30.90"),
        ),
    ),
    Formula.CINE_PLUS_CANAL: TariffPlan(
        monthly_fee=Decimal("44.90"),
        first_payment_brackets=(
            Decimal("44.90"),
            Decimal("44.90"),
            Decimal("44.90"),
            Decimal("44.90"),
        ),
    ),
    Formula.CINE_DAY: TariffPlan(
        monthly_fee=Decimal("8"),
        first_payment_brackets=(
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
        ),
    ),
}


class Abonnement:
    """Modélisation d'un abonnement UGC.

    Les méthodes retournent des `Decimal` arrondis à deux décimales.
    """

    def __init__(
        self,
        formula: Formula,
        duration_months: int,
        start_date: date,
        adults: int = 1,
        children: int = 0,
        livret_presented: bool = False,
    ) -> None:
        # Q3 - Le SUT (System Under Test) est ici la classe Abonnement car c'est
        # l'objet principal testé par les tests unitaires qui vont driver le code.
        self.formula = formula
        self.duration_months = duration_months
        self.start_date = start_date
        self.adults = adults
        self.children = children
        self.livret_presented = livret_presented
        self._tariff = self._resolve_tariff()

        # Q4 - Validation de l'abonnement Famille : l'agent vérifie la présence du
        # livret de famille et le respect du quota (max 2 adultes, 2 enfants). La
        # classe expose `validate_family()` pour reproduire ce contrôle.
        if self.formula is Formula.FAMILLE and not self.validate_family():
            raise ValueError("Composition familiale ou justificatif invalide")

    def _resolve_tariff(self) -> TariffPlan:
        if self.duration_months == 1:
            table = TABLE_1
        elif self.duration_months in (6, 12):
            table = TABLE_2
        else:
            raise ValueError("Durée d'abonnement non prise en charge (1, 6 ou 12 mois)")

        try:
            return table[self.formula]
        except KeyError as exc:  # pragma: no cover - garde de sécurité
            raise ValueError("Formule incompatible avec la durée choisie") from exc

    @property
    def monthly_fee(self) -> Decimal:
        return self._tariff.monthly_fee

    @property
    def first_payment(self) -> Decimal:
        payment = self._tariff.first_payment_for_day(self.start_date.day)
        return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total_cost(self) -> Decimal:
        """Calcule le coût total de l'abonnement sur la durée.

        Q2 - Exemple : pour 6 mois d'Illimité démarrant le 9, le premier paiement
        est de 22,90€ (tableau 2, deuxième tranche) puis 5 mensualités à 22,90€.
        Total = 22,90 + (22,90 x 5) = 137,40€. La formule se généralise pour
        toutes les tranches et durées : total = premier_paiement + mensualité x
        (durée - 1).
        """

        remaining_months = max(self.duration_months - 1, 0)
        total = self.first_payment + (self.monthly_fee * remaining_months)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def validate_family(self) -> bool:
        if self.formula is not Formula.FAMILLE:
            return True
        return self.adults <= 2 and self.children <= 2 and self.livret_presented

    def __str__(self) -> str:  # pragma: no cover - testé via tests dédiés
        return (
            f"Formule: {self.formula.value} | Durée: {self.duration_months} mois | "
            f"Mensualité: {self.monthly_fee}€ | 1er paiement: {self.first_payment}€ | "
            f"Début: {self.start_date.isoformat()}"
        )

    # Q5 - Le nom Abonnement est conservé pour refléter l'objet métier final et
    # éviter une classe Formule qui serait trop restrictive. Le design reste
    # ouvert : on pourra refactorer après l'écriture des tests (phase 3 du TDD)
    # pour extraire des classes ou renommer si besoin.


# Q8 - Plan de tests : d'abord les calculs simples (week-end individuel), puis
# les affichages utilisateur, ensuite les validations métier (famille, durées
# interdites), enfin les totaux multi-mois. Cet ordre favorise un TDD progressif
# du plus simple au plus complexe et permet un partage clair des tâches en binôme.
#
# Q9 - L'ordre des tests dans les fichiers n'influe pas sur l'exécution pytest :
# l'indépendance des tests doit être garantie, même si la lecture est séquentielle.


# Q11 - Bilan GIT : commits effectués après chaque test vert significatif et à la
# fin de chaque fonctionnalité, push régulier pour partager avec le binôme et
# sécuriser l'avancement.
