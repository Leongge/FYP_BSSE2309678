GLOB_EDGE_CASES_TESTS = {
    "argnames": ("path", "recursive", "maxdepth", "expected"),
    "argvalues": [
        ("fil?1", False, None, ["file1"]),
        ("fil?1", True, None, ["file1"]),
        ("file[1-2]", False, None, ["file1", "file2"]),
        ("file[1-2]", True, None, ["file1", "file2"]),
        ("*", False, None, ["file1", "file2"]),
        (
            "*",
            True,
            None,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir0/nesteddir/nestedfile",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        ("*", True, 1, ["file1", "file2"]),
        (
            "*",
            True,
            2,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir1/subfile1",
                "subdir1/subfile2",
            ],
        ),
        ("*1", False, None, ["file1"]),
        (
            "*1",
            True,
            None,
            [
                "file1",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        ("*1", True, 2, ["file1", "subdir1/subfile1", "subdir1/subfile2"]),
        (
            "**",
            False,
            None,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir0/nesteddir/nestedfile",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        (
            "**",
            True,
            None,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir0/nesteddir/nestedfile",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        ("**", True, 1, ["file1", "file2"]),
        (
            "**",
            True,
            2,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir0/nesteddir/nestedfile",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        (
            "**",
            False,
            2,
            [
                "file1",
                "file2",
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir1/subfile1",
                "subdir1/subfile2",
            ],
        ),
        ("**/*1", False, None, ["file1", "subdir0/subfile1", "subdir1/subfile1"]),
        (
            "**/*1",
            True,
            None,
            [
                "file1",
                "subdir0/subfile1",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        ("**/*1", True, 1, ["file1"]),
        (
            "**/*1",
            True,
            2,
            ["file1", "subdir0/subfile1", "subdir1/subfile1", "subdir1/subfile2"],
        ),
        ("**/*1", False, 2, ["file1", "subdir0/subfile1", "subdir1/subfile1"]),
        ("**/subdir0", False, None, []),
        ("**/subdir0", True, None, ["subfile1", "subfile2", "nesteddir/nestedfile"]),
        ("**/subdir0/nested*", False, 2, []),
        ("**/subdir0/nested*", True, 2, ["nestedfile"]),
        ("subdir[1-2]", False, None, []),
        ("subdir[1-2]", True, None, ["subfile1", "subfile2", "nesteddir/nestedfile"]),
        ("subdir[1-2]", True, 2, ["subfile1", "subfile2"]),
        ("subdir[0-1]", False, None, []),
        (
            "subdir[0-1]",
            True,
            None,
            [
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir0/nesteddir/nestedfile",
                "subdir1/subfile1",
                "subdir1/subfile2",
                "subdir1/nesteddir/nestedfile",
            ],
        ),
        (
            "subdir[0-1]/*fil[e]*",
            False,
            None,
            [
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir1/subfile1",
                "subdir1/subfile2",
            ],
        ),
        (
            "subdir[0-1]/*fil[e]*",
            True,
            None,
            [
                "subdir0/subfile1",
                "subdir0/subfile2",
                "subdir1/subfile1",
                "subdir1/subfile2",
            ],
        ),
    ],
}
