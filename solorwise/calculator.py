"""Pure scenario arithmetic. No tariff, solar-generation or financial model."""

from dataclasses import dataclass
from math import isfinite
from numbers import Real


# Educational guardrails, not Malaysian market prices or technical limits.
MAX_MONTHLY_BILL = 100_000.0
MAX_INSTALLATION_COST = 10_000_000.0
HORIZON_YEARS = 20


@dataclass(frozen=True)
class SolarScenario:
    monthly_bill: float
    installation_cost: float
    reduction_percentage: float
    monthly_savings: float
    new_monthly_bill: float
    annual_savings: float
    simple_payback_years: float | None

    def cumulative_savings(self, years: int = HORIZON_YEARS) -> list[float]:
        """Gross savings at year 0 through ``years``; cost is not deducted."""
        if isinstance(years, bool) or not isinstance(years, int) or not 0 <= years <= 100:
            raise ValueError("Years must be a whole number from 0 to 100.")
        return [self.annual_savings * year for year in range(years + 1)]


def _validate_number(name: str, value: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a number.")
    try:
        value = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{name} must be a finite number.") from error
    if not isfinite(value):
        raise ValueError(f"{name} must be a finite number.")
    if not 0 <= value <= maximum:
        raise ValueError(f"{name} must be between 0 and {maximum:,.0f}.")
    return value


def calculate_solar_savings(
    monthly_bill: float,
    installation_cost: float,
    reduction_percentage: float,
) -> SolarScenario:
    """Calculate the user's hypothetical bill reduction with validated inputs.

    No positive savings means payback is not applicable, even with zero cost.
    Zero cost with positive savings gives an arithmetic payback of zero years.
    """
    bill = _validate_number("Monthly bill", monthly_bill, MAX_MONTHLY_BILL)
    cost = _validate_number("Installation cost", installation_cost, MAX_INSTALLATION_COST)
    reduction = _validate_number("Bill reduction", reduction_percentage, 100)
    monthly_savings = bill * (reduction / 100)
    annual_savings = monthly_savings * 12
    # Very small positive inputs can underflow or create an infinite quotient.
    # Such a scenario has no representable finite payback.
    payback = cost / annual_savings if annual_savings > 0 else None
    if payback is not None and not isfinite(payback):
        payback = None
    return SolarScenario(
        monthly_bill=bill,
        installation_cost=cost,
        reduction_percentage=reduction,
        monthly_savings=monthly_savings,
        new_monthly_bill=bill - monthly_savings,
        annual_savings=annual_savings,
        simple_payback_years=payback,
    )
