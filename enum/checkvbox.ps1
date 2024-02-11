function checkvbox {
    # PS> . .\checkvbox.ps1
    # PS> checkvbox
    $vbox = $false
    $dsdtPath = 'HKLM:\HARDWARE\ACPI\DSDT'
    $fadtPath = 'HKLM:\HARDWARE\ACPI\FADT'

    $vboxProcessMatches = (Get-Process | Select ProcessName | Where-Object {$_.ProcessName -match "vbox"}).Count
    Write-host "Numero de procesos identificados con vbox : $vboxProcessMatches"

    $dsdtMatches = (Get-ChildItem $dsdtPath | Where-Object {$_.Name -match "vbox"} | Measure-Object).Count
    Write-host "Clave VBox en el hive del registro $dsdtPath : $dsdtMatches "

    $fadtMatches = (dir $fadtPath | Where-Object {$_.Name -match "vbox"} | measure).Count
    Write-host "Clave VBox en el hive del registro $fadtPath : $fadtMatches"

    $sumMatches = $vboxProcessMatches + $dsdtMatches + $fadtMatches
    #if (($vboxProcessMatches -gt 0) -or (($dsdtMatches -gt 0) -or ($fadtMatches -gt 0)))
    if ($sumMatches -gt 0)
    {
        $vbox = $true
    }
    Write-host "Maquina Virtual?"
    return $vbox
}
