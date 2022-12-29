from typing import Dict, Any, List, Tuple
from iorp import IORP, Asset, Position


class InsuranceCompany:
    def __init__(self, name: str, own_funds: float, total_assets: float, total_liabilities: float,
                 num_shares_outstanding: int, reinsurance_capacity: float, market_risk_factor: float, operational_risk_factor: float,
                 low_market_risk_factor: float = 0.8, high_market_risk_factor: float = 2.0,
                 low_operational_risk_factor: float = 0.9, high_operational_risk_factor: float = 2.5):
        self.name = name
        self.own_funds = own_funds
        self.total_assets = total_assets
        self.market_risk_factor = market_risk_factor
        self.operational_risk_factor = operational_risk_factor
        self.total_liabilities = total_liabilities
        self.num_shares_outstanding = num_shares_outstanding
        self.reinsurance_capacity = reinsurance_capacity
        self.low_market_risk_factor = low_market_risk_factor
        self.high_market_risk_factor = high_market_risk_factor
        self.low_operational_risk_factor = low_operational_risk_factor
        self.high_operational_risk_factor = high_operational_risk_factor

    # Calculate the MCR and SCR of an insurance company under different scenarios
    def calculate_solvency_metrics(self, total_assets: int, total_liabilities: int, own_funds: int,
                      solvency_capital_requirement_factor: float,
                      market_risk_factor: float, credit_risk_factor: float, operational_risk_factor: float) -> Tuple[
        float, float]:
        # Calculate the MCR as the sum of the total liabilities and the own funds, multiplied by the solvency capital
        # requirement factor
        mcr = (total_assets + total_liabilities + own_funds) * solvency_capital_requirement_factor

        # Calculate the SCR as the MCR, multiplied by the market risk factor and the operational risk factor
        scr = mcr * market_risk_factor * operational_risk_factor * credit_risk_factor

        return mcr, scr

    def calculate_scr_under_stress(self, total_assets: int, total_liabilities: int, own_funds: int,
                                   stress_test_scenarios: Dict[str, int]) -> Dict[str, float]:
        # Initialize a dictionary to store the SCR factor under each stress test scenario
        scr_factors = {}

        # Iterate over the stress test scenarios
        for scenario, capital_requirement in stress_test_scenarios.items():
            # Calculate the SCR factor as the capital requirement divided by the sum of the total assets and total liabilities
            scr_factor = capital_requirement / (total_assets + total_liabilities)

            # Add the SCR factor for this scenario to the dictionary
            scr_factors[scenario] = scr_factor
            return scr_factors

    def calculate_scr(self) -> float:
        """Calculate the solvency capital requirement (SCR) of the insurance company."""
        return self.own_funds * self.market_risk_factor * self.operational_risk_factor

    def calculate_mcr(self) -> float:
        """Calculate the minimum capital requirement (MCR) of the insurance company."""
        return self.calculate_scr() / 0.4

    def stress_test_scr(self) -> Dict[str, float]:
        """Perform stress tests on the SCR of the insurance company under different market and operational risk scenarios."""
        low_market_risk_scr = self.own_funds * self.low_market_risk_factor * self.operational_risk_factor
        high_market_risk_scr = self.own_funds * self.high_market_risk_factor * self.operational_risk_factor
        low_operational_risk_scr = self.own_funds * self.market_risk_factor * self.low_operational_risk_factor
        high_operational_risk_scr = self.own_funds * self.market_risk_factor * self.high_operational_risk_factor
        return {
            "low_market_risk_scr": low_market_risk_scr,
            "high_market_risk_scr": high_market_risk_scr,
            "low_operational_risk_scr": low_operational_risk_scr,
            "high_operational_risk_scr": high_operational_risk_scr
        }

    def update_reinsurance_terms(self, iorp: IORP, reinsurance_amount: float):
        """Update the reinsurance terms for an IORP.

        Args:
            iorp: The IORP for which the reinsurance terms will be updated.
            reinsurance_amount: The reinsurance amount to be provided to the IORP.
        """
        iorp.reinsurance_amount = reinsurance_amount
        iorp.reinsurance_terms_updated = True
        print(f"Reinsurance terms updated for IORP {iorp.name} with reinsurance amount {reinsurance_amount}.")

    def implement_risk_mitigation(self, strategy: str) -> None:
        """
        Implements a risk mitigation strategy to reduce the potential impact of market volatility on the IORP's investments.
        :param strategy: The risk mitigation strategy to implement.
        """
        if strategy == "stop_loss":
            # Implement a stop loss strategy to limit the potential loss on an investment
            for position in self.positions:
                if position.asset.price < position.stop_loss_price:
                    self.sell_position(position.asset, position.num_shares)
                    print(
                        f"Stop loss triggered for {position.asset.ticker} at price {position.stop_loss_price}. {position.num_shares} shares sold.")
        elif strategy == "hedging":
            # Implement a hedging strategy to offset potential losses on an investment with gains from another investment
            for position in self.positions:
                if position.asset.type == "stock":
                    hedge_asset = Asset("TLT", position.asset.price * -1)
                    self.add_position(hedge_asset, position.num_shares)
                    print(f"Hedge added for {position.asset.ticker} with {hedge_asset.ticker}.")
        else:
            print(f"Invalid risk mitigation strategy: {strategy}")


if __name__ == "__main__":

    insurance_company = InsuranceCompany("Acme Insurance", 100000000, 500000000, 400000000, 100000, 200000000, 1.6, 1.2)

    # Calculate the solvency capital requirement (SCR) of the insurance company
    scr = insurance_company.calculate_scr()
    print(f"SCR of {insurance_company.name}: {scr}")

    # Calculate the minimum capital requirement (MCR) of the insurance company
    mcr = insurance_company.calculate_mcr()
    print(f"MCR of {insurance_company.name}: {mcr}")

    # Perform a stress test on the SCR of the insurance company
    scr_stress_test = insurance_company.stress_test_scr()
    print(f"SCR stress test results for {insurance_company.name}: {scr_stress_test}")

    stocks = [Asset("AAPL", 200.00), Asset("GOOG", 250.00), Asset("MSFT", 150.00)]

    # Update the reinsurance terms between the insurance company and an IORP
    iorp = IORP(name="ABC IORP", assets=stocks, solvency_ratio=0.8, asset_diversification=0.7, industry_risk=0.9, total_assets=10000000, total_liabilities=5000000, num_employees=1000, geographical_location="Europe", industry_sector="Finance", hedge_ratio=0.1)

    for stock in stocks:
        # Create a Position object for the stock with a quantity of 50
        position = Position(stock, 50)
        # Add the Position object to the positions attribute of the IORP object
        iorp.positions.append(position)

    insurance_company.update_reinsurance_terms(iorp, 25000000)

    ### SOLVENCY STATISITCS ###

    # Example values for total assets, total liabilities, own funds, solvency capital requirement factor, market risk
    # factor, and operational risk factor
    total_assets = 100000000
    total_liabilities = 50000000
    own_funds = 20000000
    solvency_capital_requirement_factor = 0.8
    market_risk_factor = 1.2
    credit_risk_factor = 1.1
    operational_risk_factor = 1.1

    # Calculate the MCR and SCR under the base scenario
    mcr, scr = insurance_company.calculate_solvency_metrics(total_assets, total_liabilities, own_funds, solvency_capital_requirement_factor,
                             market_risk_factor, credit_risk_factor, operational_risk_factor)

    # Print the MCR and SCR under the base scenario
    print(f"Under the base scenario, the MCR is {mcr:.2f} and the SCR is {scr:.2f}.")

    # Calculate the MCR and SCR under a high market risk scenario
    market_risk_factor = 1.5
    mcr, scr = insurance_company.calculate_solvency_metrics(total_assets, total_liabilities, own_funds, solvency_capital_requirement_factor,
                             market_risk_factor, credit_risk_factor, operational_risk_factor)

    # Print the MCR and SCR under the high market risk scenario
    print(f"Under the high market risk scenario, the MCR is {mcr:.2f} and the SCR is {scr:.2f}.")

    # Calculate the MCR and SCR under a low operational risk scenario
    operational_risk_factor = 0.9
    mcr, scr = insurance_company.calculate_solvency_metrics(total_assets, total_liabilities, own_funds, solvency_capital_requirement_factor,
                             market_risk_factor, credit_risk_factor, operational_risk_factor)

    # Print the MCR and SCR under the low operational risk scenario
    print(f"Under the low operational risk scenario, the MCR is {mcr:.2f} and the SCR is {scr:.2f}")

    # Example values for total assets, total liabilities, own funds, and capital requirements for each stress test scenario
    total_assets = 100000000
    total_liabilities = 50000000
    own_funds = 20000000
    stress_test_scenarios = {
      "severe recession": 10000000,
      "major natural disaster": 3000000,
      "significant increase in interest rates": 5000000
    }

    # Calculate the SCR factor under each stress test scenario
    scr_factors = insurance_company.calculate_scr_under_stress(total_assets, total_liabilities, own_funds, stress_test_scenarios)

    # Print the SCR factor under each stress test scenario
    for scenario, scr_factor in scr_factors.items():
        print(f"SCR factor under {scenario}: {scr_factor:.2%}")

