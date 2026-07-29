"""
prepare_data.py

Run this ONCE, offline, before the tutorial — not during the session and not
by participants. It takes the full MoMTSim CSV (1.72M transactions, downloaded
manually from Mendeley: https://data.mendeley.com/datasets/zhj366m53p/1) and
produces a small, graph-ready teaching sample that gets committed to the
tutorial GitHub repo. The live and take-home notebooks both auto-download
this small file — nobody touches the 1.72M-row original during the session.

Usage:
    python prepare_data.py --input synthetic_mobile_money_transaction_dataset.csv \
                            --output momtsim_sample.csv

Output size target: roughly 4-5 MB so the wget in the notebooks is instant.

The current source CSV already contains steps 0-143. The step filter is kept
as a guardrail in case a longer MoMTSim export is used later.
"""
import argparse
import csv
import os
import random
from collections import Counter


REQUIRED_COLUMNS = {
    'step',
    'transactionType',
    'amount',
    'initiator',
    'oldBalInitiator',
    'newBalInitiator',
    'recipient',
    'oldBalRecipient',
    'newBalRecipient',
    'isFraud',
}


def build_sample(input_path: str, n_active_accounts: int = 3_000, max_edges: int = 50_000,
                  time_window_steps: int = 144) -> tuple[list[dict[str, str]], list[str]]:
    initiator_counts = Counter()

    # Keep the first 144 hourly simulation steps. For the current source CSV
    # this is the whole file, but this guard keeps longer exports comparable.
    with open(input_path, newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        missing_columns = REQUIRED_COLUMNS - set(fieldnames)
        if missing_columns:
            missing = ', '.join(sorted(missing_columns))
            raise ValueError(f'Missing required columns: {missing}')

        for row in reader:
            if int(row['step']) < time_window_steps:
                initiator_counts[row['initiator']] += 1

    # Start from the most active initiators so the sample contains repeated
    # account interactions. This is for a compact GNN teaching graph, not a
    # faithful reconstruction of complete account histories.
    top_initiators = set(
        account for account, _ in initiator_counts.most_common(n_active_accounts)
    )
    if not top_initiators:
        raise ValueError('No transactions found in the selected time window.')

    fraud_all = []
    legit_all = []
    with open(input_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['step']) >= time_window_steps:
                continue
            if row['initiator'] not in top_initiators:
                continue

            # Keep account identifiers as strings. csv.DictReader already gives
            # strings, and that is the desired representation for these columns.
            if int(row['isFraud']) == 1:
                fraud_all.append(row)
            else:
                legit_all.append(row)

    dense_count = len(fraud_all) + len(legit_all)

    if dense_count > max_edges:
        fraud_ratio = len(fraud_all) / dense_count
        n_fraud = min(int(round(max_edges * fraud_ratio)), len(fraud_all))
        n_legit = min(max_edges - n_fraud, len(legit_all))
        # Preserve the fraud rate of the active-account subset while reducing
        # the file to a notebook-friendly size.
        rng = random.Random(42)
        sample = rng.sample(fraud_all, n_fraud) + rng.sample(legit_all, n_legit)
        rng.shuffle(sample)
    else:
        sample = fraud_all + legit_all

    return sample, fieldnames


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to the full MoMTSim CSV')
    parser.add_argument('--output', default='momtsim_sample.csv')
    parser.add_argument('--n-active-accounts', type=int, default=3_000)
    parser.add_argument('--max-edges', type=int, default=50_000)
    args = parser.parse_args()

    sample, fieldnames = build_sample(args.input, args.n_active_accounts, args.max_edges)
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample)

    print(f"Wrote {len(sample):,} transactions to {args.output}")
    print(f"Unique initiators: {len({row['initiator'] for row in sample}):,}")
    print(f"Unique recipients: {len({row['recipient'] for row in sample}):,}")
    print(f"Fraud rate: {sum(int(row['isFraud']) for row in sample) / len(sample) * 100:.3f}%")
    print(f"File size target: check this manually before committing to the repo — "
          f"aim for roughly 4-5 MB so the wget in the notebooks is instant.")
