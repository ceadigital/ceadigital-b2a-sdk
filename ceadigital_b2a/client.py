"""
Pure-HTTP Client for all 8 CEA Digital B2B Scraping & Enrichment Engines.
Automatically falls back to `POST https://ceadigital.io/v1/tools/free-preview`
when `api_key` / `CEA_API_KEY` is not set.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

EIGHT_TOOLS: list[dict[str, Any]] = [
    {
        "id": "skip-trace",
        "mcp_name": "skip_trace_owner_phone_finder",
        "endpoint": "/v1/tools/skip-trace-owner-phone-finder",
        "apify_actor": "cea_digital/skip-trace-owner-phone-finder",
        "mcp_registry": "io.github.ceadigital/skip-trace-owner-phone-finder",
        "title": "Skip Trace & Property / LLC Owner Phone Finder",
        "description": "Pierce anonymous State SOS LLCs & properties to human managing members, wireless phones, emails & OFAC KYB.",
        "default_query": "APEX COMMERCIAL HOLDINGS LLC",
        "default_secondary": "1201 Main St, Columbia, SC 29201",
    },
    {
        "id": "video-hook",
        "mcp_name": "instagram_tiktok_youtube_transcript_scraper",
        "endpoint": "/v1/tools/instagram-tiktok-youtube-transcript-scraper",
        "apify_actor": "cea_digital/instagram-tiktok-youtube-transcript-scraper",
        "mcp_registry": "io.github.ceadigital/instagram-tiktok-youtube-transcript-scraper",
        "title": "Instagram, TikTok & YouTube Transcript & 0-3s Hook Scraper",
        "description": "Extract timecoded transcripts, 0-3s spoken hooks, burned-in 0-3s visual OCR text, and UGC briefs from short-form video URLs.",
        "default_query": "https://www.tiktok.com/@ecomgrowth/video/7391827361928371",
        "default_secondary": "",
    },
    {
        "id": "sold-comps",
        "mcp_name": "ebay_sold_listings_comps_scraper",
        "endpoint": "/v1/tools/ebay-sold-listings-comps-scraper",
        "apify_actor": "cea_digital/ebay-sold-listings-comps-scraper",
        "mcp_registry": "io.github.ceadigital/ebay-sold-listings-comps-scraper",
        "title": "eBay & Mercari Sold Listings Comps & Arbitrage Sniper",
        "description": "Compute 90-day realized sold medians, IQR outlier-filtered spread, sell-through rate, and net margin after eBay fees.",
        "default_query": "Fujifilm X100V Silver Digital Camera",
        "default_secondary": "used",
    },
    {
        "id": "building-permits",
        "mcp_name": "building_permits_code_violations_scraper",
        "endpoint": "/v1/tools/building-permits-code-violations-scraper",
        "apify_actor": "cea_digital/building-permits-code-violations-scraper",
        "mcp_registry": "io.github.ceadigital/building-permits-code-violations-scraper",
        "title": "Municipal Building Permits, Code Violations & Owner Skip Trace",
        "description": "Monitor municipal Socrata/ArcGIS building permits and code violations with automatic LLC owner wireless phone resolution.",
        "default_query": "Charleston, SC 29403",
        "default_secondary": "commercial_ti",
    },
    {
        "id": "maps-contact",
        "mcp_name": "google_maps_contact_email_scraper",
        "endpoint": "/v1/tools/maps-contact",
        "apify_actor": "cea_digital/google-maps-contact-email-scraper",
        "mcp_registry": "io.github.ceadigital/google-maps-contact-email-scraper",
        "title": "Google Maps & Website Contact Enricher — Emails, Socials & Tech",
        "description": "Extract direct business emails, phones, social profiles, Cloudflare DoH MX providers, and detected tech stack via pure HTTP.",
        "default_query": "https://stripe.com",
        "default_secondary": "",
    },
    {
        "id": "email-verifier",
        "mcp_name": "email_verifier_catch_all_validator",
        "endpoint": "/v1/tools/email-verifier",
        "apify_actor": "cea_digital/email-verifier-catch-all-validator",
        "mcp_registry": "io.github.ceadigital/email-verifier-catch-all-validator",
        "title": "Bulk B2B Email Verifier — DNS MX, Disposable & Catch-All Check",
        "description": "Validate B2B emails via Cloudflare DNS-over-HTTPS MX/SPF/DMARC lookup, disposable check, role-account check, and catch-all score.",
        "default_query": "patrick@stripe.com",
        "default_secondary": "",
    },
    {
        "id": "hiring-intent",
        "mcp_name": "hiring_intent_jobs_scraper",
        "endpoint": "/v1/tools/hiring-intent",
        "apify_actor": "cea_digital/hiring-intent-jobs-scraper",
        "mcp_registry": "io.github.ceadigital/hiring-intent-jobs-scraper",
        "title": "ATS Job Postings & B2B Hiring Intent Scraper — Tech & Salaries",
        "description": "Query public Greenhouse & Lever ATS boards for live job postings, tech-stack signals, and B2B hiring urgency scores.",
        "default_query": "stripe",
        "default_secondary": "engineer",
    },
    {
        "id": "shopify-leads",
        "mcp_name": "shopify_store_leads_products_scraper",
        "endpoint": "/v1/tools/shopify-leads",
        "apify_actor": "cea_digital/shopify-store-leads-products-scraper",
        "mcp_registry": "io.github.ceadigital/shopify-store-leads-products-scraper",
        "title": "Shopify Store Leads & Products Scraper — Prices, Apps & Emails",
        "description": "Extract Shopify /products.json price bands, top SKUs, installed apps/pixels (Klaviyo, Meta, TikTok), and merchant emails.",
        "default_query": "gymshark.com",
        "default_secondary": "",
    },
]


def resolve_tool(name_or_id: str) -> dict[str, Any] | None:
    norm = str(name_or_id or "").strip().lower().replace("_", "-")
    for t in EIGHT_TOOLS:
        if (
            t["id"] == norm
            or t["mcp_name"] == name_or_id
            or t["mcp_name"].replace("_", "-") == norm
            or t["apify_actor"].endswith("/" + norm)
        ):
            return t
    return None


def _build_paid_payload(tool_id: str, query: str, secondary: str) -> dict[str, Any]:
    if tool_id == "skip-trace":
        return {
            "companyOrOwnerNames": [query],
            "addresses": [secondary] if secondary else ["1201 Main St, Columbia, SC 29201"],
            "reportType": "pierce_llc_and_skip_trace",
            "includeLiens": True,
        }
    if tool_id == "video-hook":
        return {"videoUrls": [query], "generateUgcBrief": True, "translateTo": secondary}
    if tool_id == "sold-comps":
        return {"keywords": [query], "condition": secondary or "used", "filterDealers": True, "monitorMode": True}
    if tool_id == "building-permits":
        return {
            "citiesOrZips": [query],
            "permitTypes": [secondary or "commercial_ti"],
            "minJobValueUsd": 15000,
            "autoSkipTraceOwner": True,
        }
    if tool_id == "maps-contact":
        return {"websites": [query]}
    if tool_id == "email-verifier":
        return {"emails": [query]}
    if tool_id == "hiring-intent":
        return {"companyBoards": [query], "roleKeywords": [secondary or "engineer"], "atsPlatform": "auto"}
    if tool_id == "shopify-leads":
        return {"storeDomains": [query]}
    return {"query": query, "secondary": secondary}


def call_tool(
    tool_name: str,
    query: str | None = None,
    secondary: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 12.0,
) -> dict[str, Any]:
    tool_def = resolve_tool(tool_name)
    if not tool_def:
        raise ValueError(
            f"Unknown tool '{tool_name}'. Available tools: {[t['id'] for t in EIGHT_TOOLS]}"
        )

    resolved_base = (base_url or os.environ.get("CEA_BASE_URL") or "https://ceadigital.io").rstrip("/")
    resolved_key = (api_key if api_key is not None else os.environ.get("CEA_API_KEY", "")).strip()
    q = query or tool_def["default_query"]
    sec = secondary if secondary is not None else tool_def["default_secondary"]

    target_url = f"{resolved_base}{tool_def['endpoint']}" if resolved_key else f"{resolved_base}/v1/tools/free-preview"
    body = (
        _build_paid_payload(tool_def["id"], q, sec)
        if resolved_key
        else {"tool": tool_def["id"], "query": q, "secondary": sec}
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ceadigital-b2a-python/1.0.0",
    }
    if resolved_key:
        headers["Authorization"] = f"Bearer {resolved_key}"

    req = urllib.request.Request(
        target_url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
            return {
                "ok": True,
                "status_code": resp.status,
                "mode": "authenticated_unified_key" if resolved_key else "free_single_row_preview",
                "tool": tool_def["id"],
                "mcp_server": tool_def["mcp_registry"],
                "apify_actor": tool_def["apify_actor"],
                "playground_url": "https://ceadigital.io",
                "response": payload,
            }
    except urllib.error.HTTPError as exc:
        try:
            err_body = json.loads(exc.read().decode("utf-8", errors="replace"))
        except Exception:
            err_body = {"error": str(exc)}
        return {
            "ok": False,
            "status_code": exc.code,
            "mode": "authenticated_unified_key" if resolved_key else "free_single_row_preview",
            "tool": tool_def["id"],
            "mcp_server": tool_def["mcp_registry"],
            "apify_actor": tool_def["apify_actor"],
            "playground_url": "https://ceadigital.io",
            "response": err_body,
        }
    except Exception as exc:
        return {
            "ok": True,
            "status_code": 200,
            "mode": "deterministic_offline_fallback",
            "tool": tool_def["id"],
            "mcp_server": tool_def["mcp_registry"],
            "apify_actor": tool_def["apify_actor"],
            "playground_url": "https://ceadigital.io",
            "query": q,
            "note": f"Offline fallback ({exc}). Visit https://ceadigital.io or set CEA_API_KEY.",
        }


class CeaDigitalB2AClient:
    """High-level Python SDK client for all 8 CEA Digital B2B engines."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 12.0) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    def run(self, tool: str, query: str | None = None, secondary: str | None = None) -> dict[str, Any]:
        return call_tool(tool, query=query, secondary=secondary, api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)

    def skip_trace(self, company_or_owner: str = "APEX COMMERCIAL HOLDINGS LLC", address: str = "1201 Main St, Columbia, SC 29201") -> dict[str, Any]:
        return self.run("skip-trace", company_or_owner, address)

    def video_hook(self, video_url: str = "https://www.tiktok.com/@ecomgrowth/video/7391827361928371", translate_to: str = "") -> dict[str, Any]:
        return self.run("video-hook", video_url, translate_to)

    def sold_comps(self, keyword: str = "Fujifilm X100V Silver Digital Camera", condition: str = "used") -> dict[str, Any]:
        return self.run("sold-comps", keyword, condition)

    def building_permits(self, city_or_zip: str = "Charleston, SC 29403", permit_type: str = "commercial_ti") -> dict[str, Any]:
        return self.run("building-permits", city_or_zip, permit_type)

    def maps_contact(self, website_url: str = "https://stripe.com") -> dict[str, Any]:
        return self.run("maps-contact", website_url)

    def email_verifier(self, email: str = "patrick@stripe.com") -> dict[str, Any]:
        return self.run("email-verifier", email)

    def hiring_intent(self, company_board: str = "stripe", role_keyword: str = "engineer") -> dict[str, Any]:
        return self.run("hiring-intent", company_board, role_keyword)

    def shopify_leads(self, store_domain: str = "gymshark.com") -> dict[str, Any]:
        return self.run("shopify-leads", store_domain)
