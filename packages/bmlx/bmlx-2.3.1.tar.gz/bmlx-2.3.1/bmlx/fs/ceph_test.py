import unittest
from bmlx.fs.ceph import CephFileSystem


class CephTest(unittest.TestCase):
    def setUp(self):
        self.ceph_fs = CephFileSystem()

    def tearDown(self):
        pass

    def testExistAndCephReadWriteSuccess(self):
        key = "http://fs-ceph-hk.bigo.sg/bmlx-pipeline/testing-key"
        self.ceph_fs.delete(key)
        # assert not exist
        self.assertFalse(self.ceph_fs.exists(key))

        with self.ceph_fs.open(key, "wb") as f:
            f.write(b"hello, this is bmlx ceph fs test!")
        # assert exist
        self.assertTrue(self.ceph_fs.exists(key))
        with self.ceph_fs.open(key, "rb") as f:
            content = f.read()
            # assert read same content
            self.assertEqual(content, b"hello, this is bmlx ceph fs test!")
