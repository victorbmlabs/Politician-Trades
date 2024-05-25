from type import Trade


def qualify(trade: Trade):
    """Checks if the Trade qualifies for us to copy"""
    order = trade.tx_type

    if order == "buy":
        pass

    elif order == "sell":
        pass

    else:
        pass
