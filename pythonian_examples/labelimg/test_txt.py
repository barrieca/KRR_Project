#test im2txt
#python run_inference.py --checkpoint_path=C:/labelimg/model.ckpt-1000000 --vocab_file=C:/labelimg/word_counts.txt --input_files=C:/labelimg/test1.jpg
import os

imgpath = "/Users/kezhenchen/Documents/im2txt/test1.jpg"
checkpoint = "/Users/kezhenchen/Documents/im2txt/model.ckpt-1000000"
vocab = "/Users/kezhenchen/Documents/im2txt/word_counts.txt"

os.system('CHECKPOINT_DIR="'+checkpoint+'"')
os.system('IMAGE_FILE="'+imgpath+'"')
os.system('VOCAB_FILE="'+vocab+'"')
os.system('/bazel-bin/im2txt/run_inference \
                 --checkpoint_path="C:/labelimg/model.ckpt-1000000" \
                                   --vocab_file="C:/labelimg/word_counts.txt" \
                                   --input_files="C:/labelimg/test1.jpg"')