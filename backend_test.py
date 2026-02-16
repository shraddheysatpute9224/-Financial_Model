#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

class StockAnalysisPlatformTester:
    def __init__(self, base_url="https://smartdoc-review.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.passed_tests = []

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int, data: Dict = None, params: Dict = None) -> tuple:
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                self.passed_tests.append(name)
                try:
                    return success, response.json()
                except:
                    return success, response.text
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text[:500]
                })
                return False, {}

        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e)
            })
            return False, {}

    def test_health_endpoints(self):
        """Test basic health endpoints"""
        print("\n" + "="*50)
        print("TESTING HEALTH ENDPOINTS")
        print("="*50)
        
        self.run_test("API Root", "GET", "", 200)
        self.run_test("Health Check", "GET", "health", 200)

    def test_market_overview(self):
        """Test market overview endpoint"""
        print("\n" + "="*50)
        print("TESTING MARKET OVERVIEW")
        print("="*50)
        
        success, data = self.run_test("Market Overview", "GET", "market/overview", 200)
        if success and data:
            # Verify required fields
            required_fields = ['nifty_50', 'sensex', 'nifty_bank', 'india_vix', 'market_breadth', 'fii_dii']
            for field in required_fields:
                if field in data:
                    print(f"   ✓ Found {field}")
                else:
                    print(f"   ⚠️  Missing {field}")

    def test_stocks_endpoints(self):
        """Test stock-related endpoints"""
        print("\n" + "="*50)
        print("TESTING STOCKS ENDPOINTS")
        print("="*50)
        
        # Get all stocks
        success, stocks_data = self.run_test("Get All Stocks", "GET", "stocks", 200, params={"limit": 10})
        
        if success and stocks_data and len(stocks_data) > 0:
            # Test individual stock
            test_symbol = stocks_data[0]['symbol']
            print(f"   Using test symbol: {test_symbol}")
            
            self.run_test(f"Get Stock Details - {test_symbol}", "GET", f"stocks/{test_symbol}", 200)
            self.run_test(f"Get Stock Analysis - {test_symbol}", "GET", f"stocks/{test_symbol}/analysis", 200)
            
            # Test LLM insight
            llm_data = {"analysis_type": "full"}
            self.run_test(f"LLM Insight - {test_symbol}", "POST", f"stocks/{test_symbol}/llm-insight", 200, data=llm_data)
        
        # Test non-existent stock
        self.run_test("Non-existent Stock", "GET", "stocks/INVALID", 404)

    def test_screener_endpoints(self):
        """Test screener functionality"""
        print("\n" + "="*50)
        print("TESTING SCREENER ENDPOINTS")
        print("="*50)
        
        # Get presets
        self.run_test("Screener Presets", "GET", "screener/presets", 200)
        
        # Test screener with filters
        screener_data = {
            "filters": [
                {"metric": "roe", "operator": "gt", "value": 10}
            ],
            "sort_by": "market_cap",
            "sort_order": "desc",
            "limit": 10
        }
        success, results = self.run_test("Run Screener", "POST", "screener", 200, data=screener_data)
        if success and results:
            print(f"   Found {results.get('count', 0)} stocks matching criteria")

    def test_watchlist_endpoints(self):
        """Test watchlist functionality"""
        print("\n" + "="*50)
        print("TESTING WATCHLIST ENDPOINTS")
        print("="*50)
        
        # Get empty watchlist
        self.run_test("Get Watchlist", "GET", "watchlist", 200)
        
        # Add to watchlist
        watchlist_item = {
            "symbol": "RELIANCE",
            "name": "Reliance Industries Limited",
            "added_date": datetime.now().isoformat()
        }
        success, _ = self.run_test("Add to Watchlist", "POST", "watchlist", 200, data=watchlist_item)
        
        if success:
            # Get watchlist again
            self.run_test("Get Watchlist After Add", "GET", "watchlist", 200)
            
            # Update watchlist item
            update_data = {"target_price": 2500, "notes": "Test note"}
            self.run_test("Update Watchlist Item", "PUT", "watchlist/RELIANCE", 200, data=update_data)
            
            # Remove from watchlist
            self.run_test("Remove from Watchlist", "DELETE", "watchlist/RELIANCE", 200)

    def test_portfolio_endpoints(self):
        """Test portfolio functionality"""
        print("\n" + "="*50)
        print("TESTING PORTFOLIO ENDPOINTS")
        print("="*50)
        
        # Get empty portfolio
        self.run_test("Get Portfolio", "GET", "portfolio", 200)
        
        # Add holding
        holding_data = {
            "symbol": "TCS",
            "name": "Tata Consultancy Services",
            "quantity": 10,
            "avg_buy_price": 3500.0,
            "buy_date": "2024-01-01"
        }
        success, _ = self.run_test("Add Portfolio Holding", "POST", "portfolio", 200, data=holding_data)
        
        if success:
            # Get portfolio after add
            self.run_test("Get Portfolio After Add", "GET", "portfolio", 200)
            
            # Update holding
            update_data = {"quantity": 15}
            self.run_test("Update Portfolio Holding", "PUT", "portfolio/TCS", 200, data=update_data)
            
            # Remove holding
            self.run_test("Remove Portfolio Holding", "DELETE", "portfolio/TCS", 200)

    def test_news_endpoints(self):
        """Test news functionality"""
        print("\n" + "="*50)
        print("TESTING NEWS ENDPOINTS")
        print("="*50)
        
        # Get news
        success, news_data = self.run_test("Get News", "GET", "news", 200, params={"limit": 5})
        if success and news_data:
            print(f"   Found {len(news_data)} news items")
        
        # Get news summary
        self.run_test("Get News Summary", "GET", "news/summary", 200)
        
        # Filter by sentiment
        self.run_test("Filter News by Sentiment", "GET", "news", 200, params={"sentiment": "POSITIVE", "limit": 3})

    def test_reports_endpoints(self):
        """Test reports functionality"""
        print("\n" + "="*50)
        print("TESTING REPORTS ENDPOINTS")
        print("="*50)
        
        # Single stock report
        report_data = {
            "report_type": "single_stock",
            "symbols": ["RELIANCE"]
        }
        self.run_test("Single Stock Report", "POST", "reports/generate", 200, data=report_data)
        
        # Comparison report
        comparison_data = {
            "report_type": "comparison",
            "symbols": ["RELIANCE", "TCS"]
        }
        self.run_test("Comparison Report", "POST", "reports/generate", 200, data=comparison_data)
        
        # Portfolio health report
        portfolio_report_data = {
            "report_type": "portfolio_health",
            "symbols": []
        }
        self.run_test("Portfolio Health Report", "POST", "reports/generate", 200, data=portfolio_report_data)

    def test_search_endpoints(self):
        """Test search functionality"""
        print("\n" + "="*50)
        print("TESTING SEARCH ENDPOINTS")
        print("="*50)
        
        # Search stocks
        success, results = self.run_test("Search Stocks", "GET", "search", 200, params={"q": "REL"})
        if success and results:
            print(f"   Found {len(results)} search results")
        
        # Get sectors
        success, sectors = self.run_test("Get Sectors", "GET", "sectors", 200)
        if success and sectors:
            print(f"   Found {len(sectors)} sectors")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Stock Analysis Platform API Tests")
        print(f"Base URL: {self.base_url}")
        
        try:
            self.test_health_endpoints()
            self.test_market_overview()
            self.test_stocks_endpoints()
            self.test_screener_endpoints()
            self.test_watchlist_endpoints()
            self.test_portfolio_endpoints()
            self.test_news_endpoints()
            self.test_reports_endpoints()
            self.test_search_endpoints()
            
        except KeyboardInterrupt:
            print("\n⚠️  Tests interrupted by user")
        except Exception as e:
            print(f"\n💥 Unexpected error: {str(e)}")
        
        # Print final results
        self.print_results()
        
        return 0 if self.tests_passed == self.tests_run else 1

    def print_results(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        print(f"📊 Total Tests: {self.tests_run}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {len(self.failed_tests)}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for i, test in enumerate(self.failed_tests, 1):
                print(f"   {i}. {test.get('test', 'Unknown')}")
                if 'error' in test:
                    print(f"      Error: {test['error']}")
                else:
                    print(f"      Expected: {test.get('expected')}, Got: {test.get('actual')}")
        
        if self.passed_tests:
            print(f"\n✅ PASSED TESTS:")
            for i, test in enumerate(self.passed_tests, 1):
                print(f"   {i}. {test}")

def main():
    tester = StockAnalysisPlatformTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())