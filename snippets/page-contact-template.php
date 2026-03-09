<?php
/**
 * Template Name: TCJ Contact Landing
 * Description: Fixed page template for contact form landing (Zoho embed).
 */

get_header();
?>

<main id="primary" class="site-main">
  <div class="mx-auto max-w-7xl px-5 py-7.5 sm:py-[60px]">
    <article class="space-y-7.5">
      <header class="space-y-2 text-center">
        <p class="text-primary-500 font-alumni text-[21px] font-medium tracking-[0.4em]">Contact</p>
        <h1 class="font-notosansjp text-2xl font-medium tracking-[0.2em] sm:text-3xl">外国人材採用に関するお問い合わせ</h1>
        <p class="font-notosansjp text-sm font-medium tracking-[0.15em] text-gray-500 sm:text-base">
          在留資格・採用設計・教育・定着まで、現場課題に合わせてご提案します
        </p>
      </header>

      <div class="flex flex-col gap-7.5 lg:flex-row">
        <div class="seminar-entry-content">
          <img
            src="https://gaikoku-jinzai.tcj-education.com/wp-content/uploads/2026/02/3.10_%E6%A8%AA%E9%95%B7-1.jpg"
            alt="お問い合わせイメージ"
          />
          <p>下記フォームより必要事項をご入力ください。担当者よりご連絡いたします。</p>
          <p>営業目的のお問い合わせはご遠慮ください。</p>
        </div>

        <div class="space-y-9 lg:w-1/2 lg:min-w-[360px] shrink-0">
          <p class="text-center text-base text-[#252c3e] md:text-lg">必要事項をご記入の上、「送信」を押下してください。</p>
          <div class="w-full" style="height: 1400px;">
            <iframe
              frameborder="0"
              width="100%"
              height="100%"
              src="https://forms.zohopublic.com/info420tcjni1/form/Untitled21/formperma/9DD5diEqo5PrBlahQQ0hkcwtfQuRE5g6U16E9P6pc1w"
              title="TCJ contact form"
            ></iframe>
          </div>
          <p class="text-center text-sm text-gray-500">
            フォームが表示されない場合は
            <a href="https://forms.zohopublic.com/info420tcjni1/form/Untitled21/formperma/9DD5diEqo5PrBlahQQ0hkcwtfQuRE5g6U16E9P6pc1w" target="_blank" rel="noopener noreferrer">こちら</a>
            から入力してください。
          </p>
        </div>
      </div>
    </article>
  </div>
</main>

<?php
get_footer();

