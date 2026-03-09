const { BetaAnalyticsDataClient } = require('../node_modules/@google-analytics/data');

const PROPERTY_ID = '517064395';
const CREDENTIALS = 'C:/Users/suzuki.takumi/Desktop/AI/記事作成_TCJ/micro-environs-470717-j2-41ae07afc25f.json';

const client = new BetaAnalyticsDataClient({ keyFilename: CREDENTIALS });

async function run() {
  // 1. 月別セッション数・ユーザー数
  console.log('\n=== 1. 月別セッション数・ユーザー数 (2025-12 〜 2026-02) ===');
  try {
    const [monthly] = await client.runReport({
      property: `properties/${PROPERTY_ID}`,
      dateRanges: [{ startDate: '2025-12-01', endDate: '2026-02-28' }],
      dimensions: [{ name: 'yearMonth' }],
      metrics: [{ name: 'sessions' }, { name: 'totalUsers' }],
      orderBys: [{ dimension: { dimensionName: 'yearMonth' } }]
    });
    if (monthly.rows && monthly.rows.length > 0) {
      monthly.rows.forEach(row => {
        const ym = row.dimensionValues[0].value;
        const sess = row.metricValues[0].value;
        const users = row.metricValues[1].value;
        console.log(`  ${ym} | sessions: ${sess} | users: ${users}`);
      });
    } else {
      console.log('  データなし');
    }
  } catch (e) {
    console.log('  取得エラー:', e.message);
  }

  // 2. チャネル別セッション数
  console.log('\n=== 2. チャネル別セッション数 (2025-12-01 〜 2026-03-04) ===');
  try {
    const [channels] = await client.runReport({
      property: `properties/${PROPERTY_ID}`,
      dateRanges: [{ startDate: '2025-12-01', endDate: '2026-03-04' }],
      dimensions: [{ name: 'sessionDefaultChannelGrouping' }],
      metrics: [{ name: 'sessions' }],
      orderBys: [{ metric: { metricName: 'sessions' }, desc: true }]
    });
    if (channels.rows && channels.rows.length > 0) {
      channels.rows.forEach(row => {
        const channel = row.dimensionValues[0].value;
        const sess = row.metricValues[0].value;
        console.log(`  ${channel}: ${sess}`);
      });
    } else {
      console.log('  データなし');
    }
  } catch (e) {
    console.log('  取得エラー:', e.message);
  }

  // 3. ページ別セッション数 TOP20（/posts/配下のみ）
  console.log('\n=== 3. ページ別セッション数 TOP20（/posts/ 配下） (2025-12-01 〜 2026-03-04) ===');
  try {
    const [pages] = await client.runReport({
      property: `properties/${PROPERTY_ID}`,
      dateRanges: [{ startDate: '2025-12-01', endDate: '2026-03-04' }],
      dimensions: [{ name: 'pagePath' }],
      metrics: [{ name: 'sessions' }],
      dimensionFilter: {
        filter: {
          fieldName: 'pagePath',
          stringFilter: {
            matchType: 'BEGINS_WITH',
            value: '/posts/'
          }
        }
      },
      orderBys: [{ metric: { metricName: 'sessions' }, desc: true }],
      limit: 20
    });
    if (pages.rows && pages.rows.length > 0) {
      pages.rows.forEach((row, i) => {
        const path = row.dimensionValues[0].value;
        const sess = row.metricValues[0].value;
        console.log(`  ${String(i+1).padStart(2, ' ')}. ${path}: ${sess}`);
      });
    } else {
      console.log('  データなし（/posts/ 配下のページが存在しないか、セッション数が0）');
    }
  } catch (e) {
    console.log('  取得エラー:', e.message);
  }

  // 4. コンバージョンイベント
  console.log('\n=== 4. コンバージョンイベント数 (2025-12-01 〜 2026-03-04) ===');
  const keywords = ['contact', 'download', 'seminar', '申込', '資料'];
  try {
    const [events] = await client.runReport({
      property: `properties/${PROPERTY_ID}`,
      dateRanges: [{ startDate: '2025-12-01', endDate: '2026-03-04' }],
      dimensions: [{ name: 'eventName' }],
      metrics: [{ name: 'eventCount' }],
      orderBys: [{ metric: { metricName: 'eventCount' }, desc: true }],
      limit: 200
    });
    if (events.rows && events.rows.length > 0) {
      const filtered = events.rows.filter(row => {
        const name = row.dimensionValues[0].value.toLowerCase();
        return keywords.some(kw => name.includes(kw.toLowerCase()));
      });
      if (filtered.length > 0) {
        filtered.forEach(row => {
          const name = row.dimensionValues[0].value;
          const count = row.metricValues[0].value;
          console.log(`  ${name}: ${count}`);
        });
      } else {
        console.log('  該当キーワードを含むイベントは見つかりませんでした');
        console.log('  --- 全イベント一覧（参考） ---');
        events.rows.slice(0, 30).forEach(row => {
          console.log(`    ${row.dimensionValues[0].value}: ${row.metricValues[0].value}`);
        });
      }
    } else {
      console.log('  イベントデータなし');
    }
  } catch (e) {
    console.log('  取得エラー:', e.message);
  }
}

run().then(() => {
  console.log('\n--- 取得完了 ---');
}).catch(e => {
  console.error('Fatal error:', e.message);
});
