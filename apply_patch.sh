#!/usr/bin/env bash
# Applies the retrieval pipeline patch.
#
# USAGE:
#   1. Put the 6 downloaded files (retriever.py, bm25_store.py, reranker.py,
#      query_transform.py, app.py, requirements.txt) in the SAME folder as
#      this script.
#   2. cd into your project root (the folder containing app.py and src/).
#   3. Run: bash apply_patch.sh /path/to/downloaded/files
#
# Example:
#   cd ~/projects/pdf-rag-chatbot
#   bash apply_patch.sh ~/Downloads

set -euo pipefail

SRC_DIR="${1:-.}"
PROJECT_ROOT="$(pwd)"

echo "Project root: $PROJECT_ROOT"
echo "Patch files from: $SRC_DIR"

if [ ! -f "$PROJECT_ROOT/app.py" ] || [ ! -d "$PROJECT_ROOT/src" ]; then
  echo "ERROR: run this from your project root (must contain app.py and src/)."
  exit 1
fi

# 1. Backup current files that will be overwritten
BACKUP_DIR="$PROJECT_ROOT/backup_before_patch_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$PROJECT_ROOT/app.py" "$BACKUP_DIR/"
cp "$PROJECT_ROOT/requirements.txt" "$BACKUP_DIR/"
echo "Backed up app.py and requirements.txt to $BACKUP_DIR"

# 2. Copy new files into src/
cp "$SRC_DIR/retriever.py"       "$PROJECT_ROOT/src/retriever.py"
cp "$SRC_DIR/bm25_store.py"      "$PROJECT_ROOT/src/bm25_store.py"
cp "$SRC_DIR/reranker.py"        "$PROJECT_ROOT/src/reranker.py"
cp "$SRC_DIR/query_transform.py" "$PROJECT_ROOT/src/query_transform.py"
echo "Copied 4 new files into src/"

# 3. Replace app.py and requirements.txt
cp "$SRC_DIR/app.py"             "$PROJECT_ROOT/app.py"
cp "$SRC_DIR/requirements.txt"   "$PROJECT_ROOT/requirements.txt"
echo "Replaced app.py and requirements.txt"

# 4. Install new dependency (rank_bm25) plus anything else missing
pip install -r "$PROJECT_ROOT/requirements.txt"

echo ""
echo "Patch applied. Run the app with:"
echo "  streamlit run app.py"
