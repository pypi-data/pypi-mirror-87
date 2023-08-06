(function ($) {
    'use strict'

    var $sidebar = $('.control-sidebar')
    var $container = $('<div />', {
        class: 'p-3 control-sidebar-content'
    })

    $sidebar.append($container)

    var navbar_dark_skins = [
        'navbar-primary',
        'navbar-secondary',
        'navbar-info',
        'navbar-success',
        'navbar-danger',
        'navbar-indigo',
        'navbar-purple',
        'navbar-pink',
        'navbar-navy',
        'navbar-lightblue',
        'navbar-teal',
        'navbar-cyan',
        'navbar-dark',
        'navbar-gray-dark',
        'navbar-gray',
    ]

    var navbar_light_skins = [
        'navbar-light',
        'navbar-warning',
        'navbar-white',
        'navbar-orange',
    ]

    $container.append(
        '<h5>主题设置</h5><hr class="mb-2"/>'
    )

    var $no_border_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.main-header').hasClass('border-bottom-0'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.main-header').addClass('border-bottom-0')
        } else {
            $('.main-header').removeClass('border-bottom-0')
        }
    })
    var $no_border_container = $('<div />', {'class': 'mb-1'}).append($no_border_checkbox).append('<span>移除顶部导航栏边框</span>')
    // $container.append($no_border_container)

    var $text_sm_body_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('body').hasClass('text-sm'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('body').addClass('text-sm')
        } else {
            $('body').removeClass('text-sm')
        }
    })
    var $text_sm_body_container = $('<div />', {'class': 'mb-1'}).append($text_sm_body_checkbox).append('<span>正文使用小字体</span>')
    // $container.append($text_sm_body_container)

    var $text_sm_header_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.main-header').hasClass('text-sm'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.main-header').addClass('text-sm')
        } else {
            $('.main-header').removeClass('text-sm')
        }
    })
    var $text_sm_header_container = $('<div />', {'class': 'mb-1'}).append($text_sm_header_checkbox).append('<span>顶部导航使用小字体</span>')
    // $container.append($text_sm_header_container)

    var $text_sm_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.nav-sidebar').hasClass('text-sm'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.nav-sidebar').addClass('text-sm')
        } else {
            $('.nav-sidebar').removeClass('text-sm')
        }
    })
    var $text_sm_sidebar_container = $('<div />', {'class': 'mb-1'}).append($text_sm_sidebar_checkbox).append('<span>侧边栏使用小字体</span>')
    // $container.append($text_sm_sidebar_container)

    var $text_sm_footer_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.main-footer').hasClass('text-sm'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.main-footer').addClass('text-sm')
        } else {
            $('.main-footer').removeClass('text-sm')
        }
    })
    var $text_sm_footer_container = $('<div />', {'class': 'mb-1'}).append($text_sm_footer_checkbox).append('<span>页脚使用小字体</span>')
    // $container.append($text_sm_footer_container)

    var $flat_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.nav-sidebar').hasClass('nav-flat'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.nav-sidebar').addClass('nav-flat')
        } else {
            $('.nav-sidebar').removeClass('nav-flat')
        }
    })
    var $flat_sidebar_container = $('<div />', {'class': 'mb-1'}).append($flat_sidebar_checkbox).append('<span>侧边栏导航启用平面样式</span>')
    // $container.append($flat_sidebar_container)

    var $legacy_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.nav-sidebar').hasClass('nav-legacy'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.nav-sidebar').addClass('nav-legacy')
        } else {
            $('.nav-sidebar').removeClass('nav-legacy')
        }
    })
    var $legacy_sidebar_container = $('<div />', {'class': 'mb-1'}).append($legacy_sidebar_checkbox).append('<span>侧边栏导航启用旧样式</span>')
    // $container.append($legacy_sidebar_container)

    var $compact_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.nav-sidebar').hasClass('nav-compact'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.nav-sidebar').addClass('nav-compact')
        } else {
            $('.nav-sidebar').removeClass('nav-compact')
        }
    })
    var $compact_sidebar_container = $('<div />', {'class': 'mb-1'}).append($compact_sidebar_checkbox).append('<span>侧边栏导航启用紧凑样式</span>')
    // $container.append($compact_sidebar_container)

    var $child_indent_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.nav-sidebar').hasClass('nav-child-indent'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.nav-sidebar').addClass('nav-child-indent')
        } else {
            $('.nav-sidebar').removeClass('nav-child-indent')
        }
    })
    var $child_indent_sidebar_container = $('<div />', {'class': 'mb-1'}).append($child_indent_sidebar_checkbox).append('<span>侧边栏子导航缩进</span>')
    // $container.append($child_indent_sidebar_container)

    var $no_expand_sidebar_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.main-sidebar').hasClass('sidebar-no-expand'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.main-sidebar').addClass('sidebar-no-expand')
        } else {
            $('.main-sidebar').removeClass('sidebar-no-expand')
        }
    })
    var $no_expand_sidebar_container = $('<div />', {'class': 'mb-1'}).append($no_expand_sidebar_checkbox).append('<span>侧边栏禁用悬停自动展开</span>')
    // $container.append($no_expand_sidebar_container)

    var $text_sm_brand_checkbox = $('<input />', {
        type: 'checkbox',
        value: 1,
        checked: $('.brand-link').hasClass('text-sm'),
        'class': 'mr-1'
    }).on('click', function () {
        if ($(this).is(':checked')) {
            $('.brand-link').addClass('text-sm')
        } else {
            $('.brand-link').removeClass('text-sm')
        }
    })
    var $text_sm_brand_container = $('<div />', {'class': 'mb-4'}).append($text_sm_brand_checkbox).append('<span>LOGO使用小字体</span>')
    // $container.append($text_sm_brand_container)

    $container.append('<h6>顶部导航设置</h6>')

    var $navbar_variants = $('<div />', {
        'class': 'd-flex'
    })
    var navbar_all_colors = navbar_dark_skins.concat(navbar_light_skins)
    var $navbar_variants_colors = createSkinBlock(navbar_all_colors, function (e) {
        var color = $(this).data('color')
        var $main_header = $('.main-header')
        $main_header.removeClass('navbar-dark').removeClass('navbar-light')
        navbar_all_colors.map(function (color) {
            $main_header.removeClass(color)
        })

        if (navbar_dark_skins.indexOf(color) > -1) {
            $main_header.addClass('navbar-dark')
            localStorage.setItem('kelove_admin_lte_main_header_skin', 'navbar-dark')
        } else {
            $main_header.addClass('navbar-light')
            localStorage.setItem('kelove_admin_lte_main_header_skin', 'navbar-light')
        }

        $main_header.addClass(color)
        localStorage.setItem('kelove_admin_lte_main_header_skin_color', color)
    })

    $navbar_variants.append($navbar_variants_colors)

    $container.append($navbar_variants)

    var sidebar_colors = [
        'bg-primary',
        'bg-warning',
        'bg-info',
        'bg-danger',
        'bg-success',
        'bg-indigo',
        'bg-lightblue',
        'bg-navy',
        'bg-purple',
        'bg-fuchsia',
        'bg-pink',
        'bg-maroon',
        'bg-orange',
        'bg-lime',
        'bg-teal',
        'bg-olive'
    ]

    var accent_colors = [
        'accent-primary',
        'accent-warning',
        'accent-info',
        'accent-danger',
        'accent-success',
        'accent-indigo',
        'accent-lightblue',
        'accent-navy',
        'accent-purple',
        'accent-fuchsia',
        'accent-pink',
        'accent-maroon',
        'accent-orange',
        'accent-lime',
        'accent-teal',
        'accent-olive'
    ]

    var sidebar_skins = [
        'sidebar-dark-primary',
        'sidebar-dark-warning',
        'sidebar-dark-info',
        'sidebar-dark-danger',
        'sidebar-dark-success',
        'sidebar-dark-indigo',
        'sidebar-dark-lightblue',
        'sidebar-dark-navy',
        'sidebar-dark-purple',
        'sidebar-dark-fuchsia',
        'sidebar-dark-pink',
        'sidebar-dark-maroon',
        'sidebar-dark-orange',
        'sidebar-dark-lime',
        'sidebar-dark-teal',
        'sidebar-dark-olive',
        'sidebar-light-primary',
        'sidebar-light-warning',
        'sidebar-light-info',
        'sidebar-light-danger',
        'sidebar-light-success',
        'sidebar-light-indigo',
        'sidebar-light-lightblue',
        'sidebar-light-navy',
        'sidebar-light-purple',
        'sidebar-light-fuchsia',
        'sidebar-light-pink',
        'sidebar-light-maroon',
        'sidebar-light-orange',
        'sidebar-light-lime',
        'sidebar-light-teal',
        'sidebar-light-olive'
    ]

    $container.append('<h6>强调颜色设置</h6>')
    var $accent_variants = $('<div />', {
        'class': 'd-flex'
    })
    $container.append($accent_variants)
    $container.append(createSkinBlock(accent_colors, function () {
        var color = $(this).data('color')
        var accent_class = color
        var $body = $('body')
        accent_colors.map(function (skin) {
            $body.removeClass(skin)
        })

        $body.addClass(accent_class)
        localStorage.setItem('kelove_admin_lte_accent_class', accent_class)
    }))

    $container.append('<h6>暗色边栏设置</h6>')
    var $sidebar_variants_dark = $('<div />', {
        'class': 'd-flex'
    })
    $container.append($sidebar_variants_dark)
    $container.append(createSkinBlock(sidebar_colors, function () {
        var color = $(this).data('color')
        var sidebar_class = 'sidebar-dark-' + color.replace('bg-', '')
        var $sidebar = $('.main-sidebar')
        sidebar_skins.map(function (skin) {
            $sidebar.removeClass(skin)
        })

        $sidebar.addClass(sidebar_class)
        localStorage.setItem('kelove_admin_lte_sidebar_class', sidebar_class)
    }))

    $container.append('<h6>亮色边栏设置</h6>')
    var $sidebar_variants_light = $('<div />', {
        'class': 'd-flex'
    })
    $container.append($sidebar_variants_light)
    $container.append(createSkinBlock(sidebar_colors, function () {
        var color = $(this).data('color')
        var sidebar_class = 'sidebar-light-' + color.replace('bg-', '')
        var $sidebar = $('.main-sidebar')
        sidebar_skins.map(function (skin) {
            $sidebar.removeClass(skin)
        })

        $sidebar.addClass(sidebar_class)
        localStorage.setItem('kelove_admin_lte_sidebar_class', sidebar_class)
    }))

    var logo_skins = navbar_all_colors
    $container.append('<h6>品牌标志设置</h6>')
    var $logo_variants = $('<div />', {
        'class': 'd-flex'
    })
    $container.append($logo_variants)

    $container.append(createSkinBlock(logo_skins, function () {
        var color = $(this).data('color')
        var $logo = $('.brand-link')
        logo_skins.map(function (skin) {
            $logo.removeClass(skin)
        })
        $logo.addClass(color)
        localStorage.setItem('kelove_admin_lte_logo_color', color)
    }))

    function createSkinBlock(colors, callback) {
        var $block = $('<div />', {
            'class': 'd-flex flex-wrap mb-3'
        })

        colors.map(function (color) {
            var $color = $('<div />', {
                'class': (typeof color === 'object' ? color.join(' ') : color).replace('navbar-', 'bg-').replace('accent-', 'bg-') + ' elevation-2'
            })

            $block.append($color)

            $color.data('color', color)

            $color.css({
                width: '40px',
                height: '20px',
                borderRadius: '25px',
                marginRight: 10,
                marginBottom: 10,
                opacity: 0.8,
                cursor: 'pointer'
            })

            $color.hover(function () {
                $(this).css({opacity: 1}).removeClass('elevation-2').addClass('elevation-4')
            }, function () {
                $(this).css({opacity: 0.8}).removeClass('elevation-4').addClass('elevation-2')
            })

            if (callback) {
                $color.on('click', callback)
            }
        })

        return $block
    }

    $(document).ready(function () {
        /* 顶部导航初始化 */
        let main_header = $('.main-header')
        let skin_main_header = localStorage.getItem('kelove_admin_lte_main_header_skin')
        let skin_color_main_header = localStorage.getItem('kelove_admin_lte_main_header_skin_color')
        if (skin_main_header && skin_color_main_header) {
            navbar_all_colors.map(function (color) {
                main_header.removeClass(color)
            })
            main_header.addClass(skin_main_header).addClass(skin_color_main_header)
        }

        /* 强调颜色初始化 */
        let body = $('body')
        let accent_class = localStorage.getItem('kelove_admin_lte_accent_class')
        if (accent_class) {
            accent_colors.map(function (skin) {
                body.removeClass(skin)
            })
            body.addClass(accent_class)
        }

        /* 侧边栏初始化 */
        let sidebar = $('.main-sidebar')
        let sidebar_class = localStorage.getItem('kelove_admin_lte_sidebar_class')
        if (sidebar_class) {
            sidebar_skins.map(function (skin) {
                sidebar.removeClass(skin)
            })
            sidebar.addClass(sidebar_class)
        }

        /* logo初始化 */
        let logo = $('.brand-link')
        let logo_color = localStorage.getItem('kelove_admin_lte_logo_color')
        if (logo_color) {
            logo_skins.map(function (skin) {
                logo.removeClass(skin)
            })
            logo.addClass(logo_color)
        }
    });
    /* 返回顶部 */
    $(document).on("click", "#back-to-top", function () {
        $("html, body").animate({scrollTop: "0px"}, 800);
        return false;
    });
    /* 滚动条位置变化时更新按钮状态 */
    $(window).on("scroll", function () {
        let ScTop = $(this).scrollTop();
        if (ScTop > 400) {
            $("#back-to-top").fadeIn(800);
        } else {
            $("#back-to-top").fadeOut(800);
        }
    });
})(jQuery)
