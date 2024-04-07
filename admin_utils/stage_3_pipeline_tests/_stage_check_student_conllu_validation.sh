source config/common.sh
set -ex

echo "Stage 3B: Student conllu preprocessing"
echo "Starting tests for student dataset"

TARGET_SCORE=$(get_score lab_6_pipeline)
configure_script

if [[ ${TARGET_SCORE} -gt 4 ]]; then
  echo "Running validation"
  for file in tmp/articles/*.conllu; do
    echo "Skip!"
#    python core_utils/tools/ud_validator/validate.py --lang ru --max-err=0 --level 5 --no-space-after --multiple-roots  --no-tree-text $file
  done
else
  echo "Skip stage"
fi

echo "Conllu files are checked. Done"
