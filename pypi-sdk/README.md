# `ceadigital-b2a` — CEA Digital B2B Intelligence Python SDK, CLI & MCP Server

Zero-dependency Python SDK, CLI, and Stdio MCP Server for all **8 CEA Digital Pure-HTTP Scraping & Enrichment Engines** with automatic zero-signup 1-row free preview fallback (`POST https://ceadigital.io/v1/tools/free-preview`) when `CEA_API_KEY` is not set.

- **Interactive Playground & Direct API Keys ($2 Tripwire / $29/mo Growth):** [https://ceadigital.io](https://ceadigital.io)
- **GitHub Repository:** [https://github.com/ceadigital/ceadigital-b2a-sdk](https://github.com/ceadigital/ceadigital-b2a-sdk)

---

## Installation

```bash
pip install ceadigital-b2a
# Or install directly from GitHub today:
pip install git+https://github.com/ceadigital/ceadigital-b2a-sdk.git
```

---

## Python SDK Usage (Zero Signup for 1-Row Preview)

```python
from ceadigital_b2a import CeaDigitalB2AClient

client = CeaDigitalB2AClient()  # Uses free-preview automatically when CEA_API_KEY is unset

# 1. Skip Trace & State SOS LLC Piercer
print(client.skip_trace("APEX COMMERCIAL HOLDINGS LLC", "1201 Main St, Columbia, SC 29201"))

# 2. TikTok / Instagram Reels / YouTube Transcript & 0-3s Hook Extractor
print(client.video_hook("https://www.tiktok.com/@ecomgrowth/video/7391827361928371"))

# 3. eBay & Mercari 90-Day Realized Sold Comps
print(client.sold_comps("Fujifilm X100V Silver Digital Camera", "used"))

# 4. Municipal Building Permits & Code Violations
print(client.building_permits("Charleston, SC 29403", "commercial_ti"))

# 5. Google Maps & Website Contact Email Enricher
print(client.maps_contact("https://stripe.com"))

# 6. Bulk B2B Email Verifier & Catch-All Validator
print(client.email_verifier("patrick@stripe.com"))

# 7. Greenhouse & Lever ATS Hiring-Intent Jobs Scraper
print(client.hiring_intent("stripe", "engineer"))

# 8. Shopify Store Leads & /products.json Intelligence
print(client.shopify_leads("gymshark.com"))
```

---

## CLI & Stdio MCP Server Usage

```bash
# List all 8 tools
ceadigital-b2a --list

# Run any tool from the terminal
ceadigital-b2a run skip-trace "APEX COMMERCIAL HOLDINGS LLC"
ceadigital-b2a run maps-contact "https://stripe.com"

# Start Stdio MCP Server for Claude Desktop / Cursor
ceadigital-b2a --mcp
```
