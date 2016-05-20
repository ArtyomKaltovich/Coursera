import os, sys
from skimage.io import imread
from skimage import img_as_float
from sklearn.cluster import KMeans
from matplotlib.pyplot import imsave
from numpy import mean, median, array, copy, log10
from concurrent.futures import ProcessPoolExecutor, wait
PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def clusterize(n_clusters, floats, x, y):
	clf = KMeans(n_clusters=n_clusters, init='k-means++', random_state=241, n_jobs=-1)
	clusters = clf.fit_predict(floats)
	clusters = clusters.reshape(x,y)
	#print(' '.join(map(str, clusters)))
	return clusters


def find_mean(n_clusters, clusters, floats, x, y, fn):
	means = array([[0.,]*3]*n_clusters)
	for i in range(n_clusters):
		for color in range(3):
			#print(' '.join(map(str, floats[clusters==i,color])))
			means[i, color] = fn(floats[clusters==i,color])
	return means


def colorize(floats, clusters, means, x, y):
	_floats = copy(floats)
	for i in range(x):
		for j in range(y):
			for color in range(3):
				_floats[i,j,color] = means[clusters[i,j], color]
	return _floats


def PSNR(image1, image2):
	i1 = image1.reshape(image1.size)
	i2 = image2.reshape(image2.size)
	result = sum(map(lambda a,b: (a-b)**2, i1, i2))/len(i1)
	result = 10 * log10(1/result)
	return result


def psnr_and_save(floats, clusters, means, x, y, means_type):
	_floats = colorize(floats, clusters, means, x, y)
	imsave(arr=_floats, fname=directory + str(n) + '_' + means_type + '.jpg')
	psnr = PSNR(_floats, floats2D)
	print(str(n) + ' ' + means_type + ': ' + str(psnr))
	if psnr > 20.:
		io_yandex.print_result(str(n), '1.txt')
		sys.exit(0)


def one_step(n, floats, floats2D, x, y, directory):
	clusters = clusterize(n, floats2D, x, y)
	means = find_mean(n, clusters, floats, x, y, mean)
	psnr_and_save(floats, clusters, means, x, y, 'mean')
	medians = find_mean(n, clusters, floats, x, y, median)
	psnr_and_save(floats, clusters, medians, x, y, 'median')


image = imread('parrots.jpg')
#image = imread('lena.jpe')
directory = 'pics/'
if not os.path.exists(directory):
    os.makedirs(directory)
floats = img_as_float(image)
y = floats.shape[1]
x = floats.shape[0]
floats2D = floats.reshape((x*y,3))
#print(x, y, floats.shape)

futures = []
executor = ProcessPoolExecutor(8)
for n in range(1, 21):
	futures.append(executor.submit(
		one_step(n, floats, floats2D, x, y, directory)
	))
else:
	wait(futures)