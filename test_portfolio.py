"""
Automated tests for Stock Portfolio Tracker Pro.
"""

import unittest

from portfolio import (
    STOCK_PRICES,
    calculate_investment,
)


class TestPortfolio(unittest.TestCase):
    """Test portfolio calculation functionality."""

    def test_aapl_investment(self):
        """Test AAPL calculation."""

        result = calculate_investment(
            "AAPL",
            10,
        )

        self.assertEqual(
            result,
            1800.00,
        )

    def test_tsla_investment(self):
        """Test TSLA calculation."""

        result = calculate_investment(
            "TSLA",
            5,
        )

        self.assertEqual(
            result,
            1250.00,
        )

    def test_lowercase_stock_symbol(self):
        """Test lowercase ticker handling."""

        result = calculate_investment(
            "aapl",
            2,
        )

        self.assertEqual(
            result,
            360.00,
        )

    def test_invalid_stock(self):
        """Invalid stock should raise ValueError."""

        with self.assertRaises(ValueError):
            calculate_investment(
                "INVALID",
                10,
            )

    def test_zero_quantity(self):
        """Zero quantity should be rejected."""

        with self.assertRaises(ValueError):
            calculate_investment(
                "AAPL",
                0,
            )

    def test_negative_quantity(self):
        """Negative quantity should be rejected."""

        with self.assertRaises(ValueError):
            calculate_investment(
                "AAPL",
                -5,
            )

    def test_stock_prices_exist(self):
        """Verify required stocks exist."""

        self.assertIn(
            "AAPL",
            STOCK_PRICES,
        )

        self.assertIn(
            "TSLA",
            STOCK_PRICES,
        )

        self.assertIn(
            "GOOGL",
            STOCK_PRICES,
        )

        self.assertIn(
            "MSFT",
            STOCK_PRICES,
        )

        self.assertIn(
            "AMZN",
            STOCK_PRICES,
        )


if __name__ == "__main__":
    unittest.main()