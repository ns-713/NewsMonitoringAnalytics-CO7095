"""
Settings and configuration constants for News Monitoring and Analytics Application.
CO7095 - Software Measurement and Quality Assurance (2026-2027)
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
DATASET_DIR = BASE_DIR / "dataset"
REPORTS_DIR = BASE_DIR / "reports"
GENERATED_REPORTS_DIR = REPORTS_DIR / "generated"
COVERAGE_REPORTS_DIR = REPORTS_DIR / "coverage"
EXECUTION_REPORTS_DIR = REPORTS_DIR / "execution"

# Ensure data and report directories exist
for directory in [DATA_DIR, DATASET_DIR, REPORTS_DIR, GENERATED_REPORTS_DIR, COVERAGE_REPORTS_DIR, EXECUTION_REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data Persistence Files
ARTICLES_FILE = DATA_DIR / "articles.json"
SOURCES_FILE = DATA_DIR / "sources.json"
ALERT_RULES_FILE = DATA_DIR / "alert_rules.json"
ALERTS_FILE = DATA_DIR / "alerts.json"
DEMO_DATASET_FILE = DATASET_DIR / "demo_news.json"

# Config Dictionaries
CATEGORY_KEYWORDS_FILE = CONFIG_DIR / "category_keywords.json"
POSITIVE_WORDS_FILE = CONFIG_DIR / "positive_words.json"
NEGATIVE_WORDS_FILE = CONFIG_DIR / "negative_words.json"
STOP_WORDS_FILE = CONFIG_DIR / "stop_words.json"

# RSS Collection Configuration
DEFAULT_RSS_TIMEOUT_SECONDS = 10
MAX_ARTICLES_PER_FEED = 50
USER_AGENT = "NewsMonitoringBot/1.0 (CO7095 Academic Project; +http://localhost)"

# Categories
CATEGORIES = [
    "Politics",
    "Business",
    "Technology",
    "Health",
    "Sports",
    "Education",
    "Science",
    "Environment",
    "World News",
    "Entertainment",
    "Other"
]

DEFAULT_CATEGORY = "Other"

# Sentiment Classes
SENTIMENT_POSITIVE = "Positive"
SENTIMENT_NEGATIVE = "Negative"
SENTIMENT_NEUTRAL = "Neutral"

# Duplicate Detection Thresholds
SIMILARITY_THRESHOLD = 0.70  # Jaccard token overlap for headline similarity

# Application Metadata
APP_NAME = "News Monitoring and Analytics Application"
APP_VERSION = "1.0.0"
ACADEMIC_YEAR = "2026-2027"
COURSE_CODE = "CO7095"
