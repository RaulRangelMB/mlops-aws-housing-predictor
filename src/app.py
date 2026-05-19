import json
from predict import HousingPredictor

# Initialize the inference engine globally for container reuse optimization
predictor = HousingPredictor()

def lambda_handler(event, context):
    try:
        # Unpack incoming payloads
        body = event.get("body", event)
        if isinstance(body, str):
            body = json.loads(body)
            
        # Extract features array 
        features = body["features"]
        
        # Execute prediction mapping logic
        result = predictor.predict_price(features)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "success",
                "predicted_raw": round(result["raw_value"], 4),
                "estimated_usd": round(result["usd_price"], 2)
            })
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": str(e)})
        }