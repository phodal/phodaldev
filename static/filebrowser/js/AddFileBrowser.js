var FileBrowser = {
    // this is set automatically
    admin_media_prefix: '',
    // change this
    thumb_prefix: 'thumb_',
    no_thumb: 'filebrowser/img/no_thumb.gif',

    init: function() {
        // Deduce admin_media_prefix by looking at the <script>s in the
        // current document and finding the URL of *this* module.
        var scripts = document.getElementsByTagName('script');
        for (var i=0; i<scripts.length; i++) {
            if (scripts[i].src.match(/AddFileBrowser/)) {
                var idx = scripts[i].src.indexOf('filebrowser/js/AddFileBrowser');
                FileBrowser.admin_media_prefix = scripts[i].src.substring(0, idx);
                break;
            }
        }
    },
    // show FileBrowser
    show: function(id, href, close_func) {
        // var id2=String(id).split(".").join("___");
        var id2=String(id).replace(/\-/g,"____").split(".").join("___");
        FBWindow = window.open(href, String(id2), 'height=600,width=960,resizable=yes,scrollbars=yes');
        FBWindow.focus();
        if (close_func) {
            FBWindow.onbeforeunload = close_func;
        }
    },
    clear: function(id) {
        jQuery('#help_'+id+', #clear_'+id).hide();
        jQuery('#'+id).val('');
    }
}

if (!addEvent){
    function addEvent(obj, evType, fn) {
        if (obj.addEventListener) {
            obj.addEventListener(evType, fn, false);
            return true;
        } else if (obj.attachEvent) {
            var r = obj.attachEvent("on" + evType, fn);
            return r;
        } else {
            return false;
        }
    }
}

addEvent(window, 'load', FileBrowser.init);

