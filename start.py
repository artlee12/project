import os
import sys
from pathlib import Path

# Получаем абсолютный путь к текущей директории
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(current_dir)]
    ) 