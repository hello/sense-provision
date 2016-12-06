import sys
import os
import subprocess

def convert(src, dst):
    cmd = " ".join(["sox", src, "-b 16", dst, "channels 1", "rate 16k"])
    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: this src dst"
        sys.exit(1)
    from_folder = os.path.abspath(sys.argv[1])
    to_folder = os.path.abspath(sys.argv[2])
    print "Converting files from \n%s \nto \n%s"%(from_folder, to_folder)
    src_files = [f for f in os.listdir(from_folder) if "wav" in f]
    for f in src_files:
        convert(os.path.join(from_folder, f), os.path.join(to_folder, f))


