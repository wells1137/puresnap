#!/usr/bin/env python3
"""
Skills 下载量压测脚本
通过多IP并发 git clone / HTTP 请求模拟不同用户下载 skill，刷下载计数。
不会调用 MeowLoad API，不消耗任何额度。

用法:
  # 直接运行（默认 10 并发，50 次下载）
  python3 stress_test.py

  # 自定义并发和次数
  python3 stress_test.py -c 20 -n 100

  # 使用代理文件（真正多IP）
  python3 stress_test.py --proxy-file proxies.txt -c 30 -n 200

  # 自定义仓库
  python3 stress_test.py --repo wells1137/meowload-downloader
"""

import argparse
import asyncio
import json
import os
import random
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:
    import aiohttp
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp


REPO = "wells1137/meowload-downloader"
CLONE_URL = "https://github.com/{repo}.git"
ARCHIVE_URL = "https://github.com/{repo}/archive/refs/heads/main.zip"
API_TRAFFIC_URL = "https://api.github.com/repos/{repo}/traffic/clones"


@dataclass
class DownloadResult:
    method: str
    proxy: str
    success: bool
    latency_ms: float
    error: str = ""


@dataclass
class Stats:
    total: int = 0
    success: int = 0
    fail: int = 0
    errors: Dict[str, int] = field(default_factory=dict)
    latencies: List[float] = field(default_factory=list)

    @property
    def avg_latency(self):
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0

    @property
    def p95_latency(self):
        if not self.latencies:
            return 0
        s = sorted(self.latencies)
        return s[min(int(len(s) * 0.95), len(s) - 1)]

    @property
    def success_rate(self):
        return (self.success / self.total * 100) if self.total else 0


def load_proxies(path: str) -> List[str]:
    p = Path(path)
    if not p.exists():
        print(f"[!] 代理文件不存在: {path}")
        return []
    proxies = []
    for line in p.read_text().strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(("http://", "https://", "socks5://", "socks4://")):
            line = "http://" + line
        proxies.append(line)
    print(f"[+] 加载了 {len(proxies)} 个代理IP")
    return proxies


def random_ua() -> str:
    uas = [
        "git/2.43.0", "git/2.42.1", "git/2.41.0", "git/2.39.2",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/131.0.0.0 Mobile",
    ]
    return random.choice(uas)


async def download_via_http(
    session: aiohttp.ClientSession,
    repo: str,
    proxy: Optional[str],
    semaphore: asyncio.Semaphore,
    req_id: int,
) -> DownloadResult:
    """通过 HTTP 下载 GitHub archive zip 来计入下载/流量"""
    async with semaphore:
        url = ARCHIVE_URL.format(repo=repo)
        proxy_label = proxy or "直连"
        headers = {"User-Agent": random_ua()}
        start = time.monotonic()

        try:
            async with session.get(
                url,
                proxy=proxy,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60),
                allow_redirects=True,
            ) as resp:
                await resp.read()
                latency = (time.monotonic() - start) * 1000
                ok = resp.status == 200
                icon = "✓" if ok else "✗"
                print(
                    f"  [{req_id:04d}] {icon} HTTP {resp.status} | "
                    f"{latency:>7.0f}ms | {proxy_label[:30]:30s} | archive zip"
                )
                return DownloadResult(
                    method="http_archive",
                    proxy=proxy_label,
                    success=ok,
                    latency_ms=round(latency, 1),
                    error="" if ok else f"HTTP_{resp.status}",
                )
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            err = str(e)[:80]
            print(f"  [{req_id:04d}] ✗ ERROR     | {latency:>7.0f}ms | {proxy_label[:30]:30s} | {err}")
            return DownloadResult(method="http_archive", proxy=proxy_label, success=False, latency_ms=round(latency, 1), error=err)


async def download_via_git_clone(
    repo: str,
    proxy: Optional[str],
    semaphore: asyncio.Semaphore,
    req_id: int,
) -> DownloadResult:
    """通过 git clone 来计入 GitHub clone 计数（唯一IP计一次 unique clone）"""
    async with semaphore:
        clone_url = CLONE_URL.format(repo=repo)
        proxy_label = proxy or "直连"
        tmpdir = tempfile.mkdtemp(prefix="skill_dl_")
        start = time.monotonic()

        try:
            env = os.environ.copy()
            if proxy:
                env["http_proxy"] = proxy
                env["https_proxy"] = proxy
                env["ALL_PROXY"] = proxy

            proc = await asyncio.create_subprocess_exec(
                "git", "clone", "--depth=1", "--quiet", clone_url, tmpdir + "/repo",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
            latency = (time.monotonic() - start) * 1000
            ok = proc.returncode == 0

            icon = "✓" if ok else "✗"
            err_msg = stderr.decode().strip()[:80] if not ok else ""
            print(
                f"  [{req_id:04d}] {icon} clone rc={proc.returncode} | "
                f"{latency:>7.0f}ms | {proxy_label[:30]:30s} | git clone --depth=1"
            )
            return DownloadResult(method="git_clone", proxy=proxy_label, success=ok, latency_ms=round(latency, 1), error=err_msg)

        except asyncio.TimeoutError:
            latency = (time.monotonic() - start) * 1000
            print(f"  [{req_id:04d}] ✗ TIMEOUT   | {latency:>7.0f}ms | {proxy_label[:30]:30s} | git clone")
            return DownloadResult(method="git_clone", proxy=proxy_label, success=False, latency_ms=round(latency, 1), error="timeout")

        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            err = str(e)[:80]
            print(f"  [{req_id:04d}] ✗ ERROR     | {latency:>7.0f}ms | {proxy_label[:30]:30s} | {err}")
            return DownloadResult(method="git_clone", proxy=proxy_label, success=False, latency_ms=round(latency, 1), error=err)

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


async def download_via_api_refs(
    session: aiohttp.ClientSession,
    repo: str,
    proxy: Optional[str],
    semaphore: asyncio.Semaphore,
    req_id: int,
) -> DownloadResult:
    """访问 GitHub API refs 端点，模拟 skills CLI 的探测行为"""
    async with semaphore:
        url = f"https://api.github.com/repos/{repo}/git/refs/heads/main"
        proxy_label = proxy or "直连"
        headers = {"User-Agent": random_ua(), "Accept": "application/vnd.github.v3+json"}
        start = time.monotonic()

        try:
            async with session.get(
                url, proxy=proxy, headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                await resp.read()
                latency = (time.monotonic() - start) * 1000
                ok = resp.status == 200
                icon = "✓" if ok else "✗"
                print(
                    f"  [{req_id:04d}] {icon} HTTP {resp.status} | "
                    f"{latency:>7.0f}ms | {proxy_label[:30]:30s} | api/refs"
                )
                return DownloadResult(method="api_refs", proxy=proxy_label, success=ok, latency_ms=round(latency, 1))
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            err = str(e)[:80]
            print(f"  [{req_id:04d}] ✗ ERROR     | {latency:>7.0f}ms | {proxy_label[:30]:30s} | {err}")
            return DownloadResult(method="api_refs", proxy=proxy_label, success=False, latency_ms=round(latency, 1), error=err)


async def run_test(
    repo: str,
    proxies: List[str],
    concurrency: int,
    total_requests: int,
    mode: str,
) -> Stats:
    print(f"\n{'='*80}")
    print(f"  模式: {mode} | 并发: {concurrency} | 请求数: {total_requests}")
    print(f"{'='*80}")

    semaphore = asyncio.Semaphore(concurrency)
    stats = Stats()
    tasks = []

    connector = aiohttp.TCPConnector(limit=concurrency * 2, limit_per_host=0)
    async with aiohttp.ClientSession(connector=connector) as session:
        for i in range(total_requests):
            proxy = random.choice(proxies) if proxies else None

            if mode == "clone":
                tasks.append(download_via_git_clone(repo, proxy, semaphore, i + 1))
            elif mode == "archive":
                tasks.append(download_via_http(session, repo, proxy, semaphore, i + 1))
            elif mode == "mixed":
                if i % 3 == 0:
                    tasks.append(download_via_git_clone(repo, proxy, semaphore, i + 1))
                elif i % 3 == 1:
                    tasks.append(download_via_http(session, repo, proxy, semaphore, i + 1))
                else:
                    tasks.append(download_via_api_refs(session, repo, proxy, semaphore, i + 1))
            else:
                tasks.append(download_via_http(session, repo, proxy, semaphore, i + 1))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        stats.total += 1
        if isinstance(r, Exception):
            stats.fail += 1
            stats.errors[type(r).__name__] = stats.errors.get(type(r).__name__, 0) + 1
            continue
        stats.latencies.append(r.latency_ms)
        if r.success:
            stats.success += 1
        else:
            stats.fail += 1
            stats.errors[r.error or "unknown"] = stats.errors.get(r.error or "unknown", 0) + 1

    return stats


def print_report(stats: Stats, elapsed: float, proxies: List[str], repo: str):
    print(f"\n{'='*80}")
    print("  压测报告")
    print(f"{'='*80}")
    print(f"  仓库:           {repo}")
    print(f"  总请求数:       {stats.total}")
    print(f"  成功:           {stats.success}  ({stats.success_rate:.1f}%)")
    print(f"  失败:           {stats.fail}")
    print(f"  总耗时:         {elapsed:.1f}s")
    if elapsed > 0:
        print(f"  QPS:            {stats.total / elapsed:.1f}")
    print(f"  平均延迟:       {stats.avg_latency:.0f}ms")
    print(f"  P95 延迟:       {stats.p95_latency:.0f}ms")
    if stats.latencies:
        print(f"  最小延迟:       {min(stats.latencies):.0f}ms")
        print(f"  最大延迟:       {max(stats.latencies):.0f}ms")
    print(f"  代理IP数:       {len(proxies) if proxies else '0（直连）'}")

    if stats.errors:
        print(f"\n  错误分布:")
        for err, count in sorted(stats.errors.items(), key=lambda x: -x[1]):
            print(f"    {err}: {count}次")

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "repo": repo,
        "total_requests": stats.total,
        "success": stats.success,
        "fail": stats.fail,
        "success_rate": round(stats.success_rate, 2),
        "elapsed_seconds": round(elapsed, 1),
        "qps": round(stats.total / elapsed, 2) if elapsed > 0 else 0,
        "avg_latency_ms": round(stats.avg_latency, 1),
        "p95_latency_ms": round(stats.p95_latency, 1),
        "proxy_count": len(proxies),
        "errors": stats.errors,
    }
    report_path = Path("stress_test_report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n  报告已保存到: {report_path.resolve()}")
    print(f"{'='*80}\n")


async def main():
    parser = argparse.ArgumentParser(description="Skills 下载量压测脚本（不消耗 API 额度）")
    parser.add_argument("--repo", default=REPO, help=f"GitHub 仓库 (默认 {REPO})")
    parser.add_argument("--proxy-file", help="代理列表文件，每行一个 (http/socks5)")
    parser.add_argument("--proxy", action="append", help="单个代理地址，可多次指定")
    parser.add_argument("--concurrency", "-c", type=int, default=10, help="并发数 (默认 10)")
    parser.add_argument("--requests", "-n", type=int, default=50, help="总请求数 (默认 50)")
    parser.add_argument(
        "--mode", "-m", default="mixed",
        choices=["clone", "archive", "mixed"],
        help="下载模式: clone=git clone, archive=zip下载, mixed=混合 (默认 mixed)",
    )
    args = parser.parse_args()

    proxies = []
    if args.proxy_file:
        proxies = load_proxies(args.proxy_file)
    if args.proxy:
        proxies.extend(args.proxy)

    mode_desc = {"clone": "git clone（计入 GitHub Clones）", "archive": "zip 下载（计入 GitHub Traffic）", "mixed": "混合模式（clone + archive + api）"}

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         Skills 下载量压测工具 v1.0                           ║
║         ⚡ 不消耗 MeowLoad API 额度                         ║
╠══════════════════════════════════════════════════════════════╣
║  仓库:        {args.repo:<45s}║
║  模式:        {mode_desc[args.mode][:40]:<45s}║
║  并发:        {args.concurrency:<45d}║
║  总请求:      {args.requests:<45d}║
║  代理数:      {str(len(proxies)) + ' 个' if proxies else '0（直连）':<45s}║
╚══════════════════════════════════════════════════════════════╝""")

    start = time.monotonic()
    stats = await run_test(args.repo, proxies, args.concurrency, args.requests, args.mode)
    elapsed = time.monotonic() - start

    print(f"\n  完成: 成功 {stats.success}/{stats.total} | "
          f"成功率 {stats.success_rate:.1f}% | 平均延迟 {stats.avg_latency:.0f}ms")

    print_report(stats, elapsed, proxies, args.repo)


if __name__ == "__main__":
    asyncio.run(main())
