# Publishes the working tree as a new commit on main via the GitHub API.
# The new commit uses the current remote main as its parent and the ref update
# is a fast-forward only: it never force-pushes or rewrites remote history.
# Prefer plain `git push` when a normal git remote is available.
param(
  [string]$Message = "Update codex-style agentic thinking skill"
)

$ErrorActionPreference = "Stop"

$owner = "Zxxx96"
$repoName = "codex-style-agentic-thinking"
$root = (Get-Location).Path

$files = Get-ChildItem -Recurse -File | Where-Object {
  $_.FullName -notmatch "\\.git\\" -and
  $_.Name -ne "publish-via-gh-api.ps1" -and
  $_.Name -ne "分析报告与改进方案.md"
}

$treeItems = @()

foreach ($file in $files) {
  $rel = [System.IO.Path]::GetRelativePath($root, $file.FullName).Replace("\", "/")
  Write-Host "Uploading blob: $rel"

  $content = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($file.FullName))
  $blobPayload = @{
    content = $content
    encoding = "base64"
  } | ConvertTo-Json -Compress

  $blobFile = New-TemporaryFile
  Set-Content -LiteralPath $blobFile -Value $blobPayload -Encoding UTF8

  $blobSha = gh api "repos/$owner/$repoName/git/blobs" -X POST --input $blobFile --jq ".sha"
  Remove-Item -LiteralPath $blobFile -Force

  $treeItems += @{
    path = $rel
    mode = "100644"
    type = "blob"
    sha = $blobSha.Trim()
  }
}

$treePayload = @{
  tree = $treeItems
} | ConvertTo-Json -Depth 20

$treeFile = New-TemporaryFile
Set-Content -LiteralPath $treeFile -Value $treePayload -Encoding UTF8

$treeSha = gh api "repos/$owner/$repoName/git/trees" -X POST --input $treeFile --jq ".sha"
Remove-Item -LiteralPath $treeFile -Force

$parentSha = $null
try {
  $parentSha = gh api "repos/$owner/$repoName/git/ref/heads/main" --jq ".object.sha" 2>$null
} catch {
  $parentSha = $null
}

$parents = @()
if ($parentSha) {
  $parents = @($parentSha.Trim())
}

$commitPayload = @{
  message = $Message
  tree = $treeSha.Trim()
  parents = $parents
} | ConvertTo-Json -Depth 20

$commitFile = New-TemporaryFile
Set-Content -LiteralPath $commitFile -Value $commitPayload -Encoding UTF8

$commitSha = gh api "repos/$owner/$repoName/git/commits" -X POST --input $commitFile --jq ".sha"
Remove-Item -LiteralPath $commitFile -Force

if ($parentSha) {
  # No force flag: GitHub rejects non-fast-forward updates, protecting remote history.
  $refPayload = @{
    sha = $commitSha.Trim()
  } | ConvertTo-Json -Compress

  $refFile = New-TemporaryFile
  Set-Content -LiteralPath $refFile -Value $refPayload -Encoding UTF8

  gh api "repos/$owner/$repoName/git/refs/heads/main" -X PATCH --input $refFile | Out-Null
  Remove-Item -LiteralPath $refFile -Force
} else {
  $refPayload = @{
    ref = "refs/heads/main"
    sha = $commitSha.Trim()
  } | ConvertTo-Json -Compress

  $refFile = New-TemporaryFile
  Set-Content -LiteralPath $refFile -Value $refPayload -Encoding UTF8

  gh api "repos/$owner/$repoName/git/refs" -X POST --input $refFile | Out-Null
  Remove-Item -LiteralPath $refFile -Force
}

gh api "repos/$owner/$repoName" -X PATCH -f default_branch=main | Out-Null

Write-Host ""
Write-Host "Published:"
Write-Host "https://github.com/$owner/$repoName"
