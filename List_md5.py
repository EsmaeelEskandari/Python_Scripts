import hashlib, glob, csv, os

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
old_tarballs = glob.glob(old_dir+"/*.events")
new_tarballs = glob.glob(new_dir+"/*.events")
tarball_dict_new = {}
tarball_dict_old = {}

# for new_file in new_tarballs:
#     new_path = "./{1}".format(new_dir,new_file)
#     new_md5 = md5Checksum(new_path)
#     tarball_dict_new[new_md5] = new_path
#
# for old_file in old_tarballs:
#     old_path = "./{1}".format(old_dir,old_file)
#     old_md5 = md5Checksum(old_path)
#     tarball_dict_old[old_md5] = old_path
#
# w = csv.writer(open("output_new.csv", "w"))
# for key, val in tarball_dict_new.items():
#     w.writerow([key, val])
#
# v = csv.writer(open("output_old.csv", "w"))
# for key, val in tarball_dict_old.items():
#     v.writerow([key, val])

for key, val in csv.reader(open("output_new.csv")):
    tarball_dict_new[key] = val.split("/")[2]
for key, val in csv.reader(open("output_old.csv")):
    tarball_dict_old[key] = val.split("/")[2]

for key, value in tarball_dict_new.iteritems():
    new_filename = tarball_dict_new[key]
    if not tarball_dict_old.get(key): continue
    old_filename = tarball_dict_old[key]+"_1"
    #os.rename(new_filename, old_filename)
    
    