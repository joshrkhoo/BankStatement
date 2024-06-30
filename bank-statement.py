#%%
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

#%%
# Load the data
data = pd.read_csv("bank_statements/Youth&DebitBankStatementFY2023-24.csv")

#%%
# Display the first 5 rows of the data
print(data.head())

# Create a new column called 'Amount' which is the difference between 'Credit Amount' and 'Debit Amount'
data['Amount'] = data['Credit Amount'].fillna(0) - data['Debit Amount'].fillna(0)

#%%
total_original = data['Amount'].sum()
print(f'Total in original data: {total_original}')

#%%
data['Category'] = ''

#%%
food = ['uber eats', 'menulog', 'mcdonalds', 'kfc', 'dominos', 'pizza hut', 'subway', 'nandos', 'red rooster', 'hungry jacks', 'oporto', 'guzman y gomez', 'famished wolf', 'thefamishedwolf', 'hsp', 'yomg', 'schnitz', 'grilld', 'poked', 'roti bar', 'grafalis', "mcdonald's", 'lanzhou', 'sushi', 'dodee']

income = ['nab pay']

tech = ['apple', 'google', 'microsoft', 'amazon', 'samsung', 'sony', 'dell', 'hp', 'lenovo']

offering = ['action love', 'iheart', 'offering']

subscriptions = ['netflix', 'spotify', 'disney', 'amazon prime', 'youtube premium', 'apple music', 'google play music', 'hulu', 'hbo', 'stan', 'kayo', 'twitch', 'patreon', 'chatgpt']

beem_it = ['beem it', 'beem']


basketball = ['basketball']

hair = ['romeo', 'hair']

parking = ['parking', 'wilson', 'cellopark']

wise = ['wise', 'transferwise']



#%%
def categorise_transaction(description):
    description = description.lower()
    if any(word in description for word in food):
        return 'Food'
    elif any(word in description for word in income):
        return 'Income'
    elif any(word in description for word in tech):
        return 'Tech'
    elif any(word in description for word in offering):
        return 'Offering'
    elif any(word in description for word in subscriptions):
        return 'Subscriptions'
    elif any(word in description for word in beem_it):
        return 'Beem It'
    elif any(word in description for word in basketball):
        return 'Basketball'
    elif any(word in description for word in hair):
            return 'Hair'
    elif any(word in description for word in parking):
        return 'Parking Fee'
    elif description:
        doc = nlp(description)  # Process the description with SpaCy
        for ent in doc.ents:
            if ent.label_ == "PERSON" or ent.label_ == "ORG":  # Check for person or organization names
                return ent.text.title()  # Return the recognized name
    else:
        return 'Other'


    

#%%
data['Category'] = data['Narrative'].apply(categorise_transaction)

#%%
# Check csv total vs sum of categories
total_categorized = data['Amount'].sum()
print(f'Total in categorized data: {total_categorized}')

try:
    assert total_original == total_categorized
    print('Totals match')
except AssertionError:
    print('Totals do not match')


#%%
# Remove None values from categories
categories = [cat for cat in data['Category'].unique() if cat is not None]
categories = sorted(categories)


category_columns = {category: [] for category in categories}

for category in categories:
    category_data = data[data['Category'] == category][['Date', 'Narrative', 'Amount']]
    category_data = category_data.sort_values(by='Amount', ascending=False)
    category_columns[category] = category_data.values.tolist()


#%%
# Find the maximum length of lists in category_columns
max_len = max(len(values) for values in category_columns.values())

# Pad each list in category_columns to ensure they are all the same length
for category in categories:
    column_data = category_columns[category]
    category_columns[category] = column_data + ['NA'] * (max_len - len(column_data))

# Create a new DataFrame to hold the formatted data
formatted_data = pd.DataFrame({category: category_columns[category] for category in categories})

# Save the formatted data to a new CSV file
formatted_data.to_csv("organised_bank_statements/Youth&DebitBankStatementFY2023-24_formatted.csv", index=False)

# Print the first few rows to verify
print(formatted_data.head())

    