# `ceadigital-b2a-sdk` (`ceadigital-mcp-tools` & `ceadigital-b2a`)

Official **Node.js CLI / Stdio MCP Server (`ceadigital-mcp-tools` / `@ceadigital/b2a-mcp`)** and **Python SDK (`ceadigital-b2a`)** for all **8 CEA Digital Pure-HTTP Scraping & Enrichment Engines** with automatic zero-signup 1-row free preview fallback (`POST https://ceadigital.io/v1/tools/free-preview`).

- **Live Zero-Auth Playground & Direct API Keys ($2 Tripwire / $29/mo Growth):** [https://ceadigital.io](https://ceadigital.io)
- **Official MCP Servers:** `io.github.ceadigital/*`
- **Apify Store Actors (`$5/mo` Free Tier eligible, `$0.00` on misses):** [https://apify.com/cea_digital](https://apify.com/cea_digital)

---

## 1. Instant Install & Run Today (Node.js / `npx` & Python / `pip`)

### Node.js CLI & Stdio MCP Server (`npx`)
```bash
# Run directly from GitHub today (or via npm: npx -y ceadigital-mcp-tools):
npx -y github:ceadigital/ceadigital-b2a-sdk --list

# Run a live 1-row preview with zero signup or API key:
npx -y github:ceadigital/ceadigital-b2a-sdk run skip-trace "APEX COMMERCIAL HOLDINGS LLC"
npx -y github:ceadigital/ceadigital-b2a-sdk run video-hook "https://www.tiktok.com/@ecomgrowth/video/7391827361928371"
npx -y github:ceadigital/ceadigital-b2a-sdk run sold-comps "Fujifilm X100V Silver Digital Camera" "used"
npx -y github:ceadigital/ceadigital-b2a-sdk run building-permits "Charleston, SC 29403" "commercial_ti"
npx -y github:ceadigital/ceadigital-b2a-sdk run maps-contact "https://stripe.com"
npx -y github:ceadigital/ceadigital-b2a-sdk run email-verifier "patrick@stripe.com"
npx -y github:ceadigital/ceadigital-b2a-sdk run hiring-intent "stripe" "engineer"
npx -y github:ceadigital/ceadigital-b2a-sdk run shopify-leads "gymshark.com"
```

### Python SDK & CLI (`pip` / `uv`)
```bash
# Install directly from GitHub today (or via PyPI: pip install ceadigital-b2a):
pip install git+https://github.com/ceadigital/ceadigital-b2a-sdk.git

# Run from CLI:
ceadigital-b2a --list
ceadigital-b2a run skip-trace "APEX COMMERCIAL HOLDINGS LLC"
```

```python
from ceadigital_b2a import CeaDigitalB2AClient

client = CeaDigitalB2AClient()  # Automatically uses /v1/tools/free-preview when CEA_API_KEY is unset
print(client.skip_trace("APEX COMMERCIAL HOLDINGS LLC"))
print(client.maps_contact("https://stripe.com"))
print(client.shopify_leads("gymshark.com"))
```

---

## 2. Claude Desktop / Cursor / Windsurf MCP Server Config

```json
{
  "mcpServers": {
    "ceadigital-b2a": {
      "command": "npx",
      "args": ["-y", "github:ceadigital/ceadigital-b2a-sdk", "--mcp"],
      "env": {
        "CEA_API_KEY": ""
      }
    }
  }
}
```

---

## 3. All 8 Pure-HTTP B2B Engines

| # | Tool ID | MCP Tool Name | Endpoint | Apify Actor (`$5/mo` Free Tier) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `skip-trace` | `skip_trace_owner_phone_finder` | `/v1/tools/skip-trace-owner-phone-finder` | [`cea_digital/skip-trace-owner-phone-finder`](https://apify.com/cea_digital/skip-trace-owner-phone-finder) |
| 2 | `video-hook` | `instagram_tiktok_youtube_transcript_scraper` | `/v1/tools/instagram-tiktok-youtube-transcript-scraper` | [`cea_digital/instagram-tiktok-youtube-transcript-scraper`](https://apify.com/cea_digital/instagram-tiktok-youtube-transcript-scraper) |
| 3 | `sold-comps` | `ebay_sold_listings_comps_scraper` | `/v1/tools/ebay-sold-listings-comps-scraper` | [`cea_digital/ebay-sold-listings-comps-scraper`](https://apify.com/cea_digital/ebay-sold-listings-comps-scraper) |
| 4 | `building-permits` | `building_permits_code_violations_scraper` | `/v1/tools/building-permits-code-violations-scraper` | [`cea_digital/building-permits-code-violations-scraper`](https://apify.com/cea_digital/building-permits-code-violations-scraper) |
| 5 | `maps-contact` | `google_maps_contact_email_scraper` | `/v1/tools/maps-contact` | [`cea_digital/google-maps-contact-email-scraper`](https://apify.com/cea_digital/google-maps-contact-email-scraper) |
| 6 | `email-verifier` | `email_verifier_catch_all_validator` | `/v1/tools/email-verifier` | [`cea_digital/email-verifier-catch-all-validator`](https://apify.com/cea_digital/email-verifier-catch-all-validator) |
| 7 | `hiring-intent` | `hiring_intent_jobs_scraper` | `/v1/tools/hiring-intent` | [`cea_digital/hiring-intent-jobs-scraper`](https://apify.com/cea_digital/hiring-intent-jobs-scraper) |
| 8 | `shopify-leads` | `shopify_store_leads_products_scraper` | `/v1/tools/shopify-leads` | [`cea_digital/shopify-store-leads-products-scraper`](https://apify.com/cea_digital/shopify-store-leads-products-scraper) |
