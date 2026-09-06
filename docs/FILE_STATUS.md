# File Status

| Path/group | Purpose | Status | Upstream/downstream | Safe to modify/delete? |
|---|---|---|---|---|
| `data/raw/` | FAOSTAT sources | LOCKED | source → pipeline | no/no |
| `data/processed/foodshield/*.csv` | analytical outputs | LOCKED | pipeline → reports/API | no/no |
| `src/data/`, `src/exposure/`, `src/network/`, `src/shock/`, `src/replacement/` | reproducible pipeline stages | REPRODUCIBLE | data → outputs | caution/no |
| `src/analysis/`, `src/visualization/` | synthesis and figures | REPRODUCIBLE | outputs → reports | caution/no |
| `backend/` | API/data presentation | ACTIVE | validated CSVs → frontend | caution/no |
| `frontend/src/` | dashboard UI | ACTIVE | API → user | yes, with UI validation/no |
| `reports/` | final project record | DOCUMENTATION/LOCKED | outputs → submission | no/no |
| `scripts/` | operational checks | REPRODUCIBLE | CSV/API → validation | caution/no |
| `scratch/` | experiments/historical tree | DEVELOPMENT | none | yes/no until reviewed |
| `frontend/dist/`, caches | local build output | GENERATED | frontend source → build | no/yes |

`scratch/test_sens.py`, `scratch/test_script.py`, and `scratch/project_tree.md` are retained for review: unreferenced by production code but not judged safe to remove.
