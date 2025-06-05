import math
import pytest
from scripts.model_scripts.waiting_lines import WaitingLinesArrival

def test_next_arrival_interval_time_calculation():
    lambda_value = 2  # λ = 2
    controller = WaitingLinesArrival(lambda_value)

    number = 0.5  # U = 0.5
    expected_iat = -math.log(1 - number) / lambda_value

    iat = controller.next_arrival_interval_time(number)

    assert math.isclose(iat, expected_iat, rel_tol=1e-6), "El IAT no fue calculado correctamente"
    assert math.isclose(controller.iat, expected_iat, rel_tol=1e-6), "El valor interno iat no fue actualizado correctamente"
    assert math.isclose(controller.at, expected_iat, rel_tol=1e-6), "El valor acumulado at no fue actualizado correctamente"

def test_multiple_arrivals_accumulate_at():
    controller = WaitingLinesArrival(lambda_value=1)

    num1 = 0.1
    num2 = 0.3
    iat1 = controller.next_arrival_interval_time(num1)
    iat2 = controller.next_arrival_interval_time(num2)

    expected_total_at = iat1 + iat2

    assert math.isclose(controller.at, expected_total_at, rel_tol=1e-6), "El tiempo acumulado at no coincide con la suma de IATs"
