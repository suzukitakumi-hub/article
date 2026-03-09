# CSVからキーワードと検索ボリュームを抽出（UTF-8出力）
$csv = Import-Csv "Keyword Stats 2026-01-19 at 11_24_39.csv" -Delimiter "`t" -Encoding Unicode

# 検索ボリュームでソート
$sorted = $csv | Where-Object { $_.'Avg. monthly searches' -match '^\d+' } | 
ForEach-Object {
    $vol = [int]($_.'Avg. monthly searches')
    [PSCustomObject]@{
        Keyword     = $_.Keyword
        Volume      = $vol
        Competition = $_.Competition
    }
} | Sort-Object -Property Volume -Descending

# ファイルに出力（UTF-8）
$output = @()
$output += "=== TCJ外国人材キーワード 検索ボリューム TOP 30 ==="
$output += ""
$i = 1
$sorted | Select-Object -First 30 | ForEach-Object {
    $output += "$i. $($_.Keyword): $($_.Volume) (競合: $($_.Competition))"
    $i++
}

$output += ""
$output += "=== ボリューム1,000以上の最重要キーワード ==="
$output += ""
$high = $sorted | Where-Object { $_.Volume -ge 1000 }
$high | ForEach-Object {
    $output += "- $($_.Keyword): $($_.Volume)"
}

$output += ""
$output += "=== ボリューム500-999の重要キーワード ==="
$output += ""
$mid = $sorted | Where-Object { $_.Volume -ge 500 -and $_.Volume -lt 1000 }
$mid | ForEach-Object {
    $output += "- $($_.Keyword): $($_.Volume)"
}

$output += ""
$output += "=== ボリューム100-499のキーワード ==="
$output += ""
$low = $sorted | Where-Object { $_.Volume -ge 100 -and $_.Volume -lt 500 }
$low | ForEach-Object {
    $output += "- $($_.Keyword): $($_.Volume)"
}

# UTF-8で出力
$output | Out-File -FilePath "keyword_priority.txt" -Encoding UTF8
Write-Host "キーワードリストをkeyword_priority.txtに出力しました"
