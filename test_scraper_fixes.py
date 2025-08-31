#!/usr/bin/env python3
"""
Test script to demonstrate all scrapers including fixes and new additions.
Run this to see the improvements and new scrapers in action.
Tests: IDownloadCoupon, CourseVania, FreebiesGlobal, TutorialBar, and RealDiscount
"""

import asyncio
from udemy_enroller.scrapers.idownloadcoupon import IDownloadCouponScraper
from udemy_enroller.scrapers.coursevania import CoursevaniaScraper
from udemy_enroller.scrapers.freebiesglobal import FreebiesglobalScraper
from udemy_enroller.scrapers.tutorialbar import TutorialBarScraper
from udemy_enroller.scrapers.realdiscount import RealDiscountScraper

async def test_scrapers():
    """Test all fixed scrapers and show results."""
    
    print("=" * 60)
    print("UDEMY SCRAPER FIX DEMONSTRATION")
    print("=" * 60)
    print("\nTesting scrapers with fixes applied...\n")
    
    scrapers = [
        ("IDownloadCoupon", IDownloadCouponScraper(enabled=True, max_pages=1)),
        ("CourseVania", CoursevaniaScraper(enabled=True, max_pages=1)),
        ("FreebiesGlobal", FreebiesglobalScraper(enabled=True, max_pages=1)),
        ("TutorialBar", TutorialBarScraper(enabled=True, max_pages=1)),
        ("RealDiscount", RealDiscountScraper(enabled=True, max_pages=1)),
    ]
    
    total_links = 0
    working_scrapers = 0
    
    for name, scraper in scrapers:
        print(f"Testing {name}...")
        try:
            links = await scraper.run()
            count = len(links)
            total_links += count
            
            if count > 0:
                working_scrapers += 1
                print(f"  ✅ SUCCESS: Found {count} Udemy course links")
                print(f"  Sample link: {links[0][:70]}...")
            else:
                print(f"  ⚠️  No links found (site may be blocked or changed)")
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)[:100]}")
        print()
    
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Working scrapers: {working_scrapers}/{len(scrapers)}")
    print(f"📚 Total Udemy courses found: {total_links}")
    print(f"🎯 Success rate: {working_scrapers/len(scrapers)*100:.0f}%")
    
    if total_links > 0:
        print(f"\n✨ These fixes restored access to {total_links} free Udemy courses!")
    
    return total_links

if __name__ == "__main__":
    links_found = asyncio.run(test_scrapers())
    exit(0 if links_found > 0 else 1)