import oss2
import fire

ENDPOINT = "https://oss-cn-shenzhen.aliyuncs.com"
ACCESS_KEY_ID = "LTAI4FtSM2t8UaGZSt5bczn8"
ACCESS_KEY_SECRET = "ZxiGRvHBMky2lXPAUyKXuNThxi4Q14"
BUCKET_NAME = "it-snail-dev"
PREFIX = "jumpserver/"
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def upload(*files):
    for name in files:
        with open(name, "rb") as fin:
            bucket.put_object(PREFIX + name, fin)


if __name__ == "__main__":
    fire.Fire()
