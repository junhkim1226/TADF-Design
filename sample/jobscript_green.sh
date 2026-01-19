source ~/.bashrc
conda activate TADFGen

python ./../sample.py \
  gpus=0 \
  name='GREEN' \
  exp_dir='./TADF/' \
  data_dir='./../data/TADF' \
  model_path='./../result/Trained_Model/Est_S1/trained_model.tar' \
  n_sample=1000 \
  generator.batch_size=512 \
  save_property=true \
  +condition.Est=0.1 \
  +condition.S1=2.23
