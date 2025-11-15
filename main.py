"""
Main script to run all Scrapy spiders programmatically.
Usage:
    python main.py              # Run all spiders
    python main.py pik_html     # Run specific spider by name
    python main.py --list       # List all available spiders
"""

import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader


def get_all_spiders():
    """Get list of all available spider names."""
    settings = get_project_settings()
    loader = SpiderLoader.from_settings(settings)
    return loader.list()


def run_spiders(spider_names=None):
    """
    Run one or more spiders.
    
    Args:
        spider_names: List of spider names to run. If None, runs all spiders.
    """
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    if spider_names is None:
        # Run all spiders
        spider_names = get_all_spiders()
        print(f"Starting all spiders: {', '.join(spider_names)}")
    else:
        print(f"Starting spiders: {', '.join(spider_names)}")
    
    if not spider_names:
        print("No spiders found!")
        return
    
    # Add each spider to the crawler process
    for spider_name in spider_names:
        print(f"Adding spider: {spider_name}")
        process.crawl(spider_name)
    
    # Start the crawling process
    print("\nStarting crawl...")
    process.start()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list" or sys.argv[1] == "-l":
            # List all available spiders
            spiders = get_all_spiders()
            print("Available spiders:")
            for spider in spiders:
                print(f"  - {spider}")
            return
        else:
            # Run specific spider(s)
            spider_names = sys.argv[1:]
            run_spiders(spider_names)
    else:
        # Run all spiders
        run_spiders()


if __name__ == "__main__":
    main()

