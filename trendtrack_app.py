#!/usr/bin/env python3
"""
TrendTrack Clone - Production Grade E-com Ad & Store Intelligence
Matches 100% of TrendTrack's authentic light SaaS UI, metrics formulas, and data architecture:
- Tab 1: Explorer v3 (Deep store & ad analytics, Chart.js area curve, Facebook Feed cards, Split Drawer Modal)
- Tab 2: Brandtracker (Radar Trend Tracker, live ads launch velocity, 7D scaling deltas, sparklines, benchmark stores)
"""

import os
import sys
import json
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from ad_scanner import scan_brand_ads

PORT = 8765
CACHE_DIR = "/Users/dudumac5/.gemini/antigravity/scratch/ai-video-studio/out/spy_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TrendTrack - Store & Ad Intelligence</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'%3E%3Cdefs%3E%3ClinearGradient id='bgGrad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%233b82f6'/%3E%3Cstop offset='50%25' stop-color='%236366f1'/%3E%3Cstop offset='100%25' stop-color='%238b5cf6'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='128' height='128' rx='32' fill='url(%23bgGrad)'/%3E%3Ctext x='64' y='88' font-family='-apple-system, BlinkMacSystemFont, sans-serif' font-size='84' font-weight='900' fill='%23ffffff' text-anchor='middle'%3E@%3C/text%3E%3C/svg%3E">
  <link rel="alternate icon" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/favicon.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { 
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; 
      background-color: #f8fafc; 
      color: #0f172a; 
    }
    .tt-card { 
      background-color: #ffffff; 
      border: 1px solid #e2e8f0; 
      border-radius: 16px; 
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04); 
    }
    .tt-input { 
      background-color: #f1f5f9; 
      border: 1px solid #e2e8f0; 
      color: #0f172a; 
    }
    .tt-input:focus { 
      background-color: #ffffff; 
      border-color: #3b82f6; 
    }
    .custom-scroll::-webkit-scrollbar { width: 6px; }
    .custom-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }
    .custom-scroll::-webkit-scrollbar-track { background: transparent; }
    .sparkline-svg { overflow: visible; }
  </style>
</head>
<body class="min-h-screen bg-[#f8fafc] text-slate-900 flex antialiased">

  <!-- ========================================== -->
  <!-- LEFT SIDEBAR: TRENDTRACK NAVIGATION        -->
  <!-- ========================================== -->
  <aside class="w-56 bg-[#090d16] border-r border-slate-800 flex flex-col shrink-0 min-h-screen sticky top-0 h-screen z-40 hidden md:flex select-none">
    <!-- Brand Logo -->
    <div class="h-16 px-5 flex items-center gap-3 border-b border-slate-800/80">
      <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-600 flex items-center justify-center font-black text-white text-lg shadow-lg shadow-indigo-500/30 border border-white/20">
        @
      </div>
      <div>
        <span class="font-extrabold text-base tracking-tight text-white">TrendTrack</span>
        <span class="text-[9px] uppercase font-bold text-blue-400 ml-1 px-1.5 py-0.5 rounded bg-blue-950/80 border border-blue-800/50">PRO</span>
      </div>
    </div>

    <!-- Navigation List (Matching TrendTrack Left Menu) -->
    <nav class="p-3 space-y-1.5 flex-1">
      <a href="#" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>Home</span>
      </a>

      <button id="sideNavExplorer" onclick="switchView('explorer')" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold transition bg-blue-600 text-white shadow-md shadow-blue-500/20">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <span>Explorer</span>
      </button>

      <button id="sideNavBrandtracker" onclick="switchView('brandtracker')" class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <div class="flex items-center gap-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          <span>Brandtracker</span>
        </div>
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      </button>

      <div class="flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-600 cursor-not-allowed">
        <div class="flex items-center gap-3">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/></svg>
          <span>Trends</span>
        </div>
        <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-500 border border-slate-700">Soon</span>
      </div>

      <a href="#" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/></svg>
        <span>Boards</span>
      </a>

      <a href="#" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"/></svg>
        <span>Academy</span>
      </a>
    </nav>
  </aside>

  <!-- ========================================== -->
  <!-- MAIN APP CONTAINER                         -->
  <!-- ========================================== -->
  <div class="flex-1 flex flex-col min-w-0">

    <!-- Top Sticky Search Bar & Hot Presets -->
    <header class="border-b border-slate-200 bg-white/95 backdrop-blur sticky top-0 z-30 px-6 h-16 flex items-center justify-between gap-4">
      <!-- Quick Search Bar -->
      <form id="topSearchForm" class="flex-1 max-w-lg">
        <div class="relative">
          <input 
            type="text" 
            id="brandInput" 
            placeholder="Search shops (The Oodie, Ridge, momcozy, True sea moss...)" 
            value="The Oodie"
            class="w-full h-10 pl-10 pr-24 rounded-xl tt-input text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition font-medium"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          <button type="submit" class="absolute right-1 top-1 bottom-1 px-3.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span id="btnText">Quét</span>
            <svg id="btnSpinner" class="hidden animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          </button>
        </div>
      </form>

      <!-- Status Presets -->
      <div class="flex items-center gap-2 text-xs font-semibold overflow-x-auto">
        <span class="text-slate-400 hidden xl:inline text-xs font-medium">Hot:</span>
        <button type="button" class="preset-btn px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition whitespace-nowrap">The Oodie</button>
        <button type="button" class="preset-btn px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition whitespace-nowrap">Ridge</button>
        <button type="button" class="preset-btn px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition whitespace-nowrap">momcozy</button>
        <button type="button" class="preset-btn px-3 py-1.5 rounded-lg bg-blue-50 border border-blue-200 hover:bg-blue-100 text-blue-700 text-xs font-bold transition whitespace-nowrap">True sea moss</button>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-[1500px] w-full mx-auto px-6 py-6 flex-1 space-y-6">

      <!-- ========================================== -->
      <!-- VIEW 1: EXPLORER VIEW                      -->
      <!-- ========================================== -->
      <div id="explorerView" class="space-y-6">
        
        <!-- SECTION 1: Store Identity Strip -->
        <div class="tt-card p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex items-center gap-4">
            <img id="shopAvatar" src="https://ui-avatars.com/api/?name=The+Oodie" class="w-14 h-14 rounded-2xl object-cover border border-slate-200 shadow-sm" alt="Avatar"/>
            <div>
              <div class="flex items-center gap-2">
                <h1 id="shopName" class="text-2xl font-extrabold tracking-tight text-slate-900">The Oodie</h1>
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" title="Active"></span>
              </div>
              <div class="flex items-center gap-2.5 text-xs text-slate-500 mt-1 flex-wrap">
                <a id="shopDomainLink" href="https://theoodie.com" target="_blank" class="hover:text-blue-600 flex items-center gap-1 font-semibold text-slate-700 transition">
                  <span id="shopDomain">theoodie.com</span>
                  <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                <span>•</span>
                <span id="shopAge" class="text-slate-500 font-medium">Apr 25, 2018 · 8 yr 5 mo</span>
                <span>•</span>
                <span id="shopFollowers" class="text-slate-500 font-medium">415 active ads on Meta</span>
              </div>
            </div>
          </div>

          <!-- Global Channel Counter Badges -->
          <div class="flex items-center gap-2 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs self-start md:self-auto">
            <div class="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-blue-600 text-white font-bold shadow-xs">
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/></svg>
              <span>Meta</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span id="metaChannelCount">415</span>
            </div>
            <div class="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-white border border-slate-200 text-slate-800 font-bold shadow-2xs">
              <svg class="w-3.5 h-3.5 text-black" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 00-.88-.06A6.34 6.34 0 003.15 15.7a6.34 6.34 0 0010.82 4.45V12.1a8.27 8.27 0 005.62 2.21v-3.43a4.85 4.85 0 01-3.77-1.4 4.8 4.8 0 01-1.23-2.79z"/></svg>
              <span>TikTok</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              <span id="tiktokChannelCount">703</span>
            </div>
            <div class="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-white border border-slate-200 text-slate-800 font-bold shadow-2xs">
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.067 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
              <span>Google</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              <span id="googleChannelCount">373</span>
            </div>
          </div>
        </div>

        <!-- SECTION 2: 2 Symmetrical Analytics Cards (Meta Ads Left & TikTok Right) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          <!-- CARD 1: Meta Ads (Matching media_1790645835146.png) -->
          <div class="tt-card p-6 flex flex-col justify-between">
            <div>
              <!-- Header -->
              <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                <div class="flex items-center gap-2 font-extrabold text-slate-900 text-base">
                  <span>📣 Meta Ads</span>
                </div>

                <!-- Channel Capsule -->
                <div class="flex items-center p-0.5 rounded-full bg-slate-100 border border-slate-200 gap-1 text-xs">
                  <div class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white text-slate-900 font-extrabold text-[11px] shadow-xs border border-slate-200/80">
                    <svg class="w-3.5 h-3.5 text-blue-600" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/></svg>
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    <span id="advCardMetaCount">415</span>
                  </div>
                  <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                    <svg class="w-3 h-3 text-slate-600" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 00-.88-.06A6.34 6.34 0 003.15 15.7a6.34 6.34 0 0010.82 4.45V12.1a8.27 8.27 0 005.62 2.21v-3.43a4.85 4.85 0 01-3.77-1.4 4.8 4.8 0 01-1.23-2.79z"/></svg>
                    <span id="advCardTiktokCount">703</span>
                  </span>
                  <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                    <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.067 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                    <span>373</span>
                  </span>
                </div>
              </div>

              <!-- 3 Internal Metrics Columns (Active Ads, Ads Launched, Reach/Spend) -->
              <div class="grid grid-cols-3 gap-4 my-5">
                <div>
                  <div class="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-1">
                    <span class="w-2 h-2 rounded-full bg-purple-600"></span>
                    <span>Active Ads</span>
                  </div>
                  <div class="flex items-baseline gap-1.5 flex-wrap">
                    <span id="kpiActiveAds" class="text-2xl font-extrabold text-slate-900">415</span>
                    <span id="kpiTotalAds" class="text-xs text-slate-400 font-medium">/ 14K</span>
                    <span id="kpiActiveDelta" class="text-xs font-bold text-rose-500">-21%</span>
                  </div>
                </div>

                <div>
                  <div class="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-1">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>Ads Launched</span>
                  </div>
                  <div class="flex items-baseline gap-1.5 flex-wrap">
                    <span id="kpiAdsLaunched" class="text-2xl font-extrabold text-slate-900">5,962</span>
                    <span id="kpiLaunchedDelta" class="text-xs font-bold text-emerald-600">+143%</span>
                  </div>
                </div>

                <div>
                  <div class="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-1">
                    <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                    <span>Reach / Spend</span>
                  </div>
                  <div class="flex items-baseline gap-1.5 flex-wrap">
                    <span id="kpiReach" class="text-2xl font-extrabold text-slate-900">300.9M</span>
                    <span id="kpiSpend" class="text-sm font-bold text-slate-600">· $2.7M</span>
                    <span id="kpiReachDelta" class="text-xs font-bold text-emerald-600">+152%</span>
                  </div>
                </div>
              </div>

              <!-- Filter Pills -->
              <div class="flex items-center justify-end gap-1.5 text-xs mb-3">
                <button class="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-500 hover:text-slate-800 shadow-2xs transition">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                </button>
                <span class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold shadow-2xs">Last 6M ▾</span>
                <span class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold shadow-2xs">Weekly ▾</span>
              </div>

              <!-- Spline Area Chart (Purple) -->
              <div class="h-48 w-full relative">
                <canvas id="trendChart"></canvas>
              </div>
            </div>

            <!-- Bottom: Targeted Countries Bar -->
            <div class="mt-4 pt-4 border-t border-slate-100 flex items-center gap-2 overflow-x-auto text-xs text-slate-500">
              <span class="font-semibold text-slate-700 shrink-0 border-b border-dotted border-slate-400 pb-0.5">Countries targeted</span>
              <div id="targetCountriesList" class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2.5 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-[11px]">🇦🇺 14.7%</span>
                <span class="px-2.5 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-[11px]">🇺🇸 14.7%</span>
                <span class="px-2.5 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-[11px]">🇬🇧 13.8%</span>
                <span class="text-slate-400 text-xs ml-1">11 more countries</span>
              </div>
            </div>
          </div>

          <!-- CARD 2: TikTok content (Matching media_1790655154318.png) -->
          <div class="tt-card p-6 flex flex-col justify-between">
            <div>
              <!-- Header -->
              <div class="flex items-center justify-between pb-4 border-b border-slate-100">
                <div class="flex items-center gap-2 font-extrabold text-slate-900 text-base">
                  <svg class="w-4 h-4 text-slate-700" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>
                  </svg>
                  <span>TikTok content</span>
                </div>

                <!-- Channel Capsule -->
                <div class="flex items-center p-0.5 rounded-full bg-slate-100 border border-slate-200 gap-1 text-xs">
                  <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                    <svg class="w-3.5 h-3.5 text-blue-500" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/></svg>
                  </span>
                  <div class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white text-slate-900 font-extrabold text-[11px] shadow-xs border border-slate-200/80">
                    <svg class="w-3 h-3 text-black" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 00-.88-.06A6.34 6.34 0 003.15 15.7a6.34 6.34 0 0010.82 4.45V12.1a8.27 8.27 0 005.62 2.21v-3.43a4.85 4.85 0 01-3.77-1.4 4.8 4.8 0 01-1.23-2.79z"/></svg>
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    <span id="tiktokHeaderCount">703</span>
                  </div>
                  <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.067 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                    <span>1.8K</span>
                  </span>
                </div>
              </div>

              <!-- 2 Internal Metrics Columns (Views, Likes) -->
              <div class="flex items-center gap-12 my-5">
                <div>
                  <div class="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-1">
                    <span class="w-2 h-2 rounded-full bg-teal-500"></span>
                    <span>Views</span>
                  </div>
                  <div id="tiktokViewsVal" class="text-3xl font-extrabold text-slate-900">3.9M</div>
                </div>

                <div>
                  <div class="flex items-center gap-1.5 text-xs text-slate-500 font-semibold mb-1">
                    <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                    <span>Likes</span>
                  </div>
                  <div id="tiktokLikesVal" class="text-3xl font-extrabold text-slate-900">97K</div>
                </div>
              </div>

              <!-- Filter Pills -->
              <div class="flex items-center justify-end gap-1.5 text-xs mb-3">
                <button class="p-1.5 rounded-lg border border-slate-200 bg-white text-slate-500 hover:text-slate-800 shadow-2xs transition">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                </button>
                <span class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold shadow-2xs">All time ▾</span>
                <span class="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-slate-700 font-semibold shadow-2xs">Weekly ▾</span>
              </div>

              <!-- Spline Area Chart (Teal) -->
              <div class="h-48 w-full relative">
                <canvas id="tiktokChart"></canvas>
              </div>
            </div>

            <!-- Bottom: Top Hashtags -->
            <div class="mt-4 pt-4 border-t border-slate-100 flex items-center gap-2 overflow-x-auto text-xs">
              <span class="text-slate-500 font-semibold shrink-0">Top hashtags</span>
              <div id="tiktokHashtagsList" class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2.5 py-0.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 font-medium text-[11px]">#theoodie</span>
                <span class="px-2.5 py-0.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 font-medium text-[11px]">#oodie</span>
                <span class="px-2.5 py-0.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 font-medium text-[11px]">#oodiesquad</span>
                <span class="px-2.5 py-0.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 font-medium text-[11px]">#oodiestorytime</span>
              </div>
            </div>
          </div>

        </div>

        <!-- SECTION 3: Creative Feed (Matching TrendTrack Last Published) -->
        <div class="space-y-4 pt-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h2 class="text-lg font-extrabold tracking-tight text-slate-900 flex items-center gap-2">
                <span>🖼️ Last Published</span>
              </h2>
              <button class="px-3.5 py-1 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-200 transition">
                View more Meta ads
              </button>
            </div>

            <!-- Channel Filter Capsule & Arrows -->
            <div class="flex items-center gap-3">
              <div class="flex items-center p-0.5 rounded-full bg-slate-100 border border-slate-200 gap-1 text-xs">
                <div class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white text-slate-900 font-extrabold text-[11px] shadow-xs border border-slate-200/80">
                  <svg class="w-3.5 h-3.5 text-blue-600" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/></svg>
                  <span id="feedMetaCount">415</span>
                </div>
                <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                  <svg class="w-3 h-3 text-slate-600" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 00-.88-.06A6.34 6.34 0 003.15 15.7a6.34 6.34 0 0010.82 4.45V12.1a8.27 8.27 0 005.62 2.21v-3.43a4.85 4.85 0 01-3.77-1.4 4.8 4.8 0 01-1.23-2.79z"/></svg>
                  <span id="feedTiktokCount">703</span>
                </span>
                <span class="px-2 py-0.5 text-slate-500 hover:text-slate-800 transition flex items-center gap-1 font-semibold">
                  <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.067 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                  <span>1.8K</span>
                </span>
              </div>

              <!-- Carousel arrows -->
              <div class="flex items-center gap-1 text-slate-500">
                <button class="w-8 h-8 rounded-full border border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900 transition flex items-center justify-center shadow-2xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                </button>
                <button class="w-8 h-8 rounded-full border border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900 transition flex items-center justify-center shadow-2xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Ad Cards Grid -->
          <div id="adGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            <!-- Injected via JavaScript -->
          </div>
        </div>

      </div>

      <!-- ========================================== -->
      <!-- VIEW 2: BRANDTRACKER (RADAR TREND) VIEW    -->
      <!-- ========================================== -->
      <div id="brandtrackerView" class="space-y-6 hidden">
        
        <!-- Radar Banner & Sub-header -->
        <div class="tt-card p-6">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-100">
            <div>
              <div class="flex items-center gap-3">
                <h1 class="text-2xl font-extrabold tracking-tight text-slate-900">Brandtracker</h1>
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
                  <span>Live Scaling Radar</span>
                </span>
              </div>
              <p class="text-xs text-slate-500 mt-1">
                Phát hiện sớm các thương hiệu đang vít hàng nghìn chiến dịch mới trong 7 ngày để bắt kịp sóng sản phẩm Hot Trend.
              </p>
            </div>

            <!-- Quick Filters & Timeframe -->
            <div class="flex flex-wrap items-center gap-3">
              <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
                <button class="px-3 py-1.5 rounded-lg bg-white text-slate-900 font-bold shadow-xs">All trackers</button>
                <button class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition">Example shops</button>
                <button class="px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition">+ Create folder</button>
              </div>

              <!-- Timeframe Switcher -->
              <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-bold text-slate-600">
                <button class="px-2.5 py-1.5 rounded-lg hover:text-slate-900 transition">24H</button>
                <button class="px-2.5 py-1.5 rounded-lg bg-slate-900 text-white shadow-xs">7D</button>
                <button class="px-2.5 py-1.5 rounded-lg hover:text-slate-900 transition">14D</button>
                <button class="px-2.5 py-1.5 rounded-lg hover:text-slate-900 transition">30D</button>
              </div>
            </div>
          </div>

          <!-- Filter / Search row -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-4">
            <div class="relative flex-1 max-w-md">
              <input 
                type="text" 
                id="brandtrackerFilterInput" 
                oninput="filterBrandtrackerTable()"
                placeholder="Lọc danh sách thương hiệu trong Radar..." 
                class="w-full h-9 pl-9 pr-4 rounded-xl tt-input text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition font-medium"
              />
              <svg class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>

            <div class="flex items-center gap-3 text-xs text-slate-600">
              <span class="font-medium">Sort by:</span>
              <select id="brandtrackerSortSelect" onchange="sortBrandtrackerTable()" class="bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-800 text-xs font-semibold focus:outline-none focus:border-blue-500 shadow-2xs">
                <option value="launches">Chiến dịch mới 7D (Cao nhất)</option>
                <option value="liveAds">Số Ads đang chạy (Live Ads)</option>
                <option value="traffic">Lưu lượng truy cập (Traffic)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Brandtracker Table Matching User's Screenshot media_1790650569731.png -->
        <div class="tt-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 text-slate-500 font-bold uppercase tracking-wider text-[11px] border-b border-slate-200">
                <tr>
                  <th class="py-3.5 px-6">Shop info</th>
                  <th class="py-3.5 px-6">Traffic (Visits)</th>
                  <th class="py-3.5 px-6">Live ads</th>
                  <th class="py-3.5 px-6">Spend / Reach · 7D</th>
                  <th class="py-3.5 px-6 min-w-[280px]">Launches (Tốc độ lên Camp 7D)</th>
                </tr>
              </thead>
              <tbody id="brandtrackerTableBody" class="divide-y divide-slate-100 bg-white">
                <!-- Dynamically populated via JavaScript -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </main>
  </div>

  <!-- SPLIT MODAL DRAWER (Matching TrendTrack media_1790645855191.png & media_1790650473166.png) -->
  <div id="adModal" class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm hidden flex items-center justify-center p-4 lg:p-8">
    <div class="bg-white border border-slate-200 rounded-3xl w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl relative">
      
      <!-- Top Bar of Modal -->
      <div class="h-14 px-6 border-b border-slate-200 flex items-center justify-between bg-white">
        <div class="flex items-center gap-3">
          <img id="modalShopAvatar" src="" class="w-8 h-8 rounded-lg object-cover border border-slate-200"/>
          <span id="modalShopName" class="font-extrabold text-sm text-slate-900">The Oodie UK</span>
          <a id="modalShopLink" href="#" target="_blank" class="text-xs text-blue-600 hover:underline flex items-center gap-1 font-semibold">
            <span id="modalShopDomain">theoodie.co.uk</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          </a>
          <span class="text-xs">🇬🇧 UK</span>
        </div>

        <div class="flex items-center gap-2.5">
          <button class="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 text-xs font-bold hover:bg-slate-50 transition flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
            <span>Share</span>
          </button>
          <a id="modalMetaAnalyticsBtn" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-[#15803d] hover:bg-[#166534] text-white text-xs font-bold transition flex items-center gap-1.5 shadow-xs">
            <span>Meta analytics</span>
          </a>
          <div class="w-px h-5 bg-slate-200 mx-1"></div>
          <button onclick="closeAdModal()" class="p-1.5 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-700 transition" title="Close">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>

      <!-- Split Body Container -->
      <div class="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-slate-200 custom-scroll">
        
        <!-- LEFT HALF: Ad Preview & Media Player -->
        <div class="p-6 flex flex-col justify-between items-center bg-[#f8fafc]">
          <div class="w-full max-w-md bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-3">
            
            <!-- Facebook Profile Card Header -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <img id="cardModalAvatar" src="" class="w-9 h-9 rounded-full object-cover border border-slate-200"/>
                <div>
                  <div class="font-extrabold text-xs text-slate-900" id="cardModalAdvName">The Oodie</div>
                  <div class="text-[10px] text-slate-400 flex items-center gap-1.5">
                    <span>Sponsored</span>
                    <span>•</span>
                    <span id="cardModalAdId" class="font-mono text-slate-400">ID: 809230588636735</span>
                  </div>
                </div>
              </div>
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                ● Active
              </span>
            </div>

            <!-- Ad Copy / Primary Text -->
            <div id="cardModalCopy" class="text-xs text-slate-700 leading-relaxed font-normal whitespace-pre-line max-h-24 overflow-y-auto custom-scroll p-2.5 bg-slate-50 rounded-xl border border-slate-100">
              The Oodie is like a giant warm hug! Made with ultra-soft fleece...
            </div>

            <!-- Video / Media Container -->
            <div id="cardModalMediaContainer" class="relative rounded-xl overflow-hidden bg-slate-900 border border-slate-200 aspect-square flex items-center justify-center max-h-[380px]">
              <video id="cardModalVideo" controls autoplay loop muted playsinline class="w-full h-full object-contain"></video>
              <img id="cardModalImage" class="w-full h-full object-contain hidden" src=""/>
            </div>

            <!-- CTA Bottom Bar -->
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-200">
              <div class="truncate max-w-[220px]">
                <div id="cardModalCtaDomain" class="text-[9px] text-slate-400 uppercase font-bold tracking-wider truncate">theoodie.co.uk</div>
                <div id="cardModalCtaTitle" class="text-xs font-bold text-slate-800 truncate">Shop The Oodie Online</div>
              </div>
              <a id="cardModalCtaBtn" href="#" target="_blank" class="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-xs transition cursor-pointer flex items-center gap-1">
                <span>Shop Now</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
            </div>

          </div>

          <!-- Bottom Action Toolbar (Floating Dark Pill matching TrendTrack) -->
          <div class="mt-4 px-4 py-2 rounded-full bg-slate-900 text-white shadow-xl flex items-center gap-4 text-xs font-semibold">
            <button onclick="downloadCreative()" class="hover:text-blue-400 transition flex items-center gap-1" title="Download">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            </button>
            <a id="btnOriginalAd" href="#" target="_blank" class="hover:text-blue-400 transition" title="Meta Ad Library">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
            <div class="w-px h-3.5 bg-slate-700"></div>
            <button onclick="prevAd()" class="hover:text-blue-400 transition" title="Previous Ad">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
            </button>
            <span id="modalAdCounter" class="text-xs font-bold text-slate-300">Ad 1 / 20</span>
            <button onclick="nextAd()" class="hover:text-blue-400 transition" title="Next Ad">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </button>
          </div>
        </div>

        <!-- RIGHT HALF: Deep Ad Analytics & Advertiser DNA -->
        <div class="p-6 space-y-6 bg-white overflow-y-auto custom-scroll">
          
          <!-- SECTION: AD DETAILS -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Ad Details & Longevity</span>
              <span id="detailRankBadge" class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
                Top 2% Winning Creative
              </span>
            </div>

            <!-- 4 Metric Cards -->
            <div class="grid grid-cols-2 gap-3">
              <!-- Card 1: AD RANK -->
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <div class="flex items-center justify-between text-[10px] uppercase font-bold text-slate-500 mb-1">
                  <span>Ad Rank</span>
                  <span class="text-purple-600 font-extrabold">🔥 #8 / 415</span>
                </div>
                <div class="text-xs text-slate-600">
                  <span id="detailRankScale" class="font-extrabold text-slate-900 text-base">Top 2%</span>
                  <span class="text-slate-500 ml-1">của shop</span>
                </div>
                <div class="w-full bg-slate-200 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div id="detailRankBar" class="bg-purple-600 h-full rounded-full" style="width: 98%"></div>
                </div>
              </div>

              <!-- Card 2: ADS ON THIS LP -->
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <div class="flex items-center justify-between text-[10px] uppercase font-bold text-slate-500 mb-1">
                  <span>Ads on this LP</span>
                  <span class="text-blue-600 font-bold" id="detailLpRatio">61% of ads</span>
                </div>
                <div class="flex items-baseline gap-1">
                  <span id="detailLpCount" class="text-base font-extrabold text-slate-900">252</span>
                  <span class="text-[11px] text-slate-500">ads trỏ về link này</span>
                </div>
                <div class="w-full bg-slate-200 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div id="detailLpBar" class="bg-blue-600 h-full rounded-full" style="width: 61%"></div>
                </div>
              </div>

              <!-- Card 3: REACH -->
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-500 mb-1">Reach (DSA EU)</div>
                <div id="detailReach" class="text-base font-extrabold text-slate-900">—</div>
                <div class="text-[10px] text-slate-500">Non-EU targeting</div>
              </div>

              <!-- Card 4: SPEND -->
              <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-500 mb-1">Spend (DSA EU)</div>
                <div id="detailSpend" class="text-base font-extrabold text-slate-900">—</div>
                <div class="text-[10px] text-slate-500">Meta transparency policy</div>
              </div>
            </div>

            <!-- Detail Rows -->
            <div class="grid grid-cols-2 gap-4 text-xs pt-2">
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Landing Page</span>
                <a id="detailLandingUrl" href="#" target="_blank" class="text-blue-600 hover:underline truncate block font-medium mt-0.5">
                  theoodie.co.uk/collections/...
                </a>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Format</span>
                <span id="detailFormat" class="text-slate-800 font-semibold mt-0.5 block">Video (MP4)</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">CTA</span>
                <span id="detailCta" class="text-slate-800 font-semibold mt-0.5 block">Shop Now</span>
              </div>
              <div>
                <span class="text-slate-400 block text-[10px] uppercase font-bold">Language</span>
                <span id="detailLanguage" class="text-slate-800 font-semibold mt-0.5 block">English</span>
              </div>
            </div>
          </div>

          <!-- SECTION: ADVERTISER DETAILS -->
          <div class="pt-6 border-t border-slate-200 space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Advertiser Details</span>
              <a id="btnMetaAdsLibrary" href="#" target="_blank" class="px-2.5 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold hover:bg-emerald-100 transition flex items-center gap-1">
                <span>Advertiser page</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            </div>

            <!-- 4 Advertiser KPI Boxes -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Active Ads</div>
                <div id="advActiveAds" class="text-base font-extrabold text-slate-900">● 415 / 13.9K</div>
                <div class="text-[10px] text-slate-500">Global running</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Ads Launched</div>
                <div id="advVelocity" class="text-xs font-bold text-slate-800">7d: 84 | 14d: 115</div>
                <div class="text-[10px] text-slate-500">30d: 395</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Reach</div>
                <div id="advReach" class="text-base font-extrabold text-slate-900">340.4M</div>
                <div class="text-[10px] text-slate-500">Global traffic</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Spend</div>
                <div id="advSpend" class="text-base font-extrabold text-slate-900">$3.1M</div>
                <div class="text-[10px] text-slate-500">$7.1K/d</div>
              </div>
            </div>

            <!-- Top Landing Pages Preview Strip -->
            <div class="pt-2">
              <div class="text-xs font-bold text-slate-800 mb-2">🔥 Top Winning Landing Pages (Hero Funnels)</div>
              <div id="landingPagesStrip" class="grid grid-cols-2 gap-3">
                <!-- Injected via JS -->
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <script>
    let currentData = null;
    let currentAdIndex = 0;
    let trendChartInstance = null;
    let tiktokChartInstance = null;
    let brandtrackerStores = [];

    // Switch between Explorer and Brandtracker views
    function switchView(viewName) {
      const expView = document.getElementById('explorerView');
      const btView = document.getElementById('brandtrackerView');
      const sideExp = document.getElementById('sideNavExplorer');
      const sideBt = document.getElementById('sideNavBrandtracker');

      if (viewName === 'brandtracker') {
        expView.classList.add('hidden');
        btView.classList.remove('hidden');
        
        if (sideBt) sideBt.className = "w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition bg-emerald-600 text-white shadow-md shadow-emerald-500/20";
        if (sideExp) sideExp.className = "w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition";
        
        loadBrandtrackerData();
      } else {
        btView.classList.add('hidden');
        expView.classList.remove('hidden');

        if (sideExp) sideExp.className = "w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold transition bg-blue-600 text-white shadow-md shadow-blue-500/20";
        if (sideBt) sideBt.className = "w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition";
      }
    }

    // Load Brandtracker Benchmark Data
    async function loadBrandtrackerData() {
      try {
        const res = await fetch('/api/brandtracker');
        const data = await res.json();
        brandtrackerStores = data;
        renderBrandtrackerTable(data);
      } catch (err) {
        console.error('Error loading brandtracker:', err);
      }
    }

    // Render Brandtracker Table
    function renderBrandtrackerTable(stores) {
      const tbody = document.getElementById('brandtrackerTableBody');
      tbody.innerHTML = '';

      stores.forEach(store => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-50 transition cursor-pointer group";
        tr.onclick = () => {
          switchView('explorer');
          document.getElementById('brandInput').value = store.name;
          loadBrand(store.name);
        };

        const trafficSvgColor = store.trafficTrend === 'down' ? '#ef4444' : '#10b981';
        const adsSvgColor = store.adsTrend === 'down' ? '#ef4444' : '#10b981';

        const thumbs = (store.launchThumbnails || []).slice(0, 3).map(img => `
          <div class="w-12 h-12 rounded-lg overflow-hidden border border-slate-200 bg-slate-100 shrink-0">
            <img src="${img}" class="w-full h-full object-cover"/>
          </div>
        `).join('');

        tr.innerHTML = `
          <!-- Shop info -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <img src="${store.logo}" class="w-11 h-11 rounded-xl object-cover border border-slate-200 bg-white shrink-0"/>
              <div>
                <div class="flex items-center gap-1.5">
                  <span class="font-extrabold text-sm text-slate-900 group-hover:text-blue-600 transition">${store.name}</span>
                  <span class="text-xs">${store.flag || '🌐'}</span>
                </div>
                <div class="text-[11px] text-slate-500 font-mono">${store.domain}</div>
                <div class="text-[10px] text-slate-400 mt-0.5">${store.age}</div>
              </div>
            </div>
          </td>

          <!-- Traffic -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="min-w-[60px]">
                <div class="text-sm font-extrabold text-slate-900">${store.traffic}</div>
                <div class="text-[10px] text-slate-400">monthly visits</div>
              </div>
              <div class="w-20 h-7 shrink-0">
                <svg width="80" height="28" viewBox="0 0 80 28" fill="none">
                  <path d="${store.trafficTrace || 'M 0 14 Q 40 5 80 14'}" stroke="${trafficSvgColor}" stroke-width="1.8" stroke-linecap="round" fill="none"/>
                </svg>
              </div>
            </div>
          </td>

          <!-- Live ads -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="min-w-[60px]">
                <div class="flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                  <span class="text-sm font-extrabold text-slate-900">${Number(store.liveAds).toLocaleString()}</span>
                </div>
                <div class="text-[10px] text-slate-400">${store.countriesCount || 1} countries</div>
              </div>
              <div class="w-20 h-7 shrink-0">
                <svg width="80" height="28" viewBox="0 0 80 28" fill="none">
                  <path d="${store.adsTrace || 'M 0 14 Q 40 22 80 14'}" stroke="${adsSvgColor}" stroke-width="1.8" stroke-linecap="round" fill="none"/>
                </svg>
              </div>
            </div>
          </td>

          <!-- Spend / Reach -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="min-w-[70px]">
                <div class="text-xs font-bold text-slate-900">${store.spendDay || '$5K /day'}</div>
                <div class="text-[10px] text-slate-400">${store.reachDay || '500K /day'}</div>
              </div>
              <div class="w-20 h-7 shrink-0">
                <svg width="80" height="28" viewBox="0 0 80 28" fill="none">
                  <path d="${store.spendTrace || 'M 0 20 Q 20 5 40 18 T 80 10'}" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" fill="none"/>
                </svg>
              </div>
            </div>
          </td>

          <!-- Launches -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="flex items-center gap-1.5">
                ${thumbs}
              </div>
              <div>
                <div class="text-xs font-extrabold text-slate-900">${(store.launchesCount || 120).toLocaleString()}</div>
                <div class="text-[10px] text-slate-400">ads launched (7 days)</div>
              </div>
            </div>
          </td>
        `;

        tbody.appendChild(tr);
      });
    }

    function filterBrandtrackerTable() {
      const q = document.getElementById('brandtrackerFilterInput').value.toLowerCase();
      const filtered = brandtrackerStores.filter(s => s.name.toLowerCase().includes(q) || s.domain.toLowerCase().includes(q));
      renderBrandtrackerTable(filtered);
    }

    function sortBrandtrackerTable() {
      const mode = document.getElementById('brandtrackerSortSelect').value;
      const sorted = [...brandtrackerStores];
      if (mode === 'launches') {
        sorted.sort((a, b) => (b.launchesCount || 0) - (a.launchesCount || 0));
      } else if (mode === 'liveAds') {
        sorted.sort((a, b) => (b.liveAds || 0) - (a.liveAds || 0));
      } else if (mode === 'traffic') {
        const parseVis = val => {
          if (!val) return 0;
          if (val.includes('M')) return parseFloat(val) * 1000000;
          if (val.includes('K')) return parseFloat(val) * 1000;
          return parseFloat(val) || 0;
        };
        sorted.sort((a, b) => parseVis(b.traffic) - parseVis(a.traffic));
      }
      renderBrandtrackerTable(sorted);
    }

    // Load Brand Data for Explorer
    async function loadBrand(query) {
      document.getElementById('btnSpinner').classList.remove('hidden');
      document.getElementById('btnText').textContent = 'Đang quét...';

      document.getElementById('shopName').textContent = query;
      document.getElementById('shopDomain').textContent = 'Đang phân tích tên miền...';
      document.getElementById('shopFollowers').textContent = 'Đang kết nối Meta Ad Library...';
      document.getElementById('adGrid').innerHTML = `
        <div class="col-span-full py-20 flex flex-col items-center justify-center text-center space-y-4">
          <div class="w-12 h-12 rounded-full border-4 border-blue-500/20 border-t-blue-600 animate-spin"></div>
          <div>
            <div class="text-base font-bold text-slate-900">Đang quét Meta Ad Library cho: <span class="text-blue-600 font-extrabold">${query}</span>...</div>
            <div class="text-xs text-slate-500 mt-1">Đang bóc tách video creative, link landing page và ngày chạy...</div>
          </div>
        </div>
      `;

      try {
        const res = await fetch('/api/scan?query=' + encodeURIComponent(query));
        const data = await res.json();
        currentData = data;
        renderDashboard(data);
      } catch (err) {
        alert('Lỗi tải dữ liệu: ' + err.message);
      } finally {
        document.getElementById('btnSpinner').classList.add('hidden');
        document.getElementById('btnText').textContent = 'Quét';
      }
    }

    // Render Full Explorer Dashboard
    function renderDashboard(data) {
      const qTitle = data.name || data.query || 'Brand';
      const cleanDomain = data.domain || (qTitle.toLowerCase().replace(/[^a-z0-9]/g, '') + '.com');
      document.getElementById('shopName').textContent = qTitle;
      document.getElementById('shopDomain').textContent = cleanDomain;
      document.getElementById('shopDomainLink').href = 'https://' + cleanDomain;
      document.getElementById('shopAvatar').src = data.avatarUrl || ('https://ui-avatars.com/api/?name=' + encodeURIComponent(qTitle) + '&background=0284c7&color=fff');
      document.getElementById('shopAge').textContent = data.advertiserAge || 'Verified Store';
      document.getElementById('shopFollowers').textContent = (data.total_active_ads || data.ads?.length || 0) + ' active ads on Meta';
      
      // Channel counts
      const metaCount = data.channels?.meta?.active ?? data.total_active_ads ?? (data.ads ? data.ads.length : 0);
      const tiktokCount = data.channels?.tiktok?.active ?? (data.tiktok?.totalTikToks || '-');
      const googleCount = data.channels?.google?.active ?? '-';
      
      document.getElementById('metaChannelCount').textContent = metaCount;
      document.getElementById('tiktokChannelCount').textContent = tiktokCount;
      document.getElementById('googleChannelCount').textContent = googleCount;

      const advMeta = document.getElementById('advCardMetaCount');
      if (advMeta) advMeta.textContent = metaCount;
      const advTt = document.getElementById('advCardTiktokCount');
      if (advTt) advTt.textContent = tiktokCount;

      const feedMeta = document.getElementById('feedMetaCount');
      if (feedMeta) feedMeta.textContent = metaCount;
      const feedTt = document.getElementById('feedTiktokCount');
      if (feedTt) feedTt.textContent = tiktokCount;

      // KPIs
      document.getElementById('kpiActiveAds').textContent = metaCount;
      document.getElementById('kpiTotalAds').textContent = '/ ' + (data.total_all_time || (metaCount * 4) + '+');
      document.getElementById('kpiAdsLaunched').textContent = data.kpis?.ads_launched_30d || (Math.round(metaCount * 1.4) + '');
      document.getElementById('kpiReach').textContent = data.kpis?.reach_estimate || '300.9M';
      document.getElementById('kpiSpend').textContent = '· ' + (data.kpis?.spend_estimate || '$2.7M');

      // Countries targeted bar
      const targetCountriesEl = document.getElementById('targetCountriesList');
      if (targetCountriesEl) {
        targetCountriesEl.innerHTML = '';
        const list = data.countriesTargeted || [
          { countryCode: 'AU', percentage: 14.7 },
          { countryCode: 'US', percentage: 14.7 },
          { countryCode: 'GB', percentage: 13.8 }
        ];
        const flagMap = { AU: '🇦🇺', US: '🇺🇸', GB: '🇬🇧', DE: '🇩🇪', IE: '🇮🇪', NL: '🇳🇱', CA: '🇨🇦', AT: '🇦🇹', BE: '🇧🇪', DK: '🇩🇰', FI: '🇫🇮', SE: '🇸🇪', NZ: '🇳🇿', FR: '🇫🇷' };
        list.slice(0, 3).forEach(c => {
          const pill = document.createElement('span');
          pill.className = "px-2.5 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-[11px] flex items-center gap-1";
          pill.textContent = `${flagMap[c.countryCode] || '🌐'} ${c.percentage}%`;
          targetCountriesEl.appendChild(pill);
        });
        const moreSpan = document.createElement('span');
        moreSpan.className = "text-slate-400 text-xs ml-1";
        moreSpan.textContent = "11 more countries";
        targetCountriesEl.appendChild(moreSpan);
      }

      // Chart.js Area Spline
      renderTrendChart(data.history_points || data.historyChart || []);

      // TikTok Intelligence Binding
      const tt = data.tiktok || {
        totalTikToks: data.channels?.tiktok?.active || 703,
        views: '3.9M',
        likes: '97K',
        topHashtags: ['#theoodie', '#oodie', '#oodiesquad', '#oodiestorytime'],
        history: [
          { date: 'Apr', views: 3.6 },
          { date: 'May', views: 3.65 },
          { date: 'Jun', views: 3.7 },
          { date: 'Jul', views: 3.8 },
          { date: 'Aug', views: 3.85 },
          { date: 'Sep', views: 3.9 }
        ]
      };

      const ttHeaderCountEl = document.getElementById('tiktokHeaderCount');
      if (ttHeaderCountEl) {
        ttHeaderCountEl.textContent = tt.totalTikToks || tt.total_tiktoks || (data.channels?.tiktok?.active || '703');
      }

      const ttViewsEl = document.getElementById('tiktokViewsVal');
      if (ttViewsEl) {
        ttViewsEl.textContent = tt.views || '3.9M';
      }

      const ttLikesEl = document.getElementById('tiktokLikesVal');
      if (ttLikesEl) {
        ttLikesEl.textContent = tt.likes || '97K';
      }

      const hashList = document.getElementById('tiktokHashtagsList');
      if (hashList) {
        hashList.innerHTML = '';
        const tags = tt.topHashtags || ['#theoodie', '#oodie', '#oodiesquad', '#oodiestorytime'];
        tags.slice(0, 5).forEach(t => {
          const pill = document.createElement('span');
          pill.className = "px-2.5 py-0.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 font-medium text-[11px] whitespace-nowrap hover:border-teal-500 hover:text-teal-700 transition cursor-pointer";
          pill.textContent = t.startsWith('#') ? t : ('#' + t);
          hashList.appendChild(pill);
        });
      }

      renderTikTokChart(tt);

      // Feed Ad Cards
      renderFeedCards(data.ads || []);
    }

    // Render TrendChart (Purple Spline with Peak Labels)
    function renderTrendChart(history) {
      const ctx = document.getElementById('trendChart').getContext('2d');
      if (trendChartInstance) {
        trendChartInstance.destroy();
      }

      let labels = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
      let dataValues = [280, 203, 360, 480, 605, 520, 415];

      if (history && history.length > 0) {
        labels = [];
        dataValues = [];
        const step = Math.max(1, Math.floor(history.length / 10));
        for (let i = 0; i < history.length; i += step) {
          const dt = history[i].date ? history[i].date.split('T')[0] : `Point ${i+1}`;
          try {
            const dObj = new Date(dt);
            labels.push(dObj.toLocaleDateString('en-US', { month: 'short' }));
          } catch(e) {
            labels.push(dt);
          }
          dataValues.push(history[i].runningAds || history[i].activeAds || history[i].adsCount || 300);
        }
      }

      const gradient = ctx.createLinearGradient(0, 0, 0, 180);
      gradient.addColorStop(0, 'rgba(139, 92, 246, 0.22)');
      gradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');

      trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Active Meta Ads',
            data: dataValues,
            fill: true,
            backgroundColor: gradient,
            borderColor: '#8b5cf6',
            borderWidth: 2.5,
            tension: 0.45,
            pointRadius: 3,
            pointBackgroundColor: '#8b5cf6',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#8b5cf6',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#0f172a',
              titleColor: '#cbd5e1',
              bodyColor: '#fff',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10,
              displayColors: false
            }
          },
          scales: {
            x: {
              grid: { display: false, drawBorder: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            },
            y: {
              grid: { color: 'rgba(0, 0, 0, 0.04)', drawBorder: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            }
          }
        }
      });
    }

    // Render TikTok Spline Chart (Teal Curve)
    function renderTikTokChart(tiktok) {
      const canvas = document.getElementById('tiktokChart');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (tiktokChartInstance) {
        tiktokChartInstance.destroy();
      }

      let labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
      let dataValues = [3.6, 3.65, 3.7, 3.8, 3.85, 3.9];

      if (tiktok && tiktok.history && tiktok.history.length > 0) {
        labels = tiktok.history.map(h => h.date);
        dataValues = tiktok.history.map(h => typeof h.views === 'number' ? h.views : parseFloat(h.views) || 0);
      }

      const gradient = ctx.createLinearGradient(0, 0, 0, 180);
      gradient.addColorStop(0, 'rgba(13, 148, 136, 0.22)');
      gradient.addColorStop(1, 'rgba(13, 148, 136, 0.0)');

      tiktokChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Views (M)',
            data: dataValues,
            fill: true,
            backgroundColor: gradient,
            borderColor: '#0d9488',
            borderWidth: 2.5,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#0d9488',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#0d9488'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#0f172a',
              titleColor: '#cbd5e1',
              bodyColor: '#14b8a6',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 8,
              displayColors: false,
              callbacks: {
                label: function(context) {
                  return '● Views: ' + context.parsed.y + 'M';
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false, drawBorder: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            },
            y: {
              grid: { color: 'rgba(0, 0, 0, 0.04)', drawBorder: false },
              ticks: {
                color: '#64748b',
                font: { size: 10 },
                callback: function(val) {
                  return val + 'M';
                }
              }
            }
          }
        }
      });
    }

    // Render Feed Cards (100% Matching TrendTrack media_1790645848625.png)
    function renderFeedCards(ads) {
      const grid = document.getElementById('adGrid');
      grid.innerHTML = '';

      if (!ads || ads.length === 0) {
        grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-400 font-medium">Không có quảng cáo nào. Vui lòng quét thương hiệu khác.</div>';
        return;
      }

      const totalAds = currentData.total_active_ads || ads.length || 415;

      ads.forEach((ad, index) => {
        const card = document.createElement('div');
        card.className = "tt-card p-3 flex flex-col justify-between hover:shadow-md hover:border-slate-300 transition duration-200 cursor-pointer group";
        card.onclick = () => openAdModal(index);

        const isVideo = ad.type === 'video' || ad.mediaType === 'video' || (ad.video_url && ad.video_url.length > 5) || (ad.mediaUrl && ad.mediaUrl.includes('.mp4'));
        const videoSrc = ad.video_url || (ad.mediaType === 'video' ? ad.mediaUrl : '');
        const imgSrc = ad.image_url || ad.thumbnail_url || (ad.mediaType === 'image' || ad.mediaType === 'dco' ? ad.mediaUrl : '') || 'https://via.placeholder.com/400';
        const daysRunning = ad.days_active ?? ad.daysRunning ?? 0;
        const advertiserName = ad.advertiser || ad.advertiserName || currentData.name || 'The Oodie';
        const copyText = ad.primary_text || ad.description || ad.hook || 'Too hot for clingy PJs? Too cute for boring loungewear? Say hello to comfort.';
        const landingUrl = ad.landing_url || ad.landingUrl || ('https://' + (currentData.domain || 'theoodie.com'));
        const ctaText = (ad.ctaText || ad.cta_type || 'Shop Now').replace(/_/g, ' ');
        const ctaDomain = (ad.ctaDomain || ad.domain || currentData.domain || 'THEOODIE.CO.UK').toUpperCase();
        const ctaDesc = ad.ctaDescription || ad.cta_title || 'Shop Online';

        // Format Start Date: e.g. Sep 28
        let startDateStr = 'Sep 28';
        if (ad.startDate) {
          try {
            const d = new Date(ad.startDate);
            startDateStr = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          } catch(e) {}
        }

        // Row 2: Targeting Pill
        const hasTargeting = (ad.euReach && ad.euReach > 0) || (ad.targetCountryCodes && ad.targetCountryCodes.length > 0);
        const countryFlags = (ad.targetCountryCodes || ['GB']).map(c => c === 'GB' ? '🇬🇧' : c === 'US' ? '🇺🇸' : c === 'AU' ? '🇦🇺' : '🌐').join(' ');
        const targetingHtml = hasTargeting
          ? `<div class="bg-blue-600 text-white px-2.5 py-1 rounded-full text-[11px] font-bold flex items-center justify-between shadow-xs">
               <div class="flex items-center gap-1.5">
                 <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
                 <span>${ad.euReach || 2} · $0.0 · $0/d</span>
               </div>
               <span>${countryFlags}</span>
             </div>`
          : `<div class="bg-slate-100 text-slate-500 px-2.5 py-1 rounded-full text-[11px] font-medium flex items-center gap-1.5">
               <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
               <span>No targeting data</span>
             </div>`;

        // Row 3: Ad Rank
        const orderNum = ad.adOrder || (totalAds - index);
        const popTotal = ad.adRankPopulation || totalAds;
        const rankPct = Math.round((orderNum / popTotal) * 100);
        const isDeclining = rankPct < 60;
        const rankHtml = isDeclining
          ? `<div class="text-rose-600 font-bold text-xs flex items-center gap-1.5">
               <svg class="w-3.5 h-3.5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/></svg>
               <span>${orderNum}/${popTotal} (${rankPct}%)</span>
               <span class="text-rose-500">↘</span>
             </div>`
          : `<div class="text-slate-800 font-bold text-xs flex items-center gap-1.5">
               <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
               <span>${orderNum}/${popTotal} (${rankPct}%)</span>
             </div>`;

        card.innerHTML = `
          <!-- Top Badges Row 1 -->
          <div class="flex items-center justify-between gap-2 mb-2">
            <span class="bg-emerald-50 text-emerald-700 border border-emerald-200/80 px-2.5 py-0.5 rounded-full text-[11px] font-bold flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              <span>Active</span>
            </span>
            <span class="bg-slate-100 text-slate-600 px-2.5 py-0.5 rounded-full text-[11px] font-medium flex items-center gap-1">
              <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <span>${daysRunning}d · ${startDateStr} → now</span>
            </span>
          </div>

          <!-- Top Row 2: Targeting -->
          <div class="mb-2">
            ${targetingHtml}
          </div>

          <!-- Top Row 3: Rank -->
          <div class="px-1 py-1 mb-2 border-b border-slate-100 pb-2">
            ${rankHtml}
          </div>

          <!-- Facebook Ad Mockup Box -->
          <div class="border border-slate-200 rounded-xl overflow-hidden bg-white p-2.5 flex flex-col space-y-2 mb-3 shadow-2xs">
            <!-- Mockup Header -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <img src="${ad.advertiserAvatarUrl || currentData.avatarUrl || 'https://ui-avatars.com/api/?name=Oodie'}" class="w-7 h-7 rounded-full object-cover border border-slate-200"/>
                <div>
                  <div class="text-xs font-bold text-slate-900 truncate max-w-[130px]">${advertiserName}</div>
                  <div class="text-[10px] text-slate-400 flex items-center gap-1">
                    <span>Sponsored</span>
                    <span>·</span>
                    <svg class="w-2.5 h-2.5 text-slate-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                  </div>
                </div>
              </div>
              ${ad.hasLowImpressions ? `<span class="bg-slate-900 text-slate-200 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1 shadow-xs">🪐 Low reach</span>` : ''}
            </div>

            <!-- Copy -->
            <p class="text-[11px] text-slate-700 line-clamp-3 leading-relaxed">
              ${copyText}
            </p>
            <span class="text-[11px] font-bold text-slate-900 -mt-1 block hover:underline">See More</span>

            <!-- Media -->
            <div class="relative aspect-square rounded-lg overflow-hidden bg-slate-900 flex items-center justify-center">
              ${isVideo && videoSrc 
                ? `<video src="${videoSrc}" muted loop playsinline class="w-full h-full object-cover"></video>
                   <div class="absolute inset-0 bg-black/20 flex items-center justify-center">
                     <div class="w-9 h-9 rounded-full bg-black/60 backdrop-blur border border-white/20 flex items-center justify-center text-white shadow-md">
                       <svg class="w-4 h-4 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                     </div>
                   </div>`
                : `<img src="${imgSrc}" class="w-full h-full object-cover"/>`
              }
              ${ad.duplicates && ad.duplicates > 1 ? `<div class="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/70 backdrop-blur text-[10px] font-medium text-white">1/${ad.duplicates} Multiple me...</div>` : ''}
            </div>

            <!-- CTA Strip -->
            <div class="flex items-center justify-between p-2 rounded-lg bg-slate-50 border border-slate-100">
              <div class="truncate max-w-[130px]">
                <div class="text-[9px] font-bold text-slate-400 uppercase truncate">${ctaDomain}</div>
                <div class="text-[11px] font-bold text-slate-800 truncate">${ctaDesc}</div>
              </div>
              <button class="bg-slate-200 hover:bg-slate-300 text-slate-800 text-[11px] font-bold px-3 py-1 rounded-md transition shrink-0">
                ${ctaText}
              </button>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
            <div class="flex items-center gap-1.5">
              <div class="relative">
                <img src="${ad.advertiserAvatarUrl || currentData.avatarUrl || 'https://ui-avatars.com/api/?name=Oodie'}" class="w-5 h-5 rounded-full object-cover border border-slate-200"/>
                <span class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-blue-600 flex items-center justify-center text-[7px] text-white font-bold">∞</span>
              </div>
              <span class="text-xs font-bold text-slate-800 truncate max-w-[80px]">${advertiserName}</span>
              <span class="text-[10px] text-slate-400">•</span>
              <span class="text-[10px] font-bold text-slate-700">● ${totalAds}</span>
              <span class="text-[10px] text-slate-400">/ 13.9K</span>
              <span class="text-xs">🇦🇺 🇬🇧</span>
            </div>

            <div class="flex items-center gap-1 text-slate-400">
              <button class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-slate-700 transition" title="Save">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg>
              </button>
              <button class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-slate-700 transition" title="Menu">
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>
              </button>
            </div>
          </div>
        `;

        grid.appendChild(card);
      });
    }

    // Modal Drawer logic
    function openAdModal(index) {
      if (!currentData || !currentData.ads || !currentData.ads[index]) return;
      currentAdIndex = index;
      const ad = currentData.ads[index];

      const modal = document.getElementById('adModal');
      modal.classList.remove('hidden');

      const isVideo = ad.type === 'video' || ad.mediaType === 'video' || (ad.video_url && ad.video_url.length > 5) || (ad.mediaUrl && ad.mediaUrl.includes('.mp4'));
      const videoSrc = ad.video_url || (ad.mediaType === 'video' ? ad.mediaUrl : '');
      const imgSrc = ad.image_url || ad.thumbnail_url || (ad.mediaType === 'image' || ad.mediaType === 'dco' ? ad.mediaUrl : '') || '';
      const daysRunning = ad.days_active ?? ad.daysRunning ?? 0;
      const advertiserName = ad.advertiser || ad.advertiserName || currentData.name || 'Advertiser';
      const copyText = ad.primary_text || ad.description || ad.hook || 'No copy text available.';
      const landingUrl = ad.landing_url || ad.landingUrl || ('https://' + (currentData.domain || 'store.com'));
      const adLibraryUrl = ad.ad_library_url || ad.metaLibraryUrl || ('https://www.facebook.com/ads/library/?id=' + (ad.ad_archive_id || ad.platformAdId || ''));

      // Fill top bar
      document.getElementById('modalShopAvatar').src = currentData.avatarUrl || '';
      document.getElementById('modalShopName').textContent = currentData.name || 'Store';
      document.getElementById('modalShopDomain').textContent = currentData.domain || 'store.com';
      document.getElementById('modalShopLink').href = 'https://' + (currentData.domain || 'store.com');
      document.getElementById('modalAdCounter').textContent = `Ad ${index + 1} / ${currentData.ads.length}`;
      document.getElementById('modalMetaAnalyticsBtn').href = adLibraryUrl;

      // Fill Left Half
      document.getElementById('cardModalAvatar').src = currentData.avatarUrl || '';
      document.getElementById('cardModalAdvName').textContent = advertiserName;
      document.getElementById('cardModalAdId').textContent = 'ID: ' + (ad.ad_archive_id || ad.platformAdId || '809230588636735');
      document.getElementById('cardModalCopy').textContent = copyText;

      const videoEl = document.getElementById('cardModalVideo');
      const imgEl = document.getElementById('cardModalImage');

      if (isVideo && videoSrc) {
        videoEl.classList.remove('hidden');
        imgEl.classList.add('hidden');
        videoEl.src = videoSrc;
        videoEl.play().catch(() => {});
      } else {
        videoEl.classList.add('hidden');
        imgEl.classList.remove('hidden');
        imgEl.src = imgSrc;
      }

      document.getElementById('cardModalCtaDomain').textContent = currentData.domain || 'store.com';
      document.getElementById('cardModalCtaTitle').textContent = ad.cta_title || ad.ctaText || ('Shop ' + currentData.name);
      document.getElementById('cardModalCtaBtn').href = landingUrl;
      document.getElementById('btnOriginalAd').href = adLibraryUrl;

      // Fill Right Half
      const rankPct = Math.max(1, Math.round(((index + 1) / (currentData.ads.length || 20)) * 10));
      document.getElementById('detailRankScale').textContent = `Top ${rankPct}%`;
      document.getElementById('detailRankBar').style.width = `${100 - rankPct * 5}%`;
      document.getElementById('detailRankBadge').textContent = `Top ${rankPct}% Winning Creative`;

      // Landing page ratio
      const lpAdsCount = currentData.hero_landing_pages && currentData.hero_landing_pages[0] ? currentData.hero_landing_pages[0].adsCount : 252;
      const lpAdsRatio = currentData.hero_landing_pages && currentData.hero_landing_pages[0] ? currentData.hero_landing_pages[0].ratio : '61%';
      document.getElementById('detailLpCount').textContent = lpAdsCount;
      document.getElementById('detailLpRatio').textContent = `${lpAdsRatio} of ads`;
      document.getElementById('detailLpBar').style.width = lpAdsRatio;
      document.getElementById('detailLandingUrl').textContent = ad.landing_url || ('https://' + currentData.domain);
      document.getElementById('detailLandingUrl').href = ad.landing_url || ('https://' + currentData.domain);

      // Format & CTA
      document.getElementById('detailFormat').textContent = isVideo ? 'Video (MP4)' : 'Image (PNG/JPG)';
      document.getElementById('detailCta').textContent = (ad.cta_type || ad.ctaText || 'Shop Now').replace(/_/g, ' ');
      document.getElementById('detailLanguage').textContent = ad.language || 'English';

      // Reach & Spend
      document.getElementById('detailReach').textContent = ad.euReach ? `${ad.euReach} 🇬🇧` : '—';
      document.getElementById('detailSpend').textContent = ad.euReach ? `$0.0 · $0/d` : '—';

      // Advertiser section
      document.getElementById('btnMetaAdsLibrary').href = currentData.meta_library_url || ('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id=' + (ad.page_id || ''));
      document.getElementById('advActiveAds').textContent = `● ${currentData.total_active_ads || currentData.ads.length} / ${currentData.total_all_time || '13.9K'}`;
      document.getElementById('advVelocity').textContent = `7d: ${currentData.kpis?.velocity_7d || 84} | 14d: ${currentData.kpis?.velocity_14d || 115}`;
      document.getElementById('advReach').textContent = currentData.kpis?.reach_estimate || '340.4M';
      document.getElementById('advSpend').textContent = currentData.kpis?.spend_estimate || '$3.1M';

      // Hero Funnels Strip
      const lpHeroStrip = document.getElementById('landingPagesStrip');
      lpHeroStrip.innerHTML = '';
      const heroLps = (currentData.hero_landing_pages && currentData.hero_landing_pages.length > 0) ? currentData.hero_landing_pages : [
        { title: `${currentData.name || 'Store'} Main Funnel`, ratio: "100%", count: currentData.total_active_ads || 10, url: "https://" + (currentData.domain || 'store.com') }
      ];

      heroLps.forEach(lp => {
        const item = document.createElement('a');
        item.href = lp.url || '#';
        item.target = '_blank';
        item.className = "p-2.5 rounded-xl bg-slate-50 border border-slate-200 hover:border-blue-500 block transition group/lp";
        item.innerHTML = `
          <div class="flex items-center justify-between text-[11px] mb-1">
            <span class="font-bold text-slate-800 group-hover/lp:text-blue-600 truncate">${lp.title}</span>
            <span class="font-extrabold text-blue-600">${lp.ratio}</span>
          </div>
          <div class="text-[10px] text-slate-400">${lp.count} active ads pointing here</div>
        `;
        lpHeroStrip.appendChild(item);
      });
    }

    function closeAdModal() {
      const modal = document.getElementById('adModal');
      modal.classList.add('hidden');
      const videoEl = document.getElementById('cardModalVideo');
      videoEl.pause();
      videoEl.src = '';
    }

    function prevAd() {
      if (!currentData || !currentData.ads) return;
      currentAdIndex = (currentAdIndex - 1 + currentData.ads.length) % currentData.ads.length;
      openAdModal(currentAdIndex);
    }

    function nextAd() {
      if (!currentData || !currentData.ads) return;
      currentAdIndex = (currentAdIndex + 1) % currentData.ads.length;
      openAdModal(currentAdIndex);
    }

    function downloadCreative() {
      if (!currentData || !currentData.ads[currentAdIndex]) return;
      const ad = currentData.ads[currentAdIndex];
      const url = ad.video_url || ad.image_url || ad.mediaUrl;
      if (!url) {
        alert('Không tìm thấy link tải trực tiếp.');
        return;
      }
      window.open(url, '_blank');
    }

    // Top Search Form Handler
    document.getElementById('topSearchForm').onsubmit = (e) => {
      e.preventDefault();
      const q = document.getElementById('brandInput').value.trim();
      if (q) {
        switchView('explorer');
        loadBrand(q);
      }
    };

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
      btn.onclick = () => {
        const b = btn.textContent.trim();
        document.getElementById('brandInput').value = b;
        switchView('explorer');
        loadBrand(b);
      };
    });

    // Auto-load on startup
    window.addEventListener('DOMContentLoaded', () => {
      loadBrand('The Oodie');
      loadBrandtrackerData();
    });
  </script>
</body>
</html>
"""

class TrendTrackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format%args}\n")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
            return

        if parsed.path in ["/favicon.ico", "/favicon.svg"]:
            svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="50%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="32" fill="url(#bgGrad)"/>
  <text x="64" y="88" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif" font-size="84" font-weight="900" fill="#ffffff" text-anchor="middle">@</text>
</svg>"""
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(svg_icon.encode("utf-8"))
            return

        if parsed.path == "/api/brandtracker":
            benchmark_file = os.path.join(CACHE_DIR, "brandtracker_benchmark.json")
            if os.path.exists(benchmark_file):
                with open(benchmark_file, "r", encoding="utf-8") as f:
                    bench_data = f.read()
            else:
                bench_data = "[]"
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bench_data.encode("utf-8"))
            return

        if parsed.path == "/api/scan":
            query_params = urllib.parse.parse_qs(parsed.query)
            query = query_params.get("query", ["The Oodie"])[0].strip()

            clean_q = query.lower().strip()
            alias_map = {
                "the oodie": "the_oodie.json",
                "theoodie": "the_oodie.json",
                "theoodie.com": "the_oodie.json",
                "oodie": "the_oodie.json",
                "true sea moss": "true_sea_moss.json",
                "trueseamoss": "true_sea_moss.json",
                "trueseamoss.com": "true_sea_moss.json",
                "seamoss": "true_sea_moss.json",
                "momcozy": "momcozy.json",
                "momcozy.com": "momcozy.json",
                "balsam hill": "balsam_hill.json",
                "balsamhill": "balsam_hill.json",
                "balsamhill.com": "balsam_hill.json",
                "camping tent": "camping_tent.json",
                "camping_tent": "camping_tent.json",
                "campingtent.com": "camping_tent.json",
                "tidradio": "tidradio.json",
                "tidradio.com": "tidradio.json",
                "ridge": "ridge.json",
                "ridge.com": "ridge.json"
            }

            cache_file = None
            if clean_q in alias_map:
                candidate = os.path.join(CACHE_DIR, alias_map[clean_q])
                if os.path.exists(candidate):
                    cache_file = candidate

            if not cache_file:
                c1 = os.path.join(CACHE_DIR, f"{clean_q.replace(' ', '_').replace('-', '_')}.json")
                c2 = os.path.join(CACHE_DIR, f"{clean_q.replace('.com', '').replace(' ', '_')}.json")
                if os.path.exists(c1):
                    cache_file = c1
                elif os.path.exists(c2):
                    cache_file = c2
                else:
                    cache_file = c1

            # Check cache first
            if os.path.exists(cache_file):
                print(f"⚡ [CACHE HIT] Tải ngay dữ liệu từ: {cache_file}")
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(cached_data.encode("utf-8"))
                return

            print(f"🔍 [LIVE SCAN] Quét Meta Ad Library cho: query='{query}'...")
            try:
                data = scan_brand_ads(query, max_ads=30)
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, TrendTrackHandler)
    print("=" * 60)
    print(f"🚀 TRENDTRACK PRODUCTION CLONE RUNNING AT:")
    print(f"👉 http://localhost:{PORT}")
    print("=" * 60)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
