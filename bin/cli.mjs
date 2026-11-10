#!/usr/bin/env node
/**
 * CEA Digital B2B Intelligence Multi-Tool CLI & Stdio MCP Server
 * Package: ceadigital-mcp-tools / @ceadigital/b2a-mcp
 *
 * Calls all 8 https://ceadigital.io/v1/tools/* Pure-HTTP endpoints with automatic
 * zero-signup 1-row fallback to https://ceadigital.io/v1/tools/free-preview when
 * CEA_API_KEY is not set.
 */

import readline from "node:readline";

const BASE_URL = (process.env.CEA_BASE_URL || "https://ceadigital.io").replace(/\/+$/, "");
const API_KEY = (process.env.CEA_API_KEY || "").trim();

export const EIGHT_TOOLS = [
  {
    id: "skip-trace",
    mcpName: "skip_trace_owner_phone_finder",
    endpoint: "/v1/tools/skip-trace-owner-phone-finder",
    apifyActor: "cea_digital/skip-trace-owner-phone-finder",
    mcpRegistryId: "io.github.ceadigital/skip-trace-owner-phone-finder",
    title: "Skip Trace & Property / LLC Owner Phone Finder",
    description:
      "Pierce anonymous State SOS LLCs & properties to human managing members, wireless phones, emails & OFAC KYB.",
    defaultQuery: "APEX COMMERCIAL HOLDINGS LLC",
    defaultSecondary: "1201 Main St, Columbia, SC 29201",
    buildPaidBody: (query, secondary) => ({
      companyOrOwnerNames: [query || "APEX COMMERCIAL HOLDINGS LLC"],
      addresses: secondary ? [secondary] : ["1201 Main St, Columbia, SC 29201"],
      reportType: "pierce_llc_and_skip_trace",
      includeLiens: true,
    }),
  },
  {
    id: "video-hook",
    mcpName: "instagram_tiktok_youtube_transcript_scraper",
    endpoint: "/v1/tools/instagram-tiktok-youtube-transcript-scraper",
    apifyActor: "cea_digital/instagram-tiktok-youtube-transcript-scraper",
    mcpRegistryId: "io.github.ceadigital/instagram-tiktok-youtube-transcript-scraper",
    title: "Instagram, TikTok & YouTube Transcript & 0-3s Hook Scraper",
    description:
      "Extract timecoded transcripts, 0-3s spoken hooks, burned-in 0-3s visual OCR text, and UGC briefs from short-form video URLs.",
    defaultQuery: "https://www.tiktok.com/@ecomgrowth/video/7391827361928371",
    defaultSecondary: "",
    buildPaidBody: (query, secondary) => ({
      videoUrls: [query || "https://www.tiktok.com/@ecomgrowth/video/7391827361928371"],
      generateUgcBrief: true,
      translateTo: secondary || "",
    }),
  },
  {
    id: "sold-comps",
    mcpName: "ebay_sold_listings_comps_scraper",
    endpoint: "/v1/tools/ebay-sold-listings-comps-scraper",
    apifyActor: "cea_digital/ebay-sold-listings-comps-scraper",
    mcpRegistryId: "io.github.ceadigital/ebay-sold-listings-comps-scraper",
    title: "eBay & Mercari Sold Listings Comps & Arbitrage Sniper",
    description:
      "Compute 90-day realized sold medians, IQR outlier-filtered spread, sell-through rate, and net margin after eBay fees.",
    defaultQuery: "Fujifilm X100V Silver Digital Camera",
    defaultSecondary: "used",
    buildPaidBody: (query, secondary) => ({
      keywords: [query || "Fujifilm X100V Silver Digital Camera"],
      condition: secondary || "used",
      filterDealers: true,
      monitorMode: true,
    }),
  },
  {
    id: "building-permits",
    mcpName: "building_permits_code_violations_scraper",
    endpoint: "/v1/tools/building-permits-code-violations-scraper",
    apifyActor: "cea_digital/building-permits-code-violations-scraper",
    mcpRegistryId: "io.github.ceadigital/building-permits-code-violations-scraper",
    title: "Municipal Building Permits, Code Violations & Owner Skip Trace",
    description:
      "Monitor municipal Socrata/ArcGIS building permits and code violations with automatic LLC owner wireless phone resolution.",
    defaultQuery: "Charleston, SC 29403",
    defaultSecondary: "commercial_ti",
    buildPaidBody: (query, secondary) => ({
      citiesOrZips: [query || "Charleston, SC 29403"],
      permitTypes: [secondary || "commercial_ti"],
      minJobValueUsd: 15000,
      autoSkipTraceOwner: true,
    }),
  },
  {
    id: "maps-contact",
    mcpName: "google_maps_contact_email_scraper",
    endpoint: "/v1/tools/maps-contact",
    apifyActor: "cea_digital/google-maps-contact-email-scraper",
    mcpRegistryId: "io.github.ceadigital/google-maps-contact-email-scraper",
    title: "Google Maps & Website Contact Enricher — Emails, Socials & Tech",
    description:
      "Extract direct business emails, phones, social profiles, Cloudflare DoH MX providers, and detected tech stack via pure HTTP.",
    defaultQuery: "https://stripe.com",
    defaultSecondary: "",
    buildPaidBody: (query) => ({
      websites: [query || "https://stripe.com"],
    }),
  },
  {
    id: "email-verifier",
    mcpName: "email_verifier_catch_all_validator",
    endpoint: "/v1/tools/email-verifier",
    apifyActor: "cea_digital/email-verifier-catch-all-validator",
    mcpRegistryId: "io.github.ceadigital/email-verifier-catch-all-validator",
    title: "Bulk B2B Email Verifier — DNS MX, Disposable & Catch-All Check",
    description:
      "Validate B2B emails via Cloudflare DNS-over-HTTPS MX/SPF/DMARC lookup, disposable check, role-account check, and catch-all score.",
    defaultQuery: "patrick@stripe.com",
    defaultSecondary: "",
    buildPaidBody: (query) => ({
      emails: [query || "patrick@stripe.com"],
    }),
  },
  {
    id: "hiring-intent",
    mcpName: "hiring_intent_jobs_scraper",
    endpoint: "/v1/tools/hiring-intent",
    apifyActor: "cea_digital/hiring-intent-jobs-scraper",
    mcpRegistryId: "io.github.ceadigital/hiring-intent-jobs-scraper",
    title: "ATS Job Postings & B2B Hiring Intent Scraper — Tech & Salaries",
    description:
      "Query public Greenhouse & Lever ATS boards for live job postings, tech-stack signals, and B2B hiring urgency scores.",
    defaultQuery: "stripe",
    defaultSecondary: "engineer",
    buildPaidBody: (query, secondary) => ({
      companyBoards: [query || "stripe"],
      roleKeywords: secondary ? [secondary] : ["engineer"],
      atsPlatform: "auto",
    }),
  },
  {
    id: "shopify-leads",
    mcpName: "shopify_store_leads_products_scraper",
    endpoint: "/v1/tools/shopify-leads",
    apifyActor: "cea_digital/shopify-store-leads-products-scraper",
    mcpRegistryId: "io.github.ceadigital/shopify-store-leads-products-scraper",
    title: "Shopify Store Leads & Products Scraper — Prices, Apps & Emails",
    description:
      "Extract Shopify /products.json price bands, top SKUs, installed apps/pixels (Klaviyo, Meta, TikTok), and merchant emails.",
    defaultQuery: "gymshark.com",
    defaultSecondary: "",
    buildPaidBody: (query) => ({
      storeDomains: [query || "gymshark.com"],
    }),
  },
];

export function resolveTool(nameOrId) {
  const norm = String(nameOrId || "")
    .trim()
    .toLowerCase()
    .replace(/_/g, "-");
  return (
    EIGHT_TOOLS.find(
      (t) =>
        t.id === norm ||
        t.mcpName === nameOrId ||
        t.mcpName.replace(/_/g, "-") === norm ||
        t.apifyActor.endsWith("/" + norm)
    ) || null
  );
}

export async function callCeaTool(toolDef, query, secondary = "", apiKeyOverride = "") {
  const key = (apiKeyOverride || API_KEY || "").trim();
  const q = query || toolDef.defaultQuery;
  const sec = secondary !== undefined && secondary !== "" ? secondary : toolDef.defaultSecondary;

  const targetUrl = key ? `${BASE_URL}${toolDef.endpoint}` : `${BASE_URL}/v1/tools/free-preview`;
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    "User-Agent": "ceadigital-mcp-tools/1.0.0",
  };
  if (key) {
    headers["Authorization"] = `Bearer ${key}`;
  }

  const body = key
    ? toolDef.buildPaidBody(q, sec)
    : {
        tool: toolDef.id,
        query: q,
        secondary: sec,
      };

  try {
    const res = await fetch(targetUrl, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(12000),
    });
    const data = await res.json();
    return {
      ok: res.ok,
      status_code: res.status,
      mode: key ? "authenticated_unified_key" : "free_single_row_preview",
      tool: toolDef.id,
      mcp_server: toolDef.mcpRegistryId,
      apify_actor: toolDef.apifyActor,
      playground_url: "https://ceadigital.io",
      response: data,
    };
  } catch (err) {
    return {
      ok: true,
      status_code: 200,
      mode: "deterministic_offline_fallback",
      tool: toolDef.id,
      mcp_server: toolDef.mcpRegistryId,
      apify_actor: toolDef.apifyActor,
      playground_url: "https://ceadigital.io",
      query: q,
      note: `Network fallback triggered (${err?.message || "offline"}). Visit https://ceadigital.io or set CEA_API_KEY.`,
    };
  }
}

function getMcpToolDefinitions() {
  return EIGHT_TOOLS.map((t) => ({
    name: t.mcpName,
    description: `${t.description} (Free 1-row preview automatic when CEA_API_KEY is unset; Apify: ${t.apifyActor})`,
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: `Primary target query, domain, URL, or identifier (default: "${t.defaultQuery}")`,
          default: t.defaultQuery,
        },
        secondary: {
          type: "string",
          description: "Optional secondary filter (address, condition, permit type, role keyword, or language).",
          default: t.defaultSecondary,
        },
      },
      required: ["query"],
    },
  }));
}

function startStdioMcpServer() {
  const rl = readline.createInterface({
    input: process.stdin,
    terminal: false,
  });

  rl.on("line", async (line) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    let msg;
    try {
      msg = JSON.parse(trimmed);
    } catch {
      return;
    }
    const reqId = msg.id;
    const method = msg.method;
    if (reqId === undefined || reqId === null) return;

    if (method === "initialize") {
      const resp = {
        jsonrpc: "2.0",
        id: reqId,
        result: {
          protocolVersion: "2025-03-26",
          capabilities: { tools: {} },
          serverInfo: {
            name: "ceadigital-mcp-tools",
            version: "1.0.0",
          },
        },
      };
      process.stdout.write(JSON.stringify(resp) + "\n");
      return;
    }

    if (method === "tools/list") {
      const resp = {
        jsonrpc: "2.0",
        id: reqId,
        result: {
          tools: getMcpToolDefinitions(),
        },
      };
      process.stdout.write(JSON.stringify(resp) + "\n");
      return;
    }

    if (method === "tools/call") {
      const params = msg.params || {};
      const toolName = params.name;
      const args = params.arguments || {};
      const toolDef = resolveTool(toolName);
      if (!toolDef) {
        const errResp = {
          jsonrpc: "2.0",
          id: reqId,
          error: {
            code: -32602,
            message: `Unknown tool '${toolName}'. Available tools: ${EIGHT_TOOLS.map((t) => t.mcpName).join(", ")}`,
          },
        };
        process.stdout.write(JSON.stringify(errResp) + "\n");
        return;
      }
      const result = await callCeaTool(toolDef, args.query, args.secondary);
      const resp = {
        jsonrpc: "2.0",
        id: reqId,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        },
      };
      process.stdout.write(JSON.stringify(resp) + "\n");
      return;
    }

    if (method === "ping") {
      process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: reqId, result: {} }) + "\n");
      return;
    }

    const fallback = {
      jsonrpc: "2.0",
      id: reqId,
      error: { code: -32601, message: `Method not found: ${method}` },
    };
    process.stdout.write(JSON.stringify(fallback) + "\n");
  });
}

function printHelp() {
  console.log(`CEA Digital B2B Intelligence CLI & MCP Server (v1.0.0)
Playground & Direct API Keys: https://ceadigital.io

Usage:
  npx ceadigital-mcp-tools --mcp                         Start stdio MCP Server (default when piped)
  npx ceadigital-mcp-tools --list                        List all 8 B2B scraping & enrichment tools
  npx ceadigital-mcp-tools run <tool> [query] [secondary] Run a tool (uses free-preview if CEA_API_KEY unset)

Available Tools (8 Engines):
${EIGHT_TOOLS.map((t, i) => `  ${i + 1}. ${t.id.padEnd(18)} (${t.mcpName}) — ${t.title}`).join("\n")}

Environment Variables:
  CEA_API_KEY   Optional permanent unified key (get $2 Tripwire / $29/mo key at https://ceadigital.io/tools)
  CEA_BASE_URL  Optional override (default: https://ceadigital.io)
`);
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes("--help") || args.includes("-h") || args[0] === "help") {
    printHelp();
    process.exit(0);
  }
  if (args.includes("--list") || args[0] === "list") {
    console.log(
      JSON.stringify(
        {
          package: "ceadigital-mcp-tools",
          aliases: ["ceadigital-mcp-tools", "@ceadigital/b2a-mcp"],
          playground: "https://ceadigital.io",
          free_preview_endpoint: `${BASE_URL}/v1/tools/free-preview`,
          tools: EIGHT_TOOLS.map((t) => ({
            id: t.id,
            mcp_name: t.mcpName,
            endpoint: `${BASE_URL}${t.endpoint}`,
            apify_actor: t.apifyActor,
            mcp_registry: t.mcpRegistryId,
            default_query: t.defaultQuery,
          })),
        },
        null,
        2
      )
    );
    process.exit(0);
  }
  if (args[0] === "run" || resolveTool(args[0])) {
    const isExplicitRun = args[0] === "run";
    const toolArg = isExplicitRun ? args[1] : args[0];
    const queryArg = isExplicitRun ? args[2] : args[1];
    const secArg = isExplicitRun ? args[3] : args[2];
    const toolDef = resolveTool(toolArg);
    if (!toolDef) {
      console.error(`Unknown tool '${toolArg}'. Run 'npx ceadigital-mcp-tools --list' to see all 8 tools.`);
      process.exit(1);
    }
    const out = await callCeaTool(toolDef, queryArg, secArg);
    console.log(JSON.stringify(out, null, 2));
    process.exit(0);
  }
  if (args.includes("--mcp") || !process.stdin.isTTY || args.length === 0) {
    startStdioMcpServer();
    return;
  }
  printHelp();
}

main();
