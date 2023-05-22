import duckdb

conn = duckdb.connect()

conn.execute("""
CREATE TEMP TABLE txn_detail AS        
SELECT split_part("Transaction Code",'-',1) Bank, dayname("Transaction Date") "Transaction Date",
     CASE "Online or In-Person" WHEN 2 THEN 'Online' ELSE 'In-Person' END "Online or In-Person",
     "Customer Code", "Value" 
     FROM read_csv_auto('C:/Data/PreppinData/PD 2023 Wk 1 Input.csv', header=True)
""")

df1= conn.execute("""
SELECT Bank, SUM(Value) as Value FROM txn_detail GROUP BY Bank;
""").df()

df2= conn.execute("""
SELECT Bank, "Online or In-Person", "Transaction Date", SUM(Value) as Value FROM txn_detail 
GROUP BY Bank, "Online or In-Person", "Transaction Date";
""").df()

df3 = conn.execute("""
SELECT Bank, "Customer Code", SUM(Value) as Value FROM txn_detail GROUP BY Bank, "Customer Code";
""").df()

conn.close()
