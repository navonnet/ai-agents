uv sync

# Option 1: Open default browser with URL
Start-Process "http://127.0.0.1:7860"


uv run src\waBot.py
# open browser with url


# Option 2: Open specific browser (Chrome)
# Start-Process "chrome" -ArgumentList "http://localhost:8000"

# Option 3: Open specific browser (Edge)
# Start-Process "msedge" -ArgumentList "http://localhost:8000"

# Option 4: Open specific browser (Firefox)
# Start-Process "firefox" -ArgumentList "http://localhost:8000"
