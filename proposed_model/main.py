import os
import pprint
import tensorflow as tf

from model import model
from test import *


# Define flags
flags = tf.app.flags
flags.DEFINE_integer("epoch", 120, "Number of training epochs (default: 300)")
flags.DEFINE_integer("iter_per_epoch", 1000, "number of iteration per epoch(default: 1000)")#训练阶段，每个epoch迭代的次数
flags.DEFINE_float("learning_rate_D", 0.0001, "Learning rate of Adam optimizer for Discriminator (default: 0.0001)")
flags.DEFINE_float("learning_rate_G", 0.0001, "Learning rate of Adam optimizer for Generator (default: 0.0001)")
flags.DEFINE_float("learning_rate_E", 0.0001, "Learning rate of Adam optimizer for Encoder (default: 0.0001)")
flags.DEFINE_float("beta1D", 0.5, "Momentum term of Adam optimizer for Discriminator (default: 0.5)")
flags.DEFINE_float("beta1G", 0.5, "Momentum term of Adam optimizer for Generator (default: 0.5)")
flags.DEFINE_float("beta1E", 0.5, "Momentum term of Adam optimizer for Encoder (default: 0.5)")

flags.DEFINE_float("gpu_frac", 0.95, "Gpu fraction")
flags.DEFINE_float("tlw", 0.5, "True loss weight")
flags.DEFINE_float("flw", 0.5, "Fake loss weight")
flags.DEFINE_float("vi_weight", 0.01, "Weight of variational inference loss")

flags.DEFINE_integer("number_train_images", 1, "No. of labeled images for training")
flags.DEFINE_integer("number_train_unlab_images", 1, "No. of unlabeled images for training")
flags.DEFINE_integer("number_test_images", 2, "No. of images for testing")

#flags.DEFINE_string("data_directory", "../data/iSEG_preprocessed", "Directory name containing the dataset")
flags.DEFINE_string("train_dir_labeled", '../data/labeled',
                    "Directory name containing the dataset")#带标签数据训练集路径，要求该路径下包含两个子文件夹：CT和SegmentationLabel，两者里面放名字一一相同的npy文件
flags.DEFINE_string("train_dir_unlabeled", '../data/unlabeled', 
                    "Directory name containing the dataset")#无标签训练集,要求该路径下包含一个子文件夹CT，里面是npy格式的CT文件
flags.DEFINE_string("test_dir", '../data/test',
                    "Directory name containing the dataset")#带标签数据测试集（验证集）路径，要求该路径下包含两个子文件夹：CT和SegmentationLabel，两者里面放名字一一相同的npy文件
flags.DEFINE_string("checkpoint_dir", "checkpoint/current", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("best_checkpoint_dir", "checkpoint/best", "Directory name to save the best checkpoints [checkpoint]")
flags.DEFINE_string("results_dir", "results/", "Directory name to save the results [results]")
flags.DEFINE_string("validate_output_save_root","validate_output","predicted masks of validation dataset saved here")

flags.DEFINE_boolean("load_chkpt",False, "True for loading saved checkpoint")
flags.DEFINE_boolean("training", True, "True for Training ")
flags.DEFINE_boolean("testing", False, "True for Testing ")
flags.DEFINE_boolean("badGAN", False, "True if you want to run badGAN based model ")

flags.DEFINE_integer("batch_size", 4, "The size of batch images [64]")

flags.DEFINE_integer("num_mod", 1, "Number of modalities of the input 3-D image")
flags.DEFINE_integer("num_classes", 4, "Number of output classes to segment")
flags.DEFINE_integer("noise_dim", 200, "Dimension of noise vector")



FLAGS = flags.FLAGS

def main(_):
  # Create required directories
  if not os.path.exists(FLAGS.checkpoint_dir):
    os.makedirs(FLAGS.checkpoint_dir)

  if not os.path.exists(FLAGS.results_dir):
    os.makedirs(FLAGS.results_dir)

  if not os.path.exists(FLAGS.best_checkpoint_dir):
    os.makedirs(FLAGS.best_checkpoint_dir)


  # To configure the GPU fraction
  gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=FLAGS.gpu_frac)

  # Parameters of extracted training and testing patches
  patch_shape=(32,64,64)
  extraction_step=(8,8,8)
  testing_extraction_shape=(8,8,8)

  if FLAGS.training:
    # For training the network
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
      network = model(sess,patch_shape,extraction_step)
      network.build_model()
      network.train()
  if FLAGS.testing:
      # For testing the trained network
      test(patch_shape,testing_extraction_shape)


if __name__ == '__main__':
  tf.app.run()