source ~/.bashrc
conda activate TADFGen

#### Train Config ####
NAME='Est_S1'
DATA_DIR='TADF'

#### Train Option ####
TRAIN_EPOCH=50
BATCH_SIZE=64
MAX_ATOMS=93

python ../train.py \
  name=$NAME \
  exp_dir='./'$DATA_DIR \
  data_dir='../data/'$DATA_DIR \
  condition.descriptors='[Est,S1]' \
  train.num_workers=4 \
  train.max_epoch=$TRAIN_EPOCH \
  data.train.batch_size=$BATCH_SIZE \
  data.train.sampler.n_sample=27427 \
  data.train.max_atoms=$MAX_ATOMS \
  data.val.batch_size=$BATCH_SIZE \
  data.val.max_atoms=$MAX_ATOMS
