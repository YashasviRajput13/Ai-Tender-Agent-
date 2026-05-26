from typing import List, Dict

class DiscoveryAgent:
    def discover_sources(self, sources: List[str]) -> List[Dict[str, str]]:
        results = []
        for source in sources:
            results.append({
                "source": source,
                "status": "queued",
                "description": "Source queued for tender discovery.",
            })
        return results

    def parse_feed(self, feed_text: str) -> Dict[str, object]:
        return {
            "feed_length": len(feed_text),
            "tenders_found": [],
            "notes": "Feed parsed and ready for extraction.",
        }
