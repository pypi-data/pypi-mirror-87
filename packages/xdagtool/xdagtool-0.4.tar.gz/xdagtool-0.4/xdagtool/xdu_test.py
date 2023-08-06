import uuid, os
from pathlib import Path
from xdagtool import xdu


class TestPathCopy:
    def test_file_copy1(self, tmp_path: Path, capsys):
        # file a
        srcpath = tmp_path / 'srcpath-{}'.format(uuid.uuid4())
        destpath = tmp_path / 'destpath-{}'.format(uuid.uuid4())

        with capsys.disabled():
           print(tmp_path)

        srcpath.mkdir(parents=True)
        destpath.mkdir(parents=True)

        tmpfname = 'a-{}'.format(uuid.uuid4())
        tmp_txt = 'text-{}'.format(uuid.uuid4())
        srcfile_path = srcpath / tmpfname
        srcfile_path.write_text(tmp_txt)
        destfile_path = destpath / tmpfname

        xdu.path_copy(srcfile_path, destfile_path)

        assert destfile_path.exists()
        assert destfile_path.read_text() == tmp_txt

    def test_file_copy2(self, tmp_path: Path, capsys):
        # file a/b/c
        srcpath = tmp_path / 'd1'
        destpath = tmp_path / 'd2'

        srcpath.mkdir(parents=True)
        destpath.mkdir(parents=True)

        tmpfile = Path('c') / 'b' / 'a-{}'.format(uuid.uuid4())
        tmp_txt = 'text-{}'.format(uuid.uuid4())
        srcfile_path = srcpath / tmpfile
        srcfile_path.parent.mkdir(parents=True, exist_ok=True)
        srcfile_path.write_text(tmp_txt)
        destfile_path = destpath / tmpfile

        xdu.path_copy(srcfile_path, destfile_path)

        assert destfile_path.exists()
        assert destfile_path.read_text() == tmp_txt

    # @pytest.mark.skip(reason='temp')
    def test_dir_copy1(self, tmp_path: Path, capsys):
        # dir srcpath/1.dat 2.dat
        srcpath = tmp_path / 'd1'
        destpath = tmp_path / 'd2'

        srcpath.mkdir(parents=True)

        # src dir file list
        tmp_txt1 = 'text-{}'.format(uuid.uuid4())
        srcfile1 = srcpath / 'a-{}'.format(uuid.uuid4())
        srcfile1.write_text(tmp_txt1)

        tmp_txt2 = 'text-{}'.format(uuid.uuid4())
        srcfile2 = srcpath / 'a-{}'.format(uuid.uuid4())
        srcfile2.write_text(tmp_txt2)

        # go
        xdu.path_copy(srcpath, destpath)

        # assert
        assert destpath.exists()

        destfile1 = destpath / srcfile1.name
        assert destfile1.exists()
        assert destfile1.read_text() == tmp_txt1

        destfile2 = destpath / srcfile2.name
        assert destfile2.exists()
        assert destfile2.read_text() == tmp_txt2

    def test_dir_copy2(self, tmp_path: Path, capsys):
        # dir srcpath/ empty
        srcpath = tmp_path / 'd1'
        destpath = tmp_path / 'd2'

        srcpath.mkdir(parents=True)

        # src dir is empty

        # go
        xdu.path_copy(srcpath, destpath)

        # assert
        assert destpath.exists()
        assert len(os.listdir(destpath)) == 0

    def test_dir_copy3(self, tmp_path: Path, capsys):
        # dir srcpath/b/c/ empty
        srcpath = tmp_path / 'd1' / 'b' / 'c'
        destpath = tmp_path / 'd2' / 'b' / 'c'

        srcpath.mkdir(parents=True)

        # src dir is empty

        # go
        xdu.path_copy(srcpath, destpath)

        # assert
        destdir = tmp_path / 'd2'
        assert destdir.exists()

        destdir = tmp_path / 'd2' / 'b'
        assert destdir.exists()

        destdir = tmp_path / 'd2' / 'b' / 'c'
        assert destdir.exists()

        assert len(os.listdir(destdir)) == 0

    def test_dir_copy4(self, tmp_path: Path, capsys):
        # dir srcpath/b/c/ 1.dat 2.dat
        srcpath = tmp_path / 'd1' / 'b' / 'c'
        destpath = tmp_path / 'd2' / 'b' / 'c'

        srcpath.mkdir(parents=True)

        # src dir files
        tmp_txt1 = 'text-{}'.format(uuid.uuid4())
        srcfile1 = srcpath / 'a-{}'.format(uuid.uuid4())
        srcfile1.write_text(tmp_txt1)

        tmp_txt2 = 'text-{}'.format(uuid.uuid4())
        srcfile2 = srcpath / 'a-{}'.format(uuid.uuid4())
        srcfile2.write_text(tmp_txt2)

        # go
        xdu.path_copy(srcpath, destpath)

        # assert
        destdir = tmp_path / 'd2'
        assert destdir.exists()

        destdir = tmp_path / 'd2' / 'b'
        assert destdir.exists()

        destdir = tmp_path / 'd2' / 'b' / 'c'
        assert destdir.exists()

        assert destpath.exists()

        destfile1 = destpath / srcfile1.name
        assert destfile1.exists()
        assert destfile1.read_text() == tmp_txt1

        destfile2 = destpath / srcfile2.name
        assert destfile2.exists()
        assert destfile2.read_text() == tmp_txt2

    def test_dir_copy5(self, tmp_path: Path, capsys):
        # dir srcpath/b/
        #               c1/d1/1.dat 2.dat       # dir1
        #               c2/1.dat 2.dat          # dir2
        #               c3/                     # dir3
        srcpath = tmp_path / 'd1' / 'b'
        destpath = tmp_path / 'd2' / 'b'

        srcpath.mkdir(parents=True)

        # src dir initialize
        # dir1
        dir1 = srcpath / 'c1' / 'd1'
        dir1.mkdir(parents=True)

        dir1_tmp_txt1 = 'text-{}'.format(uuid.uuid4())
        dir1_srcfile1 = dir1 / 'a-{}'.format(uuid.uuid4())
        dir1_srcfile1.write_text(dir1_tmp_txt1)

        dir1_tmp_txt2 = 'text-{}'.format(uuid.uuid4())
        dir1_srcfile2 = dir1 / 'a-{}'.format(uuid.uuid4())
        dir1_srcfile2.write_text(dir1_tmp_txt2)

        # dir2
        dir2 = srcpath / 'c2'
        dir2.mkdir(parents=True)

        dir2_tmp_txt1 = 'text-{}'.format(uuid.uuid4())
        dir2_srcfile1 = dir2 / 'a-{}'.format(uuid.uuid4())
        dir2_srcfile1.write_text(dir2_tmp_txt1)

        dir2_tmp_txt2 = 'text-{}'.format(uuid.uuid4())
        dir2_srcfile2 = dir2 / 'a-{}'.format(uuid.uuid4())
        dir2_srcfile2.write_text(dir2_tmp_txt2)

        # dir3
        dir3 = srcpath / 'c3'
        dir3.mkdir(parents=True)


        # go
        xdu.path_copy(srcpath, destpath)

        # assert
        assert destpath.exists()

        # dir1
        destdir = destpath / 'c1' / 'd1'
        assert destdir.exists()

        destfile1 = destdir / dir1_srcfile1.name
        assert destfile1.exists()
        assert destfile1.read_text() == dir1_tmp_txt1

        # dir2
        destdir = destpath / 'c2'
        assert destdir.exists()

        # dir3
        destdir = destpath / 'c3'
        assert destdir.exists()


class TestPathsCopy:
    def test_paths_copy1(self, tmp_path: Path, shared_datadir: Path, capsys):
        assert (shared_datadir / 'storage').exists()
        xdu.paths_copy(str(shared_datadir / 'storage'), str(tmp_path / 'testdata'), ['01/75/f4/18.dat',
                                                                                     '01/75/f4/32.dat',
                                                                                     '01/75/f4/32.dat',
                                                                                     '01/75/f4/40.dat',
                                                                                     '01/75/f4/42.dat',  # not exist
                                                                                     '01/75/f4/sums.dat',
                                                                                     '01/75/f7',
                                                                                     '01/75/f8',    # not exist
                                                                                     '01/75/f9',
                                                                                     'empty1',
                                                                                     'empty2/empty3',])
        assert (tmp_path / 'testdata/01/75/f4/40.dat').exists()
        assert (tmp_path / 'testdata/01/75/f4/32.dat').exists()
        assert (tmp_path / 'testdata/01/75/f4/sums.dat').exists()
        assert (tmp_path / 'testdata/01/75/f7/01.dat').exists()
        assert (tmp_path / 'testdata/01/75/f9/sums.dat').exists()
        assert (tmp_path / 'testdata/empty1').exists()
        assert (tmp_path / 'testdata/empty2/empty3').exists() and (tmp_path / 'testdata/empty2/empty3').is_dir()

        assert not (tmp_path / 'testdata/01/75/f4/39.dat').exists()
        assert not (tmp_path / 'testdata/01/75/fb').exists()

        assert (not (tmp_path / 'storage/01/75/f4/42.dat').exists()) and (not (tmp_path / 'testdata/01/75/f4/42.dat').exists())
        assert (not (tmp_path / 'storage/01/75/f8').exists()) and (not (tmp_path / 'testdata/01/75/f8').exists())
