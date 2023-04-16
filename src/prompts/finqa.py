# 5-shot
code_prompt = '''
Table:
( in millions ) | dec 282013 | dec 292012
available-for-sale investments | $ 18086 | $ 14001
cash | 854 | 593
equity method investments | 1038 | 992
loans receivable | 1072 | 979
non-marketable cost method investments | 1270 | 1202
reverse repurchase agreements | 800 | 2850
trading assets | 8441 | 5685
total cash and investments | $ 31561 | $ 26302
Question: What percentage of total cash and investments as of dec . 29 2012 was comprised of available-for-sale investments?

# solution in Python:


def solution():
    """Table:
    ( in millions ) | dec 282013 | dec 292012
    available-for-sale investments | $ 18086 | $ 14001
    cash | 854 | 593
    equity method investments | 1038 | 992
    loans receivable | 1072 | 979
    non-marketable cost method investments | 1270 | 1202
    reverse repurchase agreements | 800 | 2850
    trading assets | 8441 | 5685
    total cash and investments | $ 31561 | $ 26302
    Question: What percentage of total cash and investments as of dec . 29 2012 was comprised of available-for-sale investments?
    """
    available_for_sale_investments_dec_29_2012 = 14001
    total_cash_and_investments_dec_29_2012 = 26302
    percent_available_for_sale_investments_dec_29_2012 = available_for_sale_investments_dec_29_2012 / total_cash_and_investments_dec_29_2012
    result = percent_available_for_sale_investments_dec_29_2012
    return result





Table: total consid- eration paid in cash to the robert mondavi shareholders was $ 1030.7 million . total consideration paid in cash and class a common stock to the hardy shareholders was $ 1137.4 million .
Current assets | $494,788
Property, plant and equipment | 452,902
Other assets | 178,823
Trademarks | 186,000
Goodwill | 590,459
Total assets acquired | 1,902,972
Current liabilities | 309,051
Long-term liabilities | 552,060
Total liabilities acquired | 861,111
Net assets acquired | $1,041,861
Question: Of the two acquisitions , was the purchase price of the hardy acquisition greater than the mondavi acquisition?
Choose from the the options: ['yes', 'no']

# solution in Python:


def solution():
    """Table: total consid- eration paid in cash to the robert mondavi shareholders was $ 1030.7 million . total consideration paid in cash and class a common stock to the hardy shareholders was $ 1137.4 million .
    Current assets | $494,788
    Property, plant and equipment | 452,902
    Other assets | 178,823
    Trademarks | 186,000
    Goodwill | 590,459
    Total assets acquired | 1,902,972
    Current liabilities | 309,051
    Long-term liabilities | 552,060
    Total liabilities acquired | 861,111
    Net assets acquired | $1,041,861
    Question: Of the two acquisitions , was the purchase price of the hardy acquisition greater than the mondavi acquisition?
    Choose from the the options: ['yes', 'no']
    """
    hardy_price = 1137.4
    mondavi_price = 1030.7
    if hardy_price > mondavi_price:
        result = 'yes'
    else:
        result = 'no'
    return result





Table: the chart shows that the firm posted market risk 2013related gains on 248 out of 261 days in this period , with 12 days exceeding $ 210 million .
december 31 ( in millions ) | 1 basis point increase in jpmorgan chase 2019s credit spread
2010 | $ 35
2009 | $ 39
Question: On what percent of trading days were there market gains above $ 210 million?

# solution in Python:


def solution():
    """Table: the chart shows that the firm posted market risk 2013related gains on 248 out of 261 days in this period , with 12 days exceeding $ 210 million .
    december 31 ( in millions ) | 1 basis point increase in jpmorgan chase 2019s credit spread
    2010 | $ 35
    2009 | $ 39
    Question: On what percent of trading days were there market gains above $ 210 million?
    """
    days_with_market_gains_above_210_million = 12
    total_trading_days = 261
    percent_days_with_market_gains_above_210_million = days_with_market_gains_above_210_million / total_trading_days
    result = percent_days_with_market_gains_above_210_million
    return result





Table: american tower corporation and subsidiaries notes to consolidated financial statements ( 3 ) consists of customer-related intangibles of approximately $ 75.0 million and network location intangibles of approximately $ 72.7 million . the customer-related intangibles and network location intangibles are being amortized on a straight-line basis over periods of up to 20 years .
 | preliminary purchase price allocation
current assets | $ 8763
non-current assets | 2332
property and equipment | 26711
intangible assets ( 1 ) | 21079
other non-current liabilities | -1349 ( 1349 )
fair value of net assets acquired | $ 57536
goodwill ( 2 ) | 5998
Question: for acquired customer-related and network location intangibles , what is the expected annual amortization expenses , in millions?

# solution in Python:


def solution():
    """Table: american tower corporation and subsidiaries notes to consolidated financial statements ( 3 ) consists of customer-related intangibles of approximately $ 75.0 million and network location intangibles of approximately $ 72.7 million . the customer-related intangibles and network location intangibles are being amortized on a straight-line basis over periods of up to 20 years .
     | preliminary purchase price allocation
    current assets | $ 8763
    non-current assets | 2332
    property and equipment | 26711
    intangible assets ( 1 ) | 21079
    other non-current liabilities | -1349 ( 1349 )
    fair value of net assets acquired | $ 57536
    goodwill ( 2 ) | 5998
    Question: for acquired customer-related and network location intangibles , what is the expected annual amortization expenses , in millions?
    """
    customer_related_intangibles = 75
    network_location_intangibles = 72.7
    straight_line_basis = 20
    amortization_expenses = ( customer_related_intangibles + network_location_intangibles ) / straight_line_basis
    result = amortization_expenses
    return result





Table: the aggregate commitment under the liquidity asset purchase agreements was approximately $ 23.59 billion and $ 28.37 billion at december 31 , 2008 and 2007 , respectively .
( dollars in billions ) | 2008 amount | 2008 percent of total conduit assets | 2008 amount | percent of total conduit assets
united states | $ 11.09 | 46% ( 46 % ) | $ 12.14 | 42% ( 42 % )
australia | 4.30 | 17 | 6.10 | 21
great britain | 1.97 | 8 | 2.93 | 10
spain | 1.71 | 7 | 1.90 | 7
italy | 1.66 | 7 | 1.86 | 7
portugal | 0.62 | 3 | 0.70 | 2
germany | 0.57 | 3 | 0.70 | 2
netherlands | 0.40 | 2 | 0.55 | 2
belgium | 0.29 | 1 | 0.31 | 1
greece | 0.27 | 1 | 0.31 | 1
other | 1.01 | 5 | 1.26 | 5
total conduit assets | $ 23.89 | 100% ( 100 % ) | $ 28.76 | 100% ( 100 % )
Question: what is percentage change in total conduit asset from 2007 to 2008?

# solution in Python:


def solution():
    """Table: the aggregate commitment under the liquidity asset purchase agreements was approximately $ 23.59 billion and $ 28.37 billion at december 31 , 2008 and 2007 , respectively .
    ( dollars in billions ) | 2008 amount | 2008 percent of total conduit assets | 2008 amount | percent of total conduit assets
    united states | $ 11.09 | 46% ( 46 % ) | $ 12.14 | 42% ( 42 % )
    australia | 4.30 | 17 | 6.10 | 21
    great britain | 1.97 | 8 | 2.93 | 10
    spain | 1.71 | 7 | 1.90 | 7
    italy | 1.66 | 7 | 1.86 | 7
    portugal | 0.62 | 3 | 0.70 | 2
    germany | 0.57 | 3 | 0.70 | 2
    netherlands | 0.40 | 2 | 0.55 | 2
    belgium | 0.29 | 1 | 0.31 | 1
    greece | 0.27 | 1 | 0.31 | 1
    other | 1.01 | 5 | 1.26 | 5
    total conduit assets | $ 23.89 | 100% ( 100 % ) | $ 28.76 | 100% ( 100 % )
    Question: what is percentage change in total conduit asset from 2007 to 2008?
    """
    total_conduit_assets_2007 = 28.76
    total_conduit_assets_2008 = 23.89
    net_change_in_total_conduit_assets = total_conduit_assets_2008 - total_conduit_assets_2007
    percent_change_in_total_conduit_assets = net_change_in_total_conduit_assets / total_conduit_assets_2007
    result = percent_change_in_total_conduit_assets
    return result
'''

# 3-shot
evaluate_prompt = '''
Table:
 | 2012 | 2011 | 2010
Net sales | $7,457 | $7,463 | $6,930
Operating profit | 1,256 | 1,069 | 973
Operating margins | 16.8% | 14.3% | 14.0%
Backlog at year-end | 14,700 | 14,400 | 12,800
Question: What is the growth rate in net sales for mfc in 2012?

# solution in Python:


def solution():
    """Table:
     | 2012 | 2011 | 2010
    Net sales | $7,457 | $7,463 | $6,930
    Operating profit | 1,256 | 1,069 | 973
    Operating margins | 16.8% | 14.3% | 14.0%
    Backlog at year-end | 14,700 | 14,400 | 12,800
    Question: What is the growth rate in net sales for mfc in 2012?
    """
    net_sales_2011 = 7463
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    net_sales_2010 = 6930
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    net_change_in_net_sales = net_sales_2011 - net_sales_2010
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should calculate the growth rate in 2012, which is net_sales_2012 - net_sales_2011
    growth_rate_in_net_sales = net_change_in_net_sales / net_sales_2010
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should calculate the growth rate in 2012, which is net_change_in_net_sales / net_sales_2011
    result = growth_rate_in_net_sales
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of growth_rate_in_net_sales is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table:
Millions | OperatingLeases | CapitalLeases
2016 | $491 | $217
2017 | 446 | 220
2018 | 371 | 198
2019 | 339 | 184
2020 | 282 | 193
Later years | 1,501 | 575
Total minimum lease payments | $3,430 | $1,587
Amount representing interest | N/A | (319)
Present value of minimum lease payments | N/A | $1,268
Question: What percentage of total minimum lease payments are capital leases?

# solution in Python:


def solution():
    """Table:
    Millions | OperatingLeases | CapitalLeases
    2016 | $491 | $217
    2017 | 446 | 220
    2018 | 371 | 198
    2019 | 339 | 184
    2020 | 282 | 193
    Later years | 1,501 | 575
    Total minimum lease payments | $3,430 | $1,587
    Amount representing interest | N/A | (319)
    Present value of minimum lease payments | N/A | $1,268
    Question: What percentage of total minimum lease payments are capital leases?
    """
    total_minimum_lease_payments = 3430
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should be the sum of Operating and Capital Leases, which is 3430 + 1587
    capital_lease_payments = 1268
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because capital_lease_payments should be 1587
    percent_capital_lease_payments = capital_lease_payments / total_minimum_lease_payments
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of capital_lease_payments and total_minimum_lease_payments are incorrect
    result = percent_capital_lease_payments
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of percent_capital_lease_payments is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect





Table: long-term debt at december 31 , 2009 and december 31 , 2008 includes $ 19345 million and $ 24060 million , respectively , of junior subordinated debt .
In millions of dollars | 2010 | 2011 | 2012 | 2013 | 2014 | Thereafter
Citigroup parent company | $18,030 | $20,435 | $29,706 | $17,775 | $18,916 | $92,942
Other Citigroup subsidiaries | 18,710 | 29,316 | 17,214 | 5,177 | 12,202 | 14,675
Citigroup Global Markets Holdings Inc. | 1,315 | 1,030 | 1,686 | 388 | 522 | 8,481
Citigroup Funding Inc. | 9,107 | 8,875 | 20,738 | 4,792 | 3,255 | 8,732
Total | $47,162 | $59,656 | $69,344 | $28,132 | $34,895 | $124,830
Question: What was the percent of the long-term debt junior subordinated debt and at december 31 , 2009 compared to december 31 , 2008?

# solution in Python:


def solution():
    """Table: long-term debt at december 31 , 2009 and december 31 , 2008 includes $ 19345 million and $ 24060 million , respectively , of junior subordinated debt .
    In millions of dollars | 2010 | 2011 | 2012 | 2013 | 2014 | Thereafter
    Citigroup parent company | $18,030 | $20,435 | $29,706 | $17,775 | $18,916 | $92,942
    Other Citigroup subsidiaries | 18,710 | 29,316 | 17,214 | 5,177 | 12,202 | 14,675
    Citigroup Global Markets Holdings Inc. | 1,315 | 1,030 | 1,686 | 388 | 522 | 8,481
    Citigroup Funding Inc. | 9,107 | 8,875 | 20,738 | 4,792 | 3,255 | 8,732
    Total | $47,162 | $59,656 | $69,344 | $28,132 | $34,895 | $124,830
    Question: What was the percent of the long-term debt junior subordinated debt and at december 31 , 2009 compared to december 31 , 2008?
    """
    junior_subordinated_debt_2009 = 19345
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    junior_subordinated_debt_2008 = 24060
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    net_change_in_junior_subordinated_debt = junior_subordinated_debt_2008 - junior_subordinated_debt_2009
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should be 2009 compared to 2008
    percent_change_in_junior_subordinated_debt = net_change_in_junior_subordinated_debt / junior_subordinated_debt_2008
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the sign of net_change_in_junior_subordinated_debt is incorrect and this is irrelevant to the question
    result = percent_change_in_junior_subordinated_debt
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because 2009 compared to 2008 should be junior_subordinated_debt_2009 / junior_subordinated_debt_2008
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
'''

discarded = [
'''
Table:
 | 2011 | 2012 | 2013 | 2014 | 2015 | Thereafter | Total
Property Mortgages | $246,615 | $143,646 | $656,863 | $208,025 | $260,433 | $1,884,885 | $3,400,467
Revolving Credit Facility | — | 650,000 | — | — | — | — | 650,000
Trust Preferred Securities | — | — | — | — | — | 100,000 | 100,000
Senior Unsecured Notes | 84,823 | 123,171 | — | 98,578 | 657 | 793,316 | 1,100,545
Capital lease | 1,555 | 1,555 | 1,555 | 1,555 | 1,593 | 44,056 | 51,869
Ground leases | 28,929 | 28,179 | 28,179 | 28,179 | 28,179 | 552,421 | 694,066
Estimated interest expense | 265,242 | 245,545 | 221,161 | 197,128 | 177,565 | 355,143 | 1,461,784
Joint venture debt | 207,738 | 61,491 | 41,415 | 339,184 | 96,786 | 857,305 | 1,603,919
Total | $834,902 | $1,253,587 | $949,173 | $872,649 | $565,213 | $4,587,126 | $9,062,650
Question: What was the total liability in millions for capital lease and ground leases?

# solution in Python:


def solution():
    """Table:
     | 2011 | 2012 | 2013 | 2014 | 2015 | Thereafter | Total
    Property Mortgages | $246,615 | $143,646 | $656,863 | $208,025 | $260,433 | $1,884,885 | $3,400,467
    Revolving Credit Facility | — | 650,000 | — | — | — | — | 650,000
    Trust Preferred Securities | — | — | — | — | — | 100,000 | 100,000
    Senior Unsecured Notes | 84,823 | 123,171 | — | 98,578 | 657 | 793,316 | 1,100,545
    Capital lease | 1,555 | 1,555 | 1,555 | 1,555 | 1,593 | 44,056 | 51,869
    Ground leases | 28,929 | 28,179 | 28,179 | 28,179 | 28,179 | 552,421 | 694,066
    Estimated interest expense | 265,242 | 245,545 | 221,161 | 197,128 | 177,565 | 355,143 | 1,461,784
    Joint venture debt | 207,738 | 61,491 | 41,415 | 339,184 | 96,786 | 857,305 | 1,603,919
    Total | $834,902 | $1,253,587 | $949,173 | $872,649 | $565,213 | $4,587,126 | $9,062,650
    Question: What was the total liability in millions for capital lease and ground leases?
    """
    capital_lease = 51.869
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because capital_lease should be 51869
    ground_leases = 694.066
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because ground_leases should be 694066
    total_liability = capital_lease + ground_leases
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the values of capital_lease and ground_leases are incorrect
    result = total_liability
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of total_liability is incorrect
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
''',
'''
Table: printing papers net sales for 2014 decreased 8% ( 8 % ) to $ 5.7 billion compared with $ 6.2 billion in 2013 and 8% ( 8 % ) compared with $ 6.2 billion in 2012 .
In millions | 2014 | 2013 | 2012
Sales | $5,720 | $6,205 | $6,230
Operating Profit (Loss) | (16) | 271 | 599
Question: In 2014 what was the decrease in printing papers net sales in millions?

# solution in Python:


def solution():
    """Table: printing papers net sales for 2014 decreased 8% ( 8 % ) to $ 5.7 billion compared with $ 6.2 billion in 2013 and 8% ( 8 % ) compared with $ 6.2 billion in 2012 .
    In millions | 2014 | 2013 | 2012
    Sales | $5,720 | $6,205 | $6,230
    Operating Profit (Loss) | (16) | 271 | 599
    Question: In 2014 what was the decrease in printing papers net sales in millions?
    """
    sales_2014 = 5720
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    sales_2013 = 6205
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    decrease_in_sales = sales_2013 - sales_2014
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A)
    result = decrease_in_sales
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (B), because should be in millions and negative as it is decrease
    return result
    # Is the above line of code:
    # (A) Correct
    # (B) Incorrect
    # The above line of code is: (A), but the value of result is incorrect
''',
'''
Table:
toy boat | $5.54
toy guitar | $8.23
set of juggling balls | $5.01
trivia game | $8.18
jigsaw puzzle | $5.30
toy dinosaur | $3.00
Question: Lorenzo has $13.50. Does he have enough to buy a toy guitar and a set of juggling balls?
Choose from the the options: ['yes', 'no']

# solution in Python:


def solution():
    """Table:
    toy boat | $5.54
    toy guitar | $8.23
    set of juggling balls | $5.01
    trivia game | $8.18
    jigsaw puzzle | $5.30
    toy dinosaur | $3.00
    Question: Lorenzo has $13.50. Does he have enough to buy a toy guitar and a set of juggling balls?
    Choose from the the options: ['yes', 'no']
    """
    guitar_price = 8.23
    juggling_balls = 5.01
    total_money = 13.5
    if total_money > juggling_balls + guitar_price:
        result = "yes"
    else:
        result = "no"
    return result
''',
]

choice_prefix = ['# Is the above line of code:', '# (A) Correct', '# (B) Incorrect', '# The above line of code is:']

