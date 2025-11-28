from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import os
from github_integration import GitHubAmazonQIntegration

app = FastAPI()

@app.post("/github-webhook")
async def github_webhook(request: Request):
    """Handle GitHub webhook events for PR reviews"""
    
    # Verify webhook signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_signature(await request.body(), signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"] and "pull_request" in payload:
        pr_number = payload["pull_request"]["number"]
        repo = payload["repository"]["full_name"]
        
        # Trigger Amazon Q review
        integration = GitHubAmazonQIntegration(
            github_token=os.getenv("GITHUB_TOKEN"),
            repo=repo
        )
        
        result = integration.review_pull_request(pr_number)
        
        # Post review comment
        if result["status"] == "review_triggered":
            comment = f"🤖 Amazon Q Review completed for {result['files_count']} files"
            integration.post_review_comment(
                pr_number, 
                comment, 
                payload["pull_request"]["head"]["sha"]
            )
    
    return {"status": "processed"}

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature"""
    if not signature_header:
        return False
    
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "").encode()
    expected_signature = "sha256=" + hmac.new(
        secret, payload_body, hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)