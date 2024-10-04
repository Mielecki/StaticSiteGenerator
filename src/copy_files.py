import os
import shutil

def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    
    if not os.path.exists("static"):
        return

    def traverse(src_path, dst_path):
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            return
        if dst_path != "public":
            os.mkdir(dst_path)

        for item in os.listdir(src_path):
            curr_path = os.path.join(src_path, item)
            curr_dst_path = os.path.join(dst_path, item)
            traverse(curr_path, curr_dst_path)
    
    traverse("static", "public")