def assign_category(description):
    """Categorises transactions based on text keywords."""
    desc = description.lower()
    
    if "tesco" in desc or "sainsbury" in desc or "uber" in desc:
        return "Food & Dining"
    elif "gym" in desc:
        return "Health & Fitness"
    elif "netflix" in desc or "spotify" in desc:
        return "Entertainment"
    elif "loan" in desc or "salary" in desc:
        return "Income"
    else:
        return "Uncategorised"

def generate_summary(df):
    """Calculates total income, total spending, and spending by category."""
    # Apply our categorization rule to create a new column
    df['Category'] = df['Description'].apply(assign_category)
    
    # Separate income from expenses
    income = df[df['Amount'] > 0]['Amount'].sum()
    spending = df[df['Amount'] < 0]['Amount'].sum()
    
    # Group spending by category (ignoring income)
    expenses_df = df[df['Amount'] < 0]
    category_totals = expenses_df.groupby('Category')['Amount'].sum().reset_index()
    
    # Convert negative spending values to positive for clean visual reporting
    category_totals['Amount'] = category_totals['Amount'].abs()
    
    return income, abs(spending), category_totals
