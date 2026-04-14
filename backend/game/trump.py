TRUMP_ORDER = ["spades", "diamonds", "hearts", "clubs"]


def get_trump_for_round(round_num: int) -> str:
    if round_num <= 0:
        raise ValueError("round_num must be >= 1")
    return TRUMP_ORDER[(round_num - 1) % len(TRUMP_ORDER)]
