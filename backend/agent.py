from models import ResearchResult, AgentOutput
import asyncio

class B2BAgent:
    def __init__(self):
        # Initialize tools here
        pass

    async def run(self, domain: str) -> AgentOutput:
        from tools.search import search_web
        from tools.scraper import scrape_url
        from tools.llm import generate_content
        import asyncio
        import sys

        # Force Windows Proactor Logic for Playwright in this thread
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        print(f"Starting research on {domain}...")

        # 1. Parallel Research
        # - Search for News
        # - Search for CEO
        # - Scrape Landing Page
        
        news_query = f"latest product news {domain} 2024 2025"
        ceo_query = f"CEO of {domain}"
        email_format_query = f"email address format {domain} contact"
        
        # Helper to run blocking tool in async
        def run_search(q): return search_web(q, max_results=3)
        
        # Execute searches (added email format search)
        news_results, ceo_results, email_results = await asyncio.gather(
            asyncio.to_thread(run_search, news_query),
            asyncio.to_thread(run_search, ceo_query),
            asyncio.to_thread(run_search, email_format_query)
        )
        
        # Identify CEO Name (Naive approach: ask LLM or parse first result)
        # We'll feed raw search results to LLM mostly, but useful to have name for next step.
        ceo_name_prompt = f"Extract the CEO name of {domain} from these search results: {ceo_results}. Return ONLY the name."
        ceo_name = generate_content(ceo_name_prompt).strip()
        
        print(f"Identified CEO: {ceo_name}")

        # - Search CEO Activity if found
        activity_results = []
        if ceo_name and "Error" not in ceo_name:
            activity_query = f"{ceo_name} {domain} interview podcast thoughts linkedin"
            activity_results = await asyncio.to_thread(run_search, activity_query)

        # - Scrape Homepage (limited to avoid timeouts/blocks)
        try:
            landing_page_text = await scrape_url(f"https://{domain}")
        except:
            landing_page_text = "Could not scrape homepage."

        # 2. Synthesis
        prompt = f"""
        You are an elite B2B Sales Researcher.
        TARGET COMPANY: {domain}
        CEO: {ceo_name}
        
        RESEARCH DATA:
        1. WEBSITE VARIANT: {landing_page_text[:2000]}...
        2. LATEST NEWS: {str(news_results)}
        3. CEO ACTIVITY: {str(activity_results)}
        4. EMAIL PATTERNS: {str(email_results)}

        TASK:
        1. Identify 3 specific "Pain Points" or opportunities. **CITATION REQUIRED**: You must append (Source: [URL]) to every pain point.
        2. GUESS THE CEO's EMAIL: Analyze the 'EMAIL PATTERNS' research. If the pattern is 'first.last@domain', output 'patrick.collison@{domain}'. specificy if it is a guess.
        3. Draft a personalized cold email to the CEO.
        4. Write a 30-second video script.

        OUTPUT FORMAT (JSON):
        {{
            "news_headlines": ["headline 1 (Source: url)", "headline 2 (Source: url)"],
            "ceo_name": "{ceo_name} (Email Guess: first.last@{domain})",
            "ceo_recent_activity": ["activity 1 (Source: url)", "activity 2"],
            "pain_points": ["point 1 (Source: url)", "point 2"],
            "email_draft": "Subject: ... Body: ...",
            "video_script": "..."
        }}
        Return ONLY valid JSON.
        """
        
        print("Generating insights...")
        raw_response = generate_content(prompt)
        
        # Parse JSON (Clean markdown fences if present)
        import json
        import re
        
        clean_json = raw_response.replace("```json", "").replace("```", "").strip()
        try:
            data = json.loads(clean_json)
        except:
            # Fallback simple parser or error
            print("JSON Parse Error, returning raw")
            # In production, use PydanticOutputParser or retry
            return AgentOutput(
                research=ResearchResult(
                    news_headlines=["Error parsing LLM output"], 
                    ceo_name=ceo_name, 
                    ceo_recent_activity=[], 
                    pain_points=[]
                ),
                email_draft=raw_response,
                video_script="See email draft."
            )

        return AgentOutput(
            research=ResearchResult(
                news_headlines=data.get("news_headlines", []),
                ceo_name=data.get("ceo_name", ceo_name),
                ceo_recent_activity=data.get("ceo_recent_activity", []),
                pain_points=data.get("pain_points", [])
            ),
            email_draft=data.get("email_draft", ""),
            video_script=data.get("video_script", "")
        )

