(function ($) {
    $(document).ready(function () {
        docIni();
        sidebarIni();
        $('html,body').animate({
            scrollTop: 0
        }, 500);
    });

    $(window).resize(function () {
        sidebarIni();
    });

    $(document).on('click', '.sidebar-body .catalog-body li > i.icon.caret', function () {
        $(this).parent().toggleClass('open');
        if ($(this).hasClass('down')) {
            $(this).removeClass('down').addClass('right');
        } else {
            $(this).removeClass('right').addClass('down');
        }
    });

    $(document).on('click', '.left.tools>.item.icon', function () {
        $(this).parents('.window-container .window-body').toggleClass('with-sidebar');
    });

    $(document).on('click', '.window-container .window-body .sidebar .sidebar-body', function () {
        if ($(window).width() < 600) {
            $(this).parents('.window-container .window-body').toggleClass('with-sidebar');
        }
    });

    function sidebarIni() {
        if ($(window).width() < 768) {
            $('.window-container .window-body').removeClass('with-sidebar');
        }
    }

    function getQueryString(name, value) {
        let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        //获取url中"?"符后的字符串并正则匹配
        let r = window.location.search.substr(1).match(reg);
        if (r) {
            value = r[2];
        }
        return value;
    }

    function docIni() {
        $('#doc_id').val(getQueryString('doc', 0));
        $('#detail_id').val(getQueryString('id', 0));
    }

    $(document).on('click', '.smooth a, a.smooth', function () {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '')
            && location.hostname === this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                if ($(this).hasClass('sidebar-li')) {
                    $(this).parents('.sidebar-body .catalog-body').find('li.active').removeClass('active');
                    $(this).parent('.sidebar-body .catalog-body li').addClass('active');
                }
                $('html,body').animate({
                    scrollTop: target.offset().top - 70
                }, 1000);
                return false;
            }
        }
    });
})(window.jQuery);
