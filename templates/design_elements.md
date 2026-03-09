# デザイン要素リファレンス (最終盤 - 青ベース #102891 版)

メインカラーを青（#102891）に変更したデザイン要素のスニペットです。

## 1. 見出し (Headings)

### H2 (下線青)
```html
<h2 style="font-size: 28px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 60px; margin-bottom: 24px; padding-bottom: 15px; border-bottom: 2px solid #102891;">
    見出しテキストが入ります
</h2>
```

### H3 (左線青)
```html
<h3 style="font-size: 22px; font-weight: bold; line-height: 1.3; color: #424242; margin-top: 46px; margin-bottom: 18px; border-left: 6px solid #102891; padding-left: 15px; background-color: transparent;">
    見出しテキストが入ります
</h3>
```

### H4 (左線青・細め)
```html
<h4 style="font-size: 18px; font-weight: bold; color: #102891; margin-bottom: 15px; border-left: 4px solid #102891; padding-left: 10px;">
    見出しテキストが入ります
</h4>
```

---

## 3. リスト (Lists) - nomadList1 (枠線付き)

### 基本の枠付けリスト
```html
<div class="nomadList1">
<ul>
<li>リスト項目１</li>
<li>リスト項目２</li>
<li>リスト項目３</li>
</ul>
</div>
```

---

## 4. テーブル (Tables)

### 青ヘッダーのテーブル
```html
<table style="width: 100%; border-collapse: collapse; margin-bottom: 30px; border: 1px solid #e1e1e1; font-size: 15px;">
    <thead>
        <tr style="background-color: #f0f4f8;">
            <th style="padding: 12px; border: 1px solid #e1e1e1; text-align: left;">ヘッダー1</th>
            <th style="padding: 12px; border: 1px solid #e1e1e1; text-align: left;">ヘッダー2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e1e1e1;">データ1</td>
            <td style="padding: 12px; border: 1px solid #e1e1e1;">データ2</td>
        </tr>
    </tbody>
</table>
```

---

## 4. フッター & CTA

### フッターボックス (青ベース)
```html
<div style="background-color: #f0f4f8; padding: 40px; border-radius: 10px; margin-top: 60px; text-align: center;">
    <h2 style="font-size: 26px; font-weight: bold; margin-bottom: 20px;">タイトル</h2>
    <p style="margin-bottom: 24px;">説明文</p>
    <a style="display: inline-block; background-color: #102891; color: #fff; padding: 20px 60px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 20px;" href="URL">
        ボタンテキスト →
    </a>
</div>
```
