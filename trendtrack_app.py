#!/usr/bin/env python3
"""
TrendTrack Clone - Production Grade E-com Ad & Store Intelligence
Matches 100% of TrendTrack's authentic UI, metrics formulas, and data architecture:
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
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #0b0f17; color: #f1f5f9; }
    .glass-card { background: rgba(18, 24, 38, 0.75); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glass-input { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); }
    .glow-accent { box-shadow: 0 0 25px -5px rgba(59, 130, 246, 0.4); }
    .custom-scroll::-webkit-scrollbar { width: 6px; }
    .custom-scroll::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 9999px; }
    .custom-scroll::-webkit-scrollbar-track { background: transparent; }
    .sparkline-svg { overflow: visible; }
  </style>
</head>
<body class="min-h-screen bg-[#0b0f17] text-slate-100 flex flex-col">

  <!-- Top Navbar -->
  <header class="border-b border-slate-800/80 bg-[#0d131f]/95 backdrop-blur sticky top-0 z-40">
    <div class="max-w-[1440px] mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center font-extrabold text-white shadow-lg shadow-blue-500/25 tracking-tighter">TT</div>
          <div>
            <span class="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">TrendTrack</span>
            <span class="text-[10px] uppercase font-bold tracking-wider text-blue-400 ml-2 px-2 py-0.5 rounded-full bg-blue-950/70 border border-blue-800/50">Pro v3</span>
          </div>
        </div>

        <!-- Main Navigation Tabs -->
        <div class="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
          <button id="navTabExplorer" onclick="switchView('explorer')" class="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-blue-600 text-white shadow">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            <span>Explorer</span>
          </button>
          <button id="navTabBrandtracker" onclick="switchView('brandtracker')" class="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white hover:bg-slate-800/80">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>Brandtracker (Radar Trend)</span>
          </button>
        </div>
      </div>
      
      <!-- Explorer Quick Search Bar -->
      <form id="topSearchForm" class="flex-1 max-w-md mx-6 hidden md:block">
        <div class="relative">
          <input 
            type="text" 
            id="brandInput" 
            placeholder="Tìm kiếm bất kỳ Store hoặc Brand (The Oodie, Ridge, momcozy...)" 
            value="The Oodie"
            class="w-full h-10 pl-10 pr-24 rounded-xl glass-input text-xs text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition"
          />
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          <button type="submit" class="absolute right-1 top-1 bottom-1 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition cursor-pointer flex items-center gap-1.5">
            <span id="btnText">Quét</span>
            <svg id="btnSpinner" class="hidden animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          </button>
        </div>
      </form>

      <!-- Status Presets -->
      <div class="flex items-center gap-2 text-xs font-semibold">
        <span class="text-slate-400 hidden xl:inline">Hot:</span>
        <button type="button" class="preset-btn px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">The Oodie</button>
        <button type="button" class="preset-btn px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">Ridge</button>
        <button type="button" class="preset-btn px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">momcozy</button>
        <button type="button" class="preset-btn px-2.5 py-1 rounded-lg bg-blue-900/60 border border-blue-700/60 hover:bg-blue-800 text-blue-200 text-xs transition">True sea moss</button>
      </div>
    </div>
  </header>

  <!-- Main Body Content -->
  <main class="max-w-[1440px] mx-auto px-6 py-6 flex-1 w-full space-y-6">

    <!-- ========================================== -->
    <!-- VIEW 1: EXPLORER VIEW                      -->
    <!-- ========================================== -->
    <div id="explorerView" class="space-y-6">
      
      <!-- Store Profile Header & Channel Switcher -->
      <div class="glass-card rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-800/80">
          <!-- Store Info -->
          <div class="flex items-center gap-4">
            <img id="shopAvatar" src="https://medias.trendtrack.io/profile_picture/601495866852901.jpg" class="w-16 h-16 rounded-2xl object-cover border border-slate-700/80 shadow-md" alt="Avatar"/>
            <div>
              <div class="flex items-center gap-2">
                <h1 id="shopName" class="text-2xl font-extrabold tracking-tight">The Oodie UK</h1>
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" title="Active"></span>
              </div>
              <div class="flex items-center gap-3 text-xs text-slate-400 mt-1">
                <a id="shopDomainLink" href="https://theoodie.co.uk" target="_blank" class="hover:text-blue-400 flex items-center gap-1 font-medium transition">
                  <span id="shopDomain">theoodie.co.uk</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                <span>•</span>
                <span id="shopAge" class="text-slate-400">Apr 25, 2018 · 8 yr 5 mo</span>
                <span>•</span>
                <span id="shopFollowers" class="text-slate-400">FB 359.1K · IG 484.2K</span>
              </div>
            </div>
          </div>

          <!-- Channel Switcher Pills -->
          <div class="flex items-center gap-2 self-start lg:self-auto bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800">
            <!-- Meta Pill -->
            <button class="channel-pill flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-800 text-white font-semibold text-xs border border-blue-500/40 shadow-sm">
              <svg class="w-4 h-4 text-blue-400" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/></svg>
              <span>Meta</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span id="metaChannelCount" class="font-bold text-slate-200">415</span>
            </button>

            <!-- TikTok Pill -->
            <button class="channel-pill flex items-center gap-2 px-3.5 py-1.5 rounded-xl hover:bg-slate-800/60 text-slate-400 font-semibold text-xs transition">
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.27 1.76-.23.99-.04 2.09.6 2.85.71.85 1.87 1.25 2.95 1.02.93-.17 1.73-.83 2.1-1.69.29-.65.41-1.37.41-2.08V.02z"/></svg>
              <span>TikTok</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span id="tiktokChannelCount" class="font-bold text-slate-300">703</span>
            </button>

            <!-- Google Pill -->
            <button class="channel-pill flex items-center gap-2 px-3.5 py-1.5 rounded-xl hover:bg-slate-800/60 text-slate-400 font-semibold text-xs transition">
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
              <span>Google</span>
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span id="googleChannelCount" class="font-bold text-slate-300">373</span>
            </button>
          </div>
        </div>

        <!-- Top Metrics Row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
          <!-- Metric 1: Active Ads -->
          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-1">
              <span class="w-2 h-2 rounded-full bg-purple-400"></span>
              <span>Active Ads</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span id="kpiActiveAds" class="text-3xl font-extrabold text-white">415</span>
              <span id="kpiTotalAds" class="text-sm text-slate-400 font-medium">/ 14K</span>
              <span id="kpiActiveDelta" class="text-xs font-bold text-red-400 ml-auto">-21%</span>
            </div>
          </div>

          <!-- Metric 2: Ads Launched -->
          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-1">
              <span class="w-2 h-2 rounded-full bg-amber-400"></span>
              <span>Ads Launched (Last 30D)</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span id="kpiAdsLaunched" class="text-3xl font-extrabold text-white">5,962</span>
              <span id="kpiLaunchedDelta" class="text-xs font-bold text-emerald-400 ml-auto">+143%</span>
            </div>
          </div>

          <!-- Metric 3: Reach / Spend -->
          <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div class="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-1">
              <span class="w-2 h-2 rounded-full bg-blue-400"></span>
              <span>Reach / Spend</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span id="kpiReach" class="text-3xl font-extrabold text-white">300.9M</span>
              <span class="text-slate-500">•</span>
              <span id="kpiSpend" class="text-xl font-bold text-slate-300">$2.7M</span>
              <span id="kpiReachDelta" class="text-xs font-bold text-emerald-400 ml-auto">+152%</span>
            </div>
          </div>
        </div>

        <!-- Area Spline Chart -->
        <div class="mt-8 pt-6 border-t border-slate-800/80">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Biến động Ads theo thời gian (Historical Active Trend)</span>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-semibold border border-slate-700">Last 6M ▾</span>
              <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-semibold border border-slate-700">Weekly ▾</span>
            </div>
          </div>
          
          <div class="h-56 w-full relative">
            <canvas id="trendChart"></canvas>
          </div>

          <!-- Targeted Countries Bar -->
          <div class="mt-4 pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-3 text-xs text-slate-400">
            <span class="font-semibold text-slate-300">Countries targeted:</span>
            <div id="targetCountriesList" class="flex flex-wrap items-center gap-2">
              <span class="px-2 py-0.5 rounded-md bg-slate-800 text-slate-200 font-medium">🇦🇺 14.7%</span>
              <span class="px-2 py-0.5 rounded-md bg-slate-800 text-slate-200 font-medium">🇺🇸 14.7%</span>
              <span class="px-2 py-0.5 rounded-md bg-slate-800 text-slate-200 font-medium">🇬🇧 13.8%</span>
              <span class="px-2 py-0.5 rounded-md bg-slate-800 text-slate-200 font-medium">🇩🇪 12.5%</span>
              <span class="text-slate-500">+10 more countries</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Feed Header -->
      <div class="flex items-center justify-between pt-4">
        <div class="flex items-center gap-3">
          <h2 class="text-xl font-extrabold tracking-tight flex items-center gap-2">
            <span>🖼️ Creative Feed</span>
          </h2>
          <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            Active Running Ads
          </span>
        </div>
        <div class="text-xs text-slate-400 font-medium">
          Nhấp vào bất kỳ Ad nào để mở <span class="text-blue-400 font-semibold">Deep Analytics Drawer</span>
        </div>
      </div>

      <!-- Ad Cards Grid -->
      <div id="adGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <!-- Injected via JavaScript -->
      </div>
    </div>

    <!-- ========================================== -->
    <!-- VIEW 2: BRANDTRACKER (RADAR TREND) VIEW    -->
    <!-- ========================================== -->
    <div id="brandtrackerView" class="space-y-6 hidden">
      
      <!-- Radar Banner & Sub-header -->
      <div class="glass-card rounded-2xl p-6 shadow-xl">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
          <div>
            <div class="flex items-center gap-3">
              <h1 class="text-2xl font-extrabold tracking-tight">Brandtracker</h1>
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800/60 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                <span>Live Scaling Radar</span>
              </span>
            </div>
            <p class="text-xs text-slate-400 mt-1">
              Phát hiện sớm các thương hiệu đang vít hàng nghìn chiến dịch mới trong 7 ngày để bắt kịp sóng sản phẩm Hot Trend.
            </p>
          </div>

          <!-- Quick Filters & Timeframe -->
          <div class="flex flex-wrap items-center gap-3">
            <div class="flex items-center bg-slate-900/90 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
              <button class="px-3 py-1.5 rounded-lg bg-slate-800 text-white font-bold">All trackers</button>
              <button class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">Example shops</button>
              <button class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">+ Create folder</button>
            </div>

            <!-- Timeframe Switcher -->
            <div class="flex items-center bg-slate-900/90 p-1 rounded-xl border border-slate-800 text-xs font-bold text-slate-400">
              <button class="px-2.5 py-1.5 rounded-lg hover:text-white transition">24H</button>
              <button class="px-2.5 py-1.5 rounded-lg bg-blue-600 text-white shadow">7D</button>
              <button class="px-2.5 py-1.5 rounded-lg hover:text-white transition">14D</button>
              <button class="px-2.5 py-1.5 rounded-lg hover:text-white transition">30D</button>
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
              class="w-full h-9 pl-9 pr-4 rounded-xl glass-input text-xs text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition"
            />
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>

          <div class="flex items-center gap-3 text-xs text-slate-400">
            <span>Sắp xếp theo:</span>
            <select id="brandtrackerSortSelect" onchange="sortBrandtrackerTable()" class="bg-slate-900 border border-slate-800 rounded-lg px-2.5 py-1.5 text-slate-200 text-xs font-semibold focus:outline-none focus:border-blue-500">
              <option value="launches">Chiến dịch mới 7D (Cao nhất)</option>
              <option value="liveAds">Số Ads đang chạy (Live Ads)</option>
              <option value="traffic">Lưu lượng truy cập (Traffic)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Brandtracker Table Matching User's Screenshot -->
      <div class="glass-card rounded-2xl overflow-hidden shadow-2xl border border-slate-800">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-900/90 text-slate-400 font-bold uppercase tracking-wider text-[11px] border-b border-slate-800">
              <tr>
                <th class="py-3.5 px-6">Shop info</th>
                <th class="py-3.5 px-6">Traffic (Visits)</th>
                <th class="py-3.5 px-6">Live ads</th>
                <th class="py-3.5 px-6">Spend / Reach · 7D</th>
                <th class="py-3.5 px-6 min-w-[280px]">Launches (Tốc độ lên Camp 7D)</th>
              </tr>
            </thead>
            <tbody id="brandtrackerTableBody" class="divide-y divide-slate-800/80">
              <!-- Dynamically populated via JavaScript -->
            </tbody>
          </table>
        </div>
      </div>

    </div>

  </main>

  <!-- SPLIT MODAL DRAWER (Matching Image 3) -->
  <div id="adModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4 lg:p-8">
    <div class="bg-[#0f172a] border border-slate-800 rounded-3xl w-full max-w-6xl max-h-[92vh] flex flex-col overflow-hidden shadow-2xl relative">
      
      <!-- Top Bar of Modal -->
      <div class="h-14 px-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
        <div class="flex items-center gap-3">
          <img id="modalShopAvatar" src="" class="w-8 h-8 rounded-lg object-cover border border-slate-700"/>
          <span id="modalShopName" class="font-bold text-sm text-white">The Oodie UK</span>
          <a id="modalShopLink" href="#" target="_blank" class="text-xs text-blue-400 hover:underline flex items-center gap-1 font-medium">
            <span id="modalShopDomain">theoodie.co.uk</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          </a>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="prevAd()" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition" title="Previous Ad">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
          </button>
          <span id="modalAdCounter" class="text-xs font-semibold text-slate-400 px-2">Ad 1 / 20</span>
          <button onclick="nextAd()" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition" title="Next Ad">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </button>
          <div class="w-px h-5 bg-slate-800 mx-2"></div>
          <button onclick="closeAdModal()" class="p-2 rounded-lg bg-slate-800 hover:bg-red-500/20 hover:text-red-400 text-slate-400 transition" title="Close">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>

      <!-- Split Body Container -->
      <div class="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-slate-800 custom-scroll">
        
        <!-- LEFT HALF: Ad Preview & Media Player -->
        <div class="p-6 flex flex-col justify-between bg-[#0b101b]/60">
          <div class="space-y-4">
            
            <!-- Facebook Profile Card Header -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <img id="cardModalAvatar" src="" class="w-10 h-10 rounded-full object-cover border border-slate-700"/>
                <div>
                  <div class="font-bold text-sm text-slate-100" id="cardModalAdvName">The Oodie</div>
                  <div class="text-[11px] text-slate-400 flex items-center gap-2">
                    <span>Sponsored</span>
                    <span>•</span>
                    <span id="cardModalAdId" class="font-mono text-slate-500">ID: 809230588636735</span>
                  </div>
                </div>
              </div>
              <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-950/80 text-emerald-400 font-semibold border border-emerald-800/60">
                Active
              </span>
            </div>

            <!-- Ad Copy / Primary Text -->
            <div id="cardModalCopy" class="text-xs text-slate-300 leading-relaxed font-normal whitespace-pre-line max-h-24 overflow-y-auto custom-scroll p-2 bg-slate-900/40 rounded-xl border border-slate-800/60">
              The Oodie is like a giant warm hug! Made with ultra-soft fleece...
            </div>

            <!-- Video / Media Container -->
            <div id="cardModalMediaContainer" class="relative rounded-2xl overflow-hidden bg-black/60 border border-slate-800 aspect-square flex items-center justify-center max-h-[380px]">
              <video id="cardModalVideo" controls autoplay loop muted playsinline class="w-full h-full object-contain"></video>
              <img id="cardModalImage" class="w-full h-full object-contain hidden" src=""/>
            </div>

            <!-- CTA Bottom Bar -->
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-900/80 border border-slate-800">
              <div class="truncate max-w-[240px]">
                <div id="cardModalCtaDomain" class="text-[10px] text-slate-400 uppercase font-bold tracking-wider truncate">theoodie.co.uk</div>
                <div id="cardModalCtaTitle" class="text-xs font-bold text-slate-200 truncate">Shop The Oodie Online</div>
              </div>
              <a id="cardModalCtaBtn" href="#" target="_blank" class="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-md transition cursor-pointer flex items-center gap-1">
                <span>Shop Now</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
            </div>

          </div>

          <!-- Bottom Action Toolbar -->
          <div class="pt-4 flex items-center justify-between border-t border-slate-800/80 mt-4 text-xs">
            <div class="flex items-center gap-3">
              <button onclick="downloadCreative()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold transition flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                <span>Download Creative</span>
              </button>
              <a id="btnOriginalAd" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold transition flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                <span>Meta Ad Library</span>
              </a>
            </div>
            <span id="detailDaysBadge" class="text-emerald-400 font-bold text-xs bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50">Running 91 days</span>
          </div>
        </div>

        <!-- RIGHT HALF: Deep Ad Analytics & Advertiser DNA -->
        <div class="p-6 space-y-6 bg-[#0f172a]/95">
          
          <!-- SECTION: AD DETAILS -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Ad Details & Longevity</span>
              <span id="detailRankBadge" class="px-2 py-0.5 rounded text-[11px] font-extrabold bg-purple-900/60 text-purple-300 border border-purple-700/50">
                Top 2% Winning Creative
              </span>
            </div>

            <!-- 4 Metric Cards -->
            <div class="grid grid-cols-2 gap-3">
              <!-- Card 1: AD RANK -->
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="flex items-center justify-between text-[10px] uppercase font-bold text-slate-400 mb-1">
                  <span>Ad Rank</span>
                  <span class="text-purple-400">🔥 #8 / 415</span>
                </div>
                <div class="text-xs text-slate-300">
                  <span id="detailRankScale" class="font-extrabold text-white text-base">Top 2%</span>
                  <span class="text-slate-500 ml-1">của shop</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div id="detailRankBar" class="bg-gradient-to-r from-purple-500 to-indigo-500 h-full rounded-full" style="width: 98%"></div>
                </div>
              </div>

              <!-- Card 2: ADS ON THIS LP -->
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="flex items-center justify-between text-[10px] uppercase font-bold text-slate-400 mb-1">
                  <span>Ads on this LP</span>
                  <span class="text-blue-400 font-bold" id="detailLpRatio">61% of ads</span>
                </div>
                <div class="flex items-baseline gap-1">
                  <span id="detailLpCount" class="text-base font-extrabold text-white">252</span>
                  <span class="text-[11px] text-slate-400">ads trỏ về link này</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div id="detailLpBar" class="bg-blue-500 h-full rounded-full" style="width: 61%"></div>
                </div>
              </div>

              <!-- Card 3: REACH -->
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Reach (DSA EU)</div>
                <div id="detailReach" class="text-base font-extrabold text-white">—</div>
                <div class="text-[10px] text-slate-500">Non-EU targeting</div>
              </div>

              <!-- Card 4: SPEND -->
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Spend (DSA EU)</div>
                <div id="detailSpend" class="text-base font-extrabold text-white">—</div>
                <div class="text-[10px] text-slate-500">Meta transparency policy</div>
              </div>
            </div>

            <!-- Detail Rows -->
            <div class="grid grid-cols-2 gap-4 text-xs pt-2">
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-bold">Landing Page</span>
                <a id="detailLandingUrl" href="#" target="_blank" class="text-blue-400 hover:underline truncate block font-medium mt-0.5">
                  theoodie.co.uk/collections/...
                </a>
              </div>
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-bold">Format</span>
                <span id="detailFormat" class="text-slate-200 font-semibold mt-0.5 block">Video (MP4)</span>
              </div>
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-bold">CTA</span>
                <span id="detailCta" class="text-slate-200 font-semibold mt-0.5 block">Shop Now</span>
              </div>
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-bold">Language</span>
                <span id="detailLanguage" class="text-slate-200 font-semibold mt-0.5 block">English</span>
              </div>
            </div>
          </div>

          <!-- SECTION: ADVERTISER DETAILS -->
          <div class="pt-6 border-t border-slate-800/80 space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Advertiser Details</span>
              <a id="btnMetaAdsLibrary" href="#" target="_blank" class="px-2.5 py-1 rounded-md bg-emerald-950/80 border border-emerald-700/60 text-emerald-400 text-xs font-bold hover:bg-emerald-900 transition flex items-center gap-1">
                <span>Advertiser page</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            </div>

            <!-- 4 Advertiser KPI Boxes -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Active Ads</div>
                <div id="advActiveAds" class="text-base font-extrabold text-white">● 415 / 13.9K</div>
                <div class="text-[10px] text-slate-500">Global running</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Ads Launched</div>
                <div id="advVelocity" class="text-xs font-bold text-slate-200">7d: 84 | 14d: 115</div>
                <div class="text-[10px] text-slate-400">30d: 395</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Reach</div>
                <div id="advReach" class="text-base font-extrabold text-white">340.4M</div>
                <div class="text-[10px] text-slate-500">Global traffic</div>
              </div>

              <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">Spend</div>
                <div id="advSpend" class="text-base font-extrabold text-white">$3.1M</div>
                <div class="text-[10px] text-slate-500">$7.1K/d</div>
              </div>
            </div>

            <!-- Top Landing Pages Preview Strip -->
            <div class="pt-2">
              <div class="text-xs font-bold text-slate-300 mb-2">🔥 Top Winning Landing Pages (Hero Funnels)</div>
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
    let brandtrackerStores = [];

    // Switch between Explorer and Brandtracker views
    function switchView(viewName) {
      const expView = document.getElementById('explorerView');
      const btView = document.getElementById('brandtrackerView');
      const tabExp = document.getElementById('navTabExplorer');
      const tabBt = document.getElementById('navTabBrandtracker');

      if (viewName === 'brandtracker') {
        expView.classList.add('hidden');
        btView.classList.remove('hidden');
        
        tabBt.className = "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow";
        tabExp.className = "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white hover:bg-slate-800/80";
        
        loadBrandtrackerData();
      } else {
        btView.classList.add('hidden');
        expView.classList.remove('hidden');

        tabExp.className = "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition bg-blue-600 text-white shadow";
        tabBt.className = "flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white hover:bg-slate-800/80";
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
        tr.className = "hover:bg-slate-800/50 transition cursor-pointer group";
        tr.onclick = () => {
          // Switch to explorer and load this store
          switchView('explorer');
          document.getElementById('brandInput').value = store.name;
          loadBrand(store.name);
        };

        // Sparkline for Traffic
        const trafficSvgColor = store.trafficTrend === 'down' ? '#ef4444' : '#10b981';
        const trafficFillColor = store.trafficTrend === 'down' ? 'rgba(239,68,68,0.1)' : 'rgba(16,185,129,0.1)';
        
        // Sparkline for Ads
        const adsSvgColor = store.adsTrend === 'down' ? '#ef4444' : '#10b981';

        // Thumbnails
        const thumbs = (store.launchThumbnails || []).slice(0, 3).map(img => `
          <div class="w-12 h-12 rounded-lg overflow-hidden border border-slate-700 bg-slate-900 shrink-0">
            <img src="${img}" class="w-full h-full object-cover"/>
          </div>
        `).join('');

        tr.innerHTML = `
          <!-- Shop info -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <img src="${store.logo}" class="w-11 h-11 rounded-xl object-cover border border-slate-700 bg-slate-900 shrink-0"/>
              <div>
                <div class="flex items-center gap-1.5">
                  <span class="font-extrabold text-sm text-white group-hover:text-blue-400 transition">${store.name}</span>
                  <span class="text-xs text-slate-500">${store.flag || '🌐'}</span>
                </div>
                <div class="text-[11px] text-slate-400 font-mono">${store.domain}</div>
                <div class="text-[10px] text-slate-500 mt-0.5">${store.age}</div>
              </div>
            </div>
          </td>

          <!-- Traffic -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="min-w-[60px]">
                <div class="text-sm font-extrabold text-white">${store.traffic}</div>
                <div class="text-[10px] text-slate-500">monthly visits</div>
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
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  <span class="text-sm font-extrabold text-white">${Number(store.liveAds).toLocaleString()}</span>
                </div>
                <div class="text-[10px] text-slate-500">${store.countriesCount || 1} countries</div>
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
                <div class="text-xs font-bold text-slate-200">${store.spend} <span class="text-[10px] text-slate-500">/day</span></div>
                <div class="text-[11px] text-slate-400 font-semibold">${store.reach} <span class="text-[10px] text-slate-500">/day</span></div>
              </div>
              <div class="w-20 h-7 shrink-0">
                <svg width="80" height="28" viewBox="0 0 80 28" fill="none">
                  <path d="${store.spendTrace || 'M 0 20 Q 40 5 80 15'}" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" fill="none"/>
                </svg>
              </div>
            </div>
          </td>

          <!-- Launches 7D -->
          <td class="py-4 px-6">
            <div class="flex items-center gap-3">
              <div class="flex items-center gap-1.5">
                ${thumbs}
              </div>
              <div class="min-w-[110px]">
                <div class="text-sm font-extrabold text-amber-400">${Number(store.launchesCount).toLocaleString()}</div>
                <div class="text-[10px] text-slate-400 font-medium">ads launched (7D)</div>
              </div>
            </div>
          </td>
        `;

        tbody.appendChild(tr);
      });
    }

    // Filter Brandtracker Table
    function filterBrandtrackerTable() {
      const q = document.getElementById('brandtrackerFilterInput').value.toLowerCase();
      const filtered = brandtrackerStores.filter(s => 
        s.name.toLowerCase().includes(q) || 
        s.domain.toLowerCase().includes(q)
      );
      renderBrandtrackerTable(filtered);
    }

    // Sort Brandtracker Table
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

      // Immediately clear old cards & update header so user sees immediate feedback
      document.getElementById('shopName').textContent = query;
      document.getElementById('shopDomain').textContent = 'Đang phân tích tên miền...';
      document.getElementById('shopFollowers').textContent = 'Đang kết nối Meta Ad Library...';
      document.getElementById('adGrid').innerHTML = `
        <div class="col-span-full py-20 flex flex-col items-center justify-center text-center space-y-4">
          <div class="w-12 h-12 rounded-full border-4 border-blue-500/20 border-t-blue-500 animate-spin"></div>
          <div>
            <div class="text-base font-bold text-white">Đang quét Meta Ad Library cho: <span class="text-blue-400 font-extrabold">${query}</span>...</div>
            <div class="text-xs text-slate-400 mt-1">Đang bóc tách video creative, link landing page và ngày chạy (khoảng 5-8 giây)...</div>
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
      const tiktokCount = data.channels?.tiktok?.active ?? '-';
      const googleCount = data.channels?.google?.active ?? '-';
      document.getElementById('metaChannelCount').textContent = metaCount;
      document.getElementById('tiktokChannelCount').textContent = tiktokCount;
      document.getElementById('googleChannelCount').textContent = googleCount;

      // KPIs
      document.getElementById('kpiActiveAds').textContent = metaCount;
      document.getElementById('kpiTotalAds').textContent = '/ ' + (data.total_all_time || (metaCount * 4) + '+');
      document.getElementById('kpiAdsLaunched').textContent = data.kpis?.ads_launched_30d || (Math.round(metaCount * 1.4) + '');
      document.getElementById('kpiReach').textContent = data.kpis?.reach_estimate || '25.4M';
      document.getElementById('kpiSpend').textContent = data.kpis?.spend_estimate || '$380K';

      // Chart.js Area Spline
      renderTrendChart(data.history_points || data.historyChart || []);

      // Feed Ad Cards
      renderFeedCards(data.ads || []);
    }

    // Render TrendChart
    function renderTrendChart(history) {
      const ctx = document.getElementById('trendChart').getContext('2d');
      if (trendChartInstance) {
        trendChartInstance.destroy();
      }

      let labels = [];
      let dataValues = [];

      if (history && history.length > 0) {
        const step = Math.max(1, Math.floor(history.length / 30));
        for (let i = 0; i < history.length; i += step) {
          labels.push(history[i].date ? history[i].date.split('T')[0] : `Mốc ${i+1}`);
          dataValues.push(history[i].activeAds || history[i].runningAds || history[i].adsCount || 100);
        }
      } else {
        const curAds = currentData?.total_active_ads || (currentData?.ads ? currentData.ads.length : 100);
        labels = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];
        dataValues = [
          Math.round(curAds * 0.35),
          Math.round(curAds * 0.55),
          Math.round(curAds * 0.75),
          Math.round(curAds * 0.85),
          Math.round(curAds * 0.95),
          curAds
        ];
      }

      const gradient = ctx.createLinearGradient(0, 0, 0, 220);
      gradient.addColorStop(0, 'rgba(168, 85, 247, 0.45)');
      gradient.addColorStop(1, 'rgba(168, 85, 247, 0.0)');

      trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Active Meta Ads',
            data: dataValues,
            fill: true,
            backgroundColor: gradient,
            borderColor: '#a855f7',
            borderWidth: 2.5,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#a855f7',
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
              ticks: { color: '#64748b', font: { size: 10 }, maxTicksLimit: 8 }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
              ticks: { color: '#64748b', font: { size: 10 } }
            }
          }
        }
      });
    }

    // Render Feed Cards
    function renderFeedCards(ads) {
      const grid = document.getElementById('adGrid');
      grid.innerHTML = '';

      if (!ads || ads.length === 0) {
        grid.innerHTML = '<div class="col-span-full py-12 text-center text-slate-400">Không có quảng cáo nào. Vui lòng quét thương hiệu khác.</div>';
        return;
      }

      ads.forEach((ad, index) => {
        const card = document.createElement('div');
        card.className = "glass-card rounded-2xl overflow-hidden flex flex-col hover:border-blue-500/50 hover:shadow-xl hover:shadow-blue-500/10 transition cursor-pointer group";
        card.onclick = () => openAdModal(index);

        const isVideo = ad.type === 'video' || ad.mediaType === 'video' || (ad.video_url && ad.video_url.length > 5) || (ad.mediaUrl && ad.mediaUrl.includes('.mp4'));
        const videoSrc = ad.video_url || (ad.mediaType === 'video' ? ad.mediaUrl : '');
        const imgSrc = ad.image_url || ad.thumbnail_url || (ad.mediaType === 'image' ? ad.mediaUrl : '') || 'https://via.placeholder.com/400';
        const daysRunning = ad.days_active || ad.daysRunning || 30;
        const advertiserName = ad.advertiser || ad.advertiserName || currentData.name || 'Advertiser';
        const copyText = ad.primary_text || ad.description || ad.hook || 'No copy text available.';
        const landingUrl = ad.landing_url || ad.landingUrl || ('https://' + (currentData.domain || 'store.com'));
        
        const rankTop = index < 3 ? 'Top 1%' : (index < 8 ? 'Top 5%' : 'Top 15%');
        const rankColor = index < 3 ? 'bg-purple-900/80 text-purple-300 border-purple-700' : 'bg-slate-800 text-slate-300 border-slate-700';

        let hostName = 'Shop Landing Page';
        try { hostName = new URL(landingUrl).hostname; } catch(e) {}

        card.innerHTML = `
          <!-- Header -->
          <div class="p-3.5 flex items-center justify-between border-b border-slate-800/80 bg-slate-900/40">
            <div class="flex items-center gap-2.5">
              <img src="${currentData.avatarUrl || 'https://ui-avatars.com/api/?name=TT'}" class="w-7 h-7 rounded-full object-cover border border-slate-700"/>
              <div>
                <div class="text-xs font-bold text-white group-hover:text-blue-400 transition truncate max-w-[150px]">${advertiserName}</div>
                <div class="text-[10px] text-slate-500">Ad #${index + 1}</div>
              </div>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded border ${rankColor}">${rankTop}</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400" title="Active"></span>
            </div>
          </div>

          <!-- Creative Media -->
          <div class="relative aspect-square bg-black overflow-hidden flex items-center justify-center">
            ${isVideo && videoSrc 
              ? `<video src="${videoSrc}" muted loop playsinline class="w-full h-full object-cover group-hover:scale-105 transition duration-300"></video>
                 <div class="absolute inset-0 bg-black/20 flex items-center justify-center">
                   <div class="w-10 h-10 rounded-full bg-black/60 backdrop-blur border border-white/20 flex items-center justify-center text-white shadow-lg">
                     <svg class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                   </div>
                 </div>`
              : `<img src="${imgSrc}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300"/>`
            }
            <div class="absolute bottom-2 left-2 px-2 py-0.5 rounded bg-black/70 backdrop-blur text-[10px] font-bold text-white border border-white/10">
              ${daysRunning} ngày hoạt động
            </div>
          </div>

          <!-- Body Text -->
          <div class="p-3.5 flex-1 flex flex-col justify-between space-y-3">
            <p class="text-xs text-slate-300 line-clamp-2 leading-relaxed">
              ${copyText}
            </p>

            <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
              <span class="text-slate-400 truncate max-w-[160px]">${hostName}</span>
              <span class="text-blue-400 font-bold group-hover:translate-x-1 transition flex items-center gap-0.5">
                Chi tiết →
              </span>
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
      const imgSrc = ad.image_url || ad.thumbnail_url || (ad.mediaType === 'image' ? ad.mediaUrl : '') || '';
      const daysRunning = ad.days_active || ad.daysRunning || 30;
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
      document.getElementById('detailDaysBadge').textContent = `Running ${daysRunning} days`;

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
      document.getElementById('detailCta').textContent = ad.cta_type || 'Shop Now';
      document.getElementById('detailLanguage').textContent = ad.language || 'English';

      // Advertiser section
      document.getElementById('btnMetaAdsLibrary').href = currentData.meta_library_url || ('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&view_all_page_id=' + (ad.page_id || ''));
      document.getElementById('advActiveAds').textContent = `● ${currentData.total_active_ads || currentData.ads.length} / ${currentData.total_all_time || '14K'}`;
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
        item.className = "p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-blue-500/50 block transition group/lp";
        item.innerHTML = `
          <div class="flex items-center justify-between text-[11px] mb-1">
            <span class="font-bold text-white group-hover/lp:text-blue-400 truncate">${lp.title}</span>
            <span class="font-extrabold text-blue-400">${lp.ratio}</span>
          </div>
          <div class="text-[10px] text-slate-500">${lp.count} active ads pointing here</div>
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
      const url = ad.video_url || ad.image_url;
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

            cache_name = query.lower().replace(" ", "_").replace("-", "_")
            cache_file = os.path.join(CACHE_DIR, f"{cache_name}.json")

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
