set -x
source config/common.sh

configure_script

check_skip "$1" "$2" "lab_5_scrapper"

python admin_utils/config_param_changer.py --config_path="lab_5_scrapper/scrapper_config.json"

echo "Changed config params"

python lab_5_scrapper/scrapper.py

check_if_failed

echo "Collected dataset"

ls -la tmp/articles
