param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ClaudeHome = Join-Path $HOME ".claude"

$SkillSource = Join-Path $RepoRoot "skills\office-hours"
$SkillTarget = Join-Path $ClaudeHome "skills\office-hours"
$AgentSource = Join-Path $RepoRoot "agents\office-hours-expert.md"
$AgentTarget = Join-Path $ClaudeHome "agents\office-hours-expert.md"

function Assert-SourceExists([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Source does not exist: $Path"
    }
}

function Same-File([string]$Source, [string]$Target) {
    if (-not (Test-Path -LiteralPath $Target)) {
        return $false
    }

    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Source).Hash -eq
        (Get-FileHash -Algorithm SHA256 -LiteralPath $Target).Hash
}

Assert-SourceExists $SkillSource
Assert-SourceExists $AgentSource

$SkillFileSource = Join-Path $SkillSource "SKILL.md"
$SkillFileTarget = Join-Path $SkillTarget "SKILL.md"

if ((Test-Path -LiteralPath $SkillTarget) -and -not $Force) {
    if (-not (Same-File $SkillFileSource $SkillFileTarget)) {
        throw "Office Hours skill already exists and differs: $SkillTarget. Re-run with -Force to replace it."
    }
} else {
    if ((Test-Path -LiteralPath $SkillTarget) -and $Force) {
        Remove-Item -LiteralPath $SkillTarget -Recurse -Force
    }
    New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null
    Copy-Item -LiteralPath $SkillFileSource -Destination $SkillFileTarget -Force
}

New-Item -ItemType Directory -Path (Split-Path -Parent $AgentTarget) -Force | Out-Null

if ((Test-Path -LiteralPath $AgentTarget) -and -not $Force) {
    if (-not (Same-File $AgentSource $AgentTarget)) {
        throw "Office Hours expert agent already exists and differs: $AgentTarget. Re-run with -Force to replace it."
    }
} else {
    Copy-Item -LiteralPath $AgentSource -Destination $AgentTarget -Force
}

Write-Host "Office Hours installed for Claude Code."
Write-Host "Skill: $SkillTarget"
Write-Host "Agent: $AgentTarget"
Write-Host ""
Write-Host "Start a new Claude Code session, then run:"
Write-Host "  /office-hours"
