"""Fee calculation. PLACEHOLDER.

We agreed to define the real rule once we look at a real statement together.
Right now, if MGMT_FEE_RATE is left as None in config.py, the Fee column simply
stays blank — the rest of the pipeline (Gross/Net NAV + screenshots) still works.
"""
from typing import Optional

import config
from shared.model import ClientResult


def calculate_fee(result: ClientResult) -> Optional[float]:
    # TODO(with sample): replace with your colleague's real fee rule, e.g.
    #   return round(result.net_nav * config.MGMT_FEE_RATE, 2)
    if config.MGMT_FEE_RATE is None or result.net_nav is None:
        return None
    return round(result.net_nav * config.MGMT_FEE_RATE, 2)
