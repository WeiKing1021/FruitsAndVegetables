# 使用Anaconda來建立環境
> conda create --name fruits-and-vegetables python=3.7.13

# 進入已建立的Python環境
> activate fruits-and-vegetables

# 查看目前已安裝的套件版本
> conda list

# 匯出所有安裝的套件
> pip freeze > requirements.txt
> pip list --format=freeze > requirements.txt

# 匯入所有安裝的套件
> pip3 install -r requirements.txt

# 執行伺服器
> python ./server.py

# 其他注意事項
> 1. 需要安裝 NVIDIA CUDA 來使 Tensorflow 使用 GPU (我後來安裝完後還是不能用，結果在那邊用CPU跑學習)