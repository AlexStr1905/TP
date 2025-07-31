import os
import tempfile
import pytest
from tree_utils_02.size_tree import SizeTree
from tree_utils_02.size_tree import BLOCK_SIZE


def test_size_tree_not_exist_path():
    tree = SizeTree()
    with pytest.raises(AttributeError, match="Path not exist"):
        tree.get("/not_exist/path", dirs_only=False)


def test_size_tree_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        subdir_path = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir_path)

        file1_path = os.path.join(subdir_path, "file1.txt")
        with open(file1_path, "w") as f:
            f.write("12345")

        file2_path = os.path.join(tmpdir, "file2.txt")
        with open(file2_path, "w") as f:
            f.write("1234567890")
        tree = SizeTree()
        root_node = tree.get(tmpdir, dirs_only=False)

        assert root_node.size == BLOCK_SIZE + BLOCK_SIZE + 5 + 10
        assert root_node.children[0].size == 10


def test_size_tree_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("Hello, world!")

        tree = SizeTree()
        node = tree.construct_filenode(file_path, is_dir=False)

        assert node.size == 13
