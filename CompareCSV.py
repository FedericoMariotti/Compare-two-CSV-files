import pandas as pd
import csv
import tkinter as tk
from tkinter import ttk, filedialog

def read_csv_with_fallback(filename):
    try:
        df = pd.read_csv(filename, sep=';')
    except pd.errors.ParserError:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                if len(row) == 1:
                    rows.append(row[0].split(';'))
                else:
                    rows.append(row)
        df = pd.DataFrame(rows[1:], columns=rows[0])
    return df

def calcola_percentuale_differenze(df1, df2):
    if df1.shape != df2.shape:
        # Handle cases where shapes are different
        total_elements = max(df1.size, df2.size)
        diff_elements = sum([1 for row in range(max(df1.shape[0], df2.shape[0]))
                             for col in range(max(df1.shape[1], df2.shape[1]))
                             if row < df1.shape[0] and col < df1.shape[1] and row < df2.shape[0] and col < df2.shape[1]
                             and df1.iloc[row, col] != df2.iloc[row, col]])
    else:
        total_elements = df1.size
        diff_elements = (df1 != df2).sum().sum()
    percentuale_differenze = (diff_elements / total_elements) * 100
    return f"Percentuale di differenza: {percentuale_differenze:.2f}%"

def mostra_risultati(diff_df, df1, df2):
    root = tk.Tk()
    root.title("Differenze trovate")

    tree = ttk.Treeview(root)
    tree["columns"] = tuple(diff_df.columns)
    tree.heading("#0", text="Index")
    for col in diff_df.columns:
        tree.heading(col, text=col)

    for index, row in diff_df.iterrows():
        values = tuple(row)
        tags = []
        for col_idx, val in enumerate(values):
            if df1.iloc[index, col_idx] != df2.iloc[index, col_idx]:
                tags.append("changed")
        item_id = tree.insert("", tk.END, text=index, values=values, tags=tags)

    tree.tag_configure("changed", foreground="black", background="#fdf0d5")
    tree.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()

    file1_path = filedialog.askopenfilename(title="Seleziona il primo file CSV", filetypes=[("CSV files", "*.csv")])
    file2_path = filedialog.askopenfilename(title="Seleziona il secondo file CSV", filetypes=[("CSV files", "*.csv")])

    if file1_path and file2_path:
        df1 = read_csv_with_fallback(file1_path)
        df2 = read_csv_with_fallback(file2_path)

        df1 = df1.sort_index().sort_index(axis=1)
        df2 = df2.sort_index().sort_index(axis=1)

        if df1.shape != df2.shape:
            print("Le dimensioni dei DataFrame non corrispondono.")
        else:
            try:
                diff_df = df1.compare(df2)
                print(calcola_percentuale_differenze(df1, df2))
                mostra_risultati(diff_df, df1, df2)
            except ValueError:
                print("Mannaggia! I DataFrame non possono essere confrontati (indici o colonne diversi).")
    else:
        print("Entrambi i file devono essere selezionati.")

if __name__ == "__main__":
    main()
