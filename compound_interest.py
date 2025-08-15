# Given data
principal = 3000  # Initial deposit in USD
rate = 5 / 100  # Interest rate (5% converted to decimal)
years = 33  # Tenor in years
compounds_per_year = 1  # Compounded yearly

# Compound Interest Formula: A = P (1 + r/n)^(nt)
final_amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
print(final_amount)
