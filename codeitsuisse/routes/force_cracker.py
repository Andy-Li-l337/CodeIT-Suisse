import hashlib
for k in range(100):
    for j in range(10000):
        encodingstr = f"{k}::{10+0.001*j:.3f}"
        shaed_data = hashlib.sha256(
            encodingstr.encode('utf-8')).hexdigest()
        if str(shaed_data) == "2596a046bc67248a3c2602e09a51134afc35626bb4ed580db1a7c1618f4ce961":
            print("SOLUTION:", 312503, f"{10+0.001*j:.3f}", j, f"k={k}")
