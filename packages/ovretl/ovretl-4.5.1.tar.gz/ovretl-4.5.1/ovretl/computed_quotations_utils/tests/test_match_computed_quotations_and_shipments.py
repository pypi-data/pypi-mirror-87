import numpy as np
import pandas as pd

from ovretl import match_computed_quotations_and_shipments


def test_match_computed_quotations_and_shipments():
    cq_df = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4, 5, 6],
            "shipment_id": [0, 0, 1, 1, 2, 2],
            "proposition_id": [1, np.nan, 5, np.nan, np.nan, np.nan],
            "created_at": [1, 2, 3, 4, 6, 5],
            "foresea_name": [0, 0, 0, 0, np.nan, np.nan],
            "auto": [False, False, True, True, False, False],
        }
    )
    shipments_df = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4, 10],
            "foresea_name": [0, 0, np.nan, np.nan, 10],
            "proposition_id": [1, 2, 3, 4, np.nan],
            "kronos_state": ["sent", np.nan, "auto", np.nan, "auto"],
        }
    )
    result_should_be = pd.DataFrame(
        data={
            "computed_quotation_id": [5, 3, 1],
            "shipment_id": [2, 1, 0],
            "proposition_id": [np.nan, 5, 1],
            "created_at": [6, 3, 1],
            "kronos_state": [np.nan, np.nan, "sent"],
        }
    )
    result = match_computed_quotations_and_shipments(cq_df, shipments_df)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), result_should_be.reset_index(drop=True))
