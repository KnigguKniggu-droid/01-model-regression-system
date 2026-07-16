import httpx
import asyncio

async def test():
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Classify email as: billing, technical, account, general. Output only the category name."},
            {"role": "user", "content": "Subject: Invoice shows double charge for July\nBody: Hi, I just checked my July invoice and it looks like I was charged twice for the same subscription period. Can you look into this and issue a refund for the duplicate charge?"}
        ],
        "temperature": 0.0,
        "max_tokens": 50,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Content: {data['choices'][0]['message']['content']}")

asyncio.run(test())