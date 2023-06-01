import duckdb

country_code = {'UK':'GB'}
with duckdb.connect() as conn:
    final = conn.execute(f"""  
            SELECT "Transaction ID", 
                 '{country_code["UK"]}'||"Check Digits"||"SWIFT code"|| REPLACE("Sort Code",'-','') || "Account Number" as "IBAN"
            FROM read_csv_auto('C:/Data/PreppinData/Transactions.csv', header=True) as x
            JOIN read_csv_auto('C:/Data/PreppinData/Swift Codes.csv', header=True) as y
            ON x."Bank"= y."Bank"
            """).df()
