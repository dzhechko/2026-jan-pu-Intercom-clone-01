"""Unit tests for TCO calculation logic."""

import pytest


class TestTCOCalculation:
    """Test TCO calculation algorithm (placeholder — implement with actual TCO service)."""

    def test_monthly_to_annual_conversion(self):
        monthly = 100_000  # rubles
        annual = monthly * 12
        assert annual == 1_200_000

    def test_annual_discount_applied(self):
        monthly = 100_000
        annual_discount = 0.15  # 15% off
        discounted_annual = monthly * 12 * (1 - annual_discount)
        assert discounted_annual == 1_020_000

    def test_three_year_discount(self):
        monthly = 100_000
        three_year_discount = 0.30  # 30% off
        three_year_cost = monthly * 36 * (1 - three_year_discount)
        assert three_year_cost == 2_520_000

    def test_compute_cost_calculation(self):
        """Test basic compute cost: count * price_per_vm."""
        vm_count = 50
        price_per_vm = 5_000  # rubles/month
        compute_cost = vm_count * price_per_vm
        assert compute_cost == 250_000

    def test_storage_cost_calculation(self):
        """Test storage cost: size_gb * price_per_gb."""
        size_gb = 500
        price_per_gb = 10  # rubles/month
        storage_cost = size_gb * price_per_gb
        assert storage_cost == 5_000

    def test_total_cost_breakdown(self):
        """Test total is sum of all categories."""
        compute = 250_000
        storage = 50_000
        networking = 10_000
        managed = 30_000
        total = compute + storage + networking + managed
        assert total == 340_000

    def test_cheapest_provider_selection(self):
        """Test provider selection logic."""
        providers = [
            {"name": "Cloud.ru", "monthly_cost": 300_000},
            {"name": "Yandex Cloud", "monthly_cost": 350_000},
            {"name": "VK Cloud", "monthly_cost": 320_000},
        ]
        cheapest = min(providers, key=lambda p: p["monthly_cost"])
        assert cheapest["name"] == "Cloud.ru"

    def test_savings_calculation(self):
        """Test savings percentage calculation."""
        current_cost = 500_000
        cloud_cost = 300_000
        savings_pct = (current_cost - cloud_cost) / current_cost * 100
        assert savings_pct == 40.0
