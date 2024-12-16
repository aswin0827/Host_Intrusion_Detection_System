import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from rules import Rule
from constants import rules_data_file,all_alert_notification_data_file,userManagementDataFile
from dataFormatter import load_file,save_file
from constants import alerts_data_file

class HIDSGUI:
    def __init__(self, master):
        self.master = master
        self.rules = load_file(rules_data_file)
        self.attacks_data = load_file(all_alert_notification_data_file) or []
        self.master.title("Host Intrusion Detection System")
        self.master.geometry("1000x600")
        self.userData = load_file(userManagementDataFile)
        self.create_widgets()

    def create_widgets(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        # Rules tab
        self.rules_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_frame, text="Rules")
        self.create_rules_widgets()
        
        # Detected Attacks tab
        self.attacks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.attacks_frame, text="Detected Attacks")
        self.create_attacks_widgets()
        
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="User Management")
        self.create_user_management_widgets()
        
    def create_user_management_widgets(self):
        # Email label and entry
        email_label = ttk.Label(self.users_frame, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.email_entry = ttk.Entry(self.users_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.email_entry.insert(0, self.userData['email'])

        # Toggle for receiving emails
        self.send_mail_var = tk.BooleanVar(value=self.userData['sendEmailAlerts'])
        send_mail_toggle = ttk.Checkbutton(
            self.users_frame,
            text="Send Mail Notifications",
            variable=self.send_mail_var
        )
        send_mail_toggle.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Save button
        save_button = ttk.Button(self.users_frame, text="Save", command=self.save_user_details)
        save_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Configure grid weights
        self.users_frame.grid_rowconfigure(3, weight=1)
        self.users_frame.grid_columnconfigure(1, weight=1)

    def save_user_details(self):
        # Get user input
        email = self.email_entry.get().strip()
        send_mail = self.send_mail_var.get()

        # Validate email
        if not email:
            messagebox.showerror("Invalid Input", "Email cannot be empty.")
            return

        # Update user data
        self.userData['email'] = email
        self.userData['sendEmailAlerts'] = send_mail

        # Save to file
        save_file(self.userData, userManagementDataFile)
        messagebox.showinfo("Success", "User details updated successfully.")
        
    def create_rules_widgets(self):
        # Create Treeview
        self.tree = ttk.Treeview(self.rules_frame, columns=("Index","ID", "Level", "Category", "Description", "Patterns"), show="headings")
        self.tree.heading("Index", text="Index")
        self.tree.heading("ID", text="Rule ID")
        self.tree.heading("Level", text="Level")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Patterns", text="Patterns")

        # Set column widths
        self.tree.column("Index", width=40)
        self.tree.column("ID", width=50)
        self.tree.column("Level", width=50)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=300)
        self.tree.column("Patterns", width=400)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.rules_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout for treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons frame
        btn_frame = ttk.Frame(self.rules_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Add rule button
        add_btn = ttk.Button(btn_frame, text="Add Rule", command=self.add_rule)
        add_btn.pack(side=tk.LEFT, padx=5)

        # Edit rule button
        edit_btn = ttk.Button(btn_frame, text="Edit Rule", command=self.edit_rule)
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Delete rule button
        delete_btn = ttk.Button(btn_frame, text="Delete Rule", command=self.delete_rule)
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Configure grid weights
        self.rules_frame.grid_rowconfigure(0, weight=1)
        self.rules_frame.grid_columnconfigure(0, weight=1)

        self.update_rules_treeview()
        
    def update_rules_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx,rule in enumerate(self.rules):
            self.tree.insert("", "end", values=(idx,rule.id, rule.level, rule.category, rule.description, ", ".join(rule.patterns)))

    def add_rule(self):
        id = simpledialog.askstring("Add Rule", "Enter rule ID:")
        level = simpledialog.askinteger("Add Rule", "Enter rule level:")
        description = simpledialog.askstring("Add Rule", "Enter rule description:")
        category = simpledialog.askstring("Add Rule", "Enter rule category:")
        patterns = simpledialog.askstring("Add Rule", "Enter patterns")
        
        new_rule = Rule(id, level, description, category, patterns)
        self.rules.append(new_rule)
        save_file(self.rules,rules_data_file)
        self.update_rules_treeview()

    def edit_rule(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Rule", "Please select a rule to edit.")
            return

        item = self.tree.item(selected_item)
        index = self.tree.index(selected_item)
        rule = self.rules[index]

        rule.id = simpledialog.askstring("Edit Rule", "Enter new ID:", initialvalue=rule.id)
        rule.level = simpledialog.askinteger("Edit Rule", "Enter new level:", initialvalue=rule.level)
        rule.description = simpledialog.askstring("Edit Rule", "Enter new description:", initialvalue=rule.description)
        rule.category = simpledialog.askstring("Edit Rule", "Enter new category:", initialvalue=rule.category)
        rule.patterns = simpledialog.askstring("Edit Rule", "Enter new patterns:", initialvalue=", ".join(rule.patterns))

        self.update_rules_treeview()
        save_file(self.rules,rules_data_file)

    def delete_rule(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Rule", "Please select a rule to delete.")
            return

        index = self.tree.index(selected_item)
        del self.rules[index]
        self.update_rules_treeview()
        save_file(self.rules,rules_data_file)
    
    def create_attacks_widgets(self):
        # Create Treeview for attacks
        self.attacks_tree = ttk.Treeview(self.attacks_frame, columns=("Timestamp", "Log Message", "Detedted Attacks"), show="headings")
        self.attacks_tree.heading("Timestamp", text="Timestamp")
        self.attacks_tree.heading("Log Message", text="Log Message")
        self.attacks_tree.heading("Detedted Attacks", text="Detedted Attacks")

        # Set column widths
        self.attacks_tree.column("Timestamp", width=60)
        self.attacks_tree.column("Log Message",width=440)
        self.attacks_tree.column("Detedted Attacks", width=100)
        
        # Bind click event to treeview
        self.attacks_tree.bind("<ButtonRelease-1>", self.on_tree_click)

        # Scrollbar for attacks treeview
        attacks_scrollbar = ttk.Scrollbar(self.attacks_frame, orient="vertical", command=self.attacks_tree.yview)
        self.attacks_tree.configure(yscrollcommand=attacks_scrollbar.set)

        # Grid layout for attacks treeview and scrollbar
        self.attacks_tree.grid(row=0, column=0, sticky="nsew")
        attacks_scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons frame for attacks
        attacks_btn_frame = ttk.Frame(self.attacks_frame)
        attacks_btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Add attack button
        clear_attacks_btn = ttk.Button(attacks_btn_frame, text="Clear Attacks", command=self.clear_attacks)
        clear_attacks_btn.pack(side=tk.LEFT, padx=5)

        # Remove attack button
        refresh_attacks_btn = ttk.Button(attacks_btn_frame, text="Refresh", command=self.refresh_attacks)
        refresh_attacks_btn.pack(side=tk.LEFT, padx=5)

        # Configure grid weights for attacks frame
        self.attacks_frame.grid_rowconfigure(0, weight=1)
        self.attacks_frame.grid_columnconfigure(0, weight=1)

        self.update_attacks_treeview()
        
    def on_tree_click(self, event):
        region = self.attacks_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.attacks_tree.identify_column(event.x)
            item = self.attacks_tree.identify_row(event.y)
            if item:
                values = self.attacks_tree.item(item, "values")
                column_index = int(column[1]) - 1  # Convert column string to index
                
                if column_index == 0:  # Timestamp
                    messagebox.showinfo("Timestamp", f"Timestamp: {values[0]}")
                elif column_index == 1:  # Description
                    messagebox.showinfo("Description", f"Description: {values[1]}")
                elif column_index == 2:  # Detected Attacks
                    # detected_attacks = values[2]
                    attack_index = int(self.attacks_tree.item(item, "tags")[0])
                    self.show_detected_attacks_dialog(self.attacks_data[attack_index].detectedAttacks)
                    # messagebox.showinfo("Detected Attacks", f"Detected Attacks: {detected_attacks}")
                    
    def show_detected_attacks_dialog(self, detected_attacks):
        dialog = tk.Toplevel(self.master)
        dialog.title("Detected Attacks")
        dialog.geometry("800x400")

        # Create Treeview
        tree = ttk.Treeview(dialog, columns=("ID", "Level", "Category", "Description", "Patterns"), show="headings")
        tree.heading("ID", text="Rule ID")
        tree.heading("Level", text="Level")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Patterns", text="Patterns")

        # Set column widths
        tree.column("ID", width=50)
        tree.column("Level", width=50)
        tree.column("Category", width=100)
        tree.column("Description", width=300)
        tree.column("Patterns", width=300)

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(dialog, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(dialog, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_columnconfigure(0, weight=1)

        # Populate Treeview
        for attack in detected_attacks:
            tree.insert("", "end", values=(attack.id, attack.level, attack.category, attack.description, attack.patterns))


    def update_attacks_treeview(self):
        for i in self.attacks_tree.get_children():
            self.attacks_tree.delete(i)
        # Add attacks to treeview
        for i, attack in enumerate(self.attacks_data):
            self.attacks_tree.insert("", "end", values=(attack.timestamp, attack.logMessage, f"{len(attack.detectedAttacks)} attacks"), tags=(str(i),))
        
    def clear_attacks(self):
        alerts_data = load_file(alerts_data_file)
        self.attacks_data = []
        self.update_attacks_treeview()
        alerts_data['count'] = 0
        save_file(alerts_data,alerts_data_file)
        save_file(self.attacks_data,all_alert_notification_data_file)

    def refresh_attacks(self):
        self.attacks_data = load_file(all_alert_notification_data_file) or []
        self.update_attacks_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = HIDSGUI(root)
    root.mainloop()