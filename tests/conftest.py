import os
import shutil

import pytest

from udemy_enroller.utils import get_app_dir


@pytest.fixture(scope="session", autouse=True)
def test_file_dir():
    app_dir = get_app_dir()
    test_file_dir = "test_tmp"
    full_dir = os.path.join(app_dir, test_file_dir)
    # Try to delete directory in case it wasn't deleted after last test run
    if os.path.isdir(full_dir):
        shutil.rmtree(full_dir)
    yield os.mkdir(full_dir)
    # Delete directory after all tests completed
    if os.path.isdir(full_dir):
        shutil.rmtree(full_dir)


@pytest.fixture()
def tutorialbar_main_page():
    return (
        b'    <!DOCTYPE html>\r\n<!--[if IE 8]>    <html class="ie8" lang="en-US"> <![endif]-->\r\n<!--[if IE '
        b'9]>    <html class="ie9" lang="en-US"> <![endif]-->\r\n<!--[if (gt IE 9)|!(IE)] lang="en-US"><!['
        b'endif]-->\r\n<html lang="en-US">\r\n<head>\r\n<meta charset="UTF-8" />\r\n<meta name="viewport" '
        b'content="width=device-width, initial-scale=1.0" />\r\n<!-- feeds & pingback -->\r\n<link rel="profile" '
        b'href="https://gmpg.org/xfn/11" />\r\n<link rel="pingback" href="https://www.tutorialbar.com/xmlrpc.php" '
        b"/>\r\n<!-- Optimized by SG Optimizer plugin version - 5.7.6 -->\n\t<!-- This site is optimized with the "
        b"Yoast SEO plugin v15.3 - https://yoast.com/wordpress/plugins/seo/ -->\n\t<title>All Courses - Tutorial "
        b'Bar</title>\n\t<meta name="description" content="Complete Python Bootcamp: Go from zero to hero in Python 3 '
        b'Development, Programming Languages The Data Science Course 2020: Complete Data Science Bootcamp" />\n\t<meta '
        b'name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" '
        b'/>\n\t<link rel="canonical" href="https://tutorialbar.com/all-courses/" />\n\t<meta property="og:locale" '
        b'content="en_US" />\n\t<meta property="og:type" content="article" />\n\t<meta property="og:title" '
        b'content="All Courses - Tutorial Bar" />\n\t<meta property="og:description" content="Complete Python '
        b"Bootcamp: Go from zero to hero in Python 3 Development, Programming Languages The Data Science Course 2020: "
        b'Complete Data Science Bootcamp" />\n\t<meta property="og:url" content="https://tutorialbar.com/all-courses/" '
        b'/>\n\t<meta property="og:site_name" content="Tutorial Bar" />\n\t<meta property="article:modified_time" '
        b'content="2020-02-03T08:27:01+00:00" />\n\t<meta property="og:image" '
        b'content="https://tutorialbar.com/wp-content/uploads/thumbs_dir/567828_67d0'
        b'-1w98umhs5zowdq2pvoynzl5o9fyubs7tt14gzpp8igok.jpg" />\n\t<meta name="twitter:card" '
        b'content="summary_large_image" />\n\t<meta name="twitter:label1" content="Written by">\n\t<meta '
        b'name="twitter:data1" content="Tutorial Bar">\n\t<meta name="twitter:label2" content="Est. reading '
        b'time">\n\t<meta name="twitter:data2" content="1 minute">\n\t<script type="application/ld+json" '
        b'class="yoast-schema-graph">{"@context":"https://schema.org","@graph":[{"@type":"Organization",'
        b'"@id":"https://tutorialbar.com/#organization","name":"Tutorial Bar","url":"https://tutorialbar.com/",'
        b'"sameAs":[],"logo":{"@type":"ImageObject","@id":"https://tutorialbar.com/#logo","inLanguage":"en-US",'
        b'"url":"https://www.tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png","width":489,"height":113,'
        b'"caption":"Tutorial Bar"},"image":{"@id":"https://tutorialbar.com/#logo"}},{"@type":"WebSite",'
        b'"@id":"https://tutorialbar.com/#website","url":"https://tutorialbar.com/","name":"Tutorial Bar",'
        b'"description":"","publisher":{"@id":"https://tutorialbar.com/#organization"},"potentialAction":[{'
        b'"@type":"SearchAction","target":"https://tutorialbar.com/?s={search_term_string}","query-input":"required '
        b'name=search_term_string"}],"inLanguage":"en-US"},{"@type":"ImageObject",'
        b'"@id":"https://tutorialbar.com/all-courses/#primaryimage","inLanguage":"en-US",'
        b'"url":"https://tutorialbar.com/wp-content/uploads/thumbs_dir/567828_67d0'
        b'-1w98umhs5zowdq2pvoynzl5o9fyubs7tt14gzpp8igok.jpg"},{"@type":"WebPage",'
        b'"@id":"https://tutorialbar.com/all-courses/#webpage","url":"https://tutorialbar.com/all-courses/",'
        b'"name":"All Courses - Tutorial Bar","isPartOf":{"@id":"https://tutorialbar.com/#website"},'
        b'"primaryImageOfPage":{"@id":"https://tutorialbar.com/all-courses/#primaryimage"},'
        b'"datePublished":"2020-02-02T19:18:58+00:00","dateModified":"2020-02-03T08:27:01+00:00",'
        b'"description":"Complete Python Bootcamp: Go from zero to hero in Python 3 Development, Programming Languages '
        b'The Data Science Course 2020: Complete Data Science Bootcamp","inLanguage":"en-US","potentialAction":[{'
        b'"@type":"ReadAction","target":["https://tutorialbar.com/all-courses/"]}]}]}</script>\n\t<!-- / Yoast SEO '
        b"plugin. -->\n\n\n<link rel='dns-prefetch' href='//www.googletagmanager.com' />\n<link "
        b'rel=\'dns-prefetch\' href=\'//s.w.org\' />\n<link rel="alternate" type="application/rss+xml" title="Tutorial '
        b'Bar &raquo; Feed" href="https://www.tutorialbar.com/feed/" />\n\t\t<script '
        b'type="text/javascript">\n\t\t\twindow._wpemojiSettings = {'
        b'"baseUrl":"https:\\/\\/s.w.org\\/images\\/core\\/emoji\\/13.0.0\\/72x72\\/","ext":".png",'
        b'"svgUrl":"https:\\/\\/s.w.org\\/images\\/core\\/emoji\\/13.0.0\\/svg\\/","svgExt":".svg","source":{'
        b'"concatemoji":"https:\\/\\/www.tutorialbar.com\\/wp-includes\\/js\\/wp-emoji-release.min.js?ver=5.5.3"}};\n'
        b'\t\t\t!function(e,a,t){var r,n,o,i,p=a.createElement("canvas"),s=p.getContext&&p.getContext("2d");function '
        b"c(e,t){var a=String.fromCharCode;s.clearRect(0,0,p.width,p.height),s.fillText(a.apply(this,e),0,"
        b"0);var r=p.toDataURL();return s.clearRect(0,0,p.width,p.height),s.fillText(a.apply(this,t),0,0),"
        b'r===p.toDataURL()}function l(e){if(!s||!s.fillText)return!1;switch(s.textBaseline="top",s.font="600 32px '
        b'Arial",e){case"flag":return!c([127987,65039,8205,9895,65039],[127987,65039,8203,9895,65039])&&(!c([55356,'
        b"56826,55356,56819],[55356,56826,8203,55356,56819])&&!c([55356,57332,56128,56423,56128,56418,56128,56421,"
        b"56128,56430,56128,56423,56128,56447],[55356,57332,8203,56128,56423,8203,56128,56418,8203,56128,56421,8203,"
        b'56128,56430,8203,56128,56423,8203,56128,56447]));case"emoji":return!c([55357,56424,8205,55356,57212],[55357,'
        b'56424,8203,55356,57212])}return!1}function d(e){var t=a.createElement("script");t.src=e,'
        b't.defer=t.type="text/javascript",a.getElementsByTagName("head")[0].appendChild(t)}for(i=Array("flag",'
        b'"emoji"),t.supports={everything:!0,everythingExceptFlag:!0},o=0;o<i.length;o++)t.supports[i[o]]=l(i[o]),'
        b't.supports.everything=t.supports.everything&&t.supports[i[o]],"flag"!==i[o]&&('
        b"t.supports.everythingExceptFlag=t.supports.everythingExceptFlag&&t.supports[i["
        b"o]]);t.supports.everythingExceptFlag=t.supports.everythingExceptFlag&&!t.supports.flag,t.DOMReady=!1,"
        b"t.readyCallback=function(){t.DOMReady=!0},t.supports.everything||(n=function(){t.readyCallback()},"
        b'a.addEventListener?(a.addEventListener("DOMContentLoaded",n,!1),e.addEventListener("load",n,'
        b'!1)):(e.attachEvent("onload",n),a.attachEvent("onreadystatechange",function(){'
        b'"complete"===a.readyState&&t.readyCallback()})),(r=t.source||{}).concatemoji?d('
        b"r.concatemoji):r.wpemoji&&r.twemoji&&(d(r.twemoji),d(r.wpemoji)))}(window,document,"
        b'window._wpemojiSettings);\n\t\t</script>\n\t\t<style type="text/css">\nimg.wp-smiley,\nimg.emoji {'
        b"\n\tdisplay: inline !important;\n\tborder: none !important;\n\tbox-shadow: none !important;\n\theight: 1em "
        b"!important;\n\twidth: 1em !important;\n\tmargin: 0 .07em !important;\n\tvertical-align: -0.1em "
        b"!important;\n\tbackground: none !important;\n\tpadding: 0 !important;\n}\n</style>\n\t<link "
        b"rel='stylesheet' id='wp-block-library-css'  "
        b"href='https://www.tutorialbar.com/wp-includes/css/dist/block-library/style.min.css?ver=5.5.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='cookie-notice-front-css'  "
        b"href='https://www.tutorialbar.com/wp-content/plugins/cookie-notice/css/front.min.css?ver=5.5.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='parent-style-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/style.css?ver=5.5.3' type='text/css' "
        b"media='all' />\n<link rel='stylesheet' id='elementor-icons-css'  "
        b"href='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib/eicons/css/elementor-icons.min"
        b".css?ver=5.9.1' type='text/css' media='all' />\n<link rel='stylesheet' "
        b"id='elementor-animations-css'  href='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib"
        b"/animations/animations.min.css?ver=3.0.13' type='text/css' media='all' />\n<link rel='stylesheet' "
        b"id='elementor-frontend-legacy-css'  "
        b"href='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/css/frontend-legacy.min.css?ver=3.0"
        b".13' type='text/css' media='all' />\n<link rel='stylesheet' id='elementor-frontend-css'  "
        b"href='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.0.13' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='elementor-post-10868-css'  "
        b"href='https://www.tutorialbar.com/wp-content/uploads/elementor/css/post-10868.css?ver=1604541601' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='rhstyle-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-blankchild/style.css?ver=13.3' type='text/css' "
        b"media='all' />\n<link rel='stylesheet' id='responsive-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/css/responsive.css?ver=13.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='rehubicons-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/iconstyle.css?ver=13.3' type='text/css' "
        b"media='all' />\n<link rel='stylesheet' id='google-fonts-1-css'  "
        b"href='https://fonts.googleapis.com/css?family=Roboto%3A100%2C100italic%2C200%2C200italic%2C300%2C300italic"
        b"%2C400%2C400italic%2C500%2C500italic%2C600%2C600italic%2C700%2C700italic%2C800%2C800italic%2C900%2C900italic"
        b"%7CRoboto+Slab%3A100%2C100italic%2C200%2C200italic%2C300%2C300italic%2C400%2C400italic%2C500%2C500italic"
        b"%2C600%2C600italic%2C700%2C700italic%2C800%2C800italic%2C900%2C900italic&#038;ver=5.5.3' type='text/css' "
        b"media='all' />\n<script type='text/javascript' id='cookie-notice-front-js-extra'>\n/* <![CDATA[ "
        b'*/\nvar cnArgs = {"ajaxUrl":"https:\\/\\/www.tutorialbar.com\\/wp-admin\\/admin-ajax.php",'
        b'"nonce":"0dc1b2677e","hideEffect":"none","position":"bottom","onScroll":"1","onScrollOffset":"200",'
        b'"onClick":"0","cookieName":"cookie_notice_accepted","cookieTime":"2592000","cookieTimeRejected":"2592000",'
        b'"cookiePath":"\\/","cookieDomain":"","redirection":"0","cache":"0","refuse":"0","revokeCookies":"0",'
        b'"revokeCookiesOpt":"automatic","secure":"1","coronabarActive":"0"};\n/* ]]> */\n</script>\n<script '
        b"type='text/javascript' src='https://www.tutorialbar.com/wp-content/plugins/cookie-notice/js/front.min.js"
        b"?ver=1.3.2' id='cookie-notice-front-js'></script>\n<script type='text/javascript' "
        b"src='https://www.googletagmanager.com/gtag/js?id=UA-158052069-1' id='google_gtagjs-js' "
        b"async></script>\n<script type='text/javascript' id='google_gtagjs-js-after'>\nwindow.dataLayer = "
        b"window.dataLayer || [];function gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('set', "
        b"'developer_id.dZTNiMT', true);\ngtag('config', 'UA-158052069-1', {\"anonymize_ip\":true} "
        b");\n</script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/jquery/jquery.js?ver=1.12.4-wp' "
        b'id=\'jquery-core-js\'></script>\n<link rel="https://api.w.org/" href="https://www.tutorialbar.com/wp-json/" '
        b'/><link rel="alternate" type="application/json" href="https://www.tutorialbar.com/wp-json/wp/v2/pages/19" '
        b'/><link rel="EditURI" type="application/rsd+xml" title="RSD" '
        b'href="https://www.tutorialbar.com/xmlrpc.php?rsd" />\n<link rel="wlwmanifest" '
        b'type="application/wlwmanifest+xml" href="https://www.tutorialbar.com/wp-includes/wlwmanifest.xml" /> \n<meta '
        b'name="generator" content="WordPress 5.5.3" />\n<link rel=\'shortlink\' '
        b'href=\'https://www.tutorialbar.com/?p=19\' />\n<link rel="alternate" type="application/json+oembed" '
        b'href="https://www.tutorialbar.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.tutorialbar.com%2Fall'
        b'-courses%2F" />\n<link rel="alternate" type="text/xml+oembed" '
        b'href="https://www.tutorialbar.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.tutorialbar.com%2Fall'
        b'-courses%2F&#038;format=xml" />\n<meta name="generator" content="Site Kit by Google 1.20.0" />\n<script '
        b"type='text/javascript'>\nfunction addLink() {\n    var selection = window.getSelection();\n    var htmlDiv "
        b'= document.createElement("div");\n    for (var i = 0; i < selection.rangeCount; ++i) {\n        '
        b"htmlDiv.appendChild(selection.getRangeAt(i).cloneContents());\n    }\n    var selectionHTML = "
        b'htmlDiv.innerHTML;\n    var pagelink = "<br/><br/>View more at TutorialBar: <a '
        b'href=\'"+document.location.href+"\'>"+document.location.href+"</a>";\n    var copytext = selectionHTML + '
        b"pagelink;\n    \n    var newdiv = document.createElement('div');\n    newdiv.style.position = "
        b"'absolute';\n    newdiv.style.left = '-99999px';\n    \n    document.body.appendChild(newdiv);\n    "
        b"newdiv.innerHTML = copytext;\n    selection.selectAllChildren(newdiv);\n    window.setTimeout(function () { "
        b'document.body.removeChild(newdiv); }, 0);\n}\ndocument.oncopy = addLink\n</script>\n\n<link rel="preload" '
        b'href="https://www.tutorialbar.com/wp-content/themes/rehub-theme/fonts/rhicons.woff2?leryx9" as="font" '
        b'type="font/woff2" crossorigin="crossorigin"><style type="text/css"> @media (min-width:1025px){header '
        b".logo-section{padding:5px 0;}}.logo_section_wrap{box-shadow:0 15px 30px 0 rgba(119,123,146,"
        b"0.1)}#main_header,.is-sticky .logo_section_wrap,.sticky-active.logo_section_wrap{background-color:#000000 "
        b"!important}.main-nav.white_style{border-top:none}nav.top_menu > ul:not(.off-canvas) > li > a:after{"
        b"top:auto;bottom:0}.header-top{border:none;}.footer-bottom{background-color:#000000 !important}.footer-bottom "
        b".footer_widget{border:none !important} .widget .title:after{border-bottom:2px solid "
        b"#ff4136;}.rehub-main-color-border,nav.top_menu > ul > li.vertical-menu.border-main-color .sub-menu,"
        b".rh-main-bg-hover:hover,.wp-block-quote,ul.def_btn_link_tabs li.active a,.wp-block-pullquote{"
        b"border-color:#ff4136;}.wpsm_promobox.rehub_promobox{border-left-color:#ff4136!important;}.color_link{"
        b"color:#ff4136 !important;}.search-header-contents{border-top-color:#ff4136;}.featured_slider:hover .score,"
        b".top_chart_controls .controls:hover,article.post .wpsm_toplist_heading:before{"
        b"border-color:#ff4136;}.btn_more:hover,.small_post .overlay .btn_more:hover,.tw-pagination .current{"
        b"border:1px solid #ff4136;color:#fff}.rehub_woo_review .rehub_woo_tabs_menu li.current{border-top:3px solid "
        b"#ff4136;}.gallery-pics .gp-overlay{box-shadow:0 0 0 4px #ff4136 inset;}.post .rehub_woo_tabs_menu "
        b"li.current,.woocommerce div.product .woocommerce-tabs ul.tabs li.active{border-top:2px solid "
        b"#ff4136;}.rething_item a.cat{border-bottom-color:#ff4136}nav.top_menu ul li ul.sub-menu{border-bottom:2px "
        b"solid #ff4136;}.widget.deal_daywoo,.elementor-widget-wpsm_woofeatured .deal_daywoo{border:3px solid "
        b"#ff4136;padding:20px;background:#fff;}.deal_daywoo .wpsm-bar-bar{background-color:#ff4136 !important} "
        b"#buddypress div.item-list-tabs ul li.selected a span,#buddypress div.item-list-tabs ul li.current a span,"
        b"#buddypress div.item-list-tabs ul li a span,.user-profile-div .user-menu-tab > li.active > a,"
        b".user-profile-div .user-menu-tab > li.active > a:focus,.user-profile-div .user-menu-tab > li.active > "
        b"a:hover,.slide .news_cat a,.news_in_thumb:hover .news_cat a,.news_out_thumb:hover .news_cat a,"
        b".col-feat-grid:hover .news_cat a,.carousel-style-deal .re_carousel .controls,.re_carousel .controls:hover,"
        b".openedprevnext .postNavigation a,.postNavigation a:hover,.top_chart_pagination a.selected,"
        b".flex-control-paging li a.flex-active,.flex-control-paging li a:hover,.btn_more:hover,.tabs-menu li:hover,"
        b".tabs-menu li.current,.featured_slider:hover .score,#bbp_user_edit_submit,.bbp-topic-pagination a,"
        b".bbp-topic-pagination a,.custom-checkbox label.checked:after,.slider_post .caption,ul.postpagination "
        b"li.active a,ul.postpagination li:hover a,ul.postpagination li a:focus,.top_theme h5 strong,.re_carousel "
        b".text:after,#topcontrol:hover,.main_slider .flex-overlay:hover a.read-more,.rehub_chimp #mc_embed_signup "
        b"input#mc-embedded-subscribe,#rank_1.rank_count,#toplistmenu > ul li:before,.rehub_chimp:before,.wpsm-members "
        b"> strong:first-child,.r_catbox_btn,.wpcf7 .wpcf7-submit,.comm_meta_wrap .rh_user_s2_label,.wpsm_pretty_hover "
        b"li:hover,.wpsm_pretty_hover li.current,.rehub-main-color-bg,.togglegreedybtn:after,.rh-bg-hover-color:hover "
        b".news_cat a,.rh-main-bg-hover:hover,.rh_wrapper_video_playlist .rh_video_currently_playing,"
        b".rh_wrapper_video_playlist .rh_video_currently_playing.rh_click_video:hover,.rtmedia-list-item "
        b".rtmedia-album-media-count,.tw-pagination .current,.dokan-dashboard .dokan-dash-sidebar "
        b"ul.dokan-dashboard-menu li.active,.dokan-dashboard .dokan-dash-sidebar ul.dokan-dashboard-menu li:hover,"
        b".dokan-dashboard .dokan-dash-sidebar ul.dokan-dashboard-menu li.dokan-common-links a:hover,"
        b"#ywqa-submit-question,.woocommerce .widget_price_filter .ui-slider .ui-slider-range,.rh-hov-bor-line > "
        b"a:after,nav.top_menu > ul:not(.off-canvas) > li > a:after,.rh-border-line:after,"
        b".wpsm-table.wpsm-table-main-color table tr th,.rehub_chimp_flat #mc_embed_signup "
        b"input#mc-embedded-subscribe{background:#ff4136;}@media (max-width:767px){.postNavigation a{"
        b"background:#ff4136;}}.rh-main-bg-hover:hover,.rh-main-bg-hover:hover .whitehovered{color:#fff !important} a,"
        b".carousel-style-deal .deal-item .priced_block .price_count ins,nav.top_menu ul li.menu-item-has-children ul "
        b"li.menu-item-has-children > a:before,.top_chart_controls .controls:hover,.flexslider .fa-pulse,"
        b".footer-bottom .widget .f_menu li a:hover,.comment_form h3 a,.bbp-body li.bbp-forum-info > a:hover,"
        b".bbp-body li.bbp-topic-title > a:hover,#subscription-toggle a:before,#favorite-toggle a:before,"
        b".aff_offer_links .aff_name a,.rh-deal-price,.commentlist .comment-content small a,.related_articles "
        b".title_cat_related a,article em.emph,.campare_table table.one td strong.red,.sidebar .tabs-item .detail p a,"
        b".footer-bottom .widget .title span,footer p a,.welcome-frase strong,article.post "
        b".wpsm_toplist_heading:before,.post a.color_link,.categoriesbox:hover h3 a:after,.bbp-body li.bbp-forum-info "
        b"> a,.bbp-body li.bbp-topic-title > a,.widget .title i,.woocommerce-MyAccount-navigation ul li.is-active a,"
        b".category-vendormenu li.current a,.deal_daywoo .title,.rehub-main-color,.wpsm_pretty_colored ul li.current "
        b"a,.wpsm_pretty_colored ul li.current,.rh-heading-hover-color:hover h2 a,.rh-heading-hover-color:hover h3 a,"
        b".rh-heading-hover-color:hover h4 a,.rh-heading-hover-color:hover h5 a,.rh-heading-hover-color:hover "
        b".rh-heading-hover-item a,.rh-heading-icon:before,.widget_layered_nav ul li.chosen a:before,"
        b".wp-block-quote.is-style-large p,ul.page-numbers li span.current,ul.page-numbers li a:hover,ul.page-numbers "
        b"li.active a,.page-link > span:not(.page-link-title),blockquote:not(.wp-block-quote) p,"
        b"span.re_filtersort_btn:hover,span.active.re_filtersort_btn,.deal_daywoo .price,div.sortingloading:after{"
        b"color:#ff4136;} .page-link > span:not(.page-link-title),.postimagetrend .title,.widget.widget_affegg_widget "
        b".title,.widget.top_offers .title,.widget.cegg_widget_products .title,header .header_first_style .search "
        b'form.search-form [type="submit"],header .header_eight_style .search form.search-form [type="submit"],'
        b".more_post a,.more_post span,.filter_home_pick span.active,.filter_home_pick span:hover,.filter_product_pick "
        b"span.active,.filter_product_pick span:hover,.rh_tab_links a.active,.rh_tab_links a:hover,.wcv-navigation "
        b'ul.menu li.active,.wcv-navigation ul.menu li:hover a,form.search-form [type="submit"],.rehub-sec-color-bg,'
        b"input#ywqa-submit-question,input#ywqa-send-answer,.woocommerce button.button.alt,.tabsajax "
        b"span.active.re_filtersort_btn,.wpsm-table.wpsm-table-sec-color table tr th,.rh-slider-arrow{"
        b"background:#111111 !important;color:#fff !important;outline:0}.widget.widget_affegg_widget .title:after,"
        b".widget.top_offers .title:after,.vc_tta-tabs.wpsm-tabs .vc_tta-tab.vc_active,.vc_tta-tabs.wpsm-tabs "
        b".vc_tta-panel.vc_active .vc_tta-panel-heading,.widget.cegg_widget_products .title:after{"
        b"border-top-color:#111111 !important;}.page-link > span:not(.page-link-title){border:1px solid "
        b"#111111;}.page-link > span:not(.page-link-title),.header_first_style .search form.search-form ["
        b'type="submit"] i{color:#fff !important;}.rh_tab_links a.active,.rh_tab_links a:hover,'
        b".rehub-sec-color-border,nav.top_menu > ul > li.vertical-menu.border-sec-color > .sub-menu,"
        b".rh-slider-thumbs-item--active{border-color:#111111}.rh_wrapper_video_playlist .rh_video_currently_playing,"
        b".rh_wrapper_video_playlist .rh_video_currently_playing.rh_click_video:hover{"
        b"background-color:#111111;box-shadow:1200px 0 0 #111111 inset;}.rehub-sec-color{color:#111111} "
        b'form.search-form input[type="text"]{border-radius:4px}.news .priced_block .price_count,.blog_string '
        b".priced_block .price_count,.main_slider .price_count{margin-right:5px}.right_aff .priced_block "
        b".btn_offer_block,.right_aff .priced_block .price_count{border-radius:0 "
        b'!important}form.search-form.product-search-form input[type="text"]{border-radius:4px 0 0 '
        b'4px;}form.search-form [type="submit"]{border-radius:0 4px 4px 0;}.rtl form.search-form.product-search-form '
        b'input[type="text"]{border-radius:0 4px 4px 0;}.rtl form.search-form [type="submit"]{border-radius:4px 0 0 '
        b"4px;}.price_count,.rehub_offer_coupon,#buddypress .dir-search input[type=text],.gmw-form-wrapper input["
        b"type=text],.gmw-form-wrapper select,#buddypress a.button,.btn_more,#main_header .wpsm-button,"
        b'#rh-header-cover-image .wpsm-button,#wcvendor_image_bg .wpsm-button,input[type="text"],textarea,'
        b'input[type="tel"],input[type="password"],input[type="email"],input[type="url"],input[type="number"],'
        b'.def_btn,input[type="submit"],input[type="button"],input[type="reset"],.rh_offer_list .offer_thumb '
        b".deal_img_wrap,.grid_onsale,.rehub-main-smooth,.re_filter_instore span.re_filtersort_btn:hover,"
        b".re_filter_instore span.active.re_filtersort_btn,#buddypress .standard-form input[type=text],#buddypress "
        b".standard-form textarea,.blacklabelprice{border-radius:4px}.news-community,.woocommerce .products.grid_woo "
        b".product,.rehub_chimp #mc_embed_signup input.email,#mc_embed_signup input#mc-embedded-subscribe,"
        b".rh_offer_list,.woo-tax-logo,#buddypress div.item-list-tabs ul li a,#buddypress form#whats-new-form,"
        b"#buddypress div#invite-list,#buddypress #send-reply div.message-box,.rehub-sec-smooth,.rate-bar-bar,"
        b".rate-bar,#wcfm-main-contentainer #wcfm-content,.wcfm_welcomebox_header{border-radius:5px} .woocommerce "
        b".woo-button-area .masked_coupon,.woocommerce a.woo_loop_btn,.woocommerce .button.checkout,.woocommerce "
        b"input.button.alt,.woocommerce a.add_to_cart_button:not(.flat-woo-btn),.woocommerce-page "
        b"a.add_to_cart_button:not(.flat-woo-btn),.woocommerce .single_add_to_cart_button,.woocommerce div.product "
        b"form.cart .button,.woocommerce .checkout-button.button,.woofiltersbig .prdctfltr_buttons "
        b"a.prdctfltr_woocommerce_filter_submit,.priced_block .btn_offer_block,.priced_block .button,"
        b'.rh-deal-compact-btn,input.mdf_button,#buddypress input[type="submit"],#buddypress input[type="button"],'
        b'#buddypress input[type="reset"],#buddypress button.submit,.wpsm-button.rehub_main_btn,.wcv-grid a.button,'
        b"input.gmw-submit,#ws-plugin--s2member-profile-submit,#rtmedia_create_new_album,"
        b'input[type="submit"].dokan-btn-theme,a.dokan-btn-theme,.dokan-btn-theme,#wcfm_membership_container '
        b"a.wcfm_submit_button,.woocommerce button.button,.rehub-main-btn-bg{background:none #ff4136 "
        b"!important;color:#ffffff !important;fill:#ffffff !important;border:none !important;text-decoration:none "
        b"!important;outline:0;box-shadow:-1px 6px 19px rgba(255,65,54,0.2) !important;border-radius:4px "
        b"!important;}.rehub-main-btn-bg > a{color:#ffffff !important;}.woocommerce a.woo_loop_btn:hover,.woocommerce "
        b".button.checkout:hover,.woocommerce input.button.alt:hover,.woocommerce a.add_to_cart_button:not("
        b".flat-woo-btn):hover,.woocommerce-page a.add_to_cart_button:not(.flat-woo-btn):hover,.woocommerce "
        b"a.single_add_to_cart_button:hover,.woocommerce-page a.single_add_to_cart_button:hover,.woocommerce "
        b"div.product form.cart .button:hover,.woocommerce-page div.product form.cart .button:hover,.woocommerce "
        b".checkout-button.button:hover,.woofiltersbig .prdctfltr_buttons a.prdctfltr_woocommerce_filter_submit:hover,"
        b".priced_block .btn_offer_block:hover,.wpsm-button.rehub_main_btn:hover,#buddypress input["
        b'type="submit"]:hover,#buddypress input[type="button"]:hover,#buddypress input[type="reset"]:hover,'
        b"#buddypress button.submit:hover,.small_post .btn:hover,.ap-pro-form-field-wrapper input["
        b'type="submit"]:hover,.wcv-grid a.button:hover,#ws-plugin--s2member-profile-submit:hover,.rething_button '
        b".btn_more:hover,#wcfm_membership_container a.wcfm_submit_button:hover,.woocommerce button.button:hover,"
        b".rehub-main-btn-bg:hover,.rehub-main-btn-bg:hover > a{background:none #ff4136 !important;color:#ffffff "
        b"!important;box-shadow:-1px 6px 13px rgba(255,65,54,"
        b"0.4) !important;border-color:transparent;}.rehub_offer_coupon:hover{border:1px dashed "
        b"#ff4136;}.rehub_offer_coupon:hover i.far,.rehub_offer_coupon:hover i.fal,.rehub_offer_coupon:hover i.fas{"
        b"color:#ff4136}.re_thing_btn .rehub_offer_coupon.not_masked_coupon:hover{color:#ff4136 "
        b"!important}.woocommerce a.woo_loop_btn:active,.woocommerce .button.checkout:active,.woocommerce "
        b".button.alt:active,.woocommerce a.add_to_cart_button:not(.flat-woo-btn):active,.woocommerce-page "
        b"a.add_to_cart_button:not(.flat-woo-btn):active,.woocommerce a.single_add_to_cart_button:active,"
        b".woocommerce-page a.single_add_to_cart_button:active,.woocommerce div.product form.cart .button:active,"
        b".woocommerce-page div.product form.cart .button:active,.woocommerce .checkout-button.button:active,"
        b".woofiltersbig .prdctfltr_buttons a.prdctfltr_woocommerce_filter_submit:active,"
        b'.wpsm-button.rehub_main_btn:active,#buddypress input[type="submit"]:active,#buddypress input['
        b'type="button"]:active,#buddypress input[type="reset"]:active,#buddypress button.submit:active,'
        b'.ap-pro-form-field-wrapper input[type="submit"]:active,.wcv-grid a.button:active,'
        b'#ws-plugin--s2member-profile-submit:active,input[type="submit"].dokan-btn-theme:active,'
        b"a.dokan-btn-theme:active,.dokan-btn-theme:active,.woocommerce button.button:active,"
        b".rehub-main-btn-bg:active{background:none #ff4136 !important;box-shadow:0 1px 0 #999 "
        b"!important;top:2px;color:#ffffff !important;}.rehub_btn_color{background-color:#ff4136;border:1px solid "
        b"#ff4136;color:#ffffff;text-shadow:none}.rehub_btn_color:hover{"
        b"color:#ffffff;background-color:#ff4136;border:1px solid #ff4136;}.rething_button .btn_more{border:1px solid "
        b"#ff4136;color:#ff4136;}.rething_button .priced_block.block_btnblock .price_count{"
        b"color:#ff4136;font-weight:normal;}.widget_merchant_list .buttons_col{background-color:#ff4136 "
        b"!important;}.widget_merchant_list .buttons_col a{color:#ffffff !important;}.rehub-svg-btn-fill svg{"
        b"fill:#ff4136;}.rehub-svg-btn-stroke svg{stroke:#ff4136;}@media (max-width:767px){#float-panel-woo-area{"
        b"border-top:1px solid #ff4136}}.rh_post_layout_big_offer .priced_block .btn_offer_block{"
        b"text-shadow:none}</style><style>footer#theme_footer.dark_style {background: #000000}</style><script async "
        b'src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script><script>(adsbygoogle = '
        b'window.adsbygoogle || []).push({"google_ad_client":"ca-pub-5221546730192444","enable_page_level_ads":true,'
        b'"tag_partner":"site_kit"});</script><link rel="icon" '
        b'href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-32x32.png" sizes="32x32" '
        b'/>\n<link rel="icon" href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-192x192'
        b'.png" sizes="192x192" />\n<link rel="apple-touch-icon" '
        b'href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-180x180.png" />\n<meta '
        b'name="msapplication-TileImage" content="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar'
        b'-icon-270x270.png" />\n\t\t<style type="text/css" id="wp-custom-css">\n\t\t\t.logo_image_mobile > img {'
        b'\n\twidth: 200px;\n}\t\t</style>\n\t\t</head>\r\n<body class="page-template-default page page-id-19 '
        b'cookies-set cookies-accepted elementor-default elementor-kit-10868 elementor-page elementor-page-19">\r\n\t  '
        b'             \r\n<!-- Outer Start -->\r\n<div class="rh-outer-wrap">\r\n    <div id="top_ankor"></div>\r\n   '
        b' <!-- HEADER -->\r\n            <header id="main_header" class="dark_style">\r\n            <div '
        b'class="header_wrap">\r\n                                                <!-- Logo section -->\r\n<div '
        b'class="rh-stickme header_five_style logo_section_wrap header_one_row">\r\n    <div class="rh-container '
        b'tabletblockdisplay mb0 disabletabletpadding">\r\n        <div class="logo-section rh-flex-center-align '
        b'tabletblockdisplay disabletabletpadding mb0">\r\n            <div class="logo hideontablet">\r\n             '
        b'                       <a href="https://www.tutorialbar.com" class="logo_image"><img '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Tutorial Bar" height="" '
        b'width="200" /></a>\r\n                       \r\n            </div> \r\n            <!-- Main Navigation '
        b'-->\r\n            <div class="main-nav header_icons_menu mob-logo-enabled rh-flex-right-align  dark_style"> '
        b'     \r\n                <nav class="top_menu"><ul id="menu-header-menu" class="menu"><li id="menu-item-23" '
        b'class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home"><a '
        b'href="https://www.tutorialbar.com/">Home</a></li>\n<li id="menu-item-24" class="menu-item '
        b"menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-19 "
        b'current_page_item"><a href="https://www.tutorialbar.com/all-courses/">All Courses</a></li>\n<li '
        b'id="menu-item-9702" class="menu-item menu-item-type-custom menu-item-object-custom"><a '
        b'href="https://www.tutorialbar.com/store/eduonix/">Eduonix Free Courses</a></li>\n<li id="menu-item-17258" '
        b'class="menu-item menu-item-type-custom menu-item-object-custom"><a '
        b'href="https://www.tutorialbar.com/store/edyoda/">EdYoda Free Courses</a></li>\n<li id="menu-item-1308" '
        b'class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children"><a '
        b'href="https://www.tutorialbar.com/course-categories/">Course Categories</a>\n<ul class="sub-menu">\n\t<li '
        b'id="menu-item-3330" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/development/">Development</a></li>\n\t<li id="menu-item-3331" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/it-software/">IT &amp; Software</a></li>\n\t<li '
        b'id="menu-item-3339" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/finance-accounting/">Finance &amp; Accounting</a></li>\n\t<li '
        b'id="menu-item-3338" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/design/">Design</a></li>\n\t<li id="menu-item-3332" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/business/">Business</a></li>\n\t<li id="menu-item-3333" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/marketing/">Marketing</a></li>\n\t<li id="menu-item-3341" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/health-fitness/">Health &amp; Fitness</a></li>\n\t<li '
        b'id="menu-item-3340" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/office-productivity/">Office Productivity</a></li>\n\t<li '
        b'id="menu-item-3337" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/photography/">Photography</a></li>\n\t<li id="menu-item-3334" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/personal-development/">Personal Development</a></li>\n\t<li '
        b'id="menu-item-3336" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/teaching-academics/">Teaching &amp; '
        b'Academics</a></li>\n</ul>\n</li>\n<li id="menu-item-25" class="menu-item menu-item-type-post_type '
        b'menu-item-object-page"><a href="https://www.tutorialbar.com/contact/">Contact Us</a></li>\n</ul></nav>       '
        b'         <div class="responsive_nav_wrap rh_mobile_menu">\r\n                    <div id="dl-menu" '
        b'class="dl-menuwrapper rh-flex-center-align">\r\n                        <button id="dl-trigger" '
        b'class="dl-trigger" aria-label="Menu">\r\n                            <svg viewBox="0 0 32 32" '
        b'xmlns="http://www.w3.org/2000/svg">\r\n                                <g>\r\n                               '
        b'     <line stroke-linecap="round" id="rhlinemenu_1" y2="7" x2="29" y1="7" x1="3"/>\r\n                       '
        b'             <line stroke-linecap="round" id="rhlinemenu_2" y2="16" x2="18" y1="16" x1="3"/>\r\n             '
        b'                       <line stroke-linecap="round" id="rhlinemenu_3" y2="25" x2="26" y1="25" x1="3"/>\r\n   '
        b"                             </g>\r\n                            </svg>\r\n                        "
        b'</button>\r\n                        <div id="mobile-menu-icons" class="rh-flex-center-align '
        b'rh-flex-right-align">\r\n                            <div id="slide-menu-mobile"></div>\r\n                  '
        b"      </div>\r\n                    </div>\r\n                                    </div>\r\n                "
        b'<div class="search-header-contents"><form  role="search" method="get" class="search-form" '
        b'action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" placeholder="Search"  '
        b'data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  \t<button type="submit" '
        b'class="btnsearch"><i class="rhicon rhi-search"></i></button>\r\n</form>\r\n</div>\r\n            </div>  '
        b'\r\n             \r\n                    \r\n            <div class="header-actions-logo">\r\n               '
        b' <div class="rh-flex-center-align">\r\n                                                             \r\n     '
        b"                 \r\n                                                                               \r\n     "
        b"                                    \r\n                </div> \r\n            </div>                        "
        b"\r\n            <!-- /Main Navigation -->                                                        \r\n        "
        b"</div>\r\n    </div>\r\n</div>\r\n<!-- /Logo section -->  \r\n\r\n            </div>  \r\n        "
        b'</header>\r\n            \r\n<!-- CONTENT -->\r\n<div class="rh-container def"> \r\n    <div '
        b'class="rh-content-wrap clearfix">\r\n        <!-- Main Side -->\r\n        <div class="main-side page '
        b'clearfix" id="content">\r\n            <div class="rh-post-wrapper">\r\n                <article class="post '
        b'mb0" id="page-19">       \r\n                                                            <div '
        b'class="title"><h1 class="entry-title">All Courses</h1></div>\r\n                                        '
        b'\t\t<div data-elementor-type="wp-page" data-elementor-id="19" class="elementor elementor-19" '
        b'data-elementor-settings="[]">\n\t\t\t\t\t\t<div class="elementor-inner">\n\t\t\t\t\t\t\t<div '
        b'class="elementor-section-wrap">\n\t\t\t\t\t\t\t<section class="elementor-section elementor-top-section '
        b"elementor-element elementor-element-b521b64 elementor-section-boxed elementor-section-height-default "
        b'elementor-section-height-default" data-id="b521b64" data-element_type="section">\n\t\t\t\t\t\t<div '
        b'class="elementor-container elementor-column-gap-default">\n\t\t\t\t\t\t\t<div '
        b'class="elementor-row">\n\t\t\t\t\t<div class="elementor-column elementor-col-100 elementor-top-column '
        b'elementor-element elementor-element-31eaea1" data-id="31eaea1" data-element_type="column">\n\t\t\t<div '
        b'class="elementor-column-wrap elementor-element-populated">\n\t\t\t\t\t\t\t<div '
        b'class="elementor-widget-wrap">\n\t\t\t\t\t\t<div class="elementor-element elementor-element-81e6e60 '
        b'elementor-widget elementor-widget-columngrid_loop" data-id="81e6e60" data-element_type="widget" '
        b'data-widget_type="columngrid_loop.default">\n\t\t\t\t<div '
        b'class="elementor-widget-container">\n\t\t\t\t\r\n\t   \r\n\t<div class="columned_grid_module '
        b'rh-flex-eq-height  col_wrap_three" data-filterargs=\'{"post_type":"post","posts_per_page":12,"order":"DESC",'
        b'"orderby":"date"}\' data-template="column_grid" id="rh_clmgrid_1688991757" data-innerargs=\'{'
        b'"columns":"3_col","aff_link":"","exerpt_count":"0","disable_meta":"","enable_btn":"","disable_price":"",'
        b'"image_padding":"","disablecard":""}\'>                    \r\n\t\t\r\n\t\t\t\t\t  \r\n<article '
        b'class="col_item column_grid rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div '
        b'class="button_action abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                        '
        b"              \r\n        </div>                                                           \r\n    </div> "
        b'\r\n        \r\n    <figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/" class="">\r\n   '
        b'                         <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3607708_dda9_6'
        b'-1xciia8krp8jobmo6jt68cn07dh7g8b13ixvh6vi88mc.jpeg" width="350" height="200" alt="Mindfulness Meditation For '
        b'Pain Relief &#038; Stress Management" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management'
        b'/">Mindfulness Meditation For Pain Relief &#038; Stress Management</a></h3>\r\n                              '
        b'   \r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n                  '
        b'                  <div class="post-meta mb0">\r\n                                                            '
        b'                    \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/personal-development/" class="cat">Personal '
        b"Development</a></span>\n\t            \r\n                         \r\n                        <div "
        b'class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>             '
        b"           </div>               \r\n                    </div>\r\n                                           "
        b'     <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/become-a-crm-manager-overview-for-email-marketing-starters/" class="">\r\n '
        b'                           <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3535492_fead-1'
        b'-1xciibreorwmqgvsjbmvgw363cyd71beruh9guokxhno.jpeg" width="350" height="200" alt="Become a CRM Manager: '
        b'overview for Email Marketing starters!" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/become-a-crm-manager-overview-for-email-marketing'
        b'-starters/">Become a CRM Manager: overview for Email Marketing starters!</a></h3>\r\n                        '
        b'         \r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n            '
        b'                        <div class="post-meta mb0">\r\n                                                      '
        b'                          \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/digital-marketing/" class="cat">Digital Marketing</a></span>\n\t  '
        b'          \r\n                         \r\n                        <div class="store_for_grid">\r\n          '
        b'                  <span class="tag_post_store_meta"></span>                        </div>               \r\n '
        b"                   </div>\r\n                                                <div "
        b'class="rh-flex-right-align">\r\n                    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t '
        b"\n\t\t\t\t    \t\n\t            \r\n                </div>\r\n                               \r\n            "
        b"</div>\r\n         \r\n            </div>                                   \r\n</article>\t\t\t\t\t  "
        b'\r\n<article class="col_item column_grid rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> '
        b'\r\n    <div class="button_action abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n           '
        b"                           \r\n        </div>                                                           \r\n "
        b'   </div> \r\n        \r\n    <figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/superminds-the-future-of-artificial-intelligence-ai/" class="">\r\n        '
        b'                    <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/2585846_aa47_4'
        b'-1xciiccanns3buvu71nwifhwc46m8od9p40ndalxyjdw.jpeg" width="350" height="200" alt="SuperMinds: The Future of '
        b'Artificial Intelligence (AI)" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/superminds-the-future-of-artificial-intelligence-ai'
        b'/">SuperMinds: The Future of Artificial Intelligence (AI)</a></h3>\r\n                                 \r\n  '
        b'       \r\n                            <div class="rh-flex-center-align mb10">\r\n                           '
        b'         <div class="post-meta mb0">\r\n                                                                     '
        b'           \t\t\t\t<span class="cat_link_meta"><a href="https://www.tutorialbar.com/category/data-science/" '
        b'class="cat">Data Science</a></span>\n\t            \r\n                         \r\n                        '
        b'<div class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>        '
        b"                </div>               \r\n                    </div>\r\n                                      "
        b'          <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/invade-your-classroom-with-digital-robot-teachers-in-2020/" class="">\r\n  '
        b'                          <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/2684178_375d_2'
        b'-1xciick4n8qe1vmutfxaei9x6ee7msigsl3f2ykycfj8.jpeg" width="350" height="200" alt="Invade Your Classroom with '
        b'Digital Robot Teachers in 2020" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/invade-your-classroom-with-digital-robot-teachers-in-2020'
        b'/">Invade Your Classroom with Digital Robot Teachers in 2020</a></h3>\r\n                                 '
        b'\r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n                     '
        b'               <div class="post-meta mb0">\r\n                                                               '
        b'                 \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/other-teaching-academics/" class="cat">Other Teaching &amp; '
        b"Academics</a></span>\n\t            \r\n                         \r\n                        <div "
        b'class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>             '
        b"           </div>               \r\n                    </div>\r\n                                           "
        b'     <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/introduction-au-machine-learning-python/" class="">\r\n                    '
        b'        <img loading="lazy" src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3265788_84cb'
        b'-1xciicrymtoorwdvfu6oal1y0olt0wnnw266smjyqbok.jpeg" width="350" height="200" alt="Introduction au Machine '
        b'Learning / Python" />                    </a>\r\n    </figure>\r\n        <div class="content_constructor '
        b'pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal lineheight20"><a '
        b'href="https://www.tutorialbar.com/introduction-au-machine-learning-python/">Introduction au Machine Learning '
        b"/ Python</a></h3>\r\n                                 \r\n         \r\n                            <div "
        b'class="rh-flex-center-align mb10">\r\n                                    <div class="post-meta mb0">\r\n    '
        b"                                                                            \t\t\t\t<span "
        b'class="cat_link_meta"><a href="https://www.tutorialbar.com/category/informatique-et-logiciels/" '
        b'class="cat">Informatique et logiciels</a></span>\n\t            \r\n                         \r\n            '
        b'            <div class="store_for_grid">\r\n                            <span '
        b'class="tag_post_store_meta"></span>                        </div>               \r\n                    '
        b'</div>\r\n                                                <div class="rh-flex-right-align">\r\n              '
        b"      \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/comic-creation-for-entrepreneurs-2020-edition/" class="">\r\n              '
        b'              <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3049792_cb9b_2'
        b'-1xciiczsmemzhx4w28g26ntyuytef0suzj8yiaiz47tw.jpeg" width="350" height="200" alt="Comic Creation for '
        b'Entrepreneurs (2020 Edition)" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/comic-creation-for-entrepreneurs-2020-edition/">Comic '
        b"Creation for Entrepreneurs (2020 Edition)</a></h3>\r\n                                 \r\n         \r\n     "
        b'                       <div class="rh-flex-center-align mb10">\r\n                                    <div '
        b'class="post-meta mb0">\r\n                                                                                '
        b'\t\t\t\t<span class="cat_link_meta"><a href="https://www.tutorialbar.com/category/design/" '
        b'class="cat">Design</a></span>\n\t            \r\n                         \r\n                        <div '
        b'class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>             '
        b"           </div>               \r\n                    </div>\r\n                                           "
        b'     <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/delicious-japanese-language-for-foodies-jlpt-n5-jlpt-n4/" class="">\r\n    '
        b'                        <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3439360_14af_2'
        b'-1xciid7mlzla7xvwompg2qlzp90zt4y230bq7yhzi3z8.jpeg" width="350" height="200" alt="Delicious Japanese '
        b'language for foodies (JLPT n5/JLPT n4)" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/delicious-japanese-language-for-foodies-jlpt-n5-jlpt-n4'
        b'/">Delicious Japanese language for foodies (JLPT n5/JLPT n4)</a></h3>\r\n                                 '
        b'\r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n                     '
        b'               <div class="post-meta mb0">\r\n                                                               '
        b'                 \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/language/" class="cat">Language</a></span>\n\t            \r\n    '
        b'                     \r\n                        <div class="store_for_grid">\r\n                            '
        b'<span class="tag_post_store_meta"></span>                        </div>               \r\n                   '
        b' </div>\r\n                                                <div class="rh-flex-right-align">\r\n             '
        b"       \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/sparring-tai-chi-chen-new-frame-routine-2-for-fitness/" class="">\r\n      '
        b'                      <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3623900_e2ff'
        b'-1xciidfglkjkxymxb0ytyte0jj8l79396hehxmgzw04k.jpeg" width="350" height="200" alt="Sparring Tai Chi-Chen New '
        b'Frame Routine 2 for Fitness" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/sparring-tai-chi-chen-new-frame-routine-2-for-fitness'
        b'/">Sparring Tai Chi-Chen New Frame Routine 2 for Fitness</a></h3>\r\n                                 \r\n   '
        b'      \r\n                            <div class="rh-flex-center-align mb10">\r\n                            '
        b'        <div class="post-meta mb0">\r\n                                                                      '
        b'          \t\t\t\t<span class="cat_link_meta"><a href="https://www.tutorialbar.com/category/general-health/" '
        b'class="cat">General Health</a></span>\n\t            \r\n                         \r\n                       '
        b' <div class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>       '
        b"                 </div>               \r\n                    </div>\r\n                                     "
        b'           <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/active-learning-using-games-in-education/" class="">\r\n                   '
        b'         <img loading="lazy" src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/2615718_b38b_4'
        b'-1xciidnal5hvnzdxxf87uw61dtg6ld8g9yh9nag09w9w.jpeg" width="350" height="200" alt="Active Learning &#8211; '
        b'Using Games in Education" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/active-learning-using-games-in-education/">Active '
        b"Learning &#8211; Using Games in Education</a></h3>\r\n                                 \r\n         \r\n     "
        b'                       <div class="rh-flex-center-align mb10">\r\n                                    <div '
        b'class="post-meta mb0">\r\n                                                                                '
        b'\t\t\t\t<span class="cat_link_meta"><a href="https://www.tutorialbar.com/category/other-teaching-academics/" '
        b'class="cat">Other Teaching &amp; Academics</a></span>\n\t            \r\n                         \r\n       '
        b'                 <div class="store_for_grid">\r\n                            <span '
        b'class="tag_post_store_meta"></span>                        </div>               \r\n                    '
        b'</div>\r\n                                                <div class="rh-flex-right-align">\r\n              '
        b"      \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/eiq2-coaching-for-improved-performance-and-superior-results/" '
        b'class="">\r\n                            <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3616404_bedc'
        b'-1xciie86k1dc9ddzl598wfkrmkofn0ab780njqdday04.jpeg" width="350" height="200" alt="EIQ2 Coaching for Improved '
        b'Performance and Superior Results" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/eiq2-coaching-for-improved-performance-and-superior'
        b'-results/">EIQ2 Coaching for Improved Performance and Superior Results</a></h3>\r\n                          '
        b'       \r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n              '
        b'                      <div class="post-meta mb0">\r\n                                                        '
        b'                        \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/business/" class="cat">Business</a></span>\n\t            \r\n    '
        b'                     \r\n                        <div class="store_for_grid">\r\n                            '
        b'<span class="tag_post_store_meta"></span>                        </div>               \r\n                   '
        b' </div>\r\n                                                <div class="rh-flex-right-align">\r\n             '
        b"       \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/quickbooks-pro-desktop-bookkeeping-business-easy-way/" class="">\r\n       '
        b'                     <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/1969570_ba94_3'
        b'-1xciifbchy4tvh52p4k6ctgvtzqell0aolei428f8eqs.jpeg" width="350" height="200" alt="QuickBooks Pro Desktop '
        b'-Bookkeeping Business-Easy Way" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal '
        b'lineheight20"><a href="https://www.tutorialbar.com/quickbooks-pro-desktop-bookkeeping-business-easy-way'
        b'/">QuickBooks Pro Desktop -Bookkeeping Business-Easy Way</a></h3>\r\n                                 \r\n   '
        b'      \r\n                            <div class="rh-flex-center-align mb10">\r\n                            '
        b'        <div class="post-meta mb0">\r\n                                                                      '
        b'          \t\t\t\t<span class="cat_link_meta"><a href="https://www.tutorialbar.com/category/business/" '
        b'class="cat">Business</a></span>\n\t            \r\n                         \r\n                        <div '
        b'class="store_for_grid">\r\n                            <span class="tag_post_store_meta"></span>             '
        b"           </div>               \r\n                    </div>\r\n                                           "
        b'     <div class="rh-flex-right-align">\r\n                    '
        b"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding rh-cartbox"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/quickbooks-online-bank-feeds-credit-card-feeds-2020/" class="">\r\n        '
        b'                    <img loading="lazy" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/2772158_9276_2'
        b'-1xciiftmgz0uw6w45du2rny9snk4iiof8p8yry644tr8.jpeg" width="350" height="200" alt="QuickBooks Online '
        b'\xe2\x80\x93 Bank Feeds &#038; Credit Card Feeds 2020" />                    </a>\r\n    </figure>\r\n       '
        b' <div class="content_constructor pb0 pr20 pl20">\r\n        <h3 class="mb15 mt0 font110 mobfont100 '
        b'fontnormal lineheight20"><a href="https://www.tutorialbar.com/quickbooks-online-bank-feeds-credit-card-feeds'
        b'-2020/">QuickBooks Online \xe2\x80\x93 Bank Feeds &#038; Credit Card Feeds 2020</a></h3>\r\n                 '
        b'                \r\n         \r\n                            <div class="rh-flex-center-align mb10">\r\n     '
        b'                               <div class="post-meta mb0">\r\n                                               '
        b'                                 \t\t\t\t<span class="cat_link_meta"><a '
        b'href="https://www.tutorialbar.com/category/it-software/" class="cat">IT &amp; Software</a></span>\n\t        '
        b'    \r\n                         \r\n                        <div class="store_for_grid">\r\n                '
        b'            <span class="tag_post_store_meta"></span>                        </div>               \r\n       '
        b'             </div>\r\n                                                <div class="rh-flex-right-align">\r\n '
        b"                   \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n     "
        b"           </div>\r\n                               \r\n            </div>\r\n         \r\n            "
        b'</div>                                   \r\n</article>\t\t\r\n\t\t\t\t    <div class="pagination"><ul '
        b'class="page-numbers">\n<li class="active"><a '
        b'href="https://www.tutorialbar.com/all-courses/">1</a></li>\n<li><a '
        b'href="https://www.tutorialbar.com/all-courses/page/2/">2</a></li>\n<li><a '
        b'href="https://www.tutorialbar.com/all-courses/page/3/">3</a></li>\n<li '
        b'class="hellip_paginate_link"><span>&hellip;</span></li>\n<li><a '
        b'href="https://www.tutorialbar.com/all-courses/page/601/">601</a></li>\n<li class="next_paginate_link"><a '
        b'href="https://www.tutorialbar.com/all-courses/page/2/" >Next Page '
        b"&raquo;</a></li>\n</ul>\n</div>\r\n\t\t\r\n\t</div>\r\n\t<div "
        b'class="clearfix"></div>\r\n\r\n\t\t</div>\n\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t</div'
        b">\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t</section>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div>\n\t\t\t"
        b"\t\t</div>\n\t\t                                                          \r\n                </article> "
        b"\r\n            </div>         \r\n        </div>\t\r\n        <!-- /Main Side --> \r\n         \r\n         "
        b'   <!-- Sidebar -->\r\n            <aside class="sidebar">            \r\n    <!-- SIDEBAR WIDGET AREA '
        b'-->\r\n \t\t\t<div id="search-2" class="widget widget_search"><form  role="search" method="get" '
        b'class="search-form" action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" '
        b'placeholder="Search"  data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  '
        b'\t<button type="submit" class="btnsearch"><i class="rhicon '
        b'rhi-search"></i></button>\r\n</form>\r\n</div><div id="custom_html-2" class="widget_text widget '
        b'widget_custom_html"><div class="textwidget custom-html-widget"><script '
        b'type="text/javascript">amzn_assoc_ad_type ="responsive_search_widget"; amzn_assoc_tracking_id '
        b'="deepakmalik-21"; amzn_assoc_marketplace ="amazon"; amzn_assoc_region ="IN"; amzn_assoc_placement =""; '
        b'amzn_assoc_search_type = "search_widget";amzn_assoc_width ="auto"; amzn_assoc_height ="auto"; '
        b'amzn_assoc_default_search_category =""; amzn_assoc_default_search_key ="smartphones";amzn_assoc_theme '
        b'="light"; amzn_assoc_bg_color ="FFFFFF"; </script><script '
        b'src="//z-in.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&Operation=GetScript&ID=OneJS&WS=1'
        b'&Marketplace=IN"></script></div></div><div id="rehub_sticky_on_scroll-2" class="widget '
        b'stickyscroll_widget"><div class="title">Ad</div>\t\t<script async '
        b'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<!-- Sidebar Ad '
        b'-->\r\n<ins class="adsbygoogle"\r\n     style="display:block"\r\n     '
        b'data-ad-client="ca-pub-5221546730192444"\r\n     data-ad-slot="3414440443"\r\n     data-ad-format="auto"\r\n '
        b'    data-full-width-responsive="true"></ins>\r\n<script>\r\n     (adsbygoogle = window.adsbygoogle || ['
        b"]).push({});\r\n</script>\r\n\t\t\t\r\n\t\t</div>\t        \r\n</aside>            <!-- /Sidebar --> \r\n    "
        b"        </div>\r\n</div>\r\n<!-- /CONTENT -->     \r\n<!-- FOOTER -->\r\n\t\t\t\t\r\n\t \t\t\t\t<div "
        b'class="footer-bottom dark_style">\r\n\t\t\t<div class="rh-container clearfix">\r\n\t\t\t\t\t\t\t\t\t<div '
        b'class="rh-flex-eq-height col_wrap_three">\r\n\t\t\t\t\t\t<div class="footer_widget '
        b'col_item">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="text-2" class="widget widget_text"><div '
        b'class="title">About Tutorial Bar</div>\t\t\t<div class="textwidget"><p>Tutorial Bar is a free platform for '
        b"online courses and tutorials. All the courses listed here are <strong>free for limited time</strong>. After "
        b"enrolling a course and complete it you get a <strong>certificate of "
        b"completion</strong>.</p>\n</div>\n\t\t</div>\t\t\t\t\t\t\t \r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t<div "
        b'class="footer_widget col_item">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="rehub_better_menu-2" class="widget '
        b'better_menu"><div class="simple_menu_widget"><div class="title"><i class="rhicon '
        b'rhi-info-circle"></i>Important Links</div>\r\n\t    \t    \t<ul id="menu-footer-menu" class="menu"><li '
        b'id="menu-item-63" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-privacy-policy '
        b'menu-item-63"><a href="https://www.tutorialbar.com/privacy-policy/">Privacy Policy</a></li>\n<li '
        b'id="menu-item-28" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-28"><a '
        b'href="https://www.tutorialbar.com/disclaimer/">Disclaimer</a></li>\n<li id="menu-item-27" class="menu-item '
        b'menu-item-type-post_type menu-item-object-page menu-item-27"><a '
        b'href="https://www.tutorialbar.com/contact/">Contact Us</a></li>\n<li id="menu-item-215" class="menu-item '
        b'menu-item-type-custom menu-item-object-custom menu-item-215"><a '
        b'href="https://tutorialbar.com/sitemap_index.xml">Sitemap</a></li>\n</ul>\t    '
        b"\t\r\n\r\n\t\t\t\r\n\t</div></div>\t\t\t\t\t\t\t \r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t<div "
        b'class="footer_widget col_item last">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="search-3" class="widget last '
        b'widget_search"><div class="title">Search Courses</div><form  role="search" method="get" class="search-form" '
        b'action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" placeholder="Search"  '
        b'data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  \t<button type="submit" '
        b'class="btnsearch"><i class="rhicon rhi-search"></i></button>\r\n</form>\r\n</div><div '
        b'id="rehub_social_link-2" class="widget last social_link"><div class="title">Follow Us:</div>\t\r\n\t\t\t<div '
        b'class="social_icon big_i">\r\n\t\t\r\n\r\n\t\t\t\t\t<a '
        b'href="https://www.facebook.com/groups/271891420195341/" class="fb" rel="nofollow" target="_blank"><i '
        b'class="rhicon rhi-facebook"></i></a>\r\n\t\t\t\r\n\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\r\n\t\t\r\n\t\t\t\t'
        b"\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\t\t\t\t\t<a "
        b'href="https://t.me/tutorialbar_udemy_coupons" class="telegram" rel="nofollow" target="_blank"><i '
        b'class="rhicon rhi-telegram"></i></a>\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t'
        b"</div>\r\n\r\n\t\r\n\t</div>\t\t\t\t\t\t\t "
        b"\r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t</div>\t\r\n\t\t</div>\r\n\t\t\t\t"
        b'<footer id=\'theme_footer\' class="dark_style">\r\n\t\t\t<div class="rh-container clearfix">\r\n\t\t\t\t<div '
        b'class="footer_most_bottom">\r\n\t\t\t\t\t<div class="f_text">\r\n\t\t\t\t\t\t<span '
        b'class="f_text_span">\xc2\xa9 2020 TutorialBar.Com. All rights '
        b"reserved.</span>\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t</div>\t\t\r\n\t\t\t\t</div>\r\n\t\t\t</div>\r\n\t\t</footer"
        b'>\r\n\t\t\t\t<!-- FOOTER -->\r\n</div><!-- Outer End -->\r\n<span class="rehub_scroll" id="topcontrol" '
        b'data-scrollto="#top_ankor"><i class="rhicon rhi-chevron-up"></i></span>\r\n    <div '
        b'id="logo_mobile_wrapper"><a href="https://www.tutorialbar.com" class="logo_image_mobile"><img '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Tutorial Bar" width="35" '
        b'height="35" /></a></div>   \n\n     \n\n    <div id="rhmobpnlcustom" class="rhhidden"><div id="rhmobtoppnl" '
        b'style="background-color: #000000;" class="pr15 pl15 pb15 pt15"><div class="text-center"><a '
        b'href="https://www.tutorialbar.com"><img id="mobpanelimg" '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Logo" width="150" height="45" '
        b"/></a></div></div></div>    \n              \n\n\t<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/inview.js?ver=1.0' "
        b"id='rhinview-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/pgwmodal.js?ver=2.0' "
        b"id='rhpgwmodal-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/unveil.js?ver=5.2.1' "
        b"id='rhunveil-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/hoverintent.js?ver=1.9' "
        b"id='rhhoverintent-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/countdown.js?ver=1.1' "
        b"id='rhcountdown-js'></script>\n<script type='text/javascript' id='rehub-js-extra'>\n/* <![CDATA[ "
        b'*/\nvar translation = {"back":"back","ajax_url":"\\/wp-admin\\/admin-ajax.php","fin":"That\'s all",'
        b'"noresults":"No results found","your_rating":"Your Rating:","nonce":"8517b9eea9","hotnonce":"de646ef9b3",'
        b'"wishnonce":"f6681cbd34","searchnonce":"a50570e5a0","filternonce":"48a2c16c83",'
        b'"rating_tabs_id":"94d813d08b","max_temp":"10","min_temp":"-10","helpnotnonce":"895b9b32a4"};\n/* ]]> '
        b"*/\n</script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/custom.js?ver=13.3' "
        b"id='rehub-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/jquery.sticky.js?ver=1.0.5' "
        b"id='sticky-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/wp-embed.min.js?ver=5.5.3' "
        b"id='wp-embed-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/custom_scroll.js?ver=1.1' "
        b"id='custom_scroll-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/js/frontend-modules.min.js?ver=3.0.13"
        b"' id='elementor-frontend-modules-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/jquery/ui/position.min.js?ver=1.11.4' "
        b"id='jquery-ui-position-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib/dialog/dialog.min.js?ver=4.8.1' "
        b"id='elementor-dialog-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib/waypoints/waypoints.min.js?ver=4.0"
        b".2' id='elementor-waypoints-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib/swiper/swiper.min.js?ver=5.3.6' "
        b"id='swiper-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/lib/share-link/share-link.min.js?ver=3"
        b".0.13' id='share-link-js'></script>\n<script type='text/javascript' "
        b'id=\'elementor-frontend-js-before\'>\nvar elementorFrontendConfig = {"environmentMode":{"edit":false,'
        b'"wpPreview":false},"i18n":{"shareOnFacebook":"Share on Facebook","shareOnTwitter":"Share on Twitter",'
        b'"pinIt":"Pin it","download":"Download","downloadImage":"Download image","fullscreen":"Fullscreen",'
        b'"zoom":"Zoom","share":"Share","playVideo":"Play Video","previous":"Previous","next":"Next","close":"Close"},'
        b'"is_rtl":false,"breakpoints":{"xs":0,"sm":480,"md":768,"lg":1025,"xl":1440,"xxl":1600},"version":"3.0.13",'
        b'"is_static":false,"legacyMode":{"elementWrappers":true},"urls":{'
        b'"assets":"https:\\/\\/www.tutorialbar.com\\/wp-content\\/plugins\\/elementor\\/assets\\/"},"settings":{'
        b'"page":[],"editorPreferences":[]},"kit":{"global_image_lightbox":"yes","lightbox_enable_counter":"yes",'
        b'"lightbox_enable_fullscreen":"yes","lightbox_enable_zoom":"yes","lightbox_enable_share":"yes",'
        b'"lightbox_title_src":"title","lightbox_description_src":"description"},"post":{"id":19,'
        b'"title":"All%20Courses%20-%20Tutorial%20Bar","excerpt":"","featuredImage":false}};\n</script>\n<script '
        b"type='text/javascript' src='https://www.tutorialbar.com/wp-content/plugins/elementor/assets/js/frontend"
        b".min.js?ver=3.0.13' id='elementor-frontend-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/underscore.min.js?ver=1.8.3' "
        b"id='underscore-js'></script>\n<script type='text/javascript' id='wp-util-js-extra'>\n/* <![CDATA[ "
        b'*/\nvar _wpUtilSettings = {"ajax":{"url":"\\/wp-admin\\/admin-ajax.php"}};\n/* ]]> */\n</script>\n<script '
        b"type='text/javascript' src='https://www.tutorialbar.com/wp-includes/js/wp-util.min.js?ver=5.5.3' "
        b"id='wp-util-js'></script>\n<script type='text/javascript' id='wpforms-elementor-js-extra'>\n/* <!["
        b'CDATA[ */\nvar wpformsElementorVars = {"recaptcha_type":"v2"};\n/* ]]> */\n</script>\n<script '
        b"type='text/javascript' src='https://www.tutorialbar.com/wp-content/plugins/wpforms-lite/assets/js"
        b"/integrations/elementor/frontend.min.js?ver=1.6.3.1' id='wpforms-elementor-js'></script>\n\r\n\t\t<!-- "
        b'Cookie Notice plugin v1.3.2 by Digital Factory https://dfactory.eu/ -->\r\n\t\t<div id="cookie-notice" '
        b'role="banner" class="cookie-notice-hidden cookie-revoke-hidden cn-position-bottom" aria-label="Cookie '
        b'Notice" style="background-color: rgba(0,0,0,0.8);"><div class="cookie-notice-container" style="color: '
        b'#fff;"><span id="cn-notice-text" class="cn-text-container">Our website use cookies to ensure that we give '
        b"you the best experience on our website. If you continue to use this site we will assume that you are happy "
        b'with it.</span><span id="cn-notice-buttons" class="cn-buttons-container"><a href="#" id="cn-accept-cookie" '
        b'data-cookie-set="accept" class="cn-set-cookie cn-button button" aria-label="Accept">Accept</a></span><a '
        b'href="javascript:void(0);" id="cn-close-notice" data-cookie-set="accept" class="cn-close-icon" '
        b'aria-label="Accept"></a></div>\r\n\t\t\t\r\n\t\t</div>\r\n\t\t<!-- / Cookie Notice plugin '
        b"--></body>\r\n</html>"
    )


@pytest.fixture()
def tutorialbar_course_page():
    return (
        b'<!DOCTYPE html>\r\n<!--[if IE 8]>    <html class="ie8" lang="en-US"> <![endif]-->\r\n<!--[if IE 9]>   '
        b' <html class="ie9" lang="en-US"> <![endif]-->\r\n<!--[if (gt IE 9)|!(IE)] lang="en-US"><![endif]-->\r\n<html '
        b'lang="en-US">\r\n<head>\r\n<meta charset="UTF-8" />\r\n<meta name="viewport" content="width=device-width, '
        b'initial-scale=1.0" />\r\n<!-- feeds & pingback -->\r\n<link rel="profile" href="https://gmpg.org/xfn/11" '
        b'/>\r\n<link rel="pingback" href="https://www.tutorialbar.com/xmlrpc.php" />\r\n<!-- Optimized by SG '
        b"Optimizer plugin version - 5.7.6 -->\n\t<!-- This site is optimized with the Yoast SEO plugin v15.3 - "
        b"https://yoast.com/wordpress/plugins/seo/ -->\n\t<title>[100% OFF] Mindfulness Meditation For Pain Relief "
        b'&amp; Stress Management - Tutorial Bar</title>\n\t<meta name="description" content="Mindfulness Meditation '
        b"For Pain Relief &amp; Stress Management Learn How To Use Professional Guided Mindfulness Meditation Sessions "
        b'For Effective Pain" />\n\t<meta name="robots" content="index, follow, max-snippet:-1, '
        b'max-image-preview:large, max-video-preview:-1" />\n\t<link rel="canonical" '
        b'href="https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/" />\n\t<meta '
        b'property="og:locale" content="en_US" />\n\t<meta property="og:type" content="article" />\n\t<meta '
        b'property="og:title" content="[100% OFF] Mindfulness Meditation For Pain Relief &amp; Stress Management - '
        b'Tutorial Bar" />\n\t<meta property="og:description" content="Mindfulness Meditation For Pain Relief &amp; '
        b'Stress Management Learn How To Use Professional Guided Mindfulness Meditation Sessions For Effective Pain" '
        b'/>\n\t<meta property="og:url" content="https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief'
        b'-stress-management/" />\n\t<meta property="og:site_name" content="Tutorial Bar" />\n\t<meta '
        b'property="article:published_time" content="2020-11-21T14:01:51+00:00" />\n\t<meta '
        b'property="article:modified_time" content="2020-11-21T14:01:53+00:00" />\n\t<meta property="og:image" '
        b'content="https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6.jpeg" />\n\t<meta '
        b'property="og:image:width" content="480" />\n\t<meta property="og:image:height" content="270" />\n\t<meta '
        b'name="twitter:card" content="summary_large_image" />\n\t<meta name="twitter:label1" content="Written '
        b'by">\n\t<meta name="twitter:data1" content="Deepak Malik">\n\t<meta name="twitter:label2" content="Est. '
        b'reading time">\n\t<meta name="twitter:data2" content="1 minute">\n\t<script type="application/ld+json" '
        b'class="yoast-schema-graph">{"@context":"https://schema.org","@graph":[{"@type":"Organization",'
        b'"@id":"https://tutorialbar.com/#organization","name":"Tutorial Bar","url":"https://tutorialbar.com/",'
        b'"sameAs":[],"logo":{"@type":"ImageObject","@id":"https://tutorialbar.com/#logo","inLanguage":"en-US",'
        b'"url":"https://www.tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png","width":489,"height":113,'
        b'"caption":"Tutorial Bar"},"image":{"@id":"https://tutorialbar.com/#logo"}},{"@type":"WebSite",'
        b'"@id":"https://tutorialbar.com/#website","url":"https://tutorialbar.com/","name":"Tutorial Bar",'
        b'"description":"","publisher":{"@id":"https://tutorialbar.com/#organization"},"potentialAction":[{'
        b'"@type":"SearchAction","target":"https://tutorialbar.com/?s={search_term_string}","query-input":"required '
        b'name=search_term_string"}],"inLanguage":"en-US"},{"@type":"ImageObject",'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#primaryimage",'
        b'"inLanguage":"en-US","url":"https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6.jpeg","width":480,'
        b'"height":270},{"@type":"WebPage",'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#webpage",'
        b'"url":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/","name":"[100% '
        b'OFF] Mindfulness Meditation For Pain Relief & Stress Management - Tutorial Bar","isPartOf":{'
        b'"@id":"https://tutorialbar.com/#website"},"primaryImageOfPage":{'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#primaryimage"},'
        b'"datePublished":"2020-11-21T14:01:51+00:00","dateModified":"2020-11-21T14:01:53+00:00",'
        b'"description":"Mindfulness Meditation For Pain Relief &amp; Stress Management Learn How To Use Professional '
        b'Guided Mindfulness Meditation Sessions For Effective Pain","inLanguage":"en-US","potentialAction":[{'
        b'"@type":"ReadAction","target":["https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress'
        b'-management/"]}]},{"@type":"Article",'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#article",'
        b'"isPartOf":{"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management'
        b'/#webpage"},"author":{"@id":"https://tutorialbar.com/#/schema/person/29de85ef68ace3bd985db2db9d26e6c6"},'
        b'"headline":"Mindfulness Meditation For Pain Relief &#038; Stress Management",'
        b'"datePublished":"2020-11-21T14:01:51+00:00","dateModified":"2020-11-21T14:01:53+00:00","mainEntityOfPage":{'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#webpage"},'
        b'"publisher":{"@id":"https://tutorialbar.com/#organization"},"image":{'
        b'"@id":"https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/#primaryimage"},'
        b'"articleSection":"Personal Development,Stress Management","inLanguage":"en-US"},{"@type":"Person",'
        b'"@id":"https://tutorialbar.com/#/schema/person/29de85ef68ace3bd985db2db9d26e6c6","name":"Deepak Malik",'
        b'"image":{"@type":"ImageObject","@id":"https://tutorialbar.com/#personlogo","inLanguage":"en-US",'
        b'"url":"https://secure.gravatar.com/avatar/1a4d92285ae918be6c3fe6e62e33f414?s=96&d=mm&r=g","caption":"Deepak '
        b"Malik\"}}]}</script>\n\t<!-- / Yoast SEO plugin. -->\n\n\n<link rel='dns-prefetch' "
        b"href='//www.googletagmanager.com' />\n<link rel='dns-prefetch' href='//s.w.org' />\n<link "
        b'rel="alternate" type="application/rss+xml" title="Tutorial Bar &raquo; Feed" '
        b'href="https://www.tutorialbar.com/feed/" />\n\t\t<script '
        b'type="text/javascript">\n\t\t\twindow._wpemojiSettings = {'
        b'"baseUrl":"https:\\/\\/s.w.org\\/images\\/core\\/emoji\\/13.0.0\\/72x72\\/","ext":".png",'
        b'"svgUrl":"https:\\/\\/s.w.org\\/images\\/core\\/emoji\\/13.0.0\\/svg\\/","svgExt":".svg","source":{'
        b'"concatemoji":"https:\\/\\/www.tutorialbar.com\\/wp-includes\\/js\\/wp-emoji-release.min.js?ver=5.5.3"}};\n'
        b'\t\t\t!function(e,a,t){var r,n,o,i,p=a.createElement("canvas"),s=p.getContext&&p.getContext("2d");function '
        b"c(e,t){var a=String.fromCharCode;s.clearRect(0,0,p.width,p.height),s.fillText(a.apply(this,e),0,"
        b"0);var r=p.toDataURL();return s.clearRect(0,0,p.width,p.height),s.fillText(a.apply(this,t),0,0),"
        b'r===p.toDataURL()}function l(e){if(!s||!s.fillText)return!1;switch(s.textBaseline="top",s.font="600 32px '
        b'Arial",e){case"flag":return!c([127987,65039,8205,9895,65039],[127987,65039,8203,9895,65039])&&(!c([55356,'
        b"56826,55356,56819],[55356,56826,8203,55356,56819])&&!c([55356,57332,56128,56423,56128,56418,56128,56421,"
        b"56128,56430,56128,56423,56128,56447],[55356,57332,8203,56128,56423,8203,56128,56418,8203,56128,56421,8203,"
        b'56128,56430,8203,56128,56423,8203,56128,56447]));case"emoji":return!c([55357,56424,8205,55356,57212],[55357,'
        b'56424,8203,55356,57212])}return!1}function d(e){var t=a.createElement("script");t.src=e,'
        b't.defer=t.type="text/javascript",a.getElementsByTagName("head")[0].appendChild(t)}for(i=Array("flag",'
        b'"emoji"),t.supports={everything:!0,everythingExceptFlag:!0},o=0;o<i.length;o++)t.supports[i[o]]=l(i[o]),'
        b't.supports.everything=t.supports.everything&&t.supports[i[o]],"flag"!==i[o]&&('
        b"t.supports.everythingExceptFlag=t.supports.everythingExceptFlag&&t.supports[i["
        b"o]]);t.supports.everythingExceptFlag=t.supports.everythingExceptFlag&&!t.supports.flag,t.DOMReady=!1,"
        b"t.readyCallback=function(){t.DOMReady=!0},t.supports.everything||(n=function(){t.readyCallback()},"
        b'a.addEventListener?(a.addEventListener("DOMContentLoaded",n,!1),e.addEventListener("load",n,'
        b'!1)):(e.attachEvent("onload",n),a.attachEvent("onreadystatechange",function(){'
        b'"complete"===a.readyState&&t.readyCallback()})),(r=t.source||{}).concatemoji?d('
        b"r.concatemoji):r.wpemoji&&r.twemoji&&(d(r.twemoji),d(r.wpemoji)))}(window,document,"
        b'window._wpemojiSettings);\n\t\t</script>\n\t\t<style type="text/css">\nimg.wp-smiley,\nimg.emoji {'
        b"\n\tdisplay: inline !important;\n\tborder: none !important;\n\tbox-shadow: none !important;\n\theight: 1em "
        b"!important;\n\twidth: 1em !important;\n\tmargin: 0 .07em !important;\n\tvertical-align: -0.1em "
        b"!important;\n\tbackground: none !important;\n\tpadding: 0 !important;\n}\n</style>\n\t<link "
        b"rel='stylesheet' id='wp-block-library-css'  "
        b"href='https://www.tutorialbar.com/wp-includes/css/dist/block-library/style.min.css?ver=5.5.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='cookie-notice-front-css'  "
        b"href='https://www.tutorialbar.com/wp-content/plugins/cookie-notice/css/front.min.css?ver=5.5.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='parent-style-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/style.css?ver=5.5.3' type='text/css' "
        b"media='all' />\n<link rel='stylesheet' id='rhstyle-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-blankchild/style.css?ver=13.3' type='text/css' "
        b"media='all' />\n<link rel='stylesheet' id='responsive-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/css/responsive.css?ver=13.3' "
        b"type='text/css' media='all' />\n<link rel='stylesheet' id='rehubicons-css'  "
        b"href='https://www.tutorialbar.com/wp-content/themes/rehub-theme/iconstyle.css?ver=13.3' type='text/css' "
        b"media='all' />\n<script type='text/javascript' id='cookie-notice-front-js-extra'>\n/* <![CDATA[ "
        b'*/\nvar cnArgs = {"ajaxUrl":"https:\\/\\/www.tutorialbar.com\\/wp-admin\\/admin-ajax.php",'
        b'"nonce":"0dc1b2677e","hideEffect":"none","position":"bottom","onScroll":"1","onScrollOffset":"200",'
        b'"onClick":"0","cookieName":"cookie_notice_accepted","cookieTime":"2592000","cookieTimeRejected":"2592000",'
        b'"cookiePath":"\\/","cookieDomain":"","redirection":"0","cache":"0","refuse":"0","revokeCookies":"0",'
        b'"revokeCookiesOpt":"automatic","secure":"1","coronabarActive":"0"};\n/* ]]> */\n</script>\n<script '
        b"type='text/javascript' src='https://www.tutorialbar.com/wp-content/plugins/cookie-notice/js/front.min.js"
        b"?ver=1.3.2' id='cookie-notice-front-js'></script>\n<script type='text/javascript' "
        b"src='https://www.googletagmanager.com/gtag/js?id=UA-158052069-1' id='google_gtagjs-js' "
        b"async></script>\n<script type='text/javascript' id='google_gtagjs-js-after'>\nwindow.dataLayer = "
        b"window.dataLayer || [];function gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('set', "
        b"'developer_id.dZTNiMT', true);\ngtag('config', 'UA-158052069-1', {\"anonymize_ip\":true} "
        b");\n</script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/jquery/jquery.js?ver=1.12.4-wp' "
        b'id=\'jquery-core-js\'></script>\n<link rel="https://api.w.org/" href="https://www.tutorialbar.com/wp-json/" '
        b'/><link rel="alternate" type="application/json" href="https://www.tutorialbar.com/wp-json/wp/v2/posts/30817" '
        b'/><link rel="EditURI" type="application/rsd+xml" title="RSD" '
        b'href="https://www.tutorialbar.com/xmlrpc.php?rsd" />\n<link rel="wlwmanifest" '
        b'type="application/wlwmanifest+xml" href="https://www.tutorialbar.com/wp-includes/wlwmanifest.xml" /> \n<meta '
        b'name="generator" content="WordPress 5.5.3" />\n<link rel=\'shortlink\' '
        b'href=\'https://www.tutorialbar.com/?p=30817\' />\n<link rel="alternate" type="application/json+oembed" '
        b'href="https://www.tutorialbar.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.tutorialbar.com'
        b'%2Fmindfulness-meditation-for-pain-relief-stress-management%2F" />\n<link rel="alternate" '
        b'type="text/xml+oembed" href="https://www.tutorialbar.com/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww'
        b'.tutorialbar.com%2Fmindfulness-meditation-for-pain-relief-stress-management%2F&#038;format=xml" />\n<meta '
        b'name="generator" content="Site Kit by Google 1.20.0" />\n<script type=\'text/javascript\'>\nfunction '
        b'addLink() {\n    var selection = window.getSelection();\n    var htmlDiv = document.createElement("div");\n  '
        b"  for (var i = 0; i < selection.rangeCount; ++i) {\n        htmlDiv.appendChild(selection.getRangeAt("
        b'i).cloneContents());\n    }\n    var selectionHTML = htmlDiv.innerHTML;\n    var pagelink = "<br/><br/>View '
        b'more at TutorialBar: <a href=\'"+document.location.href+"\'>"+document.location.href+"</a>";\n    var '
        b"copytext = selectionHTML + pagelink;\n    \n    var newdiv = document.createElement('div');\n    "
        b"newdiv.style.position = 'absolute';\n    newdiv.style.left = '-99999px';\n    \n    "
        b"document.body.appendChild(newdiv);\n    newdiv.innerHTML = copytext;\n    selection.selectAllChildren("
        b"newdiv);\n    window.setTimeout(function () { document.body.removeChild(newdiv); }, 0);\n}\ndocument.oncopy "
        b'= addLink\n</script>\n\n<link rel="preload" '
        b'href="https://www.tutorialbar.com/wp-content/themes/rehub-theme/fonts/rhicons.woff2?leryx9" as="font" '
        b'type="font/woff2" crossorigin="crossorigin"><style type="text/css"> @media (min-width:1025px){header '
        b".logo-section{padding:5px 0;}}.logo_section_wrap{box-shadow:0 15px 30px 0 rgba(119,123,146,"
        b"0.1)}#main_header,.is-sticky .logo_section_wrap,.sticky-active.logo_section_wrap{background-color:#000000 "
        b"!important}.main-nav.white_style{border-top:none}nav.top_menu > ul:not(.off-canvas) > li > a:after{"
        b"top:auto;bottom:0}.header-top{border:none;}.footer-bottom{background-color:#000000 !important}.footer-bottom "
        b".footer_widget{border:none !important} .widget .title:after{border-bottom:2px solid "
        b"#ff4136;}.rehub-main-color-border,nav.top_menu > ul > li.vertical-menu.border-main-color .sub-menu,"
        b".rh-main-bg-hover:hover,.wp-block-quote,ul.def_btn_link_tabs li.active a,.wp-block-pullquote{"
        b"border-color:#ff4136;}.wpsm_promobox.rehub_promobox{border-left-color:#ff4136!important;}.color_link{"
        b"color:#ff4136 !important;}.search-header-contents{border-top-color:#ff4136;}.featured_slider:hover .score,"
        b".top_chart_controls .controls:hover,article.post .wpsm_toplist_heading:before{"
        b"border-color:#ff4136;}.btn_more:hover,.small_post .overlay .btn_more:hover,.tw-pagination .current{"
        b"border:1px solid #ff4136;color:#fff}.rehub_woo_review .rehub_woo_tabs_menu li.current{border-top:3px solid "
        b"#ff4136;}.gallery-pics .gp-overlay{box-shadow:0 0 0 4px #ff4136 inset;}.post .rehub_woo_tabs_menu "
        b"li.current,.woocommerce div.product .woocommerce-tabs ul.tabs li.active{border-top:2px solid "
        b"#ff4136;}.rething_item a.cat{border-bottom-color:#ff4136}nav.top_menu ul li ul.sub-menu{border-bottom:2px "
        b"solid #ff4136;}.widget.deal_daywoo,.elementor-widget-wpsm_woofeatured .deal_daywoo{border:3px solid "
        b"#ff4136;padding:20px;background:#fff;}.deal_daywoo .wpsm-bar-bar{background-color:#ff4136 !important} "
        b"#buddypress div.item-list-tabs ul li.selected a span,#buddypress div.item-list-tabs ul li.current a span,"
        b"#buddypress div.item-list-tabs ul li a span,.user-profile-div .user-menu-tab > li.active > a,"
        b".user-profile-div .user-menu-tab > li.active > a:focus,.user-profile-div .user-menu-tab > li.active > "
        b"a:hover,.slide .news_cat a,.news_in_thumb:hover .news_cat a,.news_out_thumb:hover .news_cat a,"
        b".col-feat-grid:hover .news_cat a,.carousel-style-deal .re_carousel .controls,.re_carousel .controls:hover,"
        b".openedprevnext .postNavigation a,.postNavigation a:hover,.top_chart_pagination a.selected,"
        b".flex-control-paging li a.flex-active,.flex-control-paging li a:hover,.btn_more:hover,.tabs-menu li:hover,"
        b".tabs-menu li.current,.featured_slider:hover .score,#bbp_user_edit_submit,.bbp-topic-pagination a,"
        b".bbp-topic-pagination a,.custom-checkbox label.checked:after,.slider_post .caption,ul.postpagination "
        b"li.active a,ul.postpagination li:hover a,ul.postpagination li a:focus,.top_theme h5 strong,.re_carousel "
        b".text:after,#topcontrol:hover,.main_slider .flex-overlay:hover a.read-more,.rehub_chimp #mc_embed_signup "
        b"input#mc-embedded-subscribe,#rank_1.rank_count,#toplistmenu > ul li:before,.rehub_chimp:before,.wpsm-members "
        b"> strong:first-child,.r_catbox_btn,.wpcf7 .wpcf7-submit,.comm_meta_wrap .rh_user_s2_label,.wpsm_pretty_hover "
        b"li:hover,.wpsm_pretty_hover li.current,.rehub-main-color-bg,.togglegreedybtn:after,.rh-bg-hover-color:hover "
        b".news_cat a,.rh-main-bg-hover:hover,.rh_wrapper_video_playlist .rh_video_currently_playing,"
        b".rh_wrapper_video_playlist .rh_video_currently_playing.rh_click_video:hover,.rtmedia-list-item "
        b".rtmedia-album-media-count,.tw-pagination .current,.dokan-dashboard .dokan-dash-sidebar "
        b"ul.dokan-dashboard-menu li.active,.dokan-dashboard .dokan-dash-sidebar ul.dokan-dashboard-menu li:hover,"
        b".dokan-dashboard .dokan-dash-sidebar ul.dokan-dashboard-menu li.dokan-common-links a:hover,"
        b"#ywqa-submit-question,.woocommerce .widget_price_filter .ui-slider .ui-slider-range,.rh-hov-bor-line > "
        b"a:after,nav.top_menu > ul:not(.off-canvas) > li > a:after,.rh-border-line:after,"
        b".wpsm-table.wpsm-table-main-color table tr th,.rehub_chimp_flat #mc_embed_signup "
        b"input#mc-embedded-subscribe{background:#ff4136;}@media (max-width:767px){.postNavigation a{"
        b"background:#ff4136;}}.rh-main-bg-hover:hover,.rh-main-bg-hover:hover .whitehovered{color:#fff !important} a,"
        b".carousel-style-deal .deal-item .priced_block .price_count ins,nav.top_menu ul li.menu-item-has-children ul "
        b"li.menu-item-has-children > a:before,.top_chart_controls .controls:hover,.flexslider .fa-pulse,"
        b".footer-bottom .widget .f_menu li a:hover,.comment_form h3 a,.bbp-body li.bbp-forum-info > a:hover,"
        b".bbp-body li.bbp-topic-title > a:hover,#subscription-toggle a:before,#favorite-toggle a:before,"
        b".aff_offer_links .aff_name a,.rh-deal-price,.commentlist .comment-content small a,.related_articles "
        b".title_cat_related a,article em.emph,.campare_table table.one td strong.red,.sidebar .tabs-item .detail p a,"
        b".footer-bottom .widget .title span,footer p a,.welcome-frase strong,article.post "
        b".wpsm_toplist_heading:before,.post a.color_link,.categoriesbox:hover h3 a:after,.bbp-body li.bbp-forum-info "
        b"> a,.bbp-body li.bbp-topic-title > a,.widget .title i,.woocommerce-MyAccount-navigation ul li.is-active a,"
        b".category-vendormenu li.current a,.deal_daywoo .title,.rehub-main-color,.wpsm_pretty_colored ul li.current "
        b"a,.wpsm_pretty_colored ul li.current,.rh-heading-hover-color:hover h2 a,.rh-heading-hover-color:hover h3 a,"
        b".rh-heading-hover-color:hover h4 a,.rh-heading-hover-color:hover h5 a,.rh-heading-hover-color:hover "
        b".rh-heading-hover-item a,.rh-heading-icon:before,.widget_layered_nav ul li.chosen a:before,"
        b".wp-block-quote.is-style-large p,ul.page-numbers li span.current,ul.page-numbers li a:hover,ul.page-numbers "
        b"li.active a,.page-link > span:not(.page-link-title),blockquote:not(.wp-block-quote) p,"
        b"span.re_filtersort_btn:hover,span.active.re_filtersort_btn,.deal_daywoo .price,div.sortingloading:after{"
        b"color:#ff4136;} .page-link > span:not(.page-link-title),.postimagetrend .title,.widget.widget_affegg_widget "
        b".title,.widget.top_offers .title,.widget.cegg_widget_products .title,header .header_first_style .search "
        b'form.search-form [type="submit"],header .header_eight_style .search form.search-form [type="submit"],'
        b".more_post a,.more_post span,.filter_home_pick span.active,.filter_home_pick span:hover,.filter_product_pick "
        b"span.active,.filter_product_pick span:hover,.rh_tab_links a.active,.rh_tab_links a:hover,.wcv-navigation "
        b'ul.menu li.active,.wcv-navigation ul.menu li:hover a,form.search-form [type="submit"],.rehub-sec-color-bg,'
        b"input#ywqa-submit-question,input#ywqa-send-answer,.woocommerce button.button.alt,.tabsajax "
        b"span.active.re_filtersort_btn,.wpsm-table.wpsm-table-sec-color table tr th,.rh-slider-arrow{"
        b"background:#111111 !important;color:#fff !important;outline:0}.widget.widget_affegg_widget .title:after,"
        b".widget.top_offers .title:after,.vc_tta-tabs.wpsm-tabs .vc_tta-tab.vc_active,.vc_tta-tabs.wpsm-tabs "
        b".vc_tta-panel.vc_active .vc_tta-panel-heading,.widget.cegg_widget_products .title:after{"
        b"border-top-color:#111111 !important;}.page-link > span:not(.page-link-title){border:1px solid "
        b"#111111;}.page-link > span:not(.page-link-title),.header_first_style .search form.search-form ["
        b'type="submit"] i{color:#fff !important;}.rh_tab_links a.active,.rh_tab_links a:hover,'
        b".rehub-sec-color-border,nav.top_menu > ul > li.vertical-menu.border-sec-color > .sub-menu,"
        b".rh-slider-thumbs-item--active{border-color:#111111}.rh_wrapper_video_playlist .rh_video_currently_playing,"
        b".rh_wrapper_video_playlist .rh_video_currently_playing.rh_click_video:hover{"
        b"background-color:#111111;box-shadow:1200px 0 0 #111111 inset;}.rehub-sec-color{color:#111111} "
        b'form.search-form input[type="text"]{border-radius:4px}.news .priced_block .price_count,.blog_string '
        b".priced_block .price_count,.main_slider .price_count{margin-right:5px}.right_aff .priced_block "
        b".btn_offer_block,.right_aff .priced_block .price_count{border-radius:0 "
        b'!important}form.search-form.product-search-form input[type="text"]{border-radius:4px 0 0 '
        b'4px;}form.search-form [type="submit"]{border-radius:0 4px 4px 0;}.rtl form.search-form.product-search-form '
        b'input[type="text"]{border-radius:0 4px 4px 0;}.rtl form.search-form [type="submit"]{border-radius:4px 0 0 '
        b"4px;}.price_count,.rehub_offer_coupon,#buddypress .dir-search input[type=text],.gmw-form-wrapper input["
        b"type=text],.gmw-form-wrapper select,#buddypress a.button,.btn_more,#main_header .wpsm-button,"
        b'#rh-header-cover-image .wpsm-button,#wcvendor_image_bg .wpsm-button,input[type="text"],textarea,'
        b'input[type="tel"],input[type="password"],input[type="email"],input[type="url"],input[type="number"],'
        b'.def_btn,input[type="submit"],input[type="button"],input[type="reset"],.rh_offer_list .offer_thumb '
        b".deal_img_wrap,.grid_onsale,.rehub-main-smooth,.re_filter_instore span.re_filtersort_btn:hover,"
        b".re_filter_instore span.active.re_filtersort_btn,#buddypress .standard-form input[type=text],#buddypress "
        b".standard-form textarea,.blacklabelprice{border-radius:4px}.news-community,.woocommerce .products.grid_woo "
        b".product,.rehub_chimp #mc_embed_signup input.email,#mc_embed_signup input#mc-embedded-subscribe,"
        b".rh_offer_list,.woo-tax-logo,#buddypress div.item-list-tabs ul li a,#buddypress form#whats-new-form,"
        b"#buddypress div#invite-list,#buddypress #send-reply div.message-box,.rehub-sec-smooth,.rate-bar-bar,"
        b".rate-bar,#wcfm-main-contentainer #wcfm-content,.wcfm_welcomebox_header{border-radius:5px} .woocommerce "
        b".woo-button-area .masked_coupon,.woocommerce a.woo_loop_btn,.woocommerce .button.checkout,.woocommerce "
        b"input.button.alt,.woocommerce a.add_to_cart_button:not(.flat-woo-btn),.woocommerce-page "
        b"a.add_to_cart_button:not(.flat-woo-btn),.woocommerce .single_add_to_cart_button,.woocommerce div.product "
        b"form.cart .button,.woocommerce .checkout-button.button,.woofiltersbig .prdctfltr_buttons "
        b"a.prdctfltr_woocommerce_filter_submit,.priced_block .btn_offer_block,.priced_block .button,"
        b'.rh-deal-compact-btn,input.mdf_button,#buddypress input[type="submit"],#buddypress input[type="button"],'
        b'#buddypress input[type="reset"],#buddypress button.submit,.wpsm-button.rehub_main_btn,.wcv-grid a.button,'
        b"input.gmw-submit,#ws-plugin--s2member-profile-submit,#rtmedia_create_new_album,"
        b'input[type="submit"].dokan-btn-theme,a.dokan-btn-theme,.dokan-btn-theme,#wcfm_membership_container '
        b"a.wcfm_submit_button,.woocommerce button.button,.rehub-main-btn-bg{background:none #ff4136 "
        b"!important;color:#ffffff !important;fill:#ffffff !important;border:none !important;text-decoration:none "
        b"!important;outline:0;box-shadow:-1px 6px 19px rgba(255,65,54,0.2) !important;border-radius:4px "
        b"!important;}.rehub-main-btn-bg > a{color:#ffffff !important;}.woocommerce a.woo_loop_btn:hover,.woocommerce "
        b".button.checkout:hover,.woocommerce input.button.alt:hover,.woocommerce a.add_to_cart_button:not("
        b".flat-woo-btn):hover,.woocommerce-page a.add_to_cart_button:not(.flat-woo-btn):hover,.woocommerce "
        b"a.single_add_to_cart_button:hover,.woocommerce-page a.single_add_to_cart_button:hover,.woocommerce "
        b"div.product form.cart .button:hover,.woocommerce-page div.product form.cart .button:hover,.woocommerce "
        b".checkout-button.button:hover,.woofiltersbig .prdctfltr_buttons a.prdctfltr_woocommerce_filter_submit:hover,"
        b".priced_block .btn_offer_block:hover,.wpsm-button.rehub_main_btn:hover,#buddypress input["
        b'type="submit"]:hover,#buddypress input[type="button"]:hover,#buddypress input[type="reset"]:hover,'
        b"#buddypress button.submit:hover,.small_post .btn:hover,.ap-pro-form-field-wrapper input["
        b'type="submit"]:hover,.wcv-grid a.button:hover,#ws-plugin--s2member-profile-submit:hover,.rething_button '
        b".btn_more:hover,#wcfm_membership_container a.wcfm_submit_button:hover,.woocommerce button.button:hover,"
        b".rehub-main-btn-bg:hover,.rehub-main-btn-bg:hover > a{background:none #ff4136 !important;color:#ffffff "
        b"!important;box-shadow:-1px 6px 13px rgba(255,65,54,"
        b"0.4) !important;border-color:transparent;}.rehub_offer_coupon:hover{border:1px dashed "
        b"#ff4136;}.rehub_offer_coupon:hover i.far,.rehub_offer_coupon:hover i.fal,.rehub_offer_coupon:hover i.fas{"
        b"color:#ff4136}.re_thing_btn .rehub_offer_coupon.not_masked_coupon:hover{color:#ff4136 "
        b"!important}.woocommerce a.woo_loop_btn:active,.woocommerce .button.checkout:active,.woocommerce "
        b".button.alt:active,.woocommerce a.add_to_cart_button:not(.flat-woo-btn):active,.woocommerce-page "
        b"a.add_to_cart_button:not(.flat-woo-btn):active,.woocommerce a.single_add_to_cart_button:active,"
        b".woocommerce-page a.single_add_to_cart_button:active,.woocommerce div.product form.cart .button:active,"
        b".woocommerce-page div.product form.cart .button:active,.woocommerce .checkout-button.button:active,"
        b".woofiltersbig .prdctfltr_buttons a.prdctfltr_woocommerce_filter_submit:active,"
        b'.wpsm-button.rehub_main_btn:active,#buddypress input[type="submit"]:active,#buddypress input['
        b'type="button"]:active,#buddypress input[type="reset"]:active,#buddypress button.submit:active,'
        b'.ap-pro-form-field-wrapper input[type="submit"]:active,.wcv-grid a.button:active,'
        b'#ws-plugin--s2member-profile-submit:active,input[type="submit"].dokan-btn-theme:active,'
        b"a.dokan-btn-theme:active,.dokan-btn-theme:active,.woocommerce button.button:active,"
        b".rehub-main-btn-bg:active{background:none #ff4136 !important;box-shadow:0 1px 0 #999 "
        b"!important;top:2px;color:#ffffff !important;}.rehub_btn_color{background-color:#ff4136;border:1px solid "
        b"#ff4136;color:#ffffff;text-shadow:none}.rehub_btn_color:hover{"
        b"color:#ffffff;background-color:#ff4136;border:1px solid #ff4136;}.rething_button .btn_more{border:1px solid "
        b"#ff4136;color:#ff4136;}.rething_button .priced_block.block_btnblock .price_count{"
        b"color:#ff4136;font-weight:normal;}.widget_merchant_list .buttons_col{background-color:#ff4136 "
        b"!important;}.widget_merchant_list .buttons_col a{color:#ffffff !important;}.rehub-svg-btn-fill svg{"
        b"fill:#ff4136;}.rehub-svg-btn-stroke svg{stroke:#ff4136;}@media (max-width:767px){#float-panel-woo-area{"
        b"border-top:1px solid #ff4136}}.rh_post_layout_big_offer .priced_block .btn_offer_block{"
        b"text-shadow:none}</style><style>footer#theme_footer.dark_style {background: #000000}</style><script async "
        b'src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script><script>(adsbygoogle = '
        b'window.adsbygoogle || []).push({"google_ad_client":"ca-pub-5221546730192444","enable_page_level_ads":true,'
        b'"tag_partner":"site_kit"});</script><link rel="icon" '
        b'href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-32x32.png" sizes="32x32" '
        b'/>\n<link rel="icon" href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-192x192'
        b'.png" sizes="192x192" />\n<link rel="apple-touch-icon" '
        b'href="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar-icon-180x180.png" />\n<meta '
        b'name="msapplication-TileImage" content="https://www.tutorialbar.com/wp-content/uploads/cropped-tutorial-bar'
        b'-icon-270x270.png" />\n\t\t<style type="text/css" id="wp-custom-css">\n\t\t\t.logo_image_mobile > img {'
        b'\n\twidth: 200px;\n}\t\t</style>\n\t\t</head>\r\n<body class="post-template-default single single-post '
        b'postid-30817 single-format-standard cookies-not-set elementor-default elementor-kit-10868">\r\n\t            '
        b'   \r\n<!-- Outer Start -->\r\n<div class="rh-outer-wrap">\r\n    <div id="top_ankor"></div>\r\n    <!-- '
        b'HEADER -->\r\n            <header id="main_header" class="dark_style">\r\n            <div '
        b'class="header_wrap">\r\n                                                <!-- Logo section -->\r\n<div '
        b'class="rh-stickme header_five_style logo_section_wrap header_one_row">\r\n    <div class="rh-container '
        b'tabletblockdisplay mb0 disabletabletpadding">\r\n        <div class="logo-section rh-flex-center-align '
        b'tabletblockdisplay disabletabletpadding mb0">\r\n            <div class="logo hideontablet">\r\n             '
        b'                       <a href="https://www.tutorialbar.com" class="logo_image"><img '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Tutorial Bar" height="" '
        b'width="200" /></a>\r\n                       \r\n            </div> \r\n            <!-- Main Navigation '
        b'-->\r\n            <div class="main-nav header_icons_menu mob-logo-enabled rh-flex-right-align  dark_style"> '
        b'     \r\n                <nav class="top_menu"><ul id="menu-header-menu" class="menu"><li id="menu-item-23" '
        b'class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home"><a '
        b'href="https://www.tutorialbar.com/">Home</a></li>\n<li id="menu-item-24" class="menu-item '
        b'menu-item-type-post_type menu-item-object-page"><a href="https://www.tutorialbar.com/all-courses/">All '
        b'Courses</a></li>\n<li id="menu-item-9702" class="menu-item menu-item-type-custom menu-item-object-custom"><a '
        b'href="https://www.tutorialbar.com/store/eduonix/">Eduonix Free Courses</a></li>\n<li id="menu-item-17258" '
        b'class="menu-item menu-item-type-custom menu-item-object-custom"><a '
        b'href="https://www.tutorialbar.com/store/edyoda/">EdYoda Free Courses</a></li>\n<li id="menu-item-1308" '
        b'class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children"><a '
        b'href="https://www.tutorialbar.com/course-categories/">Course Categories</a>\n<ul class="sub-menu">\n\t<li '
        b'id="menu-item-3330" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/development/">Development</a></li>\n\t<li id="menu-item-3331" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/it-software/">IT &amp; Software</a></li>\n\t<li '
        b'id="menu-item-3339" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/finance-accounting/">Finance &amp; Accounting</a></li>\n\t<li '
        b'id="menu-item-3338" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/design/">Design</a></li>\n\t<li id="menu-item-3332" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/business/">Business</a></li>\n\t<li id="menu-item-3333" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/marketing/">Marketing</a></li>\n\t<li id="menu-item-3341" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/health-fitness/">Health &amp; Fitness</a></li>\n\t<li '
        b'id="menu-item-3340" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/office-productivity/">Office Productivity</a></li>\n\t<li '
        b'id="menu-item-3337" class="menu-item menu-item-type-taxonomy menu-item-object-category"><a '
        b'href="https://www.tutorialbar.com/category/photography/">Photography</a></li>\n\t<li id="menu-item-3334" '
        b'class="menu-item menu-item-type-taxonomy menu-item-object-category current-post-ancestor current-menu-parent '
        b'current-post-parent"><a href="https://www.tutorialbar.com/category/personal-development/">Personal '
        b'Development</a></li>\n\t<li id="menu-item-3336" class="menu-item menu-item-type-taxonomy '
        b'menu-item-object-category"><a href="https://www.tutorialbar.com/category/teaching-academics/">Teaching &amp; '
        b'Academics</a></li>\n</ul>\n</li>\n<li id="menu-item-25" class="menu-item menu-item-type-post_type '
        b'menu-item-object-page"><a href="https://www.tutorialbar.com/contact/">Contact Us</a></li>\n</ul></nav>       '
        b'         <div class="responsive_nav_wrap rh_mobile_menu">\r\n                    <div id="dl-menu" '
        b'class="dl-menuwrapper rh-flex-center-align">\r\n                        <button id="dl-trigger" '
        b'class="dl-trigger" aria-label="Menu">\r\n                            <svg viewBox="0 0 32 32" '
        b'xmlns="http://www.w3.org/2000/svg">\r\n                                <g>\r\n                               '
        b'     <line stroke-linecap="round" id="rhlinemenu_1" y2="7" x2="29" y1="7" x1="3"/>\r\n                       '
        b'             <line stroke-linecap="round" id="rhlinemenu_2" y2="16" x2="18" y1="16" x1="3"/>\r\n             '
        b'                       <line stroke-linecap="round" id="rhlinemenu_3" y2="25" x2="26" y1="25" x1="3"/>\r\n   '
        b"                             </g>\r\n                            </svg>\r\n                        "
        b'</button>\r\n                        <div id="mobile-menu-icons" class="rh-flex-center-align '
        b'rh-flex-right-align">\r\n                            <div id="slide-menu-mobile"></div>\r\n                  '
        b"      </div>\r\n                    </div>\r\n                                    </div>\r\n                "
        b'<div class="search-header-contents"><form  role="search" method="get" class="search-form" '
        b'action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" placeholder="Search"  '
        b'data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  \t<button type="submit" '
        b'class="btnsearch"><i class="rhicon rhi-search"></i></button>\r\n</form>\r\n</div>\r\n            </div>  '
        b'\r\n             \r\n                    \r\n            <div class="header-actions-logo">\r\n               '
        b' <div class="rh-flex-center-align">\r\n                                                             \r\n     '
        b"                 \r\n                                                                               \r\n     "
        b"                                    \r\n                </div> \r\n            </div>                        "
        b"\r\n            <!-- /Main Navigation -->                                                        \r\n        "
        b"</div>\r\n    </div>\r\n</div>\r\n<!-- /Logo section -->  \r\n\r\n            </div>  \r\n        "
        b'</header>\r\n            \r\n\r\n    <!-- CONTENT -->\r\n<div class="rh-container">\r\n    <div '
        b'class="rh-content-wrap clearfix">\r\n        <!-- Main Side -->\r\n        <div class="main-side single '
        b'clearfix"> \r\n            <div class="rh-post-wrapper">           \r\n                                      '
        b'                  <article class="post-inner post post-30817 type-post status-publish format-standard '
        b'has-post-thumbnail hentry category-personal-development category-stress-management language-english" '
        b'id="post-30817">\r\n                        <!-- Title area -->\r\n                        <div '
        b'class="rh_post_layout_metabig">\r\n                            <div class="title_single_area">\r\n           '
        b'                     <div class="breadcrumb"><a href="https://www.tutorialbar.com/" >Home</a> &raquo; '
        b'<span><a  href="https://www.tutorialbar.com/category/personal-development/">Personal Development</a></span> '
        b'&raquo; <span class="current">Mindfulness Meditation For Pain Relief &#038; Stress '
        b"Management</span></div><!-- .breadcrumbs --> \r\n                                <div "
        b'class="rh-cat-list-title"><a class="rh-cat-label-title rh-cat-65" '
        b'href="https://www.tutorialbar.com/category/personal-development/" title="View all posts in Personal '
        b'Development">Personal Development</a><a class="rh-cat-label-title rh-cat-460" '
        b'href="https://www.tutorialbar.com/category/stress-management/" title="View all posts in Stress '
        b'Management">Stress Management</a></div>                        \r\n                                '
        b"<h1>Mindfulness Meditation For Pain Relief &#038; Stress Management</h1>                                     "
        b'                      \r\n                                <div class="meta post-meta-big">\r\n               '
        b'                     \t\t<div class="floatleft mr15 rtlml15">\n\t\t\t\t\t\t<span class="floatleft '
        b'authortimemeta">\n\t\t\t\t\t\t\t\t\t\t\t</span>\t\n\n\t\t</div>\n\t\t<div class="floatright ml15 '
        b'postviewcomm mt5">\n\t\t\t\t\n\t\t\t\t\t\t\n\t\t</div>\t\n\t \r\n                                </div>\r\n  '
        b'                              <div class="clearfix"></div> \r\n                                              '
        b'                      <div class="top_share">\r\n                                        \t<div '
        b'class="post_share">\r\n\t    <div class="social_icon  row_social_inpost"><div class="favour_in_row '
        b'favour_btn_red"></div><span data-href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww'
        b'.tutorialbar.com%2Fmindfulness-meditation-for-pain-relief-stress-management%2F" class="fb share-link-image" '
        b'data-service="facebook"><i class="rhicon rhi-facebook"></i></span><span '
        b'data-href="https://twitter.com/share?url=https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness-meditation-for-pain'
        b'-relief-stress-management%2F&text=Mindfulness+Meditation+For+Pain+Relief+%26+Stress+Management" class="tw '
        b'share-link-image" data-service="twitter"><i class="rhicon rhi-twitter"></i></span><span '
        b'data-href="https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness'
        b"-meditation-for-pain-relief-stress-management%2F&amp;media=https://www.tutorialbar.com/wp-content/uploads"
        b'/3607708_dda9_6.jpeg&amp;description=Mindfulness+Meditation+For+Pain+Relief+%26%23038%3B+Stress+Management" '
        b'class="pn share-link-image" data-service="pinterest"><i class="rhicon rhi-pinterest-p"></i></span><span '
        b'data-href="mailto:?subject=Mindfulness+Meditation+For+Pain+Relief+%26+Stress+Management&body=Check out: '
        b"https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness-meditation-for-pain-relief-stress-management%2F - "
        b'Tutorial+Bar" class="in share-link-image" data-service="email"><i class="rhicon '
        b'rhi-envelope"></i></span></div>\t</div>\r\n                                    </div>\r\n                    '
        b'                <div class="clearfix"></div> \r\n                                   \r\n                     '
        b"                                      \r\n                            </div>\r\n                        "
        b'</div>\r\n                        <div class="mediad mediad_top"><script async '
        b'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<!-- Enroll Button Ad '
        b'-->\r\n<ins class="adsbygoogle"\r\n     style="display:block"\r\n     '
        b'data-ad-client="ca-pub-5221546730192444"\r\n     data-ad-slot="1731357560"\r\n     data-ad-format="auto"\r\n '
        b'    data-full-width-responsive="true"></ins>\r\n<script>\r\n     (adsbygoogle = window.adsbygoogle || ['
        b']).push({});\r\n</script></div><div class="clearfix"></div>                         \r\n                     '
        b'   \t\t\t\t\t\t\t\t\t\t<figure class="top_featured_image"><img width="480" height="270" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6.jpeg" class="attachment-full size-full '
        b'wp-post-image" alt="" loading="lazy" srcset="https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6'
        b".jpeg 480w, https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-300x169.jpeg 300w, "
        b"https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-1024x576.jpeg 1024w, "
        b"https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-768x432.jpeg 768w, "
        b"https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-1536x864.jpeg 1536w, "
        b"https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-2048x1152.jpeg 2048w, "
        b'https://www.tutorialbar.com/wp-content/uploads/3607708_dda9_6-788x443.jpeg 788w" sizes="(max-width: 480px) '
        b'100vw, 480px" /></figure>   \r\n\t\t\t\t\t\t                        \r\n                                \r\n '
        b"                       \r\n                        <p>Mindfulness Meditation For Pain Relief &amp; Stress "
        b'Management</p>\n<div class="udlite-text-md clp-lead__headline" data-purpose="lead-headline">\nLearn How To '
        b"Use Professional Guided Mindfulness Meditation Sessions For Effective Pain Relief &amp; Stress "
        b'Management</div>\n<h2 class="udlite-heading-xl what-you-will-learn--title--hropy">What you&#8217;ll '
        b'learn</h2>\n<ul class="unstyled-list udlite-block-list '
        b'what-you-will-learn--objectives-list--2cWZN">\n<li>\n<div data-purpose="objective" '
        b'class="udlite-block-list-item udlite-block-list-item-small udlite-block-list-item-tight '
        b'udlite-block-list-item-neutral udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to relief your pain without '
        b'medication!</span></div>\n</div>\n</li>\n<li>\n<div data-purpose="objective" class="udlite-block-list-item '
        b"udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral "
        b'udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to manage your stress on the long '
        b'term!</span></div>\n</div>\n</li>\n<li>\n<div data-purpose="objective" class="udlite-block-list-item '
        b"udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral "
        b'udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to use guided meditations to balance '
        b'yourself!</span></div>\n</div>\n</li>\n<li>\n<div data-purpose="objective" class="udlite-block-list-item '
        b"udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral "
        b'udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to use mindfulness to relax and calm '
        b'down!</span></div>\n</div>\n</li>\n<li>\n<div data-purpose="objective" class="udlite-block-list-item '
        b"udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral "
        b'udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to use additional meditations for optimal '
        b'health!</span></div>\n</div>\n</li>\n<li>\n<div data-purpose="objective" class="udlite-block-list-item '
        b"udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral "
        b'udlite-text-sm">\n<div class="udlite-block-list-item-content"><span '
        b'class="what-you-will-learn--objective-item--ECarc">&#8230; How to apply practical tips for an optimal '
        b"meditation experience!</span></div>\n</div>\n</li>\n</ul>\n<div "
        b'class="ud-component--course-landing-page-udlite--requirements" data-component-props="{'
        b'&quot;isCollapsible&quot;:false,&quot;prerequisites&quot;:[&quot;no prerequisites&quot;]}">\n<div '
        b'data-unique-id="350" style="display:none"></div>\n<div>\n<h2 class="udlite-heading-xl '
        b'requirements--title--2j7S2">Requirements</h2>\n<ul class="unstyled-list udlite-block-list">\n<li>\n<div '
        b'class="udlite-block-list-item udlite-block-list-item-small udlite-block-list-item-tight '
        b'udlite-block-list-item-neutral udlite-text-sm">\n<div class="udlite-block-list-item-content">no '
        b'prerequisites</div>\n</div>\n</li>\n</ul>\n</div>\n</div>\n<div class="styles--audience--2pZ0S" '
        b'data-purpose="target-audience">\n<h2 class="udlite-heading-xl styles--audience__title--1Sob_">Who this '
        b'course is for:</h2>\n<ul class="styles--audience__list--3NCqY">\n<li>&#8230; People that want to know how to '
        b"relief your pain without medication!</li>\n<li>&#8230; People that want to know how to manage your stress on "
        b"the long term!</li>\n<li>&#8230; People that want to know how to use guided meditations to balance "
        b"yourself!</li>\n<li>&#8230; People that want to know how to use mindfulness to relax and calm "
        b"down!</li>\n<li>&#8230; People that want to know how to use additional meditations for optimal "
        b"health!</li>\n<li>&#8230; People that want to know how to apply practical tips for an optimal meditation "
        b"experience!</li>\n</ul>\n</div>\n\r\n                    </article>\r\n                    <div "
        b'class="clearfix"></div>\r\n                    <div class="single_custom_bottom"><script async '
        b'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<!-- Enroll Button Ad '
        b'-->\r\n<ins class="adsbygoogle"\r\n     style="display:block"\r\n     '
        b'data-ad-client="ca-pub-5221546730192444"\r\n     data-ad-slot="1731357560"\r\n     data-ad-format="auto"\r\n '
        b'    data-full-width-responsive="true"></ins>\r\n<script>\r\n     (adsbygoogle = window.adsbygoogle || ['
        b']).push({});\r\n</script>\r\n<div class="text-center"><div '
        b'class="inlinestyle">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t\t        <div '
        b'class="priced_block clearfix  ">\n\t              \t        \t\n\t            \t    \t\t\t    \t\t\t<span '
        b'class="rh_button_wrapper">\n\t\t            \t<a '
        b'href="https://www.udemy.com/course/mindfulness-meditation-for-pain-relief-stress-management/?couponCode'
        b'=BA2B8F43AF87E121C75D" class="btn_offer_block re_track_btn" target="_blank" rel="nofollow '
        b'sponsored">\n\t\t\t            \t\t\t            \tEnroll Now\t\t\t            \t\t\t            \t\t        '
        b"    </a>\n\t\t        \t</span>\n\t            \t\n\t\t    \t\t\t\t\t\t\t\t    \t\t\n\t\t        \t          "
        b"  \t        \n\t        </div>\n            \t    \t\t    \t\n\t</div></div>\r\n<script async "
        b'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<ins '
        b'class="adsbygoogle"\r\n     style="display:block"\r\n     data-ad-format="autorelaxed"\r\n     '
        b'data-ad-client="ca-pub-5221546730192444"\r\n     data-ad-slot="2325423669"></ins>\r\n<script>\r\n     ('
        b'adsbygoogle = window.adsbygoogle || []).push({});\r\n</script></div><div class="clearfix"></div>\r\n    '
        b'\t<div class="post_share">\r\n\t    <div class="social_icon  row_social_inpost"><div class="favour_in_row '
        b'favour_btn_red"></div><span data-href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww'
        b'.tutorialbar.com%2Fmindfulness-meditation-for-pain-relief-stress-management%2F" class="fb share-link-image" '
        b'data-service="facebook"><i class="rhicon rhi-facebook"></i></span><span '
        b'data-href="https://twitter.com/share?url=https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness-meditation-for-pain'
        b'-relief-stress-management%2F&text=Mindfulness+Meditation+For+Pain+Relief+%26+Stress+Management" class="tw '
        b'share-link-image" data-service="twitter"><i class="rhicon rhi-twitter"></i></span><span '
        b'data-href="https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness'
        b"-meditation-for-pain-relief-stress-management%2F&amp;media=https://www.tutorialbar.com/wp-content/uploads"
        b'/3607708_dda9_6.jpeg&amp;description=Mindfulness+Meditation+For+Pain+Relief+%26%23038%3B+Stress+Management" '
        b'class="pn share-link-image" data-service="pinterest"><i class="rhicon rhi-pinterest-p"></i></span><span '
        b'data-href="mailto:?subject=Mindfulness+Meditation+For+Pain+Relief+%26+Stress+Management&body=Check out: '
        b"https%3A%2F%2Fwww.tutorialbar.com%2Fmindfulness-meditation-for-pain-relief-stress-management%2F - "
        b'Tutorial+Bar" class="in share-link-image" data-service="email"><i class="rhicon '
        b'rhi-envelope"></i></span></div>\t</div>\r\n  \r\n\r\n    <!-- PAGER SECTION -->\r\n<div '
        b'class="float-posts-nav" id="float-posts-nav">\r\n    <div class="postNavigation prevPostBox">\r\n            '
        b'        <a href="https://www.tutorialbar.com/become-a-crm-manager-overview-for-email-marketing-starters/">\r'
        b'\n                <div class="inner-prevnext">\r\n                <div class="thumbnail">\r\n                '
        b'                        \r\n                    <img class="nolazyftheme" '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3535492_fead-1'
        b'-oyqtmyce5byjjr663l128mou2ynj489u8wbx5zxum4.jpeg" width="70" height="70" alt="Mindfulness Meditation For '
        b'Pain Relief &#038; Stress Management" />                </div>\r\n                <div '
        b'class="headline"><span>Previous</span><h4>Become a CRM Manager: overview for Email Marketing '
        b"starters!</h4></div>\r\n                </div>\r\n            </a>                          \r\n            "
        b'</div>\r\n    <div class="postNavigation nextPostBox">\r\n            </div>                        '
        b'\r\n</div>\r\n<!-- /PAGER SECTION -->\r\n                    \r\n                 \r\n\r\n\t<div class="tags '
        b'mb25">\r\n\t\t\t\t\t        <p></p>\r\n\t    \t</div>\r\n\r\n               \r\n\r\n    \t\t<div '
        b'class="related_articles pt25 border-top mb0 clearfix">\r\n\t\t<div class="related_title rehub-main-font '
        b'font120 fontbold mb35">\r\n\t\t\t\t\t\t\tRelated Courses\t\t\t\t\t</div>\r\n\t\t<div '
        b'class="columned_grid_module rh-flex-eq-height col_wrap_fourth mb0" >\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  '
        b'\r\n<article class="col_item column_grid rh-heading-hover-color rh-bg-hover-color no-padding"> \r\n    <div '
        b'class="button_action abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                        '
        b"              \r\n        </div>                                                           \r\n    </div> "
        b'\r\n        \r\n    <figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/16-days-16-hours-16-screenplays/" class="">\r\n                            '
        b'<img src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3625338_bd51_7'
        b'-1xciig6og9y0rk556plpx4kz74ks61l32hpkyq4grzc4.jpeg" width="350" height="200" alt="16 days; 16 hours; 16 '
        b'screenplays!" />                    </a>\r\n    </figure>\r\n        <div class="content_constructor">\r\n   '
        b'     <h3 class="mb15 mt0 font110 mobfont100 fontnormal lineheight20"><a '
        b'href="https://www.tutorialbar.com/16-days-16-hours-16-screenplays/">16 days; 16 hours; 16 '
        b"screenplays!</a></h3>\r\n                                 \r\n         \r\n                            <div "
        b'class="rh-flex-center-align mb10">\r\n                                                <div >\r\n             '
        b"       \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    \t\n\t            \r\n                "
        b"</div>\r\n                               \r\n            </div>\r\n         \r\n            </div>           "
        b'                        \r\n</article>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  \r\n<article class="col_item '
        b'column_grid rh-heading-hover-color rh-bg-hover-color no-padding"> \r\n    <div class="button_action '
        b'abdposright pr5 pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n   '
        b"     </div>                                                           \r\n    </div> \r\n        \r\n    "
        b'<figure class="mb20 position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/guided-mindfulness-meditation-stress-management-mastery/" class="">\r\n    '
        b'                        <img src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3610338_1c70_6'
        b'-1xciigeifuwbhkw5t3v3t7d01esdk5qa5yscoe3h5vhg.jpeg" width="350" height="200" alt="Guided Mindfulness '
        b'Meditation | Stress Management Mastery" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal lineheight20"><a '
        b'href="https://www.tutorialbar.com/guided-mindfulness-meditation-stress-management-mastery/">Guided '
        b"Mindfulness Meditation | Stress Management Mastery</a></h3>\r\n                                 \r\n         "
        b'\r\n                            <div class="rh-flex-center-align mb10">\r\n                                  '
        b"              <div >\r\n                    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    "
        b"\t\n\t            \r\n                </div>\r\n                               \r\n            </div>\r\n    "
        b"     \r\n            </div>                                   "
        b'\r\n</article>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding"> \r\n    <div class="button_action abdposright pr5 '
        b'pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n        </div>     '
        b'                                                      \r\n    </div> \r\n        \r\n    <figure class="mb20 '
        b'position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/2021-exceptional-creative-writing-30-days-complete-course/" class="">\r\n  '
        b'                          <img src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/2919484_4589_7'
        b'-8-1xciil1m6xw08owj2w3c5imtzgmdxa55k33fvxide9b8.jpeg" width="350" height="200" alt="[2021] EXCEPTIONAL '
        b'Creative Writing: 30 Days COMPLETE Course" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal lineheight20"><a '
        b'href="https://www.tutorialbar.com/2021-exceptional-creative-writing-30-days-complete-course/">[2021] '
        b"EXCEPTIONAL Creative Writing: 30 Days COMPLETE Course</a></h3>\r\n                                 \r\n      "
        b'   \r\n                            <div class="rh-flex-center-align mb10">\r\n                               '
        b"                 <div >\r\n                    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t   "
        b" \t\n\t            \r\n                </div>\r\n                               \r\n            </div>\r\n   "
        b"      \r\n            </div>                                   "
        b'\r\n</article>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  \r\n<article class="col_item column_grid '
        b'rh-heading-hover-color rh-bg-hover-color no-padding"> \r\n    <div class="button_action abdposright pr5 '
        b'pt5">\r\n        <div class="floatleft mr5">\r\n                                      \r\n        </div>     '
        b'                                                      \r\n    </div> \r\n        \r\n    <figure class="mb20 '
        b'position-relative text-center">             \r\n        <a '
        b'href="https://www.tutorialbar.com/become-the-best-version-of-yourself-with-less-worry-in-2020/" '
        b'class="">\r\n                            <img '
        b'src="https://www.tutorialbar.com/wp-content/uploads/thumbs_dir/3627110_56da_2'
        b'-1xcg1guhdx1k3zbq7ejxi7nmlbk2qiv9vtblsqoz6jl0.jpeg" width="350" height="200" alt="Become The Best Version Of '
        b'Yourself With Less Worry In 2020" />                    </a>\r\n    </figure>\r\n        <div '
        b'class="content_constructor">\r\n        <h3 class="mb15 mt0 font110 mobfont100 fontnormal lineheight20"><a '
        b'href="https://www.tutorialbar.com/become-the-best-version-of-yourself-with-less-worry-in-2020/">Become The '
        b"Best Version Of Yourself With Less Worry In 2020</a></h3>\r\n                                 \r\n         "
        b'\r\n                            <div class="rh-flex-center-align mb10">\r\n                                  '
        b"              <div >\r\n                    \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\n\t\t \n\t\t\t\t    "
        b"\t\n\t            \r\n                </div>\r\n                               \r\n            </div>\r\n    "
        b"     \r\n            </div>                                   \r\n</article>\t\t</div></div>                 "
        b"     \r\n                                            </div>\r\n        </div>  \r\n        <!-- /Main Side "
        b'-->  \r\n        <!-- Sidebar -->\r\n        <aside class="sidebar">            \r\n    <!-- SIDEBAR WIDGET '
        b'AREA -->\r\n \t\t\t<div id="search-2" class="widget widget_search"><form  role="search" method="get" '
        b'class="search-form" action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" '
        b'placeholder="Search"  data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  '
        b'\t<button type="submit" class="btnsearch"><i class="rhicon '
        b'rhi-search"></i></button>\r\n</form>\r\n</div><div id="custom_html-2" class="widget_text widget '
        b'widget_custom_html"><div class="textwidget custom-html-widget"><script '
        b'type="text/javascript">amzn_assoc_ad_type ="responsive_search_widget"; amzn_assoc_tracking_id '
        b'="deepakmalik-21"; amzn_assoc_marketplace ="amazon"; amzn_assoc_region ="IN"; amzn_assoc_placement =""; '
        b'amzn_assoc_search_type = "search_widget";amzn_assoc_width ="auto"; amzn_assoc_height ="auto"; '
        b'amzn_assoc_default_search_category =""; amzn_assoc_default_search_key ="smartphones";amzn_assoc_theme '
        b'="light"; amzn_assoc_bg_color ="FFFFFF"; </script><script '
        b'src="//z-in.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&Operation=GetScript&ID=OneJS&WS=1'
        b'&Marketplace=IN"></script></div></div><div id="rehub_sticky_on_scroll-2" class="widget '
        b'stickyscroll_widget"><div class="title">Ad</div>\t\t<script async '
        b'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\r\n<!-- Sidebar Ad '
        b'-->\r\n<ins class="adsbygoogle"\r\n     style="display:block"\r\n     '
        b'data-ad-client="ca-pub-5221546730192444"\r\n     data-ad-slot="3414440443"\r\n     data-ad-format="auto"\r\n '
        b'    data-full-width-responsive="true"></ins>\r\n<script>\r\n     (adsbygoogle = window.adsbygoogle || ['
        b"]).push({});\r\n</script>\r\n\t\t\t\r\n\t\t</div>\t        \r\n</aside>        <!-- /Sidebar -->\r\n    "
        b"</div>\r\n</div>\r\n<!-- /CONTENT -->     \r\n<!-- FOOTER -->\r\n\t\t\t\t\r\n\t \t\t\t\t<div "
        b'class="footer-bottom dark_style">\r\n\t\t\t<div class="rh-container clearfix">\r\n\t\t\t\t\t\t\t\t\t<div '
        b'class="rh-flex-eq-height col_wrap_three">\r\n\t\t\t\t\t\t<div class="footer_widget '
        b'col_item">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="text-2" class="widget widget_text"><div '
        b'class="title">About Tutorial Bar</div>\t\t\t<div class="textwidget"><p>Tutorial Bar is a free platform for '
        b"online courses and tutorials. All the courses listed here are <strong>free for limited time</strong>. After "
        b"enrolling a course and complete it you get a <strong>certificate of "
        b"completion</strong>.</p>\n</div>\n\t\t</div>\t\t\t\t\t\t\t \r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t<div "
        b'class="footer_widget col_item">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="rehub_better_menu-2" class="widget '
        b'better_menu"><div class="simple_menu_widget"><div class="title"><i class="rhicon '
        b'rhi-info-circle"></i>Important Links</div>\r\n\t    \t    \t<ul id="menu-footer-menu" class="menu"><li '
        b'id="menu-item-63" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-privacy-policy '
        b'menu-item-63"><a href="https://www.tutorialbar.com/privacy-policy/">Privacy Policy</a></li>\n<li '
        b'id="menu-item-28" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-28"><a '
        b'href="https://www.tutorialbar.com/disclaimer/">Disclaimer</a></li>\n<li id="menu-item-27" class="menu-item '
        b'menu-item-type-post_type menu-item-object-page menu-item-27"><a '
        b'href="https://www.tutorialbar.com/contact/">Contact Us</a></li>\n<li id="menu-item-215" class="menu-item '
        b'menu-item-type-custom menu-item-object-custom menu-item-215"><a '
        b'href="https://tutorialbar.com/sitemap_index.xml">Sitemap</a></li>\n</ul>\t    '
        b"\t\r\n\r\n\t\t\t\r\n\t</div></div>\t\t\t\t\t\t\t \r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t<div "
        b'class="footer_widget col_item last">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div id="search-3" class="widget last '
        b'widget_search"><div class="title">Search Courses</div><form  role="search" method="get" class="search-form" '
        b'action="https://www.tutorialbar.com/">\r\n  \t<input type="text" name="s" placeholder="Search"  '
        b'data-posttype="post">\r\n  \t<input type="hidden" name="post_type" value="post" />  \t<button type="submit" '
        b'class="btnsearch"><i class="rhicon rhi-search"></i></button>\r\n</form>\r\n</div><div '
        b'id="rehub_social_link-2" class="widget last social_link"><div class="title">Follow Us:</div>\t\r\n\t\t\t<div '
        b'class="social_icon big_i">\r\n\t\t\r\n\r\n\t\t\t\t\t<a '
        b'href="https://www.facebook.com/groups/271891420195341/" class="fb" rel="nofollow" target="_blank"><i '
        b'class="rhicon rhi-facebook"></i></a>\r\n\t\t\t\r\n\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\r\n\t\t\r\n\t\t\t\t'
        b"\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\t\t\t\t\t<a "
        b'href="https://t.me/tutorialbar_udemy_coupons" class="telegram" rel="nofollow" target="_blank"><i '
        b'class="rhicon rhi-telegram"></i></a>\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t'
        b"</div>\r\n\r\n\t\r\n\t</div>\t\t\t\t\t\t\t "
        b"\r\n\t\t\t\t\t\t</div>\r\n\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t</div>\t\r\n\t\t</div>\r\n\t\t\t\t"
        b'<footer id=\'theme_footer\' class="dark_style">\r\n\t\t\t<div class="rh-container clearfix">\r\n\t\t\t\t<div '
        b'class="footer_most_bottom">\r\n\t\t\t\t\t<div class="f_text">\r\n\t\t\t\t\t\t<span '
        b'class="f_text_span">\xc2\xa9 2020 TutorialBar.Com. All rights '
        b"reserved.</span>\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t</div>\t\t\r\n\t\t\t\t</div>\r\n\t\t\t</div>\r\n\t\t</footer"
        b'>\r\n\t\t\t\t<!-- FOOTER -->\r\n</div><!-- Outer End -->\r\n<span class="rehub_scroll" id="topcontrol" '
        b'data-scrollto="#top_ankor"><i class="rhicon rhi-chevron-up"></i></span>\r\n    <div '
        b'id="logo_mobile_wrapper"><a href="https://www.tutorialbar.com" class="logo_image_mobile"><img '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Tutorial Bar" width="35" '
        b'height="35" /></a></div>   \n\n     \n\n    <div id="rhmobpnlcustom" class="rhhidden"><div id="rhmobtoppnl" '
        b'style="background-color: #000000;" class="pr15 pl15 pb15 pt15"><div class="text-center"><a '
        b'href="https://www.tutorialbar.com"><img id="mobpanelimg" '
        b'src="https://tutorialbar.com/wp-content/uploads/Tutorial-Bar-logo.png" alt="Logo" width="150" height="45" '
        b"/></a></div></div></div>    \n              \n\n\t<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/inview.js?ver=1.0' "
        b"id='rhinview-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/pgwmodal.js?ver=2.0' "
        b"id='rhpgwmodal-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/unveil.js?ver=5.2.1' "
        b"id='rhunveil-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/hoverintent.js?ver=1.9' "
        b"id='rhhoverintent-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/countdown.js?ver=1.1' "
        b"id='rhcountdown-js'></script>\n<script type='text/javascript' id='rehub-js-extra'>\n/* <![CDATA[ "
        b'*/\nvar translation = {"back":"back","ajax_url":"\\/wp-admin\\/admin-ajax.php","fin":"That\'s all",'
        b'"noresults":"No results found","your_rating":"Your Rating:","nonce":"8517b9eea9","hotnonce":"de646ef9b3",'
        b'"wishnonce":"f6681cbd34","searchnonce":"a50570e5a0","filternonce":"48a2c16c83",'
        b'"rating_tabs_id":"94d813d08b","max_temp":"10","min_temp":"-10","helpnotnonce":"895b9b32a4"};\n/* ]]> '
        b"*/\n</script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/custom.js?ver=13.3' "
        b"id='rehub-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/jquery.sticky.js?ver=1.0.5' "
        b"id='sticky-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-includes/js/wp-embed.min.js?ver=5.5.3' "
        b"id='wp-embed-js'></script>\n<script type='text/javascript' "
        b"src='https://www.tutorialbar.com/wp-content/themes/rehub-theme/js/custom_scroll.js?ver=1.1' "
        b"id='custom_scroll-js'></script>\n\r\n\t\t<!-- Cookie Notice plugin v1.3.2 by Digital Factory "
        b'https://dfactory.eu/ -->\r\n\t\t<div id="cookie-notice" role="banner" class="cookie-notice-hidden '
        b'cookie-revoke-hidden cn-position-bottom" aria-label="Cookie Notice" style="background-color: rgba(0,0,0,'
        b'0.8);"><div class="cookie-notice-container" style="color: #fff;"><span id="cn-notice-text" '
        b'class="cn-text-container">Our website use cookies to ensure that we give you the best experience on our '
        b"website. If you continue to use this site we will assume that you are happy with it.</span><span "
        b'id="cn-notice-buttons" class="cn-buttons-container"><a href="#" id="cn-accept-cookie" '
        b'data-cookie-set="accept" class="cn-set-cookie cn-button button" aria-label="Accept">Accept</a></span><a '
        b'href="javascript:void(0);" id="cn-close-notice" data-cookie-set="accept" class="cn-close-icon" '
        b'aria-label="Accept"></a></div>\r\n\t\t\t\r\n\t\t</div>\r\n\t\t<!-- / Cookie Notice plugin --></body>\r\n</html>'
    )
