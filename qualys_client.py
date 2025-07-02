"""
Simulated Qualys client — always “lags” SCCM by a bit.
"""

import random
from datetime import datetime

class FakeQualysClient:
    def __init__(self):  # token arg ignored
        self._cache = {}

    def get_compliance_by_qid(self, qid: str, sccm_ok: int, total: int) -> dict:
        # First call => cache baseline
        if qid not in self._cache:
            self._cache[qid] = 0

        # creep toward SCCM’s installed count
        self._cache[qid] = min(
            total, 
            self._cache[qid] + random.randint(0, 3),     # smaller steps
        )
        passed = self._cache[qid]
        failed = total - passed
        return {
            "total_hosts": total,
            "passed": passed,
            "failed": failed,
            "last_scanned": datetime.utcnow().isoformat() + "Z",
        }
