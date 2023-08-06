import pandas as pd


def cq_missing_categories(computed_quotations_df: pd.DataFrame):
    category_complete = computed_quotations_df.groupby("category").apply(
        lambda group: group["kronos_selected"].any()  # or group["selected"].any()
    )
    if False in category_complete.values:
        return category_complete.value_counts()[False]
    return 0


def add_missing_categories(computed_quotations_with_ocp_df: pd.DataFrame):
    cq_fullness = computed_quotations_with_ocp_df.groupby(by=["computed_quotation_id"]).apply(cq_missing_categories)

    computed_quotations_with_ocp_df = pd.merge(
        computed_quotations_with_ocp_df,
        cq_fullness.to_frame(name="missing_categories"),
        left_on="computed_quotation_id",
        right_index=True,
    )
    computed_quotations_with_ocp_df["full"] = computed_quotations_with_ocp_df["missing_categories"].apply(
        lambda x: x == 0
    )
    computed_quotations_with_ocp_df.loc[:, "proposition_id"] = computed_quotations_with_ocp_df["proposition_id"].apply(
        lambda x: int(x) if not pd.isna(x) else x
    )
    return computed_quotations_with_ocp_df
