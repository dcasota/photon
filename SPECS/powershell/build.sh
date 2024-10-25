#!/bin/bash

set -ex

# Powershell related build instructions

# See https://github.com/PowerShell/PowerShell/blob/master/docs/building/internals.md

mkdir -p /usr/lib/dotnet/sdk-manifests
for f in src/powershell-unix src/ResGen src/TypeCatalogGen; do
  dotnet restore $f
done

pushd src/ResGen
dotnet run
popd

pushd src
cp Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets Microsoft.PowerShell.SDK/obj
dotnet msbuild Microsoft.PowerShell.SDK/Microsoft.PowerShell.SDK.csproj /t:_GetDependencies "/property:DesignTimeBuild=true;_DependencyFile=$(pwd)/TypeCatalogGen/powershell.inc" /nologo
popd

pushd src/TypeCatalogGen
dotnet run ../System.Management.Automation/CoreCLR/CorePsTypeCatalog.cs powershell.inc
popd

touch DELETE_ME_TO_DISABLE_CONSOLEHOST_TELEMETRY
dotnet publish /property:GenerateFullPaths=true --configuration Linux --framework net8.0 --runtime linux-x64 src/powershell-unix --output bin

# Even after powershell rpm built, dotnet processes are alive, following to stop them:
for pid in $(pgrep dotnet); do
  if [ -n "${pid}" ]; then
    if kill -0 "${pid}"; then
      kill -15 "${pid}"
    fi
  fi
done
