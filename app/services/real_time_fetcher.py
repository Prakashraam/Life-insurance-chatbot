import requests
SERPER_API_KEY='a3891b90a6b485b2d04b3c83e4eb9ff3a9e53414'

def get_live_insurance_rates(query: str, region: str = "India") -> str:
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": f"{query} life insurance {region}",
            "gl": "in",  # Google country code for India
            "hl": "en"   # English results
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results = data.get("organic", [])[:3]
        if not results:
            return "⚠️ Sorry, I couldn't find any current information right now."

        # Format output nicely
        formatted = "\n📊 **Latest Life Insurance Info:**\n"
        for res in results:
            title = res.get("title", "No Title")
            snippet = res.get("snippet", "")
            link = res.get("link", "#")
            formatted += f"\n🔹 **{title}**\n{snippet}\n🔗 {link}\n"

        return formatted.strip()

    except Exception as e:
        print("❌ Error in get_live_insurance_rates():", e)
        return "⚠️ Unable to retrieve real-time insurance data at the moment."
