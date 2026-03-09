<?php
/**
 * Canonicalタグを自動追加する関数
 * functions.php に追加してください
 */

// Yoast SEOが既に出力している場合はスキップ
if ( ! function_exists('yoast_seo_canonical') ) {

    function add_canonical_tag() {
        // シングルページ（記事、固定ページ）の場合
        if ( is_singular() ) {
            $canonical_url = get_permalink();
            echo '<link rel="canonical" href="' . esc_url( $canonical_url ) . '" />' . "\n";
        }

        // ホームページの場合
        elseif ( is_home() || is_front_page() ) {
            $canonical_url = home_url('/');
            echo '<link rel="canonical" href="' . esc_url( $canonical_url ) . '" />' . "\n";
        }

        // カテゴリーページの場合
        elseif ( is_category() ) {
            $canonical_url = get_category_link( get_queried_object_id() );
            echo '<link rel="canonical" href="' . esc_url( $canonical_url ) . '" />' . "\n";
        }

        // タグページの場合
        elseif ( is_tag() ) {
            $canonical_url = get_tag_link( get_queried_object_id() );
            echo '<link rel="canonical" href="' . esc_url( $canonical_url ) . '" />' . "\n";
        }

        // アーカイブページの場合
        elseif ( is_archive() ) {
            $canonical_url = get_post_type_archive_link( get_post_type() );
            echo '<link rel="canonical" href="' . esc_url( $canonical_url ) . '" />' . "\n";
        }
    }

    add_action( 'wp_head', 'add_canonical_tag', 1 );
}
?>
