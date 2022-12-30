from typing import Dict, Any, List, Tuple
from iorp import IORP, Asset, Position
from sme import SME


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

    def calculate_risk_profile_sme(self, sme: SME) -> float:
        credit_rating = sme.get_credit_rating()
        credit_score = sme.get_credit_score()
        financial_statements = sme.get_financial_statements()

        # Calculate risk profile based on credit rating, credit score, and financial statements
        risk_profile = 0.0
        if sme.credit_rating == "A":
            risk_profile -= 0.1
        elif sme.credit_rating == "B":
            risk_profile += 0.1
        elif sme.credit_rating == "C":
            risk_profile += 0.2
        elif sme.credit_rating == "D":
            risk_profile += 0.3

        if sme.credit_score > 800:
            risk_profile -= 0.1
        elif sme.credit_score > 700:
            risk_profile += 0.1
        elif sme.credit_score > 600:
            risk_profile += 0.2
        elif sme.credit_score > 500:
            risk_profile += 0.3

        if "income statement" in financial_statements:
            income_statement = financial_statements["income statement"]["net income"]
            if income_statement > 0:
                risk_profile -= 0.1
            else:
                risk_profile += 0.1

        if "balance sheet" in financial_statements:
            balance_sheet = financial_statements["balance sheet"]["assets"]
            if balance_sheet > 0:
                risk_profile -= 0.1
            else:
                risk_profile += 0.1

        return risk_profile

    def calculate_maximum_coverage(self, sme: SME) -> float:
        # Calculate debt-to-equity ratio
        debt_to_equity_ratio = sme.liabilities / sme.financial_statements["balance sheet"]["equity"]

        # Calculate current ratio
        current_ratio = sme.assets / sme.liabilities
        # Set maximum coverage based on credit rating, industry, and financial ratios
        if sme.credit_rating == "A":
            max_coverage = 1000000
        elif sme.credit_rating == "B":
            max_coverage = 500000
        else:
            max_coverage = 100000
        # Adjust for industry risk
        max_coverage *= (1 + self.calculate_risk_profile_sme(sme))
        # Adjust for financial ratios
        if debt_to_equity_ratio > 1:
            max_coverage *= 0.9
        if current_ratio < 1:
            max_coverage *= 0.9
        return max_coverage

    def calculate_coverage_premium(self, sme: SME) -> float:
        # Calculate risk profile of SME using credit rating, industry, and financial ratios
        # Calculate premium based on maximum coverage, probability of claim, and potential severity of claim
        premium = self.calculate_premium(sme)

        return premium

    def calculate_probability_of_claim(self, sme: SME) -> float:

        debt_to_equity_ratio = sme.liabilities / sme.financial_statements["balance sheet"]["equity"]

        # Calculate current ratio
        current_ratio = sme.assets / sme.liabilities
        probability_of_claim = 0
        credit_rating = sme.credit_rating
        if credit_rating == "A":
            probability_of_claim = 0.01
        elif credit_rating == "B":
            probability_of_claim = 0.03
        else:
            probability_of_claim = 0.05
        # Adjust for industry risk
        probability_of_claim *= (1 + self.calculate_risk_profile_sme(sme))
        # Adjust for financial ratios
        if debt_to_equity_ratio > 1:
            probability_of_claim *= 1.1
        if current_ratio < 1:
            probability_of_claim *= 1.1
        return probability_of_claim

    def calculate_potential_severity_of_claim(self, sme: SME) -> float:
        """Calculates the potential severity of a claim based on the SME's industry and financial statements.

        Args:
            sme: The SME for which the potential severity of a claim is being calculated.

        Returns:
            The potential severity of a claim.
        """
        industry_risk = INDUSTRY_RISK_FACTORS[sme.industry]
        financial_risk = self._calculate_financial_risk(sme)
        return industry_risk * financial_risk

    def _calculate_financial_risk(self, sme: SME) -> float:
        """Calculates the financial risk of the SME based on its financial statements.

        Args:
            sme: The SME for which the financial risk is being calculated.

        Returns:
            The financial risk of the SME.
        """
        debt_to_equity_ratio = sme.liabilities / sme.financial_statements["balance sheet"]["equity"]
        current_ratio = sme.assets / sme.liabilities
        return debt_to_equity_ratio * current_ratio

    def calculate_premium(self, sme: SME) -> float:
        max_coverage = self.calculate_maximum_coverage(sme)
        probability_of_claim = self.calculate_probability_of_claim(sme)
        potential_severity_of_claim = self.calculate_potential_severity_of_claim(sme)
        return max_coverage * probability_of_claim * potential_severity_of_claim

    # The function returns the premium (in dollars) that the insurance company would charge for the annuity
    def calculate_annuity_premium(self, amount: int, term: int, interest_rate: float, inflation_rate: float) -> float:
        # Calculate the present value of the annuity
        present_value = amount / ((1 + interest_rate) ** term - 1)

        # Calculate the future value of the annuity
        future_value = present_value * ((1 + interest_rate) ** term)

        # Calculate the premium
        premium = future_value / ((1 + inflation_rate) ** term)

        return premium

    def provide_customized_reinsurance(self, iorp: IORP, coverage_amount: int, reinsurance_terms: Dict[str, Any]):
        # Determine the reinsurance amount based on the size and financial stability of the IORP
        if iorp.total_assets > 100000 and iorp.calculate_risk_profile() == "low":
            reinsurance_amount = coverage_amount
        elif iorp.total_assets > 100000 and iorp.calculate_risk_profile() == "medium":
            reinsurance_amount = coverage_amount * 0.75
        elif iorp.total_assets > 100000 and iorp.calculate_risk_profile() == "high":
            reinsurance_amount = coverage_amount * 0.50
        elif iorp.total_assets > 100000 and iorp.calculate_risk_profile() == "low":
            reinsurance_amount = coverage_amount * 0.50
        elif iorp.total_assets > 100000 and iorp.calculate_risk_profile() == "medium":
            reinsurance_amount = coverage_amount * 0.25
        else:
            reinsurance_amount = 0

        # Consider the terms and conditions of the reinsurance contract
        if reinsurance_terms["contract_length"] > 5 and reinsurance_terms["exclusions"] == []:
            reinsurance_amount *= 1.1
        elif reinsurance_terms["contract_length"] > 5:
            reinsurance_amount *= 1.05
        elif not reinsurance_terms["exclusions"]:
            reinsurance_amount *= 1.05

        # Print the final reinsurance amount
        print(f"Insurance company is providing customized reinsurance coverage for {reinsurance_amount} dollars to IORP {iorp.name}.")
        return reinsurance_amount


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
    INDUSTRY_RISK_FACTORS = {
        "manufacturing": 1.2,
        "construction": 1.5,
        "retail": 0.9,
        "finance": 1.0,
        "technology": 0.8
    }
    print("### SME INTERACTIONS ###")

    income_statement = {
        "revenue": 1000000,
        "expenses": 500000,
        "net income": 500000
    }

    balance_sheet = {
        "assets": 2000000,
        "liabilities": 1000000,
        "equity": 1000000
    }

    financial_statements = {
        "income statement": income_statement,
        "balance sheet": balance_sheet
    }
    sme = SME("Acme Co", "C", 542, "manufacturing", 2000000, 1000000, financial_statements)

    print(f"The risk profile of the SME {sme.name} is", insurance_company.calculate_risk_profile_sme(sme))
    premium = insurance_company.calculate_premium(sme)
    print(f"The premium for the SME {sme.name} is {premium}")

    print("### IORP INTERACTIONS ###")

    print("The annuity Premium", insurance_company.calculate_annuity_premium(100000, 30, 0.03, 0.02))

    insurance_company.provide_customized_reinsurance(iorp, 10000,
                                                     {"contract_length": 10, "exclusions": ["natural disasters"]})




