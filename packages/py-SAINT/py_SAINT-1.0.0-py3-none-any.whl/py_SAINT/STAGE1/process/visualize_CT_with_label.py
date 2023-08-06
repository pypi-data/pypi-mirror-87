# arg 1: input file in pickle, arg 2: output folder name
import pickle, sys, os
import matplotlib.pyplot as plt
filename = sys.argv[1]
output_dir = sys.argv[2]
data = pickle.load(open(filename, 'rb'))
colors = [[1, 0.44705882, 0], [0., 0.94117647, 0.], [0., 0., 1.], [0.64705882, 0.31372549, 0.25490196],
          [0.98039216, 0.50196078, 0.44705882]]
levels = [0.5, 1.5, 2.5, 3.5, 4.5]
image = data['image']
label = data['label']
max_num = label.max()
for i in range(image.shape[2]):
    plt.imshow(image[:, :, i], cmap="gray")
    plt.contour(label[:, :, i], levels=levels[:max_num], colors=colors[:max_num])
    plt.savefig(os.path.join(output_dir, str(i)+'.png'))
    plt.clf()
