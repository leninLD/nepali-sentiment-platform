import re
import time
import random
import unicodedata
from datetime import datetime, timedelta, timezone
from typing import Callable, List, Dict, Optional

NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.lucahammer.com",
    "https://nitter.1d4.us",
    "https://nitter.kavin.rocks",
    "https://nitter.net",
    "https://nitter.nl",
    "https://nitter.unixfox.eu",
]

MIN_DAYS = 10      # don't stop early until we've paged back at least this far
MAX_DAYS = 14       # hard stop — never go further back than this
MAX_TWEETS = 100    # hard cap on total tweets collected

_DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')

def _is_nepali(text: str, min_ratio: float = 0.25) -> bool:
    if not text:
        return False
    dev_chars    = len(_DEVANAGARI_RE.findall(text))
    total_letters = sum(1 for ch in text if unicodedata.category(ch).startswith('L'))
    if total_letters == 0:
        return False
    return (dev_chars / total_letters) >= min_ratio

_DATE_FORMATS = [
    "%b %d, %Y · %I:%M %p UTC",   # e.g. "Jul 21, 2026 · 10:15 AM UTC"
    "%b %d, %Y · %H:%M UTC",      # some instances use 24h clock
    "%d %b %Y · %I:%M %p UTC",
]

def _parse_tweet_date(title: str) -> Optional[datetime]:
    """Parse the title attribute of a Nitter '.tweet-date a' element into a
    timezone-aware UTC datetime. Returns None if it can't be parsed."""
    if not title:
        return None
    title = title.strip()
    for fmt in _DATE_FORMATS:
        try:
            dt = datetime.strptime(title, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None

def setup_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    driver.execute_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    return driver

def get_working_instance(driver) -> str | None:
    from selenium.webdriver.common.by import By
    for instance in NITTER_INSTANCES:
        try:
            driver.get(instance)
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
            return instance
        except Exception:
            continue
    return None

def scrape_nitter(
    keyword: str,
    target: int = 50,
    log_callback: Callable[[str], None] = None,
    min_days: int = MIN_DAYS,
    max_days: int = MAX_DAYS,
    max_tweets: int = MAX_TWEETS,
) -> List[Dict[str, str]]:
    from selenium.webdriver.common.by import By

    def log(msg):
        if log_callback:
            log_callback(msg)

    # Never collect more than max_tweets, regardless of what target was passed in.
    target = min(target, max_tweets)

    driver    = setup_driver()
    collected = []
    seen_text = set()
    oldest_collected_date: Optional[datetime] = None

    try:
        log("🔍 Finding a live Nitter instance...")
        base_url = get_working_instance(driver)
        if not base_url:
            log("❌ All Nitter instances are down. Try again in a few minutes.")
            return []

        log(f"✅ Connected to: {base_url}")
        encoded     = (keyword + " lang:ne").replace(" ", "+").replace('"', "")
        next_cursor = None
        page        = 1
        skipped     = 0
        old_skipped = 0
        now         = datetime.now(timezone.utc)
        cutoff      = now - timedelta(days=max_days)   # hard stop
        min_cutoff  = now - timedelta(days=min_days)   # minimum coverage required before an early stop
        reached_cutoff = False

        while len(collected) < max_tweets:
            url = (
                f"{base_url}/search?f=tweets&q={encoded}&cursor={next_cursor}"
                if next_cursor
                else f"{base_url}/search?f=tweets&q={encoded}"
            )
            driver.get(url)
            time.sleep(random.uniform(3, 5))

            articles = driver.find_elements(By.CSS_SELECTOR, ".timeline-item")
            if not articles:
                articles = driver.find_elements(By.CSS_SELECTOR, ".tweet-body")

            log(
                f"📄 Page {page} — {len(articles)} items | "
                f"{len(collected)}/{max_tweets} Nepali tweets collected "
                f"(need ≥{min_days}d coverage, hard stop at {max_days}d) | "
                f"({skipped} non-Nepali, {old_skipped} older-than-{max_days}-day skipped)..."
            )

            new_this_page = 0
            for article in articles:
                try:
                    try:
                        text = article.find_element(
                            By.CSS_SELECTOR, ".tweet-content"
                        ).text.strip()
                    except Exception:
                        text = article.text.strip()

                    if len(text) < 10:
                        continue
                    clean = text.replace("\n", " ").strip()
                    if clean in seen_text:
                        continue

                    if not _is_nepali(clean):
                        skipped += 1
                        continue

                    tweet_url  = ""
                    tweet_date = None
                    try:
                        date_link  = article.find_element(By.CSS_SELECTOR, ".tweet-date a")
                        path       = date_link.get_attribute("href")
                        tweet_url  = path if path.startswith("http") else base_url + path
                        tweet_date = _parse_tweet_date(date_link.get_attribute("title"))
                    except Exception:
                        pass

                    # Skip (and stop, since results are newest-first) once
                    # we hit a tweet older than the 2-week cutoff.
                    if tweet_date is not None and tweet_date < cutoff:
                        old_skipped += 1
                        reached_cutoff = True
                        break

                    seen_text.add(clean)

                    collected.append({
                        "text": clean,
                        "url": tweet_url,
                        "date": tweet_date.isoformat() if tweet_date else None,
                    })
                    new_this_page += 1

                    # Results are newest-first, so the last date we see on
                    # this page is the oldest one collected so far overall.
                    if tweet_date is not None:
                        oldest_collected_date = tweet_date

                    # Hard cap — never collect more than max_tweets.
                    if len(collected) >= max_tweets:
                        break

                except Exception:
                    continue

            if reached_cutoff:
                log(f"⏹️ Reached tweets older than {max_days} days — stopping. ({old_skipped} old tweet(s) skipped)")
                break
            if len(collected) >= max_tweets:
                log(f"⏹️ Hit the {max_tweets}-tweet cap — stopping.")
                break
            # Only allow an "early" stop on target count once we've also
            # paged back at least min_days — otherwise we'd stop after just
            # 2-3 days of high-volume results instead of covering the full window.
            if (
                len(collected) >= target
                and oldest_collected_date is not None
                and oldest_collected_date <= min_cutoff
            ):
                log(
                    f"✅ Collected {len(collected)} tweets spanning ≥{min_days} days — stopping."
                )
                break
            if new_this_page == 0:
                log("ℹ️ No new tweets on this page. Done.")
                break

            try:
                next_btn    = driver.find_element(By.CSS_SELECTOR, ".show-more a")
                href        = next_btn.get_attribute("href")
                next_cursor = (
                    href.split("cursor=")[-1] if "cursor=" in href else None
                )
                if not next_cursor:
                    break
            except Exception:
                break

            page += 1
            time.sleep(random.uniform(2, 4))

    except Exception as e:
        log(f"❌ Scraper error: {e}")
    finally:
        driver.quit()

    return collected