<#
PowerShell helper: Pull a Docker image from a registry and restart the container.

Usage (GHCR):
  $image = 'ghcr.io/<owner>/zeroai:latest'
  .\scripts\update_from_registry.ps1 -Image $image -ContainerName zeroai -HostPort 7860 -StorageHostPath 'C:\path\to\storage' -DataHostPath 'C:\path\to\data'

Usage (DockerHub):
  $image = 'docker.io/<user>/zeroai:latest'
  .\scripts\update_from_registry.ps1 -Image $image -ContainerName zeroai -HostPort 7860 -StorageHostPath 'C:\path\to\storage' -DataHostPath 'C:\path\to\data'

This script:
- pulls the image
- stops and removes the existing container (if any)
- runs a new container mapping volumes for /app/storage and /app/data
#>

param(
    [Parameter(Mandatory=$true)] [string]$Image,
    [Parameter(Mandatory=$true)] [string]$ContainerName,
    [int]$HostPort = 7860,
    [string]$StorageHostPath = "$PWD\storage",
    [string]$DataHostPath = "$PWD\data"
)

Write-Host "Pulling image: $Image"
docker pull $Image

Write-Host "Stopping and removing container (if exists): $ContainerName"
try { docker stop $ContainerName -t 10 } catch {}
try { docker rm $ContainerName } catch {}

Write-Host "Starting new container: $ContainerName"
docker run -d --name $ContainerName -p ${HostPort}:7860 `
  -v "${StorageHostPath}:/app/storage" `
  -v "${DataHostPath}:/app/data" `
  $Image

Write-Host "Container started. Streaming logs (CTRL+C to exit):"
docker logs -f $ContainerName
