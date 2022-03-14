## Distributing the apps as platform specific executables

The executables must be created from a machine running the same OS than the targetted executable (e.g. to generate an .exe file, pyinstaller must be run on Windows). 

To create the executable for the run.py script (which also includes the plot_tool.py) for Linux and Windows, run:


```console
pyinstaller --clean specfiles/merge_apps.spec
```

To generate signed mac executables, we need to use different spec files:

```console
pyinstaller --clean specfiles/pymedeas_mac.spec
```

To create the executable for the plot_tool.py as a single file, run:
    
```console
pyinstaller --clean specfiles/plot_mac.spec
```


---
**NOTE:**
    You must be inside a python environment that contains all required packages for pymedeas to work (use the environment.yml).

---


---
**NOTE:**
    To generate the mac executables, you need to use a code sign key (you can generate one for free using [cosign](http://docs.sigstore.dev/cosign/overview)), and you need to generate an environmental variable named KEY (e.g. export KEY=/User/paco/cosign.key) with the path to the key file.

---
