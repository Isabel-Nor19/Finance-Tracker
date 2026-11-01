import traceback
from src.validator import validate_csv
from src.auditor import generate_summary
from tabulate import tabulate

def run_dashboard():
    target_file = "mock_statement.csv"
    
    print("=" * 50)
    print(" BUDGETGAZE: PERSONAL FINANCE AUDITOR ")
    print("=" * 50)
    
    try:
        # 1. Validate and clean incoming files
        cleaned_data = validate_csv(target_file)
        
        # 2. Run calculations
        income, spending, category_breakdown = generate_summary(cleaned_data)
        
        # 3. Present high-level totals
        print(f"\n[+] Total Income Registered:  £{income:.2f}")
        print(f"[-] Total Spending Registered: £{spending:.2f}")
        print(f"[=] Net Savings:               £{income - spending:.2f}\n")
        
        # 4. Format and print the detailed breakdown table
        print("SPENDING BREAKDOWN BY CATEGORY:")
        print(tabulate(category_breakdown, headers=['Category', 'Total Spent (£)'], tablefmt='grid'))
        
    except Exception as e:
        print(f"\n[!] System Failure: {e}")

if __name__ == "__main__":
    run_dashboard()
