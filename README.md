# Insurance Company Simulator

An Insurance Company Simulator which creates Insurance Company and IORP classes, calculates risk metrics for them and creates interactions between the two.

The insurance company class is capable of:
- Calculate the MCR and SCR of an insurance company under different scenarios.
- Perform stress tests on the SCR of the insurance company under different market and operational risk scenarios.
- Update the reinsurance terms for an IORP.
- Implements a risk mitigation strategy to reduce the potential impact of market volatility on the IORP's investments.

The IORP class is capable of:
- Calculate the net asset value (NAV) of the IORP.
- Calculate the current market value of the IORP's assets.
- Calculate the risk profile of the IORP based on its solvency ratio, asset diversification, and industry risk.
- Implement a risk mitigation strategy for the IORP such as stop loss and delta hedging.

The interaction class between the two institutions is capable of:
- Determine the reinsurance amount based on the size and financial stability of the IORP.
- Determine IORP risk profile based on different factors.
- Update the contract length based on the interest rate.
- Calculate solvency ratio of IORP as the ratio of the total assets to the technical provisions and act accordingly. 

The results of an example interaction simulation are as follows:

*The premium for the annuity is 93887.49 dollars.
Insurance company is providing customized reinsurance coverage for 262500.0 dollars to IORP ABC Pension Plan.
The reinsurance premium for IORP1 with a medium risk profile and 1000000 dollars of coverage is 100000.0 dollars.
InsCo1 and IORP1 are investing 500000 dollars in bond.
InsCo1 is working with IORP1 to develop and implement risk management strategies to mitigate market risks.
InsCo1 is working with IORP2 to develop and implement risk management strategies to mitigate operational risks.

The IORP does not meet the solvency requirements of IORP II
InsCo1 is partnering with InsCo2 to share risk and potentially reduce the impact of investing in IORP1 with a high risk profile.
InsCo1 is paying a premium of 100000 dollars to InsCo2 for this reinsurance coverage.*
