"""Verify scenario arithmetic and the input contract independently of the UI."""

import math

import pytest

from calculator import MAX_INSTALLATION_COST, MAX_MONTHLY_BILL, calculate_solar_savings


def test_default_scenario():
    result = calculate_solar_savings(200, 12000, 50)
    assert result.monthly_savings == 100
    assert result.new_monthly_bill == 100
    assert result.annual_savings == 1200
    assert result.simple_payback_years == 10


def test_fractional_inputs_are_not_rounded_in_calculation():
    result = calculate_solar_savings(123.45, 9876.54, 33.3)
    assert result.monthly_savings == pytest.approx(41.10885)
    assert result.new_monthly_bill == pytest.approx(82.34115)
    assert result.annual_savings == pytest.approx(493.3062)
    assert result.simple_payback_years == pytest.approx(20.02112, rel=1e-5)


@pytest.mark.parametrize("bill,cost,reduction", [(200, 12000, 0), (0, 12000, 50), (0, 0, 0), (200, 0, 0)])
def test_zero_savings_has_no_payback(bill, cost, reduction):
    result = calculate_solar_savings(bill, cost, reduction)
    assert result.monthly_savings == 0
    assert result.annual_savings == 0
    assert result.simple_payback_years is None
    assert result.new_monthly_bill == bill


def test_zero_cost_with_savings_has_zero_payback():
    assert calculate_solar_savings(200, 0, 50).simple_payback_years == 0


def test_full_reduction_has_zero_remaining_bill():
    result = calculate_solar_savings(200, 12000, 100)
    assert result.new_monthly_bill == 0
    assert result.annual_savings == 2400
    assert result.simple_payback_years == 5


def test_cumulative_savings_are_gross_and_include_year_zero():
    result = calculate_solar_savings(200, 12000, 50)
    savings = result.cumulative_savings()
    assert len(savings) == 21
    assert savings[0] == 0
    assert savings[10] == result.installation_cost
    assert savings[20] == 24000


@pytest.mark.parametrize("values", [
    (-1, 12000, 50), (200, -1, 50), (200, 12000, -1), (200, 12000, 101),
    (MAX_MONTHLY_BILL + 1, 12000, 50), (200, MAX_INSTALLATION_COST + 1, 50),
])
def test_out_of_range_inputs_raise_a_clear_error(values):
    with pytest.raises(ValueError, match="must be between"):
        calculate_solar_savings(*values)


@pytest.mark.parametrize("position", [0, 1, 2])
@pytest.mark.parametrize("invalid", [math.nan, math.inf, -math.inf, True, "200", None, 10 ** 500])
def test_non_finite_or_non_numeric_inputs_are_rejected(position, invalid):
    values = [200, 12000, 50]
    values[position] = invalid
    with pytest.raises(ValueError, match="must be a"):
        calculate_solar_savings(*values)


@pytest.mark.parametrize("years", [-1, 101, 1.5, True, "20"])
def test_invalid_chart_horizon_is_rejected(years):
    with pytest.raises(ValueError, match="whole number"):
        calculate_solar_savings(200, 12000, 50).cumulative_savings(years)


def test_upper_bounds_remain_finite_and_bill_is_conserved():
    result = calculate_solar_savings(MAX_MONTHLY_BILL, MAX_INSTALLATION_COST, 100)
    assert math.isfinite(result.simple_payback_years)
    assert result.monthly_savings + result.new_monthly_bill == result.monthly_bill


def test_tiny_savings_do_not_produce_infinite_payback():
    result = calculate_solar_savings(1e-320, 12000, 50)
    assert result.simple_payback_years is None
