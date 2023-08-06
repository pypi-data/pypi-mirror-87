# EagleVision

## Why use this tool

This tool will help in uncovering the details in a code repository.
For example,

- Patterns in the code

- Type of asserts used in the test functions

- Test functions with no assert / pattern analysed

- Similarity in the source code/ test code functions

Note: Similarity analysis uses cosine algorithm, if the repo path given for
root and repo size is relatively large, re consider to give sub-folders,
Similarity analysis bound to take long time, since the computation is in memory
if not provided with adequate size expect potential memory overflow

- Cyclomatic complexity of functions

- Repository statistics like, Type of file, LOC, Comments, Code etc.

## Dependencies

- python 3.8 : 64 bit  

- python packages (functiondefextractor, similarity-processor, lizard)  

- cloc package `npm i -g cloc@2.6.0` `https://www.npmjs.com/package/cloc`
  Note: cloc has a dependency for pearl,
        if not installed please install pearl from `https://www.perl.org/`
  
- third party packages [Ctags, grep]

## Installation
  
[INSTALL.md](INSTALL.md)

## Usage

### Commandline

```sh
>>>python -m eaglevision --p "path\to\input\json"
```

- sample json input,  

```sh
[
  {
    "path": "repo/path",
    "run_pattern_match":true,
    "run_similarity":true,
    "extraction_annotation": null,
    "extraction_delta": null,
    "extraction_exclude": "*/test_resource/*",
    "pattern_match": ["assert"],
    "pattern_seperator": ["("],
    "similarity_range": "70,100",
    "run_cloc_metric":true,
    "cloc_args": "--exclude-dir=src --exclude-ext=*.cpp,*.java",
    "run_cyclomatic_complexity":true,
    "cyclo_args": "-l java  -l python",
    "cyclo_exclude": ["*.cpp","*.java"],
    "report_folder": null
  }
]
```

- Input Description,  

```sh
    "path": Path of the repository to be analysed
    "run_pattern_match": On/OFF switch for running Pattern match
    "run_similarity": On/OFF switch for running Similarity check
    "extraction_annotation": Functions with this annotation will be
                             extracted else all functions
    "extraction_delta": If substring of annotation is given,
                        this input (integer value) will take number of
                        lines above and below the annotation to report,
    "extraction_exclude": Pattern to exclude for Similarity and Pattern check
    "pattern_match": Type of pattern to analyse in the source code
    "pattern_seperator": Seperator in the pattern, left side of which will
                         be used for pivot reporting
    "similarity_range": Range of similarity of interest example: "70,100",
    "run_cloc_metric": On/OFF switch for running Cloc / types of
                      files/number etc in the repo
    "cloc_args": Any additional args for Cloc tool
                 example:"--exclude-dir=src --exclude-ext=*.cpp,*.java",
    "run_cyclomatic_complexity":On/OFF switch for running cyclomatic complexity check,
    "cyclo_args": Any additional args for Lizard / cyclomatic complexity tool
                 example:"-l java  -l python"
    "cyclo_exclude": Pattern to exclude for cyclomatic complexity check
                     example: ["*.cpp","*.java"]
    "report_folder": Path where report to be placed, if null will be using the path of repo

```

Note:

All the inputs are taken from the json file

1. Do not forget to have the json as list `[...]`

2. Make sure `pattern_match` and `pattern_seperator` is of same length list
 if you are not interested in any `pattern_seperator` for s specific
 `pattern_match` , mark it `null` in `pattern_seperator`

3. Make sure mark it `null` if a string or list parameter is not used

4. Make sure mark it `true/false` for bool type

```sh
refer https://www.npmjs.com/package/cloc for cloc args
refer https://pypi.org/project/lizard/ for cyclo args
refer https://pypi.org/project/functiondefextractor/ for extraction_exclude
refer https://pypi.org/project/similarity-processor/ for similarity
```

### Output
  
- Output will be available in same folder as `path` given in json under  `EagleVisionReport`

## Contact

[MAINTAINERS.md](MAINTAINERS.md)  

## License

[License.md](LICENSE.md)
