# Playwright キャッシュ削除スクリプト
# 定期実行用（タスクスケジューラで設定可能）

$cachePath = "$env:LOCALAPPDATA\ms-playwright-go"
$logPath = "$PSScriptRoot\playwright-cache-clear.log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (Test-Path $cachePath) {
    try {
        Remove-Item -Path $cachePath -Recurse -Force -ErrorAction Stop
        $message = "[$timestamp] SUCCESS: Playwright cache cleared from $cachePath"
    } catch {
        $message = "[$timestamp] ERROR: Failed to clear cache - $_"
    }
} else {
    $message = "[$timestamp] INFO: Cache directory does not exist - $cachePath"
}

# ログに記録
Add-Content -Path $logPath -Value $message
Write-Host $message
