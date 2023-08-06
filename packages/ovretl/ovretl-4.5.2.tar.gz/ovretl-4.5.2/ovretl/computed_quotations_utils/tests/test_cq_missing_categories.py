import pandas as pd
from ovretl.computed_quotations_utils.add_missing_categories import (
    cq_missing_categories,
    add_missing_categories,
)
from pandas.util.testing import assert_frame_equal


def test_cq_missing_categories_1():
    cq_df = pd.DataFrame(
        data={
            "category": ["freight", "freight", "departure_fees", "departure_fees"],
            "kronos_selected": [False, True, False, False],
            "selected": [False, False, False, False],
        }
    )
    assert cq_missing_categories(cq_df) == 1


def test_cq_missing_categories_2():
    cq_df = pd.DataFrame(
        data={
            "category": ["freight", "freight", "departure_fees", "departure_truck_freight",],
            "kronos_selected": [False, False, False, False],
            "selected": [False, True, True, False],
        }
    )
    assert cq_missing_categories(cq_df) == 3


def test_add_missing_categories():
    cq_df = pd.DataFrame(
        data={
            "category": ["freight", "freight", "departure_fees", "departure_fees", "freight",],
            "kronos_selected": [False, True, False, False, True],
            "selected": [False, False, False, False, False],
            "computed_quotation_id": [1, 1, 1, 1, 2],
            "proposition_id": [0, 0, 0, 0, 1],
        }
    )
    result_should_be = pd.DataFrame(
        data={
            "category": ["freight", "freight", "departure_fees", "departure_fees", "freight",],
            "kronos_selected": [False, True, False, False, True],
            "selected": [False, False, False, False, False],
            "computed_quotation_id": [1, 1, 1, 1, 2],
            "proposition_id": [0, 0, 0, 0, 1],
            "missing_categories": [1, 1, 1, 1, 0],
            "full": [False, False, False, False, True],
        }
    )
    result = add_missing_categories(cq_df)
    assert_frame_equal(result, result_should_be)
