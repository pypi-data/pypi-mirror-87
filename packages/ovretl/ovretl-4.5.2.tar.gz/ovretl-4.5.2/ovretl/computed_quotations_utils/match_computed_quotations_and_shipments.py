import pandas as pd


def match_computed_quotations_and_shipments(
    computed_quotations_df: pd.DataFrame, shipments_all_propositions_df: pd.DataFrame
):
    computed_quotations_df = computed_quotations_df.rename(columns={"id": "computed_quotation_id"})
    computed_quotations_df = computed_quotations_df.dropna(subset=["shipment_id"])

    # Add a foreign key, "foresea_name", to mark computed quotations which are the most relevant
    computed_quotations_df = pd.merge(
        computed_quotations_df.drop(["foresea_name", "auto"], axis=1),
        shipments_all_propositions_df[["foresea_name", "proposition_id", "kronos_state"]].dropna(
            subset=["proposition_id"]
        ),
        how="left",
        on="proposition_id",
    )

    # Sort with foresea_name first to put most relevant CQs first
    computed_quotations_df = computed_quotations_df.sort_values(
        by=["shipment_id", "foresea_name", "proposition_id", "created_at"], ascending=False,
    )
    computed_quotations_df = computed_quotations_df.drop_duplicates(subset=["shipment_id"])
    return computed_quotations_df.drop(["foresea_name"], axis=1, errors="ignore")
