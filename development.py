import os
import sys

from pathlib import Path

import uvicorn

from source.tests.development.local import check_settings_for_init_exclusion


SOURCE = Path(__file__).resolve().parent / "source"


if __name__ == "__main__":
    check_settings_for_init_exclusion()
    if str(SOURCE) not in sys.path:
        sys.path.append(str(SOURCE))
    uvicorn.run(
        "webapp.main:app",
        host=os.getenv("DEV_HOST", "127.0.0.1"),
        port=int(os.getenv("DEV_PORT", "8020")),
        reload=True,
    )
