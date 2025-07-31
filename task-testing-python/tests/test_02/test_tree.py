import os
import tempfile
import pytest
from tree_utils_02.tree import Tree
from tree_utils_02.node import FileNode


def test_get_not_exist_path():
    tree = Tree()
    with pytest.raises(AttributeError, match="Path not exist"):
        tree.get("/not_exist/path", dirs_only=False)


def test_get_not_dirs_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "file.txt"), "w") as f:
            f.write("test")

        tree = Tree()
        node = tree.get(tmpdir, dirs_only=False)

        assert node.name == os.path.basename(tmpdir)
        assert node.is_dir
        assert len(node.children) == 2


def test_get_dirs_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "file.txt"), "w") as f:
            f.write("test")

        tree = Tree()
        node = tree.get(tmpdir, dirs_only=True)

        assert node.name == os.path.basename(tmpdir)
        assert node.is_dir
        assert len(node.children) == 1


def test_get_file_path_with_dirs_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "file.txt")
        with open(file_path, "w") as f:
            f.write("test")

        tree = Tree()
        with pytest.raises(AttributeError, match="Path is not directory"):
            tree.get(file_path, dirs_only=True)


def test_get_file_path_in_recurse_mode_with_dirs_only():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("test")

        tree = Tree()
        result = tree.get(file_path, dirs_only=True, recurse_call=True)
        assert result is None


def test_filter_empty_nodes_skips_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("Hello")

        tree = Tree()
        file_node = tree.construct_filenode(file_path, is_dir=False)

        tree.filter_empty_nodes(file_node, file_path)
        assert os.path.exists(file_path)


def test_filter_empty_nodes():
    with tempfile.TemporaryDirectory() as tmpdir:
        empty_dir = os.path.join(tmpdir, "empty_dir")
        os.makedirs(empty_dir)

        tree = Tree()
        node = tree.get(tmpdir, dirs_only=False)

        assert os.path.exists(empty_dir)

        tree.filter_empty_nodes(node, tmpdir)

        assert not os.path.exists(empty_dir)


def test_filter_empty_nodes_ignores_not_empty_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("test")

        tree = Tree()
        node = tree.get(tmpdir, dirs_only=False)
        tree.filter_empty_nodes(node, tmpdir)

        assert os.path.exists(tmpdir)


def test_filter_empty_nodes_with_current_path_dot():
    tree = Tree()
    empty_node = FileNode(name="fake_dir", is_dir=True, children=[])

    with pytest.raises(ValueError, match="Code should not be executed here!"):
        tree.filter_empty_nodes(empty_node, current_path='.')
