import pickle, sys, os

train_dir = sys.argv[1]
files = os.listdir(train_dir)
count = 0
mean = 0
for file in files:
    data = pickle.load(open(os.path.join(train_dir, file), 'rb'))/4000
    count = count + 1
    mean = mean + data.mean()

mean = mean/count
var = 0
print("dataset mean is: ", mean)
for file in files:
    data = pickle.load(open(os.path.join(train_dir, file), 'rb'))/4000
    data = data*mean/data.mean()
    var = var + data.var()

var = var/count
print("dataset var is: ", var)