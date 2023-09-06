#!/bin/bash

CMD ["uvicorn", "scr.main:app", "--host", "0.0.0.0", "--port", "8080"]