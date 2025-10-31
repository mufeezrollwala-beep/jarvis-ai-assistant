#!/bin/bash
# Curl examples for Jarvis Text API

API_URL="http://localhost:8000"
API_KEY="jarvis-secret-key-123"

echo "==================================="
echo "Jarvis Text API - Curl Examples"
echo "==================================="
echo ""

# Check if API is running
echo "1. Check API information:"
echo "   curl $API_URL/"
echo ""
curl -s $API_URL/ | python3 -m json.tool
echo ""
echo ""

# Test authentication failure
echo "2. Test without authentication (should fail):"
echo "   curl -X POST $API_URL/commands -H 'Content-Type: application/json' -d '{\"command\": \"time\"}'"
echo ""
curl -s -X POST $API_URL/commands \
  -H "Content-Type: application/json" \
  -d '{"command": "time"}' | python3 -m json.tool
echo ""
echo ""

# Send time command
echo "3. Get current time:"
echo "   curl -X POST $API_URL/commands -H 'X-API-Key: $API_KEY' -H 'Content-Type: application/json' -d '{\"command\": \"what time is it\"}'"
echo ""
curl -s -X POST $API_URL/commands \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "what time is it"}' | python3 -m json.tool
echo ""
echo ""

# Wikipedia search
echo "4. Wikipedia search:"
echo "   curl -X POST $API_URL/commands -H 'X-API-Key: $API_KEY' -H 'Content-Type: application/json' -d '{\"command\": \"wikipedia artificial intelligence\"}'"
echo ""
curl -s -X POST $API_URL/commands \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "wikipedia artificial intelligence"}' | python3 -m json.tool | head -15
echo "   ... (truncated)"
echo ""
echo ""

# Get status
echo "5. Get system status:"
echo "   curl -X GET $API_URL/status -H 'X-API-Key: $API_KEY'"
echo ""
curl -s -X GET $API_URL/status \
  -H "X-API-Key: $API_KEY" | python3 -m json.tool
echo ""
echo ""

echo "==================================="
echo "✓ All examples complete!"
echo "==================================="
