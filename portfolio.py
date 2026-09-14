"""
Stock Portfolio Tracker Pro
===========================

A professional, colourful desktop stock portfolio tracker
built with Python and Tkinter.

Features:
    - Portfolio statistics
    - Donut allocation chart
    - Search/filter
    - Add stocks
    - Duplicate-stock merging
    - Edit holdings
    - Remove holdings
    - TXT export
    - CSV export
    - Light/Dark theme
    - Custom application icon

No third-party packages are required.
"""

import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


# ============================================================
# CONFIGURATION
# ============================================================

STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 420.00,
    "AMZN": 185.00,
}

APP_DIR = Path(__file__).resolve().parent
ICON_FILE = APP_DIR / "app_icon.ico"


# ============================================================
# THEMES
# ============================================================

LIGHT_THEME = {
    "background": "#F4F7FB",
    "card": "#FFFFFF",
    "text": "#17202A",
    "muted": "#64748B",
    "border": "#DCE3EC",
    "input": "#FFFFFF",
    "header": "#172554",
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "success": "#16A34A",
    "danger": "#DC2626",
    "warning": "#D97706",
}

DARK_THEME = {
    "background": "#0F172A",
    "card": "#172033",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "border": "#334155",
    "input": "#1E293B",
    "header": "#111827",
    "primary": "#60A5FA",
    "secondary": "#A78BFA",
    "success": "#4ADE80",
    "danger": "#F87171",
    "warning": "#FBBF24",
}


# ============================================================
# BUSINESS LOGIC
# ============================================================

def calculate_investment(stock: str, quantity: int) -> float:
    """
    Calculate the investment value of a stock.

    Formula:
        Investment = Stock Price × Quantity

    Args:
        stock: Stock ticker symbol.
        quantity: Number of shares.

    Returns:
        Total investment value.

    Raises:
        ValueError: If stock is invalid or quantity is invalid.
    """

    stock = stock.strip().upper()

    if stock not in STOCK_PRICES:
        raise ValueError(
            f"Stock '{stock}' is not available."
        )

    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero."
        )

    return STOCK_PRICES[stock] * quantity


def calculate_total(portfolio: list[dict]) -> float:
    """Calculate total portfolio investment."""

    return sum(
        item["investment"]
        for item in portfolio
    )


# ============================================================
# APPLICATION
# ============================================================

class StockPortfolioApp:
    """Main Stock Portfolio Tracker application."""

    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.title(
            "Stock Portfolio Tracker Pro"
        )

        self.root.geometry("1180x780")
        self.root.minsize(980, 680)

        self.portfolio = []

        self.theme_name = "light"
        self.colors = LIGHT_THEME

        self.selected_index = None

        self.configure_window()
        self.create_styles()
        self.create_header()
        self.create_statistics()
        self.create_input_area()
        self.create_portfolio_area()
        self.create_status_bar()

        self.refresh_all()

    # ========================================================
    # WINDOW
    # ========================================================

    def configure_window(self):
        """Configure the main window."""

        self.root.configure(
            bg=self.colors["background"]
        )

        if ICON_FILE.exists():
            try:
                self.root.iconbitmap(
                    str(ICON_FILE)
                )
            except tk.TclError:
                pass

    # ========================================================
    # STYLES
    # ========================================================

    def create_styles(self):
        """Configure ttk styles."""

        style = ttk.Style()

        style.theme_use("clam")

        colors = self.colors

        style.configure(
            "Treeview",
            background=colors["card"],
            fieldbackground=colors["card"],
            foreground=colors["text"],
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            background=colors["header"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=10,
        )

        style.map(
            "Treeview",
            background=[
                ("selected", colors["primary"])
            ],
            foreground=[
                ("selected", "white")
            ],
        )

        style.configure(
            "TEntry",
            fieldbackground=colors["input"],
            foreground=colors["text"],
            padding=8,
        )

        style.configure(
            "TCombobox",
            fieldbackground=colors["input"],
            foreground=colors["text"],
            padding=7,
        )

    # ========================================================
    # HELPER WIDGETS
    # ========================================================

    def create_button(
        self,
        parent,
        text,
        command,
        background,
    ):
        """Create a consistent application button."""

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=background,
            fg="white",
            activebackground=background,
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=14,
            pady=9,
            cursor="hand2",
        )

    def create_card(self, parent):
        """Create a themed card."""

        return tk.Frame(
            parent,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            bd=0,
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):
        """Create application header."""

        self.header = tk.Frame(
            self.root,
            bg=self.colors["header"],
            height=90,
        )

        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(False)

        title_frame = tk.Frame(
            self.header,
            bg=self.colors["header"],
        )

        title_frame.pack(
            side="left",
            padx=28,
            pady=13,
        )

        self.title_label = tk.Label(
            title_frame,
            text="◈  STOCK PORTFOLIO TRACKER PRO",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors["header"],
            fg="white",
        )

        self.title_label.pack(
            anchor="w"
        )

        self.subtitle_label = tk.Label(
            title_frame,
            text="Smart portfolio management • Simple • Fast • Colourful",
            font=("Segoe UI", 9),
            bg=self.colors["header"],
            fg="#BFDBFE",
        )

        self.subtitle_label.pack(
            anchor="w"
        )

        self.create_button(
            self.header,
            "◐  Theme",
            self.toggle_theme,
            "#475569",
        ).pack(
            side="right",
            padx=28,
            pady=22,
        )

    # ========================================================
    # STATISTICS
    # ========================================================

    def create_statistics(self):
        """Create portfolio statistics."""

        self.statistics_frame = tk.Frame(
            self.root,
            bg=self.colors["background"],
        )

        self.statistics_frame.pack(
            fill="x",
            padx=24,
            pady=20,
        )

        for column in range(4):
            self.statistics_frame.columnconfigure(
                column,
                weight=1,
            )

        self.total_value = self.create_stat_card(
            0,
            "TOTAL INVESTMENT",
            "$0.00",
            self.colors["success"],
            "◆",
        )

        self.total_holdings = self.create_stat_card(
            1,
            "HOLDINGS",
            "0",
            self.colors["primary"],
            "▣",
        )

        self.total_shares = self.create_stat_card(
            2,
            "TOTAL SHARES",
            "0",
            self.colors["secondary"],
            "▤",
        )

        self.average_value = self.create_stat_card(
            3,
            "AVERAGE HOLDING",
            "$0.00",
            self.colors["warning"],
            "◉",
        )

    def create_stat_card(
        self,
        column,
        title,
        value,
        accent,
        icon,
    ):
        """Create one statistics card."""

        card = self.create_card(
            self.statistics_frame
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
        )

        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["card"],
            fg=accent,
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 0),
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 21, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(3, 0),
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["card"],
            fg=self.colors["muted"],
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 15),
        )

        return value_label

    # ========================================================
    # INPUT AREA
    # ========================================================

    def create_input_area(self):
        """Create stock input controls."""

        card = self.create_card(
            self.root
        )

        card.pack(
            fill="x",
            padx=24,
            pady=(0, 10),
        )

        tk.Label(
            card,
            text="Add / Edit Investment",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="w",
            padx=18,
            pady=(14, 8),
        )

        tk.Label(
            card,
            text="Stock",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["card"],
            fg=self.colors["muted"],
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(18, 6),
        )

        tk.Label(
            card,
            text="Quantity",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["card"],
            fg=self.colors["muted"],
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=6,
        )

        self.stock_var = tk.StringVar(
            value="AAPL"
        )

        self.stock_combo = ttk.Combobox(
            card,
            textvariable=self.stock_var,
            values=list(STOCK_PRICES.keys()),
            state="readonly",
            width=14,
        )

        self.stock_combo.grid(
            row=2,
            column=0,
            padx=(18, 6),
            pady=(0, 15),
        )

        self.quantity_var = tk.StringVar()

        self.quantity_entry = ttk.Entry(
            card,
            textvariable=self.quantity_var,
            width=14,
        )

        self.quantity_entry.grid(
            row=2,
            column=2,
            padx=6,
            pady=(0, 15),
        )

        self.add_button = self.create_button(
            card,
            "＋ Add / Merge",
            self.add_stock,
            self.colors["primary"],
        )

        self.add_button.grid(
            row=2,
            column=3,
            padx=6,
            pady=(0, 15),
        )

        self.edit_button = self.create_button(
            card,
            "✎ Edit Selected",
            self.edit_selected,
            self.colors["secondary"],
        )

        self.edit_button.grid(
            row=2,
            column=4,
            padx=(6, 18),
            pady=(0, 15),
        )

        self.quantity_entry.bind(
            "<Return>",
            lambda event: self.add_stock(),
        )

    # ========================================================
    # PORTFOLIO AREA
    # ========================================================

    def create_portfolio_area(self):
        """Create holdings table and donut chart."""

        self.main_area = tk.Frame(
            self.root,
            bg=self.colors["background"],
        )

        self.main_area.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=10,
        )

        self.main_area.columnconfigure(
            0,
            weight=3,
        )

        self.main_area.columnconfigure(
            1,
            weight=2,
        )

        self.main_area.rowconfigure(
            0,
            weight=1,
        )

        self.create_table()
        self.create_chart()

    def create_table(self):
        """Create holdings table."""

        card = self.create_card(
            self.main_area
        )

        card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6),
        )

        top = tk.Frame(
            card,
            bg=self.colors["card"],
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(14, 8),
        )

        tk.Label(
            top,
            text="Your Holdings",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(
            side="left"
        )

        search_frame = tk.Frame(
            top,
            bg=self.colors["input"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )

        search_frame.pack(
            side="right"
        )

        tk.Label(
            search_frame,
            text="⌕",
            font=("Segoe UI", 13),
            bg=self.colors["input"],
            fg=self.colors["muted"],
        ).pack(
            side="left",
            padx=(8, 2),
        )

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh_table(),
        )

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=24,
            font=("Segoe UI", 10),
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            bd=0,
        ).pack(
            side="left",
            padx=(0, 8),
            pady=7,
        )

        table_frame = tk.Frame(
            card,
            bg=self.colors["card"],
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=18,
        )

        columns = (
            "stock",
            "quantity",
            "price",
            "investment",
            "percentage",
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "stock": "Stock",
            "quantity": "Quantity",
            "price": "Price",
            "investment": "Investment",
            "percentage": "Portfolio %",
        }

        widths = {
            "stock": 100,
            "quantity": 110,
            "price": 120,
            "investment": 150,
            "percentage": 120,
        }

        for column in columns:
            self.table.heading(
                column,
                text=headings[column],
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="center",
            )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.on_table_select,
        )

        self.table.bind(
            "<Double-1>",
            lambda event: self.load_selected(),
        )

        button_frame = tk.Frame(
            card,
            bg=self.colors["card"],
        )

        button_frame.pack(
            fill="x",
            padx=18,
            pady=14,
        )

        self.create_button(
            button_frame,
            "Remove Selected",
            self.remove_selected,
            self.colors["danger"],
        ).pack(
            side="left",
            padx=(0, 6),
        )

        self.create_button(
            button_frame,
            "Load for Edit",
            self.load_selected,
            self.colors["secondary"],
        ).pack(
            side="left"
        )

        self.create_button(
            button_frame,
            "Save CSV",
            self.save_csv,
            self.colors["success"],
        ).pack(
            side="right",
            padx=(6, 0),
        )

        self.create_button(
            button_frame,
            "Save TXT",
            self.save_txt,
            self.colors["primary"],
        ).pack(
            side="right"
        )

    # ========================================================
    # DONUT CHART
    # ========================================================

    def create_chart(self):
        """Create donut chart."""

        card = self.create_card(
            self.main_area
        )

        card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0),
        )

        tk.Label(
            card,
            text="Portfolio Allocation",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 0),
        )

        self.chart_canvas = tk.Canvas(
            card,
            bg=self.colors["card"],
            highlightthickness=0,
        )

        self.chart_canvas.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        self.chart_canvas.bind(
            "<Configure>",
            lambda event: self.draw_donut(),
        )

    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):
        """Create application status bar."""

        self.status_bar = tk.Label(
            self.root,
            text="Ready • Add your first holding",
            anchor="w",
            font=("Segoe UI", 9),
            bg=self.colors["header"],
            fg="#CBD5E1",
            padx=18,
            pady=6,
        )

        self.status_bar.pack(
            fill="x",
            side="bottom",
        )

    # ========================================================
    # ADD STOCK
    # ========================================================

    def add_stock(self):
        """Add a stock or merge it with an existing holding."""

        stock = self.stock_var.get().strip().upper()
        quantity_text = self.quantity_var.get().strip()

        if stock not in STOCK_PRICES:
            messagebox.showerror(
                "Invalid Stock",
                "Please select a supported stock.",
            )
            return

        try:
            quantity = int(quantity_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number.",
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero.",
            )
            return

        # Duplicate-stock handling.
        for item in self.portfolio:

            if item["stock"] == stock:

                item["quantity"] += quantity

                item["investment"] = (
                    calculate_investment(
                        stock,
                        item["quantity"],
                    )
                )

                self.quantity_var.set("")

                self.refresh_all()

                self.status_bar.config(
                    text=(
                        f"{stock} already existed • "
                        f"Added {quantity} shares"
                    )
                )

                return

        # New holding.
        self.portfolio.append(
            {
                "stock": stock,
                "quantity": quantity,
                "price": STOCK_PRICES[stock],
                "investment": calculate_investment(
                    stock,
                    quantity,
                ),
            }
        )

        self.quantity_var.set("")

        self.refresh_all()

        self.status_bar.config(
            text=f"{stock} added successfully"
        )

    # ========================================================
    # EDIT
    # ========================================================

    def on_table_select(self, event=None):
        """Track selected portfolio row."""

        selection = self.table.selection()

        if selection:
            self.selected_index = int(
                selection[0]
            )

    def load_selected(self):
        """Load selected holding into the edit fields."""

        if self.selected_index is None:
            selection = self.table.selection()

            if selection:
                self.selected_index = int(
                    selection[0]
                )

        if self.selected_index is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a holding first.",
            )
            return

        item = self.portfolio[
            self.selected_index
        ]

        self.stock_var.set(
            item["stock"]
        )

        self.quantity_var.set(
            str(item["quantity"])
        )

        self.status_bar.config(
            text=(
                f"Editing {item['stock']} • "
                "Change quantity and click Edit Selected"
            )
        )

    def edit_selected(self):
        """Edit the selected holding."""

        if self.selected_index is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a holding first.",
            )
            return

        try:
            quantity = int(
                self.quantity_var.get().strip()
            )
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number.",
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero.",
            )
            return

        stock = (
            self.stock_var.get()
            .strip()
            .upper()
        )

        if stock not in STOCK_PRICES:
            messagebox.showerror(
                "Invalid Stock",
                "Please select a supported stock.",
            )
            return

        self.portfolio[
            self.selected_index
        ] = {
            "stock": stock,
            "quantity": quantity,
            "price": STOCK_PRICES[stock],
            "investment": calculate_investment(
                stock,
                quantity,
            ),
        }

        self.merge_duplicates()

        self.selected_index = None
        self.quantity_var.set("")

        self.refresh_all()

        self.status_bar.config(
            text=f"{stock} updated successfully"
        )

    # ========================================================
    # DUPLICATE MERGING
    # ========================================================

    def merge_duplicates(self):
        """Merge duplicate ticker symbols."""

        merged = {}

        for item in self.portfolio:

            stock = item["stock"]

            merged[stock] = (
                merged.get(stock, 0)
                + item["quantity"]
            )

        self.portfolio = [
            {
                "stock": stock,
                "quantity": quantity,
                "price": STOCK_PRICES[stock],
                "investment": calculate_investment(
                    stock,
                    quantity,
                ),
            }
            for stock, quantity in merged.items()
        ]

    # ========================================================
    # REMOVE
    # ========================================================

    def remove_selected(self):
        """Remove selected holding."""

        if self.selected_index is None:
            selection = self.table.selection()

            if selection:
                self.selected_index = int(
                    selection[0]
                )

        if self.selected_index is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a holding first.",
            )
            return

        stock = self.portfolio[
            self.selected_index
        ]["stock"]

        confirm = messagebox.askyesno(
            "Remove Holding",
            f"Remove {stock} from the portfolio?",
        )

        if not confirm:
            return

        del self.portfolio[
            self.selected_index
        ]

        self.selected_index = None

        self.refresh_all()

        self.status_bar.config(
            text=f"{stock} removed successfully"
        )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_portfolio(self):
        """Clear entire portfolio."""

        if not self.portfolio:
            return

        confirm = messagebox.askyesno(
            "Clear Portfolio",
            "Are you sure you want to clear the portfolio?",
        )

        if confirm:
            self.portfolio.clear()

            self.selected_index = None

            self.refresh_all()

            self.status_bar.config(
                text="Portfolio cleared"
            )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_all(self):
        """Refresh every dashboard component."""

        self.refresh_table()
        self.update_statistics()
        self.draw_donut()

    def refresh_table(self):
        """Refresh holdings table with search filter."""

        for row in self.table.get_children():
            self.table.delete(row)

        query = self.search_var.get().strip().upper()

        total = calculate_total(
            self.portfolio
        )

        for index, item in enumerate(
            self.portfolio
        ):

            if query and query not in item["stock"]:
                continue

            percentage = (
                item["investment"]
                / total
                * 100
                if total
                else 0
            )

            self.table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    item["stock"],
                    item["quantity"],
                    f"${item['price']:,.2f}",
                    f"${item['investment']:,.2f}",
                    f"{percentage:.1f}%",
                ),
            )

    # ========================================================
    # STATISTICS
    # ========================================================

    def update_statistics(self):
        """Update dashboard statistics."""

        total = calculate_total(
            self.portfolio
        )

        holdings = len(
            self.portfolio
        )

        shares = sum(
            item["quantity"]
            for item in self.portfolio
        )

        average = (
            total / holdings
            if holdings
            else 0
        )

        self.total_value.config(
            text=f"${total:,.2f}"
        )

        self.total_holdings.config(
            text=str(holdings)
        )

        self.total_shares.config(
            text=f"{shares:,}"
        )

        self.average_value.config(
            text=f"${average:,.2f}"
        )

    # ========================================================
    # DONUT
    # ========================================================

    def draw_donut(self):
        """Draw colourful portfolio allocation donut."""

        self.chart_canvas.delete("all")

        if not self.portfolio:
            width = max(
                self.chart_canvas.winfo_width(),
                280,
            )

            height = max(
                self.chart_canvas.winfo_height(),
                220,
            )

            cx = width // 2
            cy = height // 2

            radius = 70

            self.chart_canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline=self.colors["border"],
                width=28,
            )

            self.chart_canvas.create_text(
                cx,
                cy,
                text="No Holdings",
                fill=self.colors["muted"],
                font=("Segoe UI", 11, "bold"),
            )

            return

        total = calculate_total(
            self.portfolio
        )

        width = max(
            self.chart_canvas.winfo_width(),
            280,
        )

        height = max(
            self.chart_canvas.winfo_height(),
            220,
        )

        cx = width // 2
        cy = height // 2

        radius = min(
            width,
            height,
        ) // 2 - 30

        colors = [
            "#2563EB",
            "#7C3AED",
            "#EC4899",
            "#F97316",
            "#14B8A6",
            "#22C55E",
            "#EAB308",
            "#06B6D4",
        ]

        start_angle = 0

        for index, item in enumerate(
            self.portfolio
        ):

            extent = (
                item["investment"]
                / total
                * 360
            )

            self.chart_canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start_angle,
                extent=extent,
                fill=colors[
                    index % len(colors)
                ],
                outline=self.colors["card"],
                width=2,
            )

            start_angle += extent

        inner_radius = radius - 32

        self.chart_canvas.create_oval(
            cx - inner_radius,
            cy - inner_radius,
            cx + inner_radius,
            cy + inner_radius,
            fill=self.colors["card"],
            outline=self.colors["card"],
        )

        self.chart_canvas.create_text(
            cx,
            cy - 8,
            text=f"${total:,.0f}",
            fill=self.colors["text"],
            font=("Segoe UI", 16, "bold"),
        )

        self.chart_canvas.create_text(
            cx,
            cy + 15,
            text="Total Value",
            fill=self.colors["muted"],
            font=("Segoe UI", 8, "bold"),
        )

    # ========================================================
    # SEARCH
    # ========================================================

    # Search is automatically handled through
    # self.search_var.trace_add() in create_table().

    # ========================================================
    # THEME
    # ========================================================

    def toggle_theme(self):
        """Switch between light and dark themes."""

        self.theme_name = (
            "dark"
            if self.theme_name == "light"
            else "light"
        )

        self.colors = (
            DARK_THEME
            if self.theme_name == "dark"
            else LIGHT_THEME
        )

        portfolio_copy = [
            item.copy()
            for item in self.portfolio
        ]

        search_text = self.search_var.get()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.portfolio = portfolio_copy
        self.selected_index = None

        self.root.configure(
            bg=self.colors["background"]
        )

        self.create_styles()
        self.create_header()
        self.create_statistics()
        self.create_input_area()
        self.create_portfolio_area()
        self.create_status_bar()

        self.search_var.set(
            search_text
        )

        self.refresh_all()

    # ========================================================
    # SAVE TXT
    # ========================================================

    def save_txt(self):
        """Export portfolio as a text report."""

        if not self.portfolio:
            messagebox.showwarning(
                "Empty Portfolio",
                "Add at least one stock before saving.",
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Save Portfolio Report",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        total = calculate_total(
            self.portfolio
        )

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "STOCK PORTFOLIO TRACKER PRO\n"
            )

            file.write(
                "=" * 60 + "\n\n"
            )

            for item in self.portfolio:

                file.write(
                    f"{item['stock']}: "
                    f"{item['quantity']} shares × "
                    f"${item['price']:.2f} = "
                    f"${item['investment']:.2f}\n"
                )

            file.write(
                "\n" + "=" * 60 + "\n"
            )

            file.write(
                f"TOTAL INVESTMENT: ${total:.2f}\n"
            )

        messagebox.showinfo(
            "Saved",
            "Portfolio report saved successfully.",
        )

    # ========================================================
    # SAVE CSV
    # ========================================================

    def save_csv(self):
        """Export portfolio as CSV."""

        if not self.portfolio:
            messagebox.showwarning(
                "Empty Portfolio",
                "Add at least one stock before saving.",
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Save Portfolio CSV",
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        total = calculate_total(
            self.portfolio
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Stock",
                    "Quantity",
                    "Price",
                    "Investment",
                    "Portfolio %",
                ]
            )

            for item in self.portfolio:

                percentage = (
                    item["investment"]
                    / total
                    * 100
                )

                writer.writerow(
                    [
                        item["stock"],
                        item["quantity"],
                        f"{item['price']:.2f}",
                        f"{item['investment']:.2f}",
                        f"{percentage:.1f}%",
                    ]
                )

            writer.writerow([])

            writer.writerow(
                [
                    "TOTAL",
                    "",
                    "",
                    f"{total:.2f}",
                    "100.0%",
                ]
            )

        messagebox.showinfo(
            "Saved",
            "Portfolio CSV saved successfully.",
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():
    """Start the application."""

    root = tk.Tk()

    StockPortfolioApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()