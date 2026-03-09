<?php
/**
 * Code Snippets 用スニペット
 * 固定ページのテーマテンプレートをバイパスして 2カラム + Zoho フォームを直接描画する
 *
 * 対象ページ:
 *   - /contact      お問い合わせ
 *   - /doc-request  資料請求
 */

add_action( 'template_redirect', function () {

    if ( is_page( 'contact' ) ) {

        status_header( 200 );
        get_header();
        ?>
        <main id="primary" class="site-main">
            <div class="mx-auto max-w-7xl px-5 py-7.5 sm:py-[60px]">
                <article class="space-y-7.5">

                    <header class="space-y-2 text-center">
                        <p class="text-primary-500 font-alumni text-[21px] font-medium tracking-[0.4em]">Contact</p>
                        <h1 class="font-notosansjp text-2xl font-medium tracking-[0.2em] sm:text-3xl">
                            外国人材採用に関するお問い合わせ
                        </h1>
                        <p class="font-notosansjp text-sm font-medium tracking-[0.15em] text-gray-500 sm:text-base">
                            在留資格・採用設計・教育・定着まで、現場課題に合わせてご提案します
                        </p>
                    </header>

                    <div class="flex flex-col gap-7.5 lg:flex-row">

                        <!-- 左カラム：説明 -->
                        <div class="seminar-entry-content" style="padding-top: 120px;">
                            <p>下記フォームより必要事項をご入力ください。担当者より1-2営業日以内にご連絡いたします。</p>
                            <p>営業目的のお問い合わせはご遠慮ください。</p>
                        </div>

                        <!-- 右カラム：Zoho フォーム -->
                        <div class="space-y-9 lg:w-1/2 lg:min-w-[360px] shrink-0 w-full">
                            <p class="text-center text-base text-[#252c3e] md:text-lg">
                                必要事項をご記入の上、「送信」を押下してください。
                            </p>
                            <div class="w-full" style="min-height: 1400px; height: auto;">
                                <iframe
                                    frameborder="0"
                                    width="100%"
                                    height="1400"
                                    src="https://forms.zohopublic.com/info420tcjni1/form/Untitled21/formperma/9DD5diEqo5PrBlahQQ0hkcwtfQuRE5g6U16E9P6pc1w"
                                    title="TCJ お問い合わせフォーム"
                                    style="display: block; width: 100%;"
                                ></iframe>
                            </div>
                        </div>

                    </div>
                </article>
            </div>
        </main>
        <?php
        get_footer();
        exit;

    } elseif ( is_page( 'doc-request' ) ) {

        status_header( 200 );
        get_header();
        ?>
        <main id="primary" class="site-main">
            <div class="mx-auto max-w-7xl px-5 py-7.5 sm:py-[60px]">
                <article class="space-y-7.5">

                    <header class="space-y-2 text-center">
                        <p class="text-primary-500 font-alumni text-[21px] font-medium tracking-[0.4em]">Document Request</p>
                        <h1 class="font-notosansjp text-2xl font-medium tracking-[0.2em] sm:text-3xl">
                            外国人材採用に関する資料請求
                        </h1>
                        <p class="font-notosansjp text-sm font-medium tracking-[0.15em] text-gray-500 sm:text-base">
                            在留資格・採用設計・教育・定着まで、現場課題に合わせてご提案します
                        </p>
                    </header>

                    <div class="flex flex-col gap-7.5 lg:flex-row">

                        <!-- 左カラム：説明 -->
                        <div class="seminar-entry-content" style="padding-top: 120px;">
                            <p>下記フォームより必要事項をご入力ください。担当者より1-2営業日以内にご連絡いたします。</p>
                            <p>営業目的のお問い合わせはご遠慮ください。</p>
                        </div>

                        <!-- 右カラム：Zoho フォーム -->
                        <div class="space-y-9 lg:w-1/2 lg:min-w-[360px] shrink-0 w-full">
                            <p class="text-center text-base text-[#252c3e] md:text-lg">
                                必要事項をご記入の上、「送信」を押下してください。
                            </p>
                            <div class="w-full" style="min-height: 1400px; height: auto;">
                                <iframe
                                    frameborder="0"
                                    width="100%"
                                    height="1400"
                                    src="https://forms.zohopublic.com/info420tcjni1/form/Untitled22/formperma/nmrXxbae-UHJnLnOKeOUR4l5AmC9f_Brv2OMC2cWmzY"
                                    title="TCJ 資料請求フォーム"
                                    style="display: block; width: 100%;"
                                ></iframe>
                            </div>
                        </div>

                    </div>
                </article>
            </div>
        </main>
        <?php
        get_footer();
        exit;

    }
} );
