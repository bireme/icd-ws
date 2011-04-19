function(doc, req) {  
    // !code vendor/isis/_attachments/listfields.js
    var ddoc = this;
    var rows = [];
    var Mustache = require('vendor/couchapp/lib/mustache');
    var rows = listfields(doc)
    var view = {
        rows: rows  
    };
    var html = Mustache.to_html(ddoc.templates.chap_detail, view);
    
    return {
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html
    }
    
  
}
