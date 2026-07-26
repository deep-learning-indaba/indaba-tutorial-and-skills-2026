# Graph Neural Networks: Foundations and Applications for Real-World Networks

**Session leaders:**  Godbless James, Nataram Odumo, Nwandu Christian

## Summary

This tutorial introduces Graph Neural Networks (GNNs) from first principles, using
account-level fraud detection on mobile money transaction data as a running example.
Participants build a graph from raw transaction records, train a Graph Convolutional
Network, and compare it against a non-graph baseline to see what relational structure
actually contributes.

## How to run

Both notebooks are Colab-ready — dependencies install automatically in the first cell,
and the dataset downloads automatically (no manual upload required).

| Notebook | Description | |
|---|---|---|
| `GNN_Tutorial_Live.ipynb` | The live-session notebook: baseline → GCN → structure-only ablation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Whizz-tamie/indaba-tutorial-and-skills-2026/blob/add-gnn-tutorial-materials/practicals/graph-neural-networks/GNN_Tutorial_Live.ipynb) |
| `GNN_Tutorial_TakeHome.ipynb` | The full companion notebook: dataset EDA, subsampling rationale, GAT extension, exercises | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Whizz-tamie/indaba-tutorial-and-skills-2026/blob/add-gnn-tutorial-materials/practicals/graph-neural-networks/GNN_Tutorial_TakeHome.ipynb) |

## Slides

[`slides/DLI2026_GNNs_slidedeck.pdf`](slides/DLI2026_GNNs_slidedeck.pdf)

## Data

`data/momtsim_sample.csv` — a small, prepared sample (~50,000 transactions) of the
[Synthetic Mobile Money Transaction Dataset](https://data.mendeley.com/datasets/zhj366m53p/2)
(Azamuke, Katarahweire & Bainomugisha, Makerere University — CC BY 4.0). Generated with
`prepare_data.py`; see the take-home notebook for the full dataset citation and licensing
details.