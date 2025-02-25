window.djangoFileBrowser = (callback, value, meta) => {
    let fbURL = "/admin/filebrowser/browse/?pop=5&dir=uploads";
    fbURL = fbURL + "&type=" + meta.filetype;
    if (value) fbURL += "&input=";
    tinyMCE.activeEditor.windowManager.openUrl({
        title: "Filebrowser image/media/file picker",
        url: fbURL,
        width: 850,
        height: 500,
        onMessage: function (dialogApi, details) {
            callback(details.content);
            dialogApi.close();
        }
    });
    return false;
};