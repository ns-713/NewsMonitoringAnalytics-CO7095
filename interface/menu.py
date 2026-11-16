"""
Interactive Command-Line Menu and Dashboard Interface
Connects user actions to underlying domain services with formatted reports and robust error trapping.
Responsibility: Jalakam Prashanth (Pj161 - US11, US36) with team integration
"""

import sys
from typing import Optional
from config.settings import APP_NAME, APP_VERSION, ACADEMIC_YEAR, COURSE_CODE, CATEGORIES
from interface.formatting import Formatter
from interface.input_handler import InputHandler

from services.news_service import NewsService
from services.rss_service import RssService
from services.search_service import SearchService
from services.categorisation_service import CategorisationService
from services.sentiment_service import SentimentService
from services.duplicate_service import DuplicateService
from services.trend_service import TrendService
from services.source_analytics_service import SourceAnalyticsService
from services.time_analytics_service import TimeAnalyticsService
from services.alert_service import AlertService
from services.report_service import ReportService
from services.dashboard_service import DashboardService
from storage.json_storage import JsonStorage
from config.settings import ARTICLES_FILE, SOURCES_FILE, ALERT_RULES_FILE, ALERTS_FILE


class MainMenu:
    """
    Coordinates interactive terminal menus, data display, and workflow routing.
    """

    def __init__(self):
        self.categorisation_service = CategorisationService()
        self.sentiment_service = SentimentService()
        self.duplicate_service = DuplicateService()
        self.trend_service = TrendService()
        self.alert_service = AlertService()
        self.rss_service = RssService()
        self.report_service = ReportService()

        self.news_service = NewsService(
            categorisation_service=self.categorisation_service,
            sentiment_service=self.sentiment_service,
            duplicate_service=self.duplicate_service,
            alert_service=self.alert_service
        )

        self.dashboard_service = DashboardService(
            news_service=self.news_service,
            alert_service=self.alert_service,
            trend_service=self.trend_service
        )

    def run(self) -> None:
        """Starts interactive main event loop."""
        Formatter.print_banner(
            f"{APP_NAME} v{APP_VERSION}",
            f"{COURSE_CODE} Software Measurement and QA ({ACADEMIC_YEAR})"
        )

        while True:
            self.display_main_menu()
            choice = InputHandler.get_string("\nEnter your option (0-19)", default="1")

            if choice == "0":
                if InputHandler.confirm("Are you sure you want to exit?"):
                    print("\nExiting application. Thank you for using News Monitoring and Analytics!")
                    break
            elif choice == "1":
                self.show_dashboard()
            elif choice == "2":
                self.view_all_news()
            elif choice == "3":
                self.add_news_manually()
            elif choice == "4":
                self.collect_news_from_rss()
            elif choice == "5":
                self.manage_news_sources()
            elif choice == "6":
                self.search_news()
            elif choice == "7":
                self.filter_news()
            elif choice == "8":
                self.view_categories()
            elif choice == "9":
                self.show_sentiment_analytics()
            elif choice == "10":
                self.show_trending_topics()
            elif choice == "11":
                self.show_source_analytics()
            elif choice == "12":
                self.show_time_analytics()
            elif choice == "13":
                self.show_duplicate_detection()
            elif choice == "14":
                self.manage_keyword_monitoring()
            elif choice == "15":
                self.view_alerts()
            elif choice == "16":
                self.generate_reports()
            elif choice == "17":
                self.export_csv()
            elif choice == "18":
                self.load_demo_dataset()
            elif choice == "19":
                self.data_management()
            else:
                Formatter.print_error("Invalid selection. Please choose an option from 0 to 19.")

    def display_main_menu(self) -> None:
        """Renders main numbered menu."""
        print("\n" + "=" * 60)
        print("                 MAIN APPLICATION MENU")
        print("=" * 60)
        print("  [1]  Interactive Dashboard      [11] Source Analytics")
        print("  [2]  View All News              [12] Time Analytics")
        print("  [3]  Add News Manually          [13] Duplicate Detection")
        print("  [4]  Collect News from RSS      [14] Manage Keyword Rules")
        print("  [5]  Manage News Sources        [15] View Keyword Alerts")
        print("  [6]  Search News                [16] View System Reports")
        print("  [7]  Filter News (Multi-filter) [17] Export Reports to CSV")
        print("  [8]  View Categories            [18] Load Demo Dataset (Offline)")
        print("  [9]  Sentiment Analytics        [19] Data Management & Backups")
        print("  [10] Trending Topics & Keywords [0]  Exit")
        print("=" * 60)

    # ----------------------------------------------------
    # Menu Actions
    # ----------------------------------------------------

    def show_dashboard(self) -> None:
        """Displays real-time system metrics and alert status."""
        metrics = self.dashboard_service.get_dashboard_metrics()
        Formatter.print_section(">>> EXECUTIVE DASHBOARD")

        print(f"  Total Articles Stored : {metrics['total_articles']}")
        print(f"  Registered Sources    : {metrics['total_sources']}")
        print(f"  Active Keyword Rules  : {metrics['active_rules']}")
        print(f"  Total Alerts Logged   : {metrics['total_alerts']} ({metrics['unread_alerts']} Unread)")

        # Sentiment Summary
        sent = metrics["sentiment"]
        total_scored = sum(sent.values())
        print(f"\n  Sentiment Distribution (Total: {total_scored}):")
        print(f"    - Positive : {sent['Positive']} ({round(sent['Positive']/total_scored*100, 1) if total_scored else 0}%)")
        print(f"    - Negative : {sent['Negative']} ({round(sent['Negative']/total_scored*100, 1) if total_scored else 0}%)")
        print(f"    - Neutral  : {sent['Neutral']} ({round(sent['Neutral']/total_scored*100, 1) if total_scored else 0}%)")

        # Top Categories
        print("\n  Top 5 News Categories:")
        if metrics["top_categories"]:
            cat_rows = [[cat, count] for cat, count in metrics["top_categories"]]
            Formatter.print_table(["Category", "Article Count"], cat_rows)
        else:
            print("    (No articles categorised yet)")

        # Top Sources
        print("\n  Top 5 Sources by Volume:")
        if metrics["top_sources"]:
            src_rows = [[src, count] for src, count in metrics["top_sources"]]
            Formatter.print_table(["Source", "Article Count"], src_rows)
        else:
            print("    (No sources tracked yet)")

        # Trending Keywords
        print("\n  Top 10 Trending Keywords:")
        if metrics["trending_keywords"]:
            kw_rows = [[rank + 1, kw, count] for rank, (kw, count) in enumerate(metrics["trending_keywords"])]
            Formatter.print_table(["Rank", "Keyword", "Mentions"], kw_rows)
        else:
            print("    (No trending terms found)")

        # Recent Articles
        print("\n  Latest Articles Ingested:")
        if metrics["latest_articles"]:
            latest_rows = [
                [a.article_id, Formatter.truncate(a.headline, 38), a.source_name, a.category, a.sentiment]
                for a in metrics["latest_articles"]
            ]
            Formatter.print_table(["Article ID", "Headline", "Source", "Category", "Sentiment"], latest_rows)
        else:
            print("    (No articles in repository)")

    def view_all_news(self) -> None:
        """Lists articles with pagination and detailed inspect option."""
        articles = self.news_service.get_all_articles()
        Formatter.print_section(f">>> VIEW ALL NEWS ARTICLES (Total: {len(articles)})")
        if not articles:
            Formatter.print_info("No articles currently stored. Load demo dataset or collect RSS feeds.")
            return

        page_size = 10
        total_pages = (len(articles) + page_size - 1) // page_size
        page = 1

        while True:
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            batch = articles[start_idx:end_idx]

            print(f"\n--- Page {page} of {total_pages} ---")
            rows = [
                [idx + 1, a.article_id, Formatter.truncate(a.headline, 40), a.source_name, a.category, a.sentiment]
                for idx, a in enumerate(batch, start=start_idx)
            ]
            Formatter.print_table(["#", "ID", "Headline", "Source", "Category", "Sentiment"], rows)

            print("\nOptions: [N]ext Page | [P]revious Page | [V]iew Article Details | [D]elete Article | [B]ack to Menu")
            action = InputHandler.get_string("Choose action", default="B").upper()

            if action == "N" and page < total_pages:
                page += 1
            elif action == "P" and page > 1:
                page -= 1
            elif action == "V":
                art_id = InputHandler.get_string("Enter Article ID to inspect")
                self.inspect_article(art_id)
            elif action == "D":
                art_id = InputHandler.get_string("Enter Article ID to delete")
                if InputHandler.confirm(f"Confirm deletion of '{art_id}'?"):
                    ok, msg = self.news_service.delete_article(art_id)
                    if ok:
                        Formatter.print_success(msg)
                        articles = self.news_service.get_all_articles()
                        total_pages = max(1, (len(articles) + page_size - 1) // page_size)
                        page = min(page, total_pages)
                    else:
                        Formatter.print_error(msg)
            elif action == "B":
                break

    def inspect_article(self, article_id: str) -> None:
        """Renders comprehensive details of a single article."""
        article = self.news_service.get_article_by_id(article_id)
        if not article:
            Formatter.print_error(f"Article '{article_id}' not found.")
            return

        Formatter.print_section(f"ARTICLE DETAILS: {article.article_id}")
        print(f"  Headline         : {article.headline}")
        print(f"  Source           : {article.source_name} ({article.source_url})")
        print(f"  Article URL      : {article.article_url}")
        print(f"  Publication Date : {article.publication_date}")
        print(f"  Category         : {article.category}")
        print(f"  Sentiment        : {article.sentiment} (Score: {article.sentiment_score})")
        print(f"  Keywords         : {', '.join(article.keywords) if article.keywords else '(none)'}")
        print(f"  Description      : {article.description}")
        print(f"\n  Content Preview  :\n  {article.content[:400]}...")

    def add_news_manually(self) -> None:
        """Prompts user to manually add an article."""
        Formatter.print_section(">>> ADD NEWS ARTICLE MANUALLY")
        headline = InputHandler.get_string("Headline", allow_empty=False)
        source_name = InputHandler.get_string("Source Name", default="Manual Entry", allow_empty=False)
        article_url = InputHandler.get_string("Article URL (optional)")
        description = InputHandler.get_string("Description (optional)")
        content = InputHandler.get_string("Content (optional)")
        pub_date = InputHandler.get_string("Publication Date (YYYY-MM-DD, optional)")
        category = InputHandler.get_choice("Category", CATEGORIES, default="Other")

        ok, msg, created = self.news_service.add_article(
            headline=headline,
            source_name=source_name,
            article_url=article_url,
            description=description,
            content=content,
            publication_date=pub_date or None,
            category=category
        )

        if ok and created:
            Formatter.print_success(f"{msg} ID: {created.article_id}")
            print(f"  Classified Category : {created.category}")
            print(f"  Calculated Tone     : {created.sentiment} (Score: {created.sentiment_score})")
        else:
            Formatter.print_error(msg)

    def collect_news_from_rss(self) -> None:
        """Collects articles from registered RSS feeds or offline demo mode."""
        sources = [s for s in self.news_service.get_sources() if s.enabled]
        Formatter.print_section(">>> COLLECT NEWS FROM RSS FEEDS")

        print("  [1] Collect from All Enabled RSS Sources")
        print("  [2] Collect from a Specific Source")
        print("  [3] Offline Demonstration RSS Ingestion (No Internet Needed)")
        print("  [0] Back")

        sub_choice = InputHandler.get_string("Select mode", default="1")
        if sub_choice == "0":
            return

        if sub_choice == "3":
            # Offline demo collection
            Formatter.print_info("Ingesting articles via offline demonstration feed...")
            articles = self.rss_service.load_offline_demo_feed()
            stats = self.news_service.import_articles_batch(articles, source_name="Demo Feed")
            Formatter.print_success(
                f"Offline collection finished! Added: {stats['added']}, Duplicates skipped: {stats['duplicates_skipped']}"
            )
            return

        if not sources:
            Formatter.print_warning("No active RSS sources registered. Register feeds in Option 5.")
            return

        target_sources = sources
        if sub_choice == "2":
            src_names = [s.name for s in sources]
            selected_name = InputHandler.get_choice("Choose source", src_names)
            target_sources = [s for s in sources if s.name == selected_name]

        total_added = 0
        total_dups = 0

        for s in target_sources:
            print(f"\n  Fetching RSS feed for '{s.name}' ({s.feed_url})...")
            ok, articles, err = self.rss_service.collect_from_feed(s)
            if not ok:
                Formatter.print_warning(f"Failed to fetch '{s.name}': {err} (Continuing other feeds)")
                continue

            stats = self.news_service.import_articles_batch(articles, source_name=s.name)
            print(f"    -> Parsed {len(articles)} items | Added: {stats['added']} | Duplicates skipped: {stats['duplicates_skipped']}")
            total_added += stats["added"]
            total_dups += stats["duplicates_skipped"]

        Formatter.print_success(f"RSS Collection completed. Total added: {total_added}, Duplicates skipped: {total_dups}")

    def manage_news_sources(self) -> None:
        """Registers, inspects, and removes RSS news sources."""
        while True:
            sources = self.news_service.get_sources()
            Formatter.print_section(">>> MANAGE NEWS SOURCES")

            rows = [
                [s.source_id, s.name, Formatter.truncate(s.feed_url, 35), "Yes" if s.enabled else "No", s.article_count]
                for s in sources
            ]
            Formatter.print_table(["Source ID", "Name", "Feed URL", "Enabled", "Articles"], rows)

            print("\nOptions: [A]dd Feed | [R]emove Feed | [B]ack to Main Menu")
            action = InputHandler.get_string("Choose action", default="B").upper()

            if action == "A":
                name = InputHandler.get_string("Source Name", allow_empty=False)
                feed_url = InputHandler.get_string("RSS Feed URL (http/https/file)", allow_empty=False)
                site_url = InputHandler.get_string("Website URL (optional)")
                category = InputHandler.get_choice("Primary Category", CATEGORIES, default="General")

                ok, msg, _ = self.news_service.add_source(name=name, feed_url=feed_url, url=site_url, category=category)
                if ok:
                    Formatter.print_success(msg)
                else:
                    Formatter.print_error(msg)
            elif action == "R":
                src_id = InputHandler.get_string("Enter Source ID to remove")
                ok, msg = self.news_service.remove_source(src_id)
                if ok:
                    Formatter.print_success(msg)
                else:
                    Formatter.print_error(msg)
            elif action == "B":
                break

    def search_news(self) -> None:
        """Executes case-insensitive substring search over headlines, content, and keywords."""
        Formatter.print_section(">>> SEARCH NEWS")
        query = InputHandler.get_string("Enter search term (or leave empty to view all)")
        field = InputHandler.get_choice("Search in", ["Headline", "Content", "Keywords", "All"], default="All")

        articles = self.news_service.get_all_articles()

        if field == "Headline":
            results = SearchService.search_headline(articles, query)
        elif field == "Content":
            results = SearchService.search_content(articles, query)
        elif field == "Keywords":
            results = SearchService.search_keywords(articles, query)
        else:
            results = SearchService.combined_filter(articles, query=query)

        Formatter.print_info(f"Found {len(results)} matching articles for query '{query}':")
        rows = [
            [a.article_id, Formatter.truncate(a.headline, 42), a.source_name, a.category, a.sentiment]
            for a in results[:20]
        ]
        Formatter.print_table(["ID", "Headline", "Source", "Category", "Sentiment"], rows)
        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more articles.")

    def filter_news(self) -> None:
        """Multi-criteria filtering by source, category, sentiment, and date range."""
        Formatter.print_section(">>> COMBINED MULTI-FILTER")
        articles = self.news_service.get_all_articles()

        src_filter = InputHandler.get_string("Source name filter (leave blank for any)")
        cat_choices = ["All"] + CATEGORIES
        cat_filter = InputHandler.get_choice("Category filter", cat_choices, default="All")
        sent_filter = InputHandler.get_choice("Sentiment filter", ["All", "Positive", "Negative", "Neutral"], default="All")
        start_date = InputHandler.get_string("Start date (YYYY-MM-DD, optional)")
        end_date = InputHandler.get_string("End date (YYYY-MM-DD, optional)")

        results = SearchService.combined_filter(
            articles=articles,
            source=src_filter,
            category=cat_filter,
            sentiment=sent_filter,
            start_date=start_date or None,
            end_date=end_date or None
        )

        Formatter.print_info(f"Matched {len(results)} articles across applied criteria:")
        rows = [
            [a.article_id, Formatter.truncate(a.headline, 40), a.source_name, a.category, a.publication_date]
            for a in results[:25]
        ]
        Formatter.print_table(["ID", "Headline", "Source", "Category", "Date"], rows)

    def view_categories(self) -> None:
        """Displays configured categories and keyword rules."""
        Formatter.print_section(">>> NEWS CATEGORIES CONFIGURATION")
        categories = self.categorisation_service.get_categories()
        articles = self.news_service.get_all_articles()
        counts = self.trend_service.get_category_frequencies(articles)

        rows = []
        for cat in categories:
            kws = self.categorisation_service.get_keywords_for_category(cat)
            sample_kws = ", ".join(kws[:6]) + ("..." if len(kws) > 6 else "")
            rows.append([cat, counts.get(cat, 0), sample_kws or "(None)"])

        Formatter.print_table(["Category", "Current Articles", "Configured Keywords (Sample)"], rows, max_col_widths=[15, 18, 40])

    def show_sentiment_analytics(self) -> None:
        """Displays rule-based sentiment distributions and allows interactive test scoring."""
        Formatter.print_section(">>> SENTIMENT ANALYTICS")
        articles = self.news_service.get_all_articles()

        metrics = self.dashboard_service.get_dashboard_metrics()["sentiment"]
        tot = sum(metrics.values())

        print(f"  Total Articles Evaluated: {tot}")
        rows = [
            ["Positive", metrics["Positive"], f"{round(metrics['Positive']/tot*100, 1) if tot else 0}%"],
            ["Negative", metrics["Negative"], f"{round(metrics['Negative']/tot*100, 1) if tot else 0}%"],
            ["Neutral", metrics["Neutral"], f"{round(metrics['Neutral']/tot*100, 1) if tot else 0}%"]
        ]
        Formatter.print_table(["Sentiment Class", "Count", "Percentage"], rows)

        print("\n  [T] Test Custom Text Sentiment | [B] Back")
        action = InputHandler.get_string("Select option", default="B").upper()
        if action == "T":
            sample_text = InputHandler.get_string("Enter text to analyse", allow_empty=False)
            res = self.sentiment_service.analyse_text(sample_text)
            print(f"\n  Result Score    : {res['score']}")
            print(f"  Classification  : {res['label']}")
            print(f"  Positive Words  : {', '.join(res['positive_words']) or '(None)'} (Count: {res['positive_count']})")
            print(f"  Negative Words  : {', '.join(res['negative_words']) or '(None)'} (Count: {res['negative_count']})")

    def show_trending_topics(self) -> None:
        """Displays top discussed keywords and category momentum."""
        Formatter.print_section(">>> TRENDING TOPICS AND KEYWORDS")
        articles = self.news_service.get_all_articles()
        if not articles:
            Formatter.print_info("No articles stored. Load demo dataset or collect RSS.")
            return

        trending = self.trend_service.get_keyword_frequencies(articles, top_n=15)
        rows = [[idx + 1, kw, count] for idx, (kw, count) in enumerate(trending)]
        Formatter.print_table(["Rank", "Trending Keyword", "Frequency"], rows)

        print("\n  Filter Trending by Specific Date?")
        if InputHandler.confirm("Enter a date filter?", default_yes=False):
            dt = InputHandler.get_string("Enter Date (YYYY-MM-DD)")
            date_trends = self.trend_service.get_trending_by_date(articles, dt, top_n=10)
            print(f"\n  Trending on {dt}:")
            dt_rows = [[idx + 1, kw, c] for idx, (kw, c) in enumerate(date_trends)]
            Formatter.print_table(["Rank", "Keyword", "Frequency"], dt_rows)

    def show_source_analytics(self) -> None:
        """Displays source volume, distribution, and sentiment profiles."""
        Formatter.print_section(">>> NEWS SOURCE ANALYTICS")
        print("  NOTE: Source article counts measure collection volume, NOT journalistic accuracy or credibility.\n")

        articles = self.news_service.get_all_articles()
        if not articles:
            Formatter.print_info("No articles stored.")
            return

        dist = SourceAnalyticsService.get_source_distribution(articles)
        dist_rows = [[d["source"], d["article_count"], f"{d['percentage']}%"] for d in dist]
        Formatter.print_table(["Source", "Total Articles", "Share (%)"], dist_rows)

        print("\n  Source Sentiment Breakdown:")
        sent_by_src = SourceAnalyticsService.get_sentiment_distribution_by_source(articles)
        sent_rows = [
            [src, data["total"], f"{data['positive']} ({data['positive_pct']}%)",
             f"{data['negative']} ({data['negative_pct']}%)", f"{data['neutral']} ({data['neutral_pct']}%)"]
            for src, data in sent_by_src.items()
        ]
        Formatter.print_table(["Source", "Total", "Positive", "Negative", "Neutral"], sent_rows)

    def show_time_analytics(self) -> None:
        """Displays publication volume grouped by day, week, and month."""
        Formatter.print_section(">>> TIME-BASED ANALYTICS")
        articles = self.news_service.get_all_articles()
        if not articles:
            Formatter.print_info("No articles stored.")
            return

        print("  [1] Daily Statistics")
        print("  [2] Weekly Statistics")
        print("  [3] Monthly Statistics")
        choice = InputHandler.get_string("Choose time bucket", default="1")

        if choice == "2":
            weekly = TimeAnalyticsService.get_weekly_statistics(articles)
            rows = [[wk, count] for wk, count in weekly.items()]
            Formatter.print_table(["Calendar Week", "Articles Published"], rows)
        elif choice == "3":
            monthly = TimeAnalyticsService.get_monthly_statistics(articles)
            rows = [[m, count] for m, count in monthly.items()]
            Formatter.print_table(["Month", "Articles Published"], rows)
        else:
            daily = TimeAnalyticsService.get_daily_statistics(articles)
            rows = [[dt, count] for dt, count in daily.items()]
            Formatter.print_table(["Date", "Articles Published"], rows)

    def show_duplicate_detection(self) -> None:
        """Identifies URL, exact headline, and token-similarity duplicate pairs."""
        Formatter.print_section(">>> DUPLICATE NEWS DETECTION")
        articles = self.news_service.get_all_articles()
        if not articles:
            Formatter.print_info("No articles stored.")
            return

        duplicates = self.duplicate_service.find_all_duplicates(articles)
        Formatter.print_info(f"Identified {len(duplicates)} duplicate pairs/groups:")

        rows = [
            [d["article_a_id"], Formatter.truncate(d["article_a_headline"], 28),
             d["article_b_id"], Formatter.truncate(d["article_b_headline"], 28),
             Formatter.truncate(d["reason"], 30)]
            for d in duplicates
        ]
        Formatter.print_table(["Article A", "Headline A", "Article B", "Headline B", "Reason"], rows)

    def manage_keyword_monitoring(self) -> None:
        """Configures keyword alert monitoring rules."""
        while True:
            Formatter.print_section(">>> MANAGE KEYWORD MONITORING RULES")
            rules = self.alert_service.get_rules()

            rows = [
                [r.rule_id, r.keyword, r.category_filter or "(Any)", "Active" if r.enabled else "Disabled", r.description]
                for r in rules
            ]
            Formatter.print_table(["Rule ID", "Monitored Keyword", "Category Filter", "Status", "Description"], rows)

            print("\nOptions: [A]dd Rule | [T]oggle Rule | [D]elete Rule | [B]ack to Main Menu")
            action = InputHandler.get_string("Choose action", default="B").upper()

            if action == "A":
                kw = InputHandler.get_string("Keyword to monitor", allow_empty=False)
                desc = InputHandler.get_string("Description")
                cat_choices = ["None"] + CATEGORIES
                cat_filter = InputHandler.get_choice("Category constraint", cat_choices, default="None")
                cat_val = None if cat_filter == "None" else cat_filter

                ok, msg, _ = self.alert_service.add_rule(kw, description=desc, category_filter=cat_val)
                if ok:
                    Formatter.print_success(msg)
                else:
                    Formatter.print_error(msg)
            elif action == "T":
                r_id = InputHandler.get_string("Rule ID to toggle")
                ok, msg = self.alert_service.toggle_rule(r_id)
                if ok:
                    Formatter.print_success(msg)
                else:
                    Formatter.print_error(msg)
            elif action == "D":
                r_id = InputHandler.get_string("Rule ID to delete")
                ok, msg = self.alert_service.delete_rule(r_id)
                if ok:
                    Formatter.print_success(msg)
                else:
                    Formatter.print_error(msg)
            elif action == "B":
                break

    def view_alerts(self) -> None:
        """Lists generated alerts and marks alerts as read."""
        while True:
            Formatter.print_section(">>> KEYWORD ALERTS")
            alerts = self.alert_service.get_alerts()
            unread_count = sum(1 for a in alerts if a.status == "UNREAD")

            print(f"  Total Alerts: {len(alerts)} | Unread: {unread_count}\n")
            rows = [
                [a.alert_id, a.keyword, a.article_id, Formatter.truncate(a.headline, 35), a.alert_date[:10], a.status]
                for a in alerts
            ]
            Formatter.print_table(["Alert ID", "Matched Keyword", "Article ID", "Headline", "Date", "Status"], rows)

            print("\nOptions: [R]ead Specific Alert | [M]ark All As Read | [B]ack to Main Menu")
            action = InputHandler.get_string("Choose action", default="B").upper()

            if action == "R":
                a_id = InputHandler.get_string("Enter Alert ID")
                if self.alert_service.mark_alert_read(a_id):
                    Formatter.print_success(f"Alert '{a_id}' marked as read.")
                else:
                    Formatter.print_error("Alert not found.")
            elif action == "M":
                count = self.alert_service.mark_all_alerts_read()
                Formatter.print_success(f"{count} alerts marked as read.")
            elif action == "B":
                break

    def generate_reports(self) -> None:
        """Prints a consolidated system report summary."""
        Formatter.print_section(">>> CONSOLIDATED SYSTEM ANALYTICS REPORT")
        metrics = self.dashboard_service.get_dashboard_metrics()
        articles = self.news_service.get_all_articles()

        print(f"  Report Timestamp     : {articles[0].created_timestamp if articles else 'N/A'}")
        print(f"  Total Articles       : {metrics['total_articles']}")
        print(f"  Total Sources        : {metrics['total_sources']}")
        print(f"  Monitored Keywords   : {metrics['active_rules']}")
        print(f"  Alert Notifications  : {metrics['total_alerts']} ({metrics['unread_alerts']} unread)")

        # Category Table
        cat_counts = self.trend_service.get_category_frequencies(articles)
        print("\n  Category Breakdown:")
        cat_rows = [[c, cnt] for c, cnt in cat_counts.items()]
        Formatter.print_table(["Category", "Articles"], cat_rows)

        # Source Table
        dist = SourceAnalyticsService.get_source_distribution(articles)
        print("\n  Source Ingestion Distribution:")
        dist_rows = [[d["source"], d["article_count"], f"{d['percentage']}%"] for d in dist]
        Formatter.print_table(["Source", "Count", "Percentage"], dist_rows)

        Formatter.print_info("Use Option 17 to export these report tables to CSV files.")

    def export_csv(self) -> None:
        """Exports analytics data to CSV files in reports/generated/."""
        Formatter.print_section(">>> EXPORT ANALYTICS TO CSV")
        articles = self.news_service.get_all_articles()
        if not articles:
            Formatter.print_warning("No articles in storage to export.")
            return

        cat_counts = self.trend_service.get_category_frequencies(articles)
        source_dist = SourceAnalyticsService.get_source_distribution(articles)
        trends = self.trend_service.get_keyword_frequencies(articles, top_n=25)
        alerts = self.alert_service.get_alerts()
        duplicates = self.duplicate_service.find_all_duplicates(articles)
        daily_counts = TimeAnalyticsService.get_daily_statistics(articles)

        f1 = self.report_service.export_articles_csv(articles)
        f2 = self.report_service.export_category_distribution_csv(cat_counts)
        f3 = self.report_service.export_source_analytics_csv(source_dist)
        f4 = self.report_service.export_trending_topics_csv(trends)
        f5 = self.report_service.export_alerts_csv(alerts)
        f6 = self.report_service.export_duplicates_csv(duplicates)
        f7 = self.report_service.export_time_trends_csv(daily_counts)

        Formatter.print_success("Successfully exported reports to CSV:")
        for path in [f1, f2, f3, f4, f5, f6, f7]:
            print(f"  - {path}")

    def load_demo_dataset(self) -> None:
        """Loads synthetic demonstration data into repository."""
        Formatter.print_section(">>> LOAD OFFLINE DEMONSTRATION DATASET")
        print("  This imports 105 synthetic articles with categories, sentiment, and duplicate examples.")
        if InputHandler.confirm("Proceed with demo dataset import?"):
            ok, msg, count = self.news_service.load_demo_data()
            if ok:
                Formatter.print_success(msg)
            else:
                Formatter.print_error(msg)

    def data_management(self) -> None:
        """Manages storage integrity, backups, and restores."""
        Formatter.print_section(">>> DATA MANAGEMENT AND PERSISTENCE")
        print("  [1] Validate JSON Storage Integrity")
        print("  [2] Create Manual Backup of All Files")
        print("  [3] Restore Files from Backup (.bak)")
        print("  [4] Reset Data to Empty Repositories")
        print("  [0] Back")

        choice = InputHandler.get_string("Select option", default="1")
        files = [ARTICLES_FILE, SOURCES_FILE, ALERT_RULES_FILE, ALERTS_FILE]

        if choice == "1":
            for f in files:
                valid = JsonStorage.validate_file(f)
                status = "[VALID]" if valid else "[INVALID / MISSING]"
                print(f"  {status} {f.name}")
            Formatter.print_info("Integrity check completed.")

        elif choice == "2":
            for f in files:
                bak = JsonStorage.create_backup(f)
                if bak:
                    print(f"  Backup created: {bak.name}")
            Formatter.print_success("Backups created for all data stores.")

        elif choice == "3":
            if InputHandler.confirm("Restore data files from backup? Current unbacked changes will be overwritten."):
                for f in files:
                    restored = JsonStorage.restore_from_backup(f)
                    print(f"  {'Restored' if restored else 'No backup for'} {f.name}")
                self.news_service.load_all()
                self.alert_service.load_all()
                Formatter.print_success("Data restoration complete.")

        elif choice == "4":
            if InputHandler.confirm("CAUTION: Clear all articles and alerts?", default_yes=False):
                self.news_service.articles = []
                self.news_service.save_articles()
                self.alert_service.alerts = []
                self.alert_service.save_alerts()
                Formatter.print_success("Repositories cleared.")
