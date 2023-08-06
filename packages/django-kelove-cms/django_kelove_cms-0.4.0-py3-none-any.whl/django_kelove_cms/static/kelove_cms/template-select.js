window.addEventListener('change', function (e) {

    let target_id = e.target.id;
    if (target_id === 'id_template') {
        let _val = document.getElementById(target_id).value;
        if (confirm("确定要重新选择模板码？当前页面数据将会清空！")) {
            let _href = window.location.href
            window.location.replace(keloveCMSChangeURLArg(_href, "kelove_tpl", _val));
        }
    }

    function keloveCMSChangeURLArg(url, arg, arg_val) {
        let pattern = arg + '=([^&]*)';
        let replaceText = arg + '=' + arg_val;
        if (url.match(pattern)) {
            let tmp = '/(' + arg + '=)([^&]*)/gi';
            tmp = url.replace(eval(tmp), replaceText);
            return tmp;
        } else {
            if (url.match('[\?]')) {
                return url + '&' + replaceText;
            } else {
                return url + '?' + replaceText;
            }
        }
    }
}, true);

window.addEventListener('load', function (e) {
    let kelove_tpl = getURLString('kelove_tpl');
    if (kelove_tpl) {
        document.getElementById('id_template').value = kelove_tpl;
    }

    function getURLString(arg) {
        let reg = new RegExp("(^|&)" + arg + "=([^&]*)(&|$)", "i");
        let r = window.location.search.substr(1).match(reg);
        if (r != null)
            return unescape(r[2]);
        return null;
    }
});