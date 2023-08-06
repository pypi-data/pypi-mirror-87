"""模型保存加载路径"""
pre_trained = "pytorch.pth"
onnx_path = "pytorch.onnx"

"""hyperparameter"""
inputs_size = [[1, 28, 28]]  # 网络输入 list of list, no batch
train_batch = 4  # 训练 batch size
num_workers = 4  # 训练加载数据的cpu数量
epoch_range = [0, 100, 5]  # epoch设置 [起始, 终止, 间隔], 每个间隔会执行模型评估等
loss_avg_step = 10  # 每n个batch， 统计一次loss



