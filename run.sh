#!/bin/bash

# Simple script to run the AID Curriculum Backend API

echo "Starting AID Curriculum Backend API..."
echo "API will be available at http://localhost:8000"
echo "Interactive API docs at http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
