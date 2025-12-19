#!/usr/bin/env python3
"""
Statement viewer - converts FIO statements JSON to HTML table and terminal display.

Usage:
    uv run fioview tmp/statements.json
    uv run fioview tmp/statements.json --locale cs_CZ
    uv run fioview tmp/statements.json --no-terminal
"""

import argparse
import json
import locale
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def format_symbol(value: str | int | None) -> str:
    """Format symbol (VS, SS, KS) into groups of 3 digits."""
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    # Remove leading zeros for display but keep grouping
    s = s.lstrip("0") or "0"
    # Group from right to left in groups of 3
    result = []
    while len(s) > 3:
        result.insert(0, s[-3:])
        s = s[:-3]
    if s:
        result.insert(0, s)
    return " ".join(result)


def format_date(timestamp_ms: int | None, locale_name: str) -> str:
    """Format timestamp to locale-appropriate date string."""
    if timestamp_ms is None:
        return ""
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    if locale_name.startswith("cs"):
        return dt.strftime("%d.%m.%Y")
    else:
        return dt.strftime("%m/%d/%Y")


def format_amount(amount: float | None, locale_name: str) -> str:
    """Format amount with locale-appropriate decimal separator."""
    if amount is None:
        return ""
    if locale_name.startswith("cs"):
        # Czech format: 1 234,56
        formatted = f"{amount:,.2f}"
        # Swap , and . for Czech format
        formatted = formatted.replace(",", " ").replace(".", ",")
        return formatted
    else:
        # US format: 1,234.56
        return f"{amount:,.2f}"


def get_column_value(transaction: dict, col_id: int) -> Any:
    """Extract value from transaction column by ID."""
    key = f"column{col_id}"
    col = transaction.get(key)
    if col is None:
        return None
    return col.get("value")


def get_column_name(transaction: dict, col_id: int) -> str:
    """Extract column name from transaction."""
    key = f"column{col_id}"
    col = transaction.get(key)
    if col is None:
        return f"Col{col_id}"
    return col.get("name", f"Col{col_id}")


# Column definitions: (id, display_name_cs, display_name_en, is_priority)
COLUMNS = [
    (0, "Datum", "Date", True),
    (1, "Objem", "Amount", True),
    (5, "VS", "VS", True),
    (6, "SS", "SS", True),
    (4, "KS", "KS", True),
    (7, "Uživatelská identifikace", "User ID", True),
    (14, "Měna", "Currency", False),
    (8, "Typ", "Type", False),
    (2, "Protiúčet", "Counter Account", False),
    (3, "Kód banky", "Bank Code", False),
    (12, "Název banky", "Bank Name", False),
    (22, "ID pohybu", "Movement ID", False),
    (17, "ID pokynu", "Instruction ID", False),
]


def extract_row(transaction: dict, locale_name: str) -> dict:
    """Extract a row of data from transaction."""
    row = {}
    for col_id, name_cs, name_en, _ in COLUMNS:
        value = get_column_value(transaction, col_id)
        name = name_cs if locale_name.startswith("cs") else name_en

        if col_id == 0:  # Date
            row[name] = format_date(value, locale_name)
        elif col_id == 1:  # Amount
            row[name] = format_amount(value, locale_name)
        elif col_id in (4, 5, 6):  # KS, VS, SS
            row[name] = format_symbol(value)
        else:
            row[name] = str(value) if value is not None else ""

    return row


def generate_html(data: dict, locale_name: str) -> str:
    """Generate HTML table from statement data."""
    info = data.get("accountStatement", {}).get("info", {})
    transactions = (
        data.get("accountStatement", {})
        .get("transactionList", {})
        .get("transaction", [])
    )

    # Header names based on locale
    headers = [
        (name_cs if locale_name.startswith("cs") else name_en)
        for _, name_cs, name_en, _ in COLUMNS
    ]

    # Build rows
    rows = []
    for trans in transactions:
        row = extract_row(trans, locale_name)
        rows.append([row.get(h, "") for h in headers])

    # CSS styles with light/dark theme support
    css = """
    <style>
        * { box-sizing: border-box; }

        /* Light theme (default) */
        :root {
            --bg-primary: #f8f9fa;
            --bg-secondary: #ffffff;
            --bg-table: #ffffff;
            --bg-header: linear-gradient(180deg, #e3f2fd 0%, #f5f5f5 100%);
            --bg-row-even: #f8f9fa;
            --bg-hover: #e3f2fd;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --text-muted: #adb5bd;
            --border-color: #dee2e6;
            --border-light: #e9ecef;
            --accent: #0077b6;
            --shadow: rgba(0, 0, 0, 0.1);
            --col-date: #2d6a4f;
            --col-amount-pos: #198754;
            --col-amount-neg: #dc3545;
            --col-vs: #7c3aed;
            --col-ss: #0891b2;
            --col-ks: #d97706;
            --col-message: #92400e;
            --col-type: #0369a1;
            --col-account: #4b5563;
            --col-id: #9ca3af;
        }

        /* Dark theme */
        [data-theme="dark"] {
            --bg-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            --bg-secondary: rgba(255, 255, 255, 0.05);
            --bg-table: rgba(255, 255, 255, 0.02);
            --bg-header: linear-gradient(180deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 212, 255, 0.1) 100%);
            --bg-row-even: rgba(255, 255, 255, 0.02);
            --bg-hover: rgba(0, 212, 255, 0.08);
            --text-primary: #e8e8e8;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --border-color: rgba(255, 255, 255, 0.1);
            --border-light: rgba(255, 255, 255, 0.05);
            --accent: #00d4ff;
            --shadow: rgba(0, 0, 0, 0.3);
            --col-date: #a8e6cf;
            --col-amount-pos: #2ecc71;
            --col-amount-neg: #e74c3c;
            --col-vs: #c4b5fd;
            --col-ss: #67e8f9;
            --col-ks: #fbbf24;
            --col-message: #fcd34d;
            --col-type: #87ceeb;
            --col-account: #b8b8b8;
            --col-id: #666;
        }

        body {
            font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
            transition: background 0.3s ease, color 0.3s ease;
        }
        .container {
            max-width: 1600px;
            margin: 0 auto;
        }
        .header-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }
        h1 {
            text-align: center;
            color: var(--accent);
            font-weight: 300;
            font-size: 2.5rem;
            margin: 0;
            letter-spacing: 0.1em;
        }
        [data-theme="dark"] h1 {
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }
        .subtitle {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }

        /* Theme toggle switch */
        .theme-toggle {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
        }
        .theme-toggle button {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px var(--shadow);
        }
        .theme-toggle button:hover {
            transform: scale(1.1);
        }
        .theme-toggle .icon-light { display: block; }
        .theme-toggle .icon-dark { display: none; }
        [data-theme="dark"] .theme-toggle .icon-light { display: none; }
        [data-theme="dark"] .theme-toggle .icon-dark { display: block; }

        .account-info {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
        }
        .account-info div {
            padding: 0.5rem;
        }
        .account-info .label {
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        .account-info .value {
            color: var(--accent);
            font-size: 1.1rem;
            font-weight: 500;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }
        .table-wrapper {
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 8px 32px var(--shadow);
            border: 1px solid var(--border-color);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-table);
            font-size: 0.9rem;
        }
        th {
            background: var(--bg-header);
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            padding: 1rem 0.75rem;
            text-align: left;
            border-bottom: 2px solid var(--border-color);
            position: sticky;
            top: 0;
            white-space: nowrap;
        }
        td {
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-light);
            vertical-align: top;
            white-space: nowrap;
        }
        tr:hover {
            background: var(--bg-hover);
        }
        tr:nth-child(even) {
            background: var(--bg-row-even);
        }
        tr:nth-child(even):hover {
            background: var(--bg-hover);
        }
        .col-date { white-space: nowrap; color: var(--col-date); font-weight: 500; }
        .col-amount {
            text-align: right;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            white-space: nowrap;
            font-weight: 600;
        }
        .col-amount.positive { color: var(--col-amount-pos); }
        .col-amount.negative { color: var(--col-amount-neg); }
        .col-vs {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: var(--col-vs);
            text-align: right;
            font-weight: 500;
        }
        .col-ss {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: var(--col-ss);
            text-align: right;
            font-weight: 500;
        }
        .col-ks {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: var(--col-ks);
            text-align: right;
            font-weight: 500;
        }
        .col-message {
            max-width: 300px;
            color: var(--col-message);
        }
        .col-type { color: var(--col-type); }
        .col-account {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: var(--col-account);
        }
        .col-id {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: var(--col-id);
            font-size: 0.8rem;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            color: var(--text-muted);
            font-size: 0.8rem;
        }
        .count {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }

        /* Legend for symbol colors */
        .legend {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
            font-size: 0.85rem;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .legend-dot.vs { background: var(--col-vs); }
        .legend-dot.ss { background: var(--col-ss); }
        .legend-dot.ks { background: var(--col-ks); }
    </style>
    """

    # JavaScript for theme toggle
    js = """
    <script>
        (function() {
            // Check for saved theme preference or default to light
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);

            function toggleTheme() {
                const current = document.documentElement.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                document.documentElement.setAttribute('data-theme', next);
                localStorage.setItem('theme', next);
            }

            // Expose function globally
            window.toggleTheme = toggleTheme;
        })();
    </script>
    """

    # Account info section
    account_html = f"""
    <div class="account-info">
        <div>
            <div class="label">{"Číslo účtu" if locale_name.startswith("cs") else "Account"}</div>
            <div class="value">{info.get('accountId', 'N/A')}/{info.get('bankId', '')}</div>
        </div>
        <div>
            <div class="label">IBAN</div>
            <div class="value">{info.get('iban', 'N/A')}</div>
        </div>
        <div>
            <div class="label">{"Měna" if locale_name.startswith("cs") else "Currency"}</div>
            <div class="value">{info.get('currency', 'N/A')}</div>
        </div>
        <div>
            <div class="label">{"Počáteční zůstatek" if locale_name.startswith("cs") else "Opening Balance"}</div>
            <div class="value">{format_amount(info.get('openingBalance'), locale_name)}</div>
        </div>
        <div>
            <div class="label">{"Konečný zůstatek" if locale_name.startswith("cs") else "Closing Balance"}</div>
            <div class="value">{format_amount(info.get('closingBalance'), locale_name)}</div>
        </div>
    </div>
    """

    # Table header
    header_html = "<tr>\n"
    for h in headers:
        header_html += f"        <th>{h}</th>\n"
    header_html += "      </tr>"

    # Table rows
    rows_html = ""
    for trans in transactions:
        row = extract_row(trans, locale_name)
        rows_html += "      <tr>\n"
        for i, (col_id, name_cs, name_en, _) in enumerate(COLUMNS):
            h = name_cs if locale_name.startswith("cs") else name_en
            val = row.get(h, "")

            # Determine CSS class - distinct colors for VS, SS, KS
            if col_id == 0:
                cls = "col-date"
            elif col_id == 1:
                amount_val = get_column_value(trans, 1)
                if amount_val is not None and amount_val < 0:
                    cls = "col-amount negative"
                else:
                    cls = "col-amount positive"
            elif col_id == 5:  # VS - purple
                cls = "col-vs"
            elif col_id == 6:  # SS - cyan
                cls = "col-ss"
            elif col_id == 4:  # KS - amber/orange
                cls = "col-ks"
            elif col_id == 7:
                cls = "col-message"
            elif col_id == 8:
                cls = "col-type"
            elif col_id in (2, 3):
                cls = "col-account"
            elif col_id in (22, 17):
                cls = "col-id"
            else:
                cls = ""

            rows_html += f'        <td class="{cls}">{val}</td>\n'
        rows_html += "      </tr>\n"

    # Legend labels
    legend_vs = "Variabilní symbol" if locale_name.startswith("cs") else "Variable Symbol"
    legend_ss = "Specifický symbol" if locale_name.startswith("cs") else "Specific Symbol"
    legend_ks = "Konstantní symbol" if locale_name.startswith("cs") else "Constant Symbol"

    html = f"""<!DOCTYPE html>
<html lang="{locale_name[:2]}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{"Výpis transakcí" if locale_name.startswith("cs") else "Transaction Statement"}</title>
    {js}
    {css}
</head>
<body>
    <div class="theme-toggle">
        <button onclick="toggleTheme()" title="{"Přepnout téma" if locale_name.startswith("cs") else "Toggle theme"}">
            <span class="icon-light">🌙</span>
            <span class="icon-dark">☀️</span>
        </button>
    </div>
    <div class="container">
        <h1>{"💳 Výpis transakcí" if locale_name.startswith("cs") else "💳 Transaction Statement"}</h1>
        <div class="subtitle">FIO Banking API Emulator</div>
        {account_html}
        <div class="count">{len(transactions)} {"transakcí" if locale_name.startswith("cs") else "transactions"}</div>
        <div class="legend">
            <div class="legend-item"><span class="legend-dot vs"></span> {legend_vs} (VS)</div>
            <div class="legend-item"><span class="legend-dot ss"></span> {legend_ss} (SS)</div>
            <div class="legend-item"><span class="legend-dot ks"></span> {legend_ks} (KS)</div>
        </div>
        <div class="table-wrapper">
            <table>
                <thead>
                    {header_html}
                </thead>
                <tbody>
{rows_html}
                </tbody>
            </table>
        </div>
        <div class="footer">
            {"Vygenerováno" if locale_name.startswith("cs") else "Generated"}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
</body>
</html>
"""
    return html


def print_terminal_table(data: dict, locale_name: str):
    """Print transaction table to terminal with colors."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.text import Text
    except ImportError:
        print(
            "Warning: 'rich' library not installed. Terminal output disabled.",
            file=sys.stderr,
        )
        print("Install with: uv add rich", file=sys.stderr)
        return

    transactions = (
        data.get("accountStatement", {})
        .get("transactionList", {})
        .get("transaction", [])
    )

    console = Console()
    terminal_width = shutil.get_terminal_size().columns

    # Priority columns for terminal display
    priority_cols = [(col_id, name_cs, name_en) for col_id, name_cs, name_en, is_priority in COLUMNS if is_priority]

    # Create table
    title = "📊 Výpis transakcí" if locale_name.startswith("cs") else "📊 Transaction Statement"
    table = Table(title=title, show_header=True, header_style="bold cyan", border_style="dim")

    # Add columns with distinct colors for VS, SS, KS (right-aligned)
    for col_id, name_cs, name_en, _ in COLUMNS:
        if not any(c[0] == col_id for c in priority_cols):
            continue
        name = name_cs if locale_name.startswith("cs") else name_en

        if col_id == 1:  # Amount - right align
            table.add_column(name, justify="right", style="green", no_wrap=True)
        elif col_id == 0:  # Date
            table.add_column(name, style="bright_green", no_wrap=True)
        elif col_id == 5:  # VS - purple/magenta, right-aligned
            table.add_column(name, justify="right", style="magenta", no_wrap=True)
        elif col_id == 6:  # SS - cyan, right-aligned
            table.add_column(name, justify="right", style="cyan", no_wrap=True)
        elif col_id == 4:  # KS - yellow/gold, right-aligned
            table.add_column(name, justify="right", style="yellow", no_wrap=True)
        elif col_id == 7:  # Message
            table.add_column(name, style="bright_yellow", max_width=40, overflow="ellipsis", no_wrap=True)
        else:
            table.add_column(name, no_wrap=True)

    # Add rows with colored symbols
    for trans in transactions:
        row = extract_row(trans, locale_name)
        row_values = []

        for col_id, name_cs, name_en, _ in COLUMNS:
            if not any(c[0] == col_id for c in priority_cols):
                continue
            name = name_cs if locale_name.startswith("cs") else name_en
            val = row.get(name, "")

            # Apply distinct colors to each column type
            if col_id == 1:  # Amount coloring
                amount_val = get_column_value(trans, 1)
                if amount_val is not None and amount_val < 0:
                    val = Text(val, style="red")
                else:
                    val = Text(val, style="green")
            elif col_id == 5:  # VS - purple/magenta
                val = Text(val, style="magenta")
            elif col_id == 6:  # SS - cyan
                val = Text(val, style="cyan")
            elif col_id == 4:  # KS - yellow
                val = Text(val, style="yellow")

            row_values.append(val)

        table.add_row(*row_values)

    console.print()
    console.print(table)
    console.print()

    # Summary
    info = data.get("accountStatement", {}).get("info", {})
    summary_label = "Transakcí" if locale_name.startswith("cs") else "Transactions"
    balance_label = "Konečný zůstatek" if locale_name.startswith("cs") else "Closing Balance"
    console.print(
        f"[dim]{summary_label}: {len(transactions)} | "
        f"{balance_label}: {format_amount(info.get('closingBalance'), locale_name)} {info.get('currency', '')}[/dim]"
    )
    console.print()


def main():
    parser = argparse.ArgumentParser(
        description="View FIO statement JSON as HTML table and terminal output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run fioview tmp/statements.json
  uv run fioview tmp/statements.json --locale cs_CZ
  uv run fioview tmp/statements.json --no-terminal
  uv run fioview tmp/statements.json --no-html
        """,
    )
    parser.add_argument("input_file", type=Path, help="Input JSON file with statements")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output HTML file (default: same as input with .html extension)",
    )
    parser.add_argument(
        "-l", "--locale",
        default="cs_CZ",
        choices=["cs_CZ", "en_US"],
        help="Locale for date/number formatting (default: cs_CZ)",
    )
    parser.add_argument(
        "--no-terminal",
        action="store_true",
        help="Skip terminal table output",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML file generation",
    )

    args = parser.parse_args()

    # Read input file
    input_path = args.input_file
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    output_path = args.output or input_path.with_suffix(".html")

    # Generate HTML
    if not args.no_html:
        html = generate_html(data, args.locale)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ HTML saved to: {output_path}")

    # Print terminal table
    if not args.no_terminal:
        print_terminal_table(data, args.locale)


if __name__ == "__main__":
    main()

