# `ceadigital-mcp-tools` (`@ceadigital/b2a-mcp`)

**CEA Digital B2B Intelligence Multi-Tool CLI & Stdio MCP Server** — 8 Pure-HTTP Scraping & Enrichment Engines with automatic zero-signup 1-row free preview fallback (`POST https://ceadigital.io/v1/tools/free-preview`) when `CEA_API_KEY` is not set.

- **Interactive Playground & Direct API Keys ($2 Tripwire / $29/mo Growth):** [https://ceadigital.io](https://ceadigital.io)
- **GitHub Repository:** [https://github.com/ceadigital/ceadigital-b2a-sdk](https://github.com/ceadigital/ceadigital-b2a-sdk)

---

## Quick Start (Zero Signup Required)

Run directly with `npx` (via npm or GitHub):

```bash
# List all 8 pure-HTTP engines
npx -y ceadigital-mcp-tools --list
# or directly from GitHub today:
npx -y github:ceadigital/ceadigital-b2a-sdk --list

# Run a 1-row live preview (zero API key required!)
npx -y ceadigital-mcp-tools run skip-trace "APEX COMMERCIAL HOLDINGS LLC"
npx -y ceadigital-mcp-tools run video-hook "https://www.tiktok.com/@ecomgrowth/video/7391827361928371"
npx -y ceadigital-mcp-tools run sold-comps "Fujifilm X100V Silver Digital Camera" "used"
npx -y ceadigital-mcp-tools run building-permits "Charleston, SC 29403" "commercial_ti"
npx -y ceadigital-mcp-tools run maps-contact "https://stripe.com"
npx -y ceadigital-mcp-tools run email-verifier "patrick@stripe.com"
npx -y ceadigital-mcp-tools run hiring-intent "stripe" "engineer"
npx -y ceadigital-mcp-tools run shopify-leads "gymshark.com"
```

---

## Claude Desktop / Cursor / Windsurf / Cline MCP Configuration

Add to your `claude_desktop_config.json` or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ceadigital-b2a": {
      "command": "npx",
      "args": ["-y", "ceadigital-mcp-tools", "--mcp"],
      "env": {
        "CEA_API_KEY": ""
      }
    }
  }
}
```

When `CEA_API_KEY` is empty, every tool call automatically routes to `https://ceadigital.io/v1/tools/free-preview` so you can test all 8 tools immediately. Set `CEA_API_KEY=cea_live_...` (from [https://ceadigital.io/tools](https://ceadigital.io/tools)) to unlock full bulk runs.

---

## The 8 Pure-HTTP B2B Engines

| CLI Tool ID | MCP Tool Name | Endpoint | Apify Actor (`$5/mo` Free Tier) |
| :--- | :--- | :--- | :--- |
| `skip-trace` | `skip_trace_owner_phone_finder` | `/v1/tools/skip-trace-owner-phone-finder` | `cea_digital/skip-trace-owner-phone-finder` |
| `video-hook` | `instagram_tiktok_youtube_transcript_scraper` | `/v1/tools/instagram-tiktok-youtube-transcript-scraper` | `cea_digital/instagram-tiktok-youtube-transcript-scraper` |
| `sold-comps` | `ebay_sold_listings_comps_scraper` | `/v1/tools/ebay-sold-listings-comps-scraper` | `cea_digital/ebay-sold-listings-comps-scraper` |
| `building-permits` | `building_permits_code_violations_scraper` | `/v1/tools/building-permits-code-violations-scraper` | `cea_digital/building-permits-code-violations-scraper` |
| `maps-contact` | `google_maps_contact_email_scraper` | `/v1/tools/maps-contact` | `cea_digital/google-maps-contact-email-scraper` |
| `email-verifier` | `email_verifier_catch_all_validator` | `/v1/tools/email-verifier` | `cea_digital/email-verifier-catch-all-validator` |
| `hiring-intent` | `hiring_intent_jobs_scraper` | `/v1/tools/hiring-intent` | `cea_digital/hiring-intent-jobs-scraper` |
| `shopify-leads` | `shopify_store_leads_products_scraper` | `/v1/tools/shopify-leads` | `cea_digital/shopify-store-leads-products-scraper` |
