## EPIC: Machine‑Learning Classifier Integration

*Augmenting `glyphsieve` with an ML‑powered **is_gpu** signal to close the last 2 % gap in normalization accuracy.*

---

### 🧠 Why This Matters

The current rule engine (regex + fuzzy + blacklist) already labels ≈ 10 k Shopify rows with **≈ 98 % precision** for identifying **NVIDIA GPUs**.  
Residual false‑positives and ‑negatives, however, still leak through and distort downstream scoring.  
A lightweight **binary classifier** will:

1. **Learn** from the existing `stage_normalized.csv` (~10530 rows).  
2. **Predict** whether a listing is a real **NVIDIA GPU** (ignoring Intel/AMD/others) when rules say `"UNKNOWN"`.  
3. **Emit** a confidence score that the pipeline can merge with rule signals for safer decisions.

The model **never overrides** deterministic matches — it only boosts confidence where rules are weak.

---

### 📦 Project Snapshot (2025‑07‑30)

| Capability                | Status / Location                                   |
|---------------------------|-----------------------------------------------------|
| Rule signals              | `regex`, `fuzzy`, manual allow/deny lists           |
| Labeled column            | `canonical_model` (`"UNKNOWN"` ⇒ not a GPU)         |
| Normalized dataset        | `tmp/work/stage_normalized.csv`                     |
| Python environment        | `uv` + Python 3.12 · scikit‑learn already installed |
| Model storage directory   | `models/` (new)                                     |
| CLI runner                | `uv run glyphsieve ...`                             |
| Safe long‑running process | `.junie/scripts/safe-run.sh`                        |
| Task dependencies         | Tasks 1 → 2 → 3 → 4 → 5 → 6 (+7 optional)           |
| Tests                     | `pytest` (unit) · full‑pipeline regression suite    |

> **Note:** For the purposes of this model, `is_gpu = True` means the listing is a recognized **NVIDIA GPU**. Intel, AMD, or unknown GPUs are treated as `is_gpu = False`.

---

### 🔭 Strategic Roadmap & Tasks

| # | Task ID                                              | What Junie must deliver                                                                                                                                                                                                                        | Key Outputs                               |
|---|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| 1 | **TASK.ml.01.extract-labeled-training-set**          | Build `training_set.csv` with columns `title`, `bulk_notes`, `is_gpu` (1 ⟺ `canonical_model != "UNKNOWN"` and is an NVIDIA GPU). 80 / 20 split → `train.csv`, `test.csv`.                                                                      | 2 CSV files under `glyphsieve/ml/data/`   |
| 2 | **TASK.ml.02.train-binary-gpu-classifier**           | Baseline pipeline **TF‑IDF → LogisticRegression**.<br>▪️ Hyper‑params via grid search.<br>▪️ Persist model to `models/gpu_classifier.pkl`.<br>▪️ Provide `glyphsieve/ml/train_gpu_classifier.py` + Typer CLI.                                  | Pickled model · `metrics.json` (train cv) |
| 3 | **TASK.ml.03.evaluate-on-testset**                   | Run model on `test.csv`.<br>▪️ Report **precision, recall, F1, ROC‑AUC**.<br>▪️ Write `evaluation_report.md` + `confusion_matrix.png` (matplotlib).<br>▪️ Dump top‑20 FP/FN rows to `fp_fn_sample.csv`.                                        | Markdown report + plots                   |
| 4 | **TASK.ml.04.integrate-ml-into-normalizer**          | New module `glyphsieve/ml_signal.py`:<br>```python<br>def predict_is_gpu(title: str, bulk_notes: str) -> tuple[bool, float]: ...<br>```<br>Add `--use-ml` flag to pipeline CLI. Append `ml_is_gpu`, `ml_score` columns in output when enabled. | Updated pipeline & docs                   |
| 5 | **TASK.ml.05.score-disagreement-cases**              | CLI `glyphsieve ml-disagreements` that writes `disagreements.csv` where:<br>▪️ Rules = `UNKNOWN` **and** `ml_is_gpu == 1` **OR**<br>▪️ Rules ≠ `UNKNOWN` **but** `ml_is_gpu == 0`.                                                             | CSV for analyst review                    |
| 6 | **TASK.ml.06.create-backfill-script**                | Script `glyphsieve ml-backfill` to batch‑update any normalized CSVs (folder in/out). Ensures backward‑compatible column order.                                                                                                                 | Backfilled files + CLI help               |
| 7 | **TASK.ml.07.plan-multiclass-categorizer** (stretch) | ADR‑style markdown outlining path to **multiclass** GPU‑family model: feature ideas, label sourcing, incremental rollout.                                                                                                                      | `docs/adr/ADR_ml_multiclass.md`           |

---

#### 🧩 Task Dependency Graph
Each task is expected to build on the outputs of the previous one. Do not begin downstream tasks until upstream artifacts exist:

1 → 2 → 3
      ↘
       4 → 5 → 6
               ↘
                7 (optional stretch)

Tasks 2–6 require the output of TASK.ml.01. Task 7 may only be started once classifier integration (TASK.ml.04) is stable.

### 🛠Execution Constraints & Guardrails

* **Offline, CPU‑only**—no cloud notebooks or CUDA dependencies.
* All ML code lives in **`glyphsieve/ml/`**; keep the rest of the project import‑free from heavy libs.
* **No Jupyter/IPython artifacts.** Pure `.py`, well‑tested.
* Model training must be runnable headlessly:

```bash
./.junie/scripts/safe-run.sh -n ml-train -b -- \
  uv run glyphsieve ml-train \
    --input tmp/work/stage_normalized.csv \
    --output models/gpu_classifier.pkl
```

- 	Append columns; never reorder or drop existing ones.
-	Add unit tests around feature extraction & prediction; expand existing pipeline tests.
-	Update pyproject.toml + uv sync --all-packages.

⸻

## ✅Definition of Done

1. Model artifacts (gpu_classifier.pkl, metrics.yaml) present or CI‑generated from TASK.ml.02 and evaluated in TASK.ml.03.
2. Pipeline run with --use-ml adds ml_is_gpu, ml_score and passes all regression tests.
3. Precision & recall ≥95% on held‑out test split.
4. disagreements.csv<3% of total rows.
5. pytest green, linters clean (ruff, flake8, GLS00X rules).
6. Updated docs & ADR committed.
7. All tasks completed in dependency order, with correct file and module references.

## 📜Process & Sequencing

```text
(1) extract → (2) train → (3) evaluate
      ↘
       (4) integrate → (5) disagreements → (6) backfill
                                         ↘
                                          (7) multiclass ADR (optional)
```

Create each task file in .junie/tasks/open/ using the IDs above. Close sequentially with completion summaries. Use
safe-run.sh for any process expected to run >30s.

Happy modeling, Junie‑Web & Goose‑ML! 🎉

---

### 📝 Retrospective (2025‑08‑01)

**What went well**
- *Agent autonomy* – Junie executed all seven tasks in a single session with zero manual hot‑fixes.
- *Model quality* – Title‑only V2 model reached **99 %+ precision / recall** on hold‑out data **and** generalized to the Perplexity dataset (≈86 % agreement → 100 % manual spot‑check accuracy).
- *Tooling* – `safe-run.sh`, YAML metrics, and the manual spot‑checker GUI formed a tight evaluation loop.
- *Integration* – `ml_is_gpu` and `ml_score` columns flow through the pipeline without breaking existing tests or CSV schemas.

**What surprised us**
- Bulk‑note features *reduced* generalization; removing them increased robustness.
- `TF‑IDF + LR` was “good enough”; no need for heavier embeddings… yet.
- The disagreement rate (13.8 %) surfaced genuine edge cases for future rule tuning.

**What could be better**
- No automated drift monitoring – a future cron should re‑evaluate metrics monthly.
- Training code still mixes CLI parsing and core logic; refactor into a service layer.
- Pickle chosen over joblib under time pressure; revisit serialization format.

**Follow‑on opportunities**
1. Ship `/api/ml/is_gpu` inference endpoint in `glyphd` for crawler use.
2. Automate disagreement sampling into a labeling UI (human‑in‑the‑loop).
3. Begin ADR for **multiclass** GPU‑family classifier (stretch task 7).
4. Explore on‑the‑fly active learning during live crawls (online fine‑tuning).

> *“Hot‑dog / not‑hot‑dog is now a micro‑service. Mission accomplished.”* 🍻