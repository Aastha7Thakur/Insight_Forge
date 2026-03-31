import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind 
from scipy.stats import chi2_contingency
from scipy.stats import linregress


df = None
root = tk.Tk()
root.title("InsightForge")
root.geometry("700x600")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)
tk.Label(top_frame, text="InsightForge", font=("Arial", 18, "bold")).pack()
tk.Label(top_frame, text="Statistical Analysis Tool", font=("Arial", 10)).pack()

middle_frame = tk.Frame(root)
middle_frame.pack(pady=10)
tk.Label(middle_frame, text="Controls", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(middle_frame, text="").grid(row=5, column=0)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=20)

selected_num = tk.StringVar()
selected_cat = tk.StringVar()
selected_cat2 = tk.StringVar()
selected_num2 = tk.StringVar()

#upload csv button
def upload_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if file_path:
     try:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "CSV file loaded successfully!")

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        # -------- Numeric Dropdown (X) --------
        menu = num_dropdown["menu"]
        menu.delete(0, "end")
        for col in numeric_cols:
            menu.add_command(label=col, command=lambda value=col: selected_num.set(value))

        # -------- Second Numeric Dropdown (Y) --------
        menu = num2_dropdown["menu"]
        menu.delete(0, "end")
        for col in numeric_cols:
            menu.add_command(label=col, command=lambda value=col: selected_num2.set(value))

        # -------- First Categorical Dropdown --------
        menu = cat_dropdown["menu"]
        menu.delete(0, "end")
        for col in categorical_cols:
            menu.add_command(label=col, command=lambda value=col: selected_cat.set(value))

        # -------- Second Categorical Dropdown --------
        menu = cat2_dropdown["menu"]
        menu.delete(0, "end")
        for col in categorical_cols:
            menu.add_command(label=col, command=lambda value=col: selected_cat2.set(value))

        # -------- Default Values --------
        if len(numeric_cols) > 0:
            selected_num.set(numeric_cols[0])
            selected_num2.set(numeric_cols[0])

        if len(categorical_cols) > 0:
            selected_cat.set(categorical_cols[0])
            selected_cat2.set(categorical_cols[0])

     except Exception:
        messagebox.showerror("Error", "Failed to load CSV file.")

upload_button = tk.Button(middle_frame, text="Upload CSV", width=20, command=upload_file)
upload_button.grid(row=1, column=0, padx=10, pady=5)

#dropdowns for variable selection
tk.Label(middle_frame, text="Select 1st Numeric Variable").grid(row=5, column=0, padx=10, pady=5, sticky="e")
num_dropdown = tk.OptionMenu(middle_frame, selected_num, "")
num_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

tk.Label(middle_frame, text="Select 1st Categorical Variable").grid(row=6, column=0, padx=10, pady=5, sticky="e")
cat_dropdown = tk.OptionMenu(middle_frame, selected_cat, "")
cat_dropdown.grid(row=6, column=1, padx=10, pady=5, sticky="w")

tk.Label(middle_frame, text="Select 2nd Categorical Variable").grid(row=7, column=0, padx=10, pady=5, sticky="e")
cat2_dropdown = tk.OptionMenu(middle_frame, selected_cat2, "")
cat2_dropdown.grid(row=7, column=1, padx=10, pady=5, sticky="w")

tk.Label(middle_frame, text="Select 2nd Numeric Variable (Y)").grid(row=8, column=0, padx=10, pady=5, sticky="e")
num2_dropdown = tk.OptionMenu(middle_frame, selected_num2, "")
num2_dropdown.grid(row=8, column=1, padx=10, pady=5, sticky="w")

#Data profiling features
def profile_data():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    rows, cols = df.shape
    data_types = df.dtypes
    missing_values = df.isnull().sum()
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Clear previous output
    output_text.delete("1.0", tk.END)
    
    # Insert new output
    output_text.insert(tk.END, f"Rows: {rows}\n")
    output_text.insert(tk.END, f"Columns: {cols}\n\n")
    
    output_text.insert(tk.END, "Data Types:\n")
    output_text.insert(tk.END, f"{data_types}\n\n")
    
    output_text.insert(tk.END, "Missing Values:\n")
    output_text.insert(tk.END, f"{missing_values}\n\n")
    
    output_text.insert(tk.END, "Numeric Columns:\n")
    output_text.insert(tk.END, f"{list(numeric_cols)}\n\n")
    
    output_text.insert(tk.END, "Categorical Columns:\n")
    output_text.insert(tk.END, f"{list(categorical_cols)}\n")

#descriptive statistics function
def descriptive_stats():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    output_text.delete("1.0", tk.END)
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    output_text.insert(tk.END, "===== DESCRIPTIVE STATISTICS =====\n\n")
    
    # Numerical Summary
    if len(numeric_cols) > 0:
        output_text.insert(tk.END, "Numerical Variables:\n\n")
        
        for col in numeric_cols:
            output_text.insert(tk.END, f"Column: {col}\n")
            output_text.insert(tk.END, f"Mean: {df[col].mean():.2f}\n")
            output_text.insert(tk.END, f"Median: {df[col].median():.2f}\n")
            output_text.insert(tk.END, f"Std Dev: {df[col].std():.2f}\n")
            
            q1 = df[col].quantile(0.25)
            q2 = df[col].quantile(0.50)
            q3 = df[col].quantile(0.75)
            
            output_text.insert(tk.END, f"Q1: {q1:.2f}\n")
            output_text.insert(tk.END, f"Q2 (Median): {q2:.2f}\n")
            output_text.insert(tk.END, f"Q3: {q3:.2f}\n")
            output_text.insert(tk.END, "-"*40 + "\n")
    
    # Categorical Summary
    if len(categorical_cols) > 0:
        output_text.insert(tk.END, "\nCategorical Variables:\n\n")
        
        for col in categorical_cols:
            output_text.insert(tk.END, f"Column: {col}\n")
            freq_table = df[col].value_counts()
            output_text.insert(tk.END, f"{freq_table}\n")
            output_text.insert(tk.END, "-"*40 + "\n")

#correlation analysis function
def correlation_analysis():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    if numeric_df.shape[1] < 2:
        messagebox.showinfo("Info", "Not enough numerical variables for correlation.")
        return
    
    corr_matrix = numeric_df.corr()
    
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "===== CORRELATION MATRIX =====\n\n")
    output_text.insert(tk.END, f"{corr_matrix}\n\n")
    
    # Heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    
    #
    # Ask user if they want to save
    save_choice = messagebox.askyesno("Save Heatmap", "Do you want to save the heatmap?")
    #
    if save_choice:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")]) 
        if file_path:
          plt.savefig(file_path)
          messagebox.showinfo("Success", "Correlation heatmap saved successfully!")
    plt.show()
#hypothesis testing function
def hypothesis_test():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    num_col = selected_num.get()
    cat_col = selected_cat.get()
    
    if num_col == "" or cat_col == "":
        messagebox.showwarning("Warning", "Please select variables.")
        return
    
    # Get top 2 categories
    top_two = df[cat_col].value_counts().index[:2]
    df_filtered = df[df[cat_col].isin(top_two)]
    
    group1 = df_filtered[df_filtered[cat_col] == top_two[0]][num_col]
    group2 = df_filtered[df_filtered[cat_col] == top_two[1]][num_col]
    
    t_stat, p_value = ttest_ind(group1, group2, nan_policy='omit')
    
    output_text.delete("1.0", tk.END)
    
    # Hypothesis
    output_text.insert(tk.END, "===== HYPOTHESIS TEST (t-test) =====\n\n")
    output_text.insert(tk.END, f"Numeric Variable: {num_col}\n")
    output_text.insert(tk.END, f"Grouping Variable: {cat_col}\n\n")
    
    output_text.insert(tk.END, "H0: No significant difference between group means\n")
    output_text.insert(tk.END, "H1: Significant difference between group means\n\n")
    
    output_text.insert(tk.END, f"Groups Compared:\n{top_two[0]} vs {top_two[1]}\n\n")
    
    output_text.insert(tk.END, f"T-Statistic: {t_stat:.4f}\n")
    output_text.insert(tk.END, f"P-Value: {p_value:.4f}\n\n")
    
    if p_value < 0.05:
        output_text.insert(tk.END, "Conclusion: Reject H0 (Significant difference exists)\n")
    else:
        output_text.insert(tk.END, "Conclusion: Fail to reject H0 (No significant difference)\n")

#chi-square test function
def chi_square_test():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    cat1 = selected_cat.get()
    cat2 = selected_cat2.get()
    
    if cat1 == "" or cat2 == "":
        messagebox.showwarning("Warning", "Please select both categorical variables.")
        return
    
    if cat1 == cat2:
        messagebox.showwarning("Warning", "Please select two different variables.")
        return
    
    # Create contingency table
    contingency_table = pd.crosstab(df[cat1], df[cat2])
    
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    output_text.delete("1.0", tk.END)
    
    output_text.insert(tk.END, "===== CHI-SQUARE TEST =====\n\n")
    output_text.insert(tk.END, f"Variable 1: {cat1}\n")
    output_text.insert(tk.END, f"Variable 2: {cat2}\n\n")
    
    output_text.insert(tk.END, "H0: Variables are independent\n")
    output_text.insert(tk.END, "H1: Variables are associated\n\n")
    
    output_text.insert(tk.END, f"Chi-Square Statistic: {chi2:.4f}\n")
    output_text.insert(tk.END, f"P-Value: {p:.4f}\n\n")
    
    if p < 0.05:
        output_text.insert(tk.END, "Conclusion: Reject H0 (Variables are associated)\n")
    else:
        output_text.insert(tk.END, "Conclusion: Fail to reject H0 (No association)\n")

#regression function
def regression_analysis():
    global df
    
    if df is None:
        messagebox.showwarning("Warning", "Please upload a CSV file first.")
        return
    
    x_col = selected_num.get()
    y_col = selected_num2.get()
    
    if x_col == "" or y_col == "":
        messagebox.showwarning("Warning", "Please select both variables.")
        return
    
    if x_col == y_col:
        messagebox.showwarning("Warning", "Select different variables.")
        return
    
    x = df[x_col]
    y = df[y_col]
    
    # Remove missing values
    valid_data = df[[x_col, y_col]].dropna()
    x = valid_data[x_col]
    y = valid_data[y_col]
    
    result = linregress(x, y)
    
    output_text.delete("1.0", tk.END)
    
    output_text.insert(tk.END, "===== LINEAR REGRESSION =====\n\n")
    output_text.insert(tk.END, f"Independent Variable (X): {x_col}\n")
    output_text.insert(tk.END, f"Dependent Variable (Y): {y_col}\n\n")
    
    output_text.insert(tk.END, f"Slope: {result.slope:.4f}\n")
    output_text.insert(tk.END, f"Intercept: {result.intercept:.4f}\n")
    output_text.insert(tk.END, f"R-squared: {result.rvalue**2:.4f}\n")
    output_text.insert(tk.END, f"P-value: {result.pvalue:.4f}\n\n")
    
    if result.pvalue < 0.05:
        output_text.insert(tk.END, "Conclusion: Significant linear relationship exists.\n")
    else:
        output_text.insert(tk.END, "Conclusion: No significant linear relationship.\n")
    
    # Plot
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(6,4))
    plt.scatter(x, y)
    plt.plot(x, result.intercept + result.slope * x)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title("Regression Plot")
    plt.show()

profile_button = tk.Button(middle_frame, text="Profile Dataset", width=20, command=profile_data)
profile_button.grid(row=1, column=1, padx=10, pady=5)

stats_button = tk.Button(middle_frame, text="Descriptive Statistics", width=20, command=descriptive_stats)
stats_button.grid(row=2, column=0, padx=10, pady=5)

corr_button = tk.Button(middle_frame, text="Correlation Analysis", width=20, command=correlation_analysis)
corr_button.grid(row=2, column=1, padx=10, pady=5)

test_button = tk.Button(middle_frame, text="Hypothesis Test (t-test)", width=20, command=hypothesis_test)
test_button.grid(row=3, column=0, padx=10, pady=5)

chi_button = tk.Button(middle_frame, text="Chi-Square Test", width=20, command=chi_square_test)
chi_button.grid(row=3, column=1, padx=10, pady=5)

reg_button = tk.Button(middle_frame, text="Linear Regression", width=20, command=regression_analysis)
reg_button.grid(row=4, column=0, columnspan=2, pady=5)

# ✅ Output Label 
tk.Label(bottom_frame, text="Output", font=("Arial", 13, "bold")).pack(pady=5)

#scrollable text area for output
scrollbar = tk.Scrollbar(bottom_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#text box for displaying results
output_text = tk.Text(bottom_frame, height=18, width=80, yscrollcommand=scrollbar.set)
output_text.pack(side=tk.LEFT)

scrollbar.config(command=output_text.yview)

#export report function
from tkinter import filedialog

def export_report():
    try:
        content = output_text.get("1.0", tk.END)
        
        if content.strip() == "":
            messagebox.showwarning("Warning", "No content to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            
            messagebox.showinfo("Success", "Report saved successfully!")
    
    except Exception:
        messagebox.showerror("Error", "Failed to save report.")

export_button = tk.Button(middle_frame, text="Export Report", width=20, command=export_report)
export_button.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()