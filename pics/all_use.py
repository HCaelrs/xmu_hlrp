import os
for i in range(9):
    os.system(f"cd {i} && python3 test.py")
    
for i in range(9):
    os.system(f"cp {i}/{i}.npy ../pic_arr")