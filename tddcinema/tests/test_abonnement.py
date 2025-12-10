import pytest
from datetime import date
from decimal import Decimal

from tddcinema.abonnement import Abonnement, Formula


@pytest.fixture
def may_2024():
    return date(2024, 5, 10)


def test_weekend_individuel_first_payment(may_2024):
    """Q6 - Vérifie le calcul de la formule Week-end individuelle (>26 ans).

    Date dans la tranche du 9 au 16 -> premier paiement 22,43€.
    """

    abonnement = Abonnement(
        formula=Formula.ILLIMITE_WEEKEND,
        duration_months=1,
        start_date=may_2024,
    )

    assert abonnement.first_payment == Decimal("22.43")
    assert abonnement.monthly_fee == Decimal("16.90")


def test_to_string_contains_details(may_2024):
    """Q7 - Vérifie la lisibilité de l'affichage utilisateur."""

    abonnement = Abonnement(
        formula=Formula.ILLIMITE_SEMAINE,
        duration_months=1,
        start_date=may_2024,
    )

    rendered = str(abonnement)
    assert "UGC Illimité Semaine" in rendered
    assert "Durée: 1 mois" in rendered
    assert "Mensualité: 19.90" in rendered
    assert "1er paiement: 27.46" in rendered
    assert "2024-05-10" in rendered


def test_family_validation_requires_documents():
    abonnement = Abonnement(
        formula=Formula.FAMILLE,
        duration_months=1,
        start_date=date(2024, 1, 5),
        adults=2,
        children=2,
        livret_presented=True,
    )

    assert abonnement.validate_family()

    with pytest.raises(ValueError):
        Abonnement(
            formula=Formula.FAMILLE,
            duration_months=1,
            start_date=date(2024, 1, 5),
            adults=3,
            children=2,
            livret_presented=False,
        )


def test_total_cost_for_multi_month():
    """Q10 - Test d'un calcul complet sur 6 mois."""

    abonnement = Abonnement(
        formula=Formula.ILLIMITE_26_PLUS,
        duration_months=6,
        start_date=date(2024, 5, 9),
    )

    # premier paiement 22,90 + 5 mensualités à 22,90 = 137,40
    assert abonnement.first_payment == Decimal("22.90")
    assert abonnement.total_cost == Decimal("137.40")


def test_invalid_duration():
    with pytest.raises(ValueError):
        Abonnement(
            formula=Formula.ILLIMITE_WEEKEND,
            duration_months=3,
            start_date=date(2024, 5, 1),
        )


def test_formula_not_available_for_duration():
    with pytest.raises(ValueError):
        Abonnement(
            formula=Formula.ILLIMITE_WEEKEND,
            duration_months=6,
            start_date=date(2024, 5, 1),
        )


def test_cineday_simple_first_payment():
    abonnement = Abonnement(
        formula=Formula.CINE_DAY,
        duration_months=6,
        start_date=date(2024, 5, 20),
    )

    assert abonnement.first_payment == Decimal("8.00")
    assert abonnement.total_cost == Decimal("48.00")
