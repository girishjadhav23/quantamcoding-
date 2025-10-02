# wiper.py
import os
import time

def overwrite_file(file_path, passes=3):
    """Securely overwrite a file with random data"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    try:
        length = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            for p in range(1, passes + 1):
                print(f"🔄 Overwriting {file_path} [Pass {p}/{passes}]...")
                f.seek(0)
                f.write(os.urandom(length))
                f.flush()
                os.fsync(f.fileno())
        os.remove(file_path)
        print(f"✅ File securely wiped and deleted: {file_path}")
        return True
    except Exception as e:
        print(f"⚠️ Error wiping file {file_path}: {e}")
        return False


def wipe_multiple_files(file_list, passes=3, log_file="wipe_log.txt"):
    """Wipe multiple files and log the results"""
    with open(log_file, "a") as log:
        log.write(f"\n---- Secure Data Wipe Report ({time.ctime()}) ----\n")
        for file in file_list:
            result = overwrite_file(file, passes)
            status = "SUCCESS" if result else "FAILED"
            log.write(f"{file} --> {status}\n")
    print(f"\n📄 Wipe report saved to {log_file}")
