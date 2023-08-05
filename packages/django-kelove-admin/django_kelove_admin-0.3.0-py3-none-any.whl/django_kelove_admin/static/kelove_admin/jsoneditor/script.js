function keloveJsonEditorInit(json_editor_controller_id) {
    let _editor_id = 'json_editor_' + json_editor_controller_id;
    let jsonValue = document.getElementById(json_editor_controller_id).value;
    try {
        jsonValue = JSON.parse(jsonValue);
    } catch (e) {
        jsonValue = jsonValue.replace(/[\r\n]/g, '');
    }
    let _editorConfig;
    try {
        _editorConfig = document.getElementById(json_editor_controller_id).attributes["field_settings"].nodeValue;
        _editorConfig = JSON.parse(_editorConfig);
    } catch (e) {
        _editorConfig = {};
    }

    _editorConfig.onChangeText = function (jsonString) {
        document.getElementById(json_editor_controller_id).value = jsonString;
    };
    (new JSONEditor(document.getElementById(_editor_id), _editorConfig)).set(jsonValue);
}