"""
Proxy Manager Microservice for TrendTrack / Data Underground Crawler
Supports:
- Webshare, Smartproxy, BrightData, IPRoyal
- Formats: IP:PORT:USER:PASS, USER:PASS@IP:PORT, HTTP/SOCKS5
- Auto-Rotation (Round-Robin, Random)
- Health Checking, Latency Benchmarking, Auto-Blacklisting dead IPs
"""

import os
import random
import time
import requests
from typing import Optional, List, Dict, Any

class Proxy:
    def __init__(self, raw_str: str):
        self.raw_str = raw_str.strip()
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""
        self.protocol = "http"
        self.is_alive = True
        self.fail_count = 0
        self.last_checked = 0
        self.latency_ms = 0
        self._parse()

    def _parse(self):
        s = self.raw_str
        if "://" in s:
            parts = s.split("://")
            self.protocol = parts[0].lower()
            s = parts[1]

        if "@" in s:
            # Format: user:pass@host:port
            auth, host_port = s.split("@", 1)
            u_p = auth.split(":", 1)
            self.username = u_p[0]
            self.password = u_p[1] if len(u_p) > 1 else ""
            h_p = host_port.split(":", 1)
            self.host = h_p[0]
            self.port = int(h_p[1]) if len(h_p) > 1 else 80
        elif s.count(":") == 3:
            # Format: host:port:user:pass (Standard Webshare export)
            parts = s.split(":")
            self.host = parts[0]
            self.port = int(parts[1])
            self.username = parts[2]
            self.password = parts[3]
        elif s.count(":") == 1:
            # Format: host:port (No auth / IP whitelist)
            parts = s.split(":")
            self.host = parts[0]
            self.port = int(parts[1])
        else:
            self.host = s

    def to_url(self) -> str:
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"

    def to_playwright_dict(self) -> Dict[str, str]:
        d = {
            "server": f"{self.protocol}://{self.host}:{self.port}"
        }
        if self.username and self.password:
            d["username"] = self.username
            d["password"] = self.password
        return d

    def to_requests_dict(self) -> Dict[str, str]:
        url = self.to_url()
        return {"http": url, "https": url}

class ProxyManager:
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies: List[Proxy] = []
        self._current_idx = 0
        self.max_fails = 3
        self.load_proxies()

    def load_proxies(self, lines: Optional[List[str]] = None):
        """Loads proxies from file or string list."""
        self.proxies = []
        if lines:
            for l in lines:
                if l.strip() and not l.startswith("#"):
                    self.proxies.append(Proxy(l))
            print(f"🛡️ [PROXY MANAGER] Loaded {len(self.proxies)} proxies from memory.")
            return

        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.proxies.append(Proxy(line))
            print(f"🛡️ [PROXY MANAGER] Loaded {len(self.proxies)} proxies from '{self.proxy_file}'.")
        else:
            print(f"ℹ️ [PROXY MANAGER] No '{self.proxy_file}' found. Running in Direct Connection mode.")

    def add_proxy(self, raw_proxy: str):
        p = Proxy(raw_proxy)
        self.proxies.append(p)

    def get_proxy(self, mode: str = "round_robin") -> Optional[Proxy]:
        """Returns an active proxy."""
        alive = [p for p in self.proxies if p.is_alive]
        if not alive:
            # If all are dead, revive all to avoid hard stop
            if self.proxies:
                for p in self.proxies:
                    p.is_alive = True
                    p.fail_count = 0
                alive = self.proxies
            else:
                return None

        if mode == "random":
            return random.choice(alive)
        
        # Round Robin
        proxy = alive[self._current_idx % len(alive)]
        self._current_idx += 1
        return proxy

    def mark_failure(self, proxy: Proxy):
        proxy.fail_count += 1
        if proxy.fail_count >= self.max_fails:
            proxy.is_alive = False
            print(f"⚠️ [PROXY MANAGER] Blacklisted dead proxy: {proxy.host}:{proxy.port} ({proxy.fail_count} failures)")

    def mark_success(self, proxy: Proxy):
        proxy.fail_count = max(0, proxy.fail_count - 1)
        proxy.is_alive = True

    def health_check(self, test_url: str = "https://httpbin.org/ip", timeout: int = 5) -> Dict[str, Any]:
        """Tests all proxies and removes dead ones."""
        total = len(self.proxies)
        active = 0
        results = []

        print(f"🔍 [PROXY MANAGER] Starting health check on {total} proxies...")
        for p in self.proxies:
            t0 = time.time()
            try:
                res = requests.get(test_url, proxies=p.to_requests_dict(), timeout=timeout)
                if res.status_code == 200:
                    p.latency_ms = int((time.time() - t0) * 1000)
                    p.is_alive = True
                    p.fail_count = 0
                    active += 1
                    results.append({"proxy": f"{p.host}:{p.port}", "status": "UP", "latency": f"{p.latency_ms}ms"})
                else:
                    self.mark_failure(p)
                    results.append({"proxy": f"{p.host}:{p.port}", "status": "FAIL_STATUS", "code": res.status_code})
            except Exception as e:
                self.mark_failure(p)
                results.append({"proxy": f"{p.host}:{p.port}", "status": "DOWN", "error": str(e)[:40]})

        print(f"✅ [PROXY MANAGER] Health Check done: {active}/{total} alive.")
        return {"total": total, "alive": active, "results": results}

# Global Singleton Instance
proxy_manager = ProxyManager()
