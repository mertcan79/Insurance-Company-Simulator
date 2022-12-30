from typing import Dict, List, Any


class SME:
    def __init__(self, name: str, credit_rating: str, credit_score: int, industry: str, assets: float, liabilities: float, financial_statements: dict):
        self.name = name
        self.credit_rating = credit_rating
        self.credit_score = credit_score
        self.industry = industry
        self.assets = assets
        self.liabilities = liabilities
        self.financial_statements = financial_statements

    def get_credit_rating(self) -> str:
        return self.credit_rating

    def get_credit_score(self) -> int:
        return self.credit_score

    def get_financial_statements(self) -> Dict[str, int]:
        return self.financial_statements

    def debt_to_equity_ratio(self) -> float:
        return self.liabilities / self.financial_statements["balance sheet"]["equity"]


if __name__ == "__main__":
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

    sme = SME("Acme Co", "A", 642, "manufacturing", 2000000, 1000000, financial_statements)

    print(f"The debt to equity ratio is {sme.debt_to_equity_ratio()}")
