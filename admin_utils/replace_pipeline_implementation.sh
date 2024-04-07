set -ex

ls -la lab_6_pipeline/
rm lab_6_pipeline/pipeline.py lab_6_pipeline/pos_frequency_pipeline.py
ls -la lab_6_pipeline/
mv lab_6_pipeline/stanza_pipeline.py lab_6_pipeline/pipeline.py
mv lab_6_pipeline/stanza_pos_frequency_pipeline.py lab_6_pipeline/pos_frequency_pipeline.py
ls -la lab_6_pipeline/
