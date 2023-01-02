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

The results of an example insurance company simulation are as follows: 

*
- SCR of Acme Insurance: 192000000.0
- MCR of Acme Insurance: 480000000.0
- SCR stress test results for Acme Insurance: {'low_market_risk_scr': 96000000.0, 'high_market_risk_scr': 240000000.0, 'low_operational_risk_scr': 144000000.0, 'high_operational_risk_scr': 400000000.0}
- Reinsurance terms updated for IORP ABC IORP with reinsurance amount 25000000.
- Under the base scenario, the MCR is 136000000.00 and the SCR is 197472000.00.
- Under the high market risk scenario, the MCR is 136000000.00 and the SCR is 246840000.00.
- Under the low operational risk scenario, the MCR is 136000000.00 and the SCR is 201960000.00
- SCR factor under severe recession: 6.67%*

The results of an example IORP simulation are as follows: 

*
- The market value of the position is 2500.00
- The NAV of the IORP is 350.00
- Market value is above the stop-loss threshold. No action needed.
- Selling 200 worth of stocks to offset positive delta*


The results of an example interactions between insurer and IORP & SME are as follows:

*### SME INTERACTIONS ###
The risk profile of the SME Acme Co is 0.30000000000000004
The premium for the SME Acme Co is 20280.0
### SME INTERACTIONS ###
The annuity Premium 93887.49282676155
Insurance company is providing customized reinsurance coverage for 7875.0 dollars to IORP ABC IORP.*
