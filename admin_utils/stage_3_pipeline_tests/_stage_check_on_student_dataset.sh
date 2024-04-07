source config/common.sh
set -ex

echo -e '\n'
echo "Check processing on student dataset"

TARGET_SCORE=$(get_score lab_6_pipeline)
configure_script

if [[ ${TARGET_SCORE} != 0 ]]; then
  python admin_utils/unpack_archived_dataset.py lab_6_pipeline
  python lab_6_pipeline/pipeline.py
  ls -la tmp/articles
else
  echo "Skip stage"
fi
