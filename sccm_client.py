"""
Simulated SCCM client — drops external dependencies.
Returns synthetic counts that converge to 100 % after ±2 minutes.
"""

import random
import time

class FakeSCCMClient:
    def __init__(self, total_devices: int = 50) -> None:
        self.total = total_devices
        self._progress = 0            # 0‒total “installed”
        self._start = time.time()

    # Pretend this is “DeploymentID lookup”
    def get_deployment_id(self, qid: str) -> str:
        return f"SIM-{qid}-999"

    # Pretend this is “DeploymentStatus”
    def get_status(self, deployment_id: str) -> dict:
        # ramp success by 2–6 devices every call
        self._progress = min(self.total, self._progress + random.randint(2, 6))
        return {
            "DeploymentID": deployment_id,
            "TotalCount": self.total,
            "SuccessCount": self._progress,
            "ErrorCount": 0,
            "UnknownCount": self.total - self._progress,
            "Elapsed": round(time.time() - self._start, 1),
        }
