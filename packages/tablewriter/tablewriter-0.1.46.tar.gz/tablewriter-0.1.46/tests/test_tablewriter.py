from transparentpath import TransparentPath as Path

from tablewriter import TableWriter

df = (Path("tests") / "data" / "input.csv").read(index_col=0)


def test_tablewriter_from_dataframe():
    table = TableWriter(
        path_output="tests/data/ouput",
        data=df,
        to_latex_args={"column_format": "lrr"},
        label="tab::example",
        caption="TableWriter example",
        hide_numbering=True,
    )
    table.compile(silenced=False)
    assert Path("tests/data/ouput.tex").is_file()
    assert Path("tests/data/ouput.pdf").is_file()
    Path("tests/data/ouput.pdf").rm()
    Path("tests/data/ouput.tex").rm()


def test_tablewriter_from_file():
    table = TableWriter(
        path_output="tests/data/ouput_from_file",
        path_input="tests/data/input.csv",
        label="tab::example",
        caption="TableWriter example",
        read_from_file_args={"index_col": 0},
        number=3,
    )
    table.compile(silenced=False)
    assert Path("tests/data/ouput_from_file.tex").is_file()
    assert Path("tests/data/ouput_from_file.pdf").is_file()
    Path("tests/data/ouput_from_file.pdf").rm()
    Path("tests/data/ouput_from_file.tex").rm()
