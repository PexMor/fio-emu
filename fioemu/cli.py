#!/usr/bin/env python
"""CLI tool for generating random FIO bank statement JSON responses."""
import argparse
import json
import sys

from fioemu.generator import generate_statement


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate random FIO bank statement JSON responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--account-id",
        type=str,
        help="Account ID (10 digits, default: random)",
    )
    parser.add_argument(
        "--bank-id",
        type=str,
        help="Bank code (default: random from common Czech banks)",
    )
    parser.add_argument(
        "--currency",
        type=str,
        default="CZK",
        help="Currency code (default: CZK)",
    )
    parser.add_argument(
        "--date-from",
        type=str,
        help="Start date in YYYY-MM-DD format (default: 30 days ago)",
    )
    parser.add_argument(
        "--date-to",
        type=str,
        help="End date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--num-transactions",
        type=int,
        default=10,
        help="Number of transactions to generate (default: 10)",
    )
    parser.add_argument(
        "--min-amount",
        type=float,
        help="Minimum transaction amount (default: -10000)",
    )
    parser.add_argument(
        "--max-amount",
        type=float,
        help="Maximum transaction amount (default: 10000)",
    )
    parser.add_argument(
        "--opening-balance",
        type=float,
        help="Opening balance (default: 0.0)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output",
    )

    args = parser.parse_args()

    try:
        statement = generate_statement(
            account_id=args.account_id,
            bank_id=args.bank_id,
            currency=args.currency,
            date_from=args.date_from,
            date_to=args.date_to,
            num_transactions=args.num_transactions,
            min_amount=args.min_amount,
            max_amount=args.max_amount,
            opening_balance=args.opening_balance,
        )

        json_output = json.dumps(statement, indent=2 if args.pretty else None, ensure_ascii=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_output)
        else:
            print(json_output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
