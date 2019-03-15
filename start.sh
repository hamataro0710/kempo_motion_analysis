# git clone --recursive https://github.com/hamataro0710/kempo-motion-analysis.git
apt-get install swig
apt-get install ffmpeg
cd kempo-motion-analysis/
mv tf-pose-estimation/* .
# cd tf_pose_estimation
pip install -r requirements.txt
bash ./models/graph/cmu/download.sh
cd tf_pose/pafprocess/
swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
cd ../..