import hashlib, glob

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
        
old_dir = "old_tarballs"
new_dir = "new_tarballs"
old_tarballs = glob.glob(old_dir+"/*.tar.gz")
new_tarballs = glob.glob(new_dir+"/*.tar.gz")
tarball_dict_new = []
tarball_dict_old = []

for new_file in new_tarballs:
    new_path = "./{0}".format(new_dir)
    for old_file in old_tarballs:
        old_path = "./{0}".format(old_dir)
        new_md5 = md5Checksum(new_path)
        old_md5 = md5Checksum(old_path)
        if old_md5 == new_md5:
            print "{0}:{1}".format(new_file,old_file)
            tarball_dict_new.append(new_file)
            tarball_dict_old.append(old_file)
            old_tarballs.remove(old_file)
            continue

if len(tarball_dict_new) == len(tarball_dict_old):
    tarball_dict = dict(zip(tarball_dict_new,tarball_dict_old))
    print tarball_dict
else:
    print "tarball_dict_new and tarball_dict_old are not the same size!!"
    print "Tarball_dict_new:\n", tarball_dict_new, "\n"
    print "Tarball_dict_old:\n", tarball_dict_old