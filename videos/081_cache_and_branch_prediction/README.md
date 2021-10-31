To run the C++ benchmarks you will need the Google benchmark and Google test libraries cloned into the extern subdirectory.

```shell
cd extern
git clone https://github.com/google/benchmark.git
git clone https://github.com/google/googletest.git
```

Then you can build and run the project as a normal CMake project.
The Python file `plots.py` generates the plots using Plotly and the data contained in the json files.