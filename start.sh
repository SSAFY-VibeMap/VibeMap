if ["$RESET_DB" = "true"]; then
    rm -f backend/vibemap.db
fi

exec python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000